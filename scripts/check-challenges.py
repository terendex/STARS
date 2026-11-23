"""Checks every challenge.yml for common mistakes, before you sync. It only reads
files: it changes nothing, and CTFd doesn't need to be running.

    scripts\\check.ps1            every CTF (Windows)
    scripts\\check.ps1 sits       one CTF, by its folder name
    bash scripts/check.sh         the same on Linux

ERROR means the challenge is broken or ctfcli will get it wrong. Fix these
before you sync. warn means it's probably a mistake: read it and decide.
docs/making-challenges.md explains each rule.

A CTF is any folder here with a docker-compose.yml and a challenges/ folder,
so a new event is checked without changing this script.
"""
import collections
import configparser
import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent

# Points for each difficulty tag: (starting value, taken off per solve, lowest value).
# A challenge without an "extra" section has fixed points (the demo does this).
DIFFICULTY = {
    "★ Easy": (30, 1, 15),
    "★★ Medium": (60, 3, 30),
    "★★★ Hard": (100, 5, 50),
}
REQUIRED = ["name", "category", "type", "value", "description", "flags"]
TOOLS_LINE = re.compile(r"\*\*(Commands|Tools)[^*]*may need[^*]*\*\*")
IP = re.compile(r"(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?![\d.])")
# Example text from docs/challenge-template/challenge.yml that should have been replaced.
TEMPLATE_TEXT = {
    "name": ["Challenge name"],
    "author": ["Your name"],
    "description": ["One or two sentences of story.", "what to find, and where the flag will be"],
    "flags": ["replace_me"],
    "hints": ["A nudge that adds something new."],
}


def flag_text(flag):
    """A flag is either a plain string or {type, content, data}."""
    if isinstance(flag, dict):
        return str(flag.get("content", "")), flag.get("type", "static")
    return str(flag), "static"


def find_ctfs():
    return sorted(
        path.parent for path in REPO.glob("*/docker-compose.yml") if (path.parent / "challenges").is_dir()
    )


def registered(ctf):
    """Challenge folders listed in the CTF's .ctf/config, or None before setup."""
    config_file = ctf / ".ctf" / "config"
    if not config_file.exists():
        return None
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str  # keep the folder names' capitals
    config.read(config_file, encoding="utf-8")
    return set(config["challenges"]) if config.has_section("challenges") else set()


def check_ctf(ctf, problems):
    """Checks one CTF's challenges. Returns {flag: challenge name} for the cross-CTF check."""

    def report(level, path, message):
        problems.append((level, f"{path.relative_to(REPO).as_posix()}: {message}"))

    challenges = []
    for path in sorted((ctf / "challenges").rglob("challenge.yml")):
        if len(path.relative_to(ctf).parts) != 4:
            report("ERROR", path, "is in the wrong place. Use challenges/<category>/<challenge>/challenge.yml")
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            report("ERROR", path, f"isn't valid YAML: {str(error).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            report("ERROR", path, "is empty or isn't a list of fields")
            continue
        missing = [field for field in REQUIRED if not data.get(field)]
        if missing:
            report("ERROR", path, f"is missing {', '.join(missing)}")
            continue
        challenges.append((path, data))

    # The flag format this CTF mostly uses, like STARS or FLAG.
    prefixes = collections.Counter()
    for _, data in challenges:
        for flag in data["flags"]:
            text, kind = flag_text(flag)
            match = re.fullmatch(r"([A-Za-z0-9_]+)\{.+\}", text)
            if kind == "static" and match:
                prefixes[match.group(1)] += 1
    prefix = prefixes.most_common(1)[0][0] if prefixes else None

    answers_file = ctf / "ANSWERS.md"
    answers = answers_file.read_text(encoding="utf-8") if answers_file.exists() else None
    if answers is None:
        report("warn", answers_file, "doesn't exist, so flags can't be checked against it")
    in_ctfd = registered(ctf)
    names = collections.Counter(data["name"] for _, data in challenges)
    flags = {}
    # This CTF's own address. set-host only updates it in connection_info, so
    # anywhere else it goes stale when the IP changes.
    host_ips = {ip for _, data in challenges for ip in IP.findall(str(data.get("connection_info") or ""))}
    # The address most challenges use. One that differs was usually copied from
    # somewhere else, like the template's example.
    used = collections.Counter(ip for _, data in challenges for ip in IP.findall(str(data.get("connection_info") or "")))
    usual_ip = used.most_common(1)[0][0] if used else None

    for path, data in challenges:
        folder = path.parent
        name = data["name"]

        for ip in IP.findall(str(data.get("connection_info") or "")):
            if usual_ip and ip != usual_ip:
                report("warn", path, f"connection_info uses {ip}, but this CTF's other challenges use {usual_ip}. "
                                     "Copy the line from one of them (or delete it if there's no port)")

        player_text = data["description"] + " ".join(
            str(hint.get("content", "")) for hint in data.get("hints") or [] if isinstance(hint, dict))
        fields = {
            "name": [str(data["name"])],
            "author": [str(data.get("author") or ""), str(data.get("attribution") or "")],
            "description": [data["description"]],
            "flags": [flag_text(flag)[0] for flag in data["flags"]],
            "hints": [str(hint.get("content", "")) for hint in data.get("hints") or [] if isinstance(hint, dict)],
        }
        leftovers = [text for field, examples in TEMPLATE_TEXT.items() for text in examples
                     if any(text in value for value in fields[field])]
        if leftovers:
            report("warn", path, "still has the template's example text: " + ", ".join(f'"{t}"' for t in leftovers))

        if host_ips & set(IP.findall(player_text)):
            report("warn", path, "has the CTF's IP written in the description or a hint. It won't change when "
                                 "the IP does, so say \"the address below\" instead")

        if names[name] > 1:
            report("ERROR", path, f'another challenge in {ctf.name} is also named "{name}". Names must be different')

        if data["type"] != "standard":
            report("ERROR", path, f'type is "{data["type"]}". Use "standard": the points dropping is built into it')

        tags = [tag for tag in data.get("tags") or [] if tag in DIFFICULTY]
        if len(tags) != 1:
            report("ERROR", path, f"needs exactly one difficulty tag: {', '.join(repr(t) for t in DIFFICULTY)}")
        else:
            start, decay, minimum = DIFFICULTY[tags[0]]
            if data["value"] != start:
                report("ERROR", path, f"value is {data['value']}, but {tags[0]} starts at {start}")
            extra = data.get("extra")
            if extra:
                wanted = {"initial": start, "decay": decay, "minimum": minimum}
                wrong = [f"{key} is {extra.get(key)} (should be {value})"
                         for key, value in wanted.items() if extra.get(key) != value]
                if wrong:
                    report("ERROR", path, f"extra: {', '.join(wrong)} for {tags[0]}")
            if tags[0] != "★★★ Hard" and not TOOLS_LINE.search(data["description"]):
                report("warn", path, 'Easy and Medium descriptions end with a "**Tools you may need ...**" line')

        if "**Your goal:**" not in data["description"]:
            report("warn", path, 'the description has no "**Your goal:**" line')

        for listed in data.get("files") or []:
            if not (folder / listed).is_file():
                report("ERROR", path, f"lists the file {listed}, which doesn't exist")

        for flag in data["flags"]:
            text, kind = flag_text(flag)
            if kind != "static":
                continue
            if prefix and (not text.startswith(prefix + "{") or not text.endswith("}")):
                report("ERROR", path, f"flag {text} doesn't look like {prefix}{{...}}, the format {ctf.name} uses")
            if answers is not None and text not in answers and text.lower() not in answers.lower():
                report("warn", path, f"flag {text} isn't in {ctf.name}/ANSWERS.md. Add the walkthrough")
            flags[text] = name

        if in_ctfd is not None and folder.relative_to(ctf).as_posix() not in in_ctfd:
            report("warn", path, "isn't added to CTFd yet. Run ctfcli challenge add (docs/making-challenges.md)")

    # Lines in .ctf/config whose folder was deleted.
    folders = {path.parent.relative_to(ctf).as_posix() for path, _ in challenges}
    for listed in sorted(in_ctfd or ()):
        if listed not in folders and not (ctf / listed / "challenge.yml").exists():
            report("warn", ctf / ".ctf" / "config", f"lists {listed}, which has no challenge.yml. "
                                                     "Delete that line, or every sync says it could not be found")

    return len(challenges), flags


def main():
    ctfs = find_ctfs()
    wanted = sys.argv[1:]
    unknown = [name for name in wanted if name not in {ctf.name for ctf in ctfs}]
    if unknown:
        sys.exit(f"No CTF folder called {', '.join(unknown)}. These exist: {', '.join(c.name for c in ctfs)}")
    if wanted:
        ctfs = [ctf for ctf in ctfs if ctf.name in wanted]

    problems = []
    total = 0
    seen = {}
    for ctf in ctfs:
        before = len(problems)
        count, flags = check_ctf(ctf, problems)
        total += count
        for text, name in flags.items():
            if text in seen and seen[text][0] != ctf.name:
                other_ctf, other_name = seen[text]
                problems.append(("warn", f'{ctf.name}: "{name}" has the same flag as "{other_name}" in {other_ctf}'))
            seen.setdefault(text, (ctf.name, name))
        found = problems[before:]
        print(f"{ctf.name}: {count} challenges, " + (f"{len(found)} problem(s)" if found else "no problems"))
        for level, message in found:
            print(f"  {level:5}  {message}")

    errors = sum(1 for level, _ in problems if level == "ERROR")
    warnings = len(problems) - errors
    print()
    if not problems:
        print(f"All good: {total} challenges checked.")
    else:
        print(f"{errors} error(s) and {warnings} warning(s) in {total} challenges.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
