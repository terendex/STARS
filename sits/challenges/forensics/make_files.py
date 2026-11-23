"""Regenerates the player downloads for every SITS Forensics challenge, using
only the standard library.

Run this after changing a flag, then push the files with scripts\\sits.ps1 sync.
Each challenge checks its own download where Python can: the flag has to come
back out the way a player would get it, and the obvious shortcuts must not give
it away. Flags drawn as pictures use capital letters only, from FONT below, so
there are no look-alike characters, and CTFd accepts them in any case.
"""
import io
import math
import pathlib
import random
import struct
import wave
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parent


def write(folder, name, data):
    path = ROOT / folder / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


# --- Pictures -----------------------------------------------------------------

def scene(width, height, seed, sky_top, sky_bottom, ground, horizon=0.62, sun=None, noise=4):
    """An everyday-looking picture: a sky fading between two colours, a sun, and
    the ground. The noise makes every pixel's lowest bits random, as in a photo."""
    rng = random.Random(seed)
    pixels = bytearray(width * height * 3)
    line = int(height * horizon)
    for y in range(height):
        for x in range(width):
            if y < line:
                t = y / line
                color = [sky_top[i] + (sky_bottom[i] - sky_top[i]) * t for i in range(3)]
                if sun:
                    sx, sy, radius, sun_color = sun
                    distance = math.hypot(x - sx, y - sy)
                    glow = max(0.0, 1 - distance / (radius * 3))
                    if distance < radius:
                        color = list(sun_color)
                    else:
                        color = [color[i] + (sun_color[i] - color[i]) * glow * 0.5 for i in range(3)]
            else:
                t = (y - line) / max(1, height - line)
                color = [ground[i] * (1 - 0.35 * t) for i in range(3)]
            offset = (y * width + x) * 3
            for i in range(3):
                pixels[offset + i] = max(0, min(255, int(color[i]) + rng.randint(-noise, noise)))
    return pixels


def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))


def png(width, height, pixels, extra_chunks=b""):
    rows = b"".join(
        b"\x00" + bytes(pixels[y * width * 3 : (y + 1) * width * 3]) for y in range(height)
    )
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + extra_chunks
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


def read_png(data):
    """Just enough of a PNG reader to check this script's own images."""
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    position, idat, texts = 8, b"", {}
    while position < len(data):
        length, kind = struct.unpack(">I4s", data[position : position + 8])
        body = data[position + 8 : position + 8 + length]
        if kind == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        elif kind == b"IDAT":
            idat += body
        elif kind == b"tEXt":
            key, value = body.split(b"\x00", 1)
            texts[key] = value
        position += 12 + length
        if kind == b"IEND":
            break
    raw = zlib.decompress(idat)
    stride = width * 3 + 1
    assert all(raw[row * stride] == 0 for row in range(height))
    pixels = b"".join(raw[row * stride + 1 : (row + 1) * stride] for row in range(height))
    return width, height, pixels, texts, position


# A 5x7 capital-letter font, for flags that players read off a picture.
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "{": ["00110", "00100", "00100", "01000", "00100", "00100", "00110"],
    "}": ["01100", "00100", "00100", "00010", "00100", "00100", "01100"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def text_image(text, scale, fg, bg, margin):
    """Draws text in FONT. Returns (width, height, RGB pixels)."""
    width = margin * 2 + len(text) * 6 * scale - scale
    height = margin * 2 + 7 * scale
    pixels = bytearray(bytes(bg) * (width * height))
    for index, char in enumerate(text):
        for row, bits in enumerate(FONT[char]):
            for column, bit in enumerate(bits):
                if bit == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            x = margin + index * 6 * scale + column * scale + dx
                            y = margin + row * scale + dy
                            pixels[(y * width + x) * 3 : (y * width + x) * 3 + 3] = bytes(fg)
    return width, height, pixels


def read_text(width, pixels, scale, fg, margin, length, left=None, top=None):
    """Reads FONT text back out of a picture, to check a drawn flag. `fg` is a
    function from a pixel's (r, g, b) to whether it's ink, or an ink colour."""
    is_ink = fg if callable(fg) else (lambda rgb: rgb == tuple(fg))
    left = margin if left is None else left
    top = margin if top is None else top
    glyphs = {"".join(rows): char for char, rows in FONT.items()}
    out = ""
    for index in range(length):
        rows = []
        for row in range(7):
            bits = ""
            for column in range(5):
                x = left + index * 6 * scale + column * scale
                y = top + row * scale
                bits += "1" if is_ink(tuple(pixels[(y * width + x) * 3 : (y * width + x) * 3 + 3])) else "0"
            rows.append(bits)
        out += glyphs.get("".join(rows), "?")
    return out


# --- PDFs -----------------------------------------------------------------------

def pdf(stream, info=None):
    """A one-page PDF with Helvetica, drawing the given content stream. `info`
    is an optional document-information dictionary (the file's metadata)."""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    if info:
        objects.append(info)
    out = b"%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    trailer = b"/Size %d /Root 1 0 R" % (len(objects) + 1)
    if info:
        trailer += b" /Info %d 0 R" % len(objects)
    out += b"trailer\n<< %s >>\nstartxref\n%d\n%%%%EOF\n" % (trailer, xref)
    return out


def pdf_hex(text):
    """A PDF string written as hex, so searching the file for the text finds nothing."""
    return b"<" + text.encode().hex().upper().encode() + b">"


# --- GIFs -----------------------------------------------------------------------

def lzw(indices, min_code_size):
    """GIF's LZW compression."""
    clear, end = 1 << min_code_size, (1 << min_code_size) + 1
    out, buffer, bits = bytearray(), 0, 0
    code_size = min_code_size + 1

    def emit(code):
        nonlocal buffer, bits
        buffer |= code << bits
        bits += code_size
        while bits >= 8:
            out.append(buffer & 0xFF)
            buffer >>= 8
            bits -= 8

    def reset():
        return {bytes([i]): i for i in range(clear)}, end + 1

    table, next_code = reset()
    emit(clear)
    current = b""
    for index in indices:
        candidate = current + bytes([index])
        if candidate in table:
            current = candidate
            continue
        emit(table[current])
        if next_code < 4096:
            table[candidate] = next_code
            next_code += 1
            if next_code > (1 << code_size) and code_size < 12:
                code_size += 1
        else:
            emit(clear)
            table, next_code = reset()
            code_size = min_code_size + 1
        current = bytes([index])
    emit(table[current])
    emit(end)
    if bits:
        out.append(buffer & 0xFF)
    return bytes(out)


def gif(width, height, palette, frames):
    """frames: list of (palette indices, delay in hundredths of a second)."""
    depth = max(2, (len(palette) - 1).bit_length())
    table = b"".join(bytes(c) for c in palette) + b"\x00\x00\x00" * ((1 << depth) - len(palette))
    out = b"GIF89a" + struct.pack("<HHBBB", width, height, 0x80 | ((depth - 1) << 4) | (depth - 1), 0, 0) + table
    out += b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00"  # loop forever
    for indices, delay in frames:
        out += b"\x21\xF9\x04" + struct.pack("<BHB", 1 << 2, delay, 0) + b"\x00"
        out += b"\x2C" + struct.pack("<HHHHB", 0, 0, width, height, 0)
        compressed = lzw(indices, depth)
        out += bytes([depth])
        for start in range(0, len(compressed), 255):
            block = compressed[start : start + 255]
            out += bytes([len(block)]) + block
        out += b"\x00"
    return out + b"\x3B"


def unlzw(data, min_code_size):
    """GIF LZW decoder, to check the encoder."""
    clear, end = 1 << min_code_size, (1 << min_code_size) + 1
    code_size, position, out = min_code_size + 1, 0, bytearray()
    table, previous = None, None
    bitstream = int.from_bytes(data, "little")
    while True:
        code = (bitstream >> position) & ((1 << code_size) - 1)
        position += code_size
        if code == clear:
            table = [bytes([i]) for i in range(clear)] + [b"", b""]
            code_size, previous = min_code_size + 1, None
            continue
        if code == end:
            return bytes(out)
        if previous is None:
            entry = table[code]
        else:
            entry = table[code] if code < len(table) else table[previous] + table[previous][:1]
            if len(table) < 4096:
                table.append(table[previous] + entry[:1])
                if len(table) == (1 << code_size) and code_size < 12:
                    code_size += 1
        out += entry
        previous = code


def read_gif(data):
    """Returns [(indices, delay)] for every frame, to check the file."""
    width, height, packed = struct.unpack("<HHB", data[6:11])
    depth = (packed & 7) + 1
    position, frames, delay = 13 + 3 * (1 << depth), [], 0
    while data[position] != 0x3B:
        if data[position] == 0x21:
            label = data[position + 1]
            if label == 0xF9:
                delay = struct.unpack("<H", data[position + 4 : position + 6])[0]
            position += 2
            while data[position]:
                position += data[position] + 1
            position += 1
        else:
            position += 10
            min_code = data[position]
            position += 1
            compressed = b""
            while data[position]:
                compressed += data[position + 1 : position + 1 + data[position]]
                position += data[position] + 1
            position += 1
            frames.append((unlzw(compressed, min_code), delay))
    return width, height, frames


# --- Zips -----------------------------------------------------------------------

def dos_time(date_time):
    year, month, day, hour, minute, second = date_time
    return (hour << 11) | (minute << 5) | (second // 2), ((year - 1980) << 9) | (month << 5) | day


def locked_zip(name, content, password, date_time, seed):
    """A zip holding one stored (uncompressed) file, locked with the classic zip
    password scheme ("ZipCrypto"), which File Explorer and 7-Zip both open.
    Python's zipfile can read these but not write them."""
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
        table.append(c)
    keys = [0x12345678, 0x23456789, 0x34567890]

    def crc_step(value, byte):
        return (value >> 8) ^ table[(value ^ byte) & 0xFF]

    def update(byte):
        keys[0] = crc_step(keys[0], byte)
        keys[1] = ((keys[1] + (keys[0] & 0xFF)) * 134775813 + 1) & 0xFFFFFFFF
        keys[2] = crc_step(keys[2], keys[1] >> 24)

    def stream_byte():
        t = (keys[2] | 2) & 0xFFFF
        return ((t * (t ^ 1)) >> 8) & 0xFF

    for byte in password.encode():
        update(byte)
    crc = zlib.crc32(content) & 0xFFFFFFFF
    header = bytes(random.Random(seed).randrange(256) for _ in range(11)) + bytes([crc >> 24])
    encrypted = bytearray()
    for byte in header + content:
        encrypted.append(byte ^ stream_byte())
        update(byte)
    mtime, mdate = dos_time(date_time)
    raw_name = name.encode()
    local = struct.pack("<IHHHHHIIIHH", 0x04034B50, 20, 1, 0, mtime, mdate, crc,
                        len(encrypted), len(content), len(raw_name), 0) + raw_name + bytes(encrypted)
    central = struct.pack("<IHHHHHHIIIHHHHHII", 0x02014B50, 20, 20, 1, 0, mtime, mdate, crc,
                          len(encrypted), len(content), len(raw_name), 0, 0, 0, 0, 0x20, 0) + raw_name
    end = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, 1, 1, len(central), len(local), 0)
    return local + central + end


def plain_zip(files, date_time):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name, content in files.items():
            info = zipfile.ZipInfo(name, date_time=date_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, content)
    return archive.getvalue()


# --- Network captures -------------------------------------------------------------

CLIENT = bytes((192, 168, 1, 23))
SERVER = bytes((192, 168, 1, 10))
CLIENT_MAC = bytes.fromhex("02aabbcc0023")
SERVER_MAC = bytes.fromhex("02aabbcc0010")
SYN, ACK, PSH, FIN = 0x02, 0x10, 0x08, 0x01


def checksum(data):
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF


def frame(from_client, client_port, server_port, seq, ack, flags, payload=b"", ident=[1000]):
    src, dst = (CLIENT, SERVER) if from_client else (SERVER, CLIENT)
    sport, dport = (client_port, server_port) if from_client else (server_port, client_port)
    tcp = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 5 << 4, flags, 65535, 0, 0)
    pseudo = src + dst + struct.pack("!BBH", 0, 6, len(tcp) + len(payload))
    tcp = tcp[:16] + struct.pack("!H", checksum(pseudo + tcp + payload)) + tcp[18:]
    ident[0] += 1
    ip = struct.pack(
        "!BBHHHBBH4s4s", 0x45, 0, 20 + len(tcp) + len(payload), ident[0], 0x4000, 64, 6, 0, src, dst
    )
    ip = ip[:10] + struct.pack("!H", checksum(ip)) + ip[12:]
    macs = SERVER_MAC + CLIENT_MAC if from_client else CLIENT_MAC + SERVER_MAC
    return macs + b"\x08\x00" + ip + tcp + payload


def conversation(client_port, server_port, exchanges):
    """A whole TCP connection: handshake, each (from_client, data) in 1460-byte
    segments with ACKs, then a clean close."""
    c, s = 1000, 5000
    f = lambda *args, **kw: frame(*args[:1], client_port, server_port, *args[1:], **kw)
    frames = [f(True, c, 0, SYN), f(False, s, c + 1, SYN | ACK)]
    c, s = c + 1, s + 1
    frames.append(f(True, c, s, ACK))
    for from_client, payload in exchanges:
        for start in range(0, len(payload), 1460):
            part = payload[start : start + 1460]
            if from_client:
                frames.append(f(True, c, s, PSH | ACK, part))
                c += len(part)
                frames.append(f(False, s, c, ACK))
            else:
                frames.append(f(False, s, c, PSH | ACK, part))
                s += len(part)
                frames.append(f(True, c, s, ACK))
    frames.append(f(True, c, s, FIN | ACK))
    c += 1
    frames.append(f(False, s, c, FIN | ACK))
    s += 1
    frames.append(f(True, c, s, ACK))
    return frames


def pcap(frames, start=1795000000):
    out = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    for index, data in enumerate(frames):
        out += struct.pack("<IIII", start + index // 10, index * 10000 % 1000000, len(data), len(data))
        out += data
    return out


def http_get(path, host="intranet.office.local", extra=""):
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0\r\n{extra}\r\n".encode()


def http_reply(status, content_type, body):
    if isinstance(body, str):
        body = body.encode()
    head = f"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\n\r\n"
    return head.encode() + body


# === Easy ======================================================================

# Photo Notes ("start here"): the flag is in a PNG text chunk, which Notepad
# shows as readable text among the gibberish.
FLAG = "FLAG{ph0t0s_c4n_h0ld_n0t3s}"
pixels = scene(480, 300, "photo-notes", (90, 160, 230), (250, 200, 150), (230, 205, 150),
               horizon=0.6, sun=(360, 120, 26, (255, 236, 170)))
note = chunk(b"tEXt", b"Comment\x00Note to self: best beach day ever. " + FLAG.encode())
data = png(480, 300, pixels, note)
write("photo-notes", "beach_day.png", data)
assert data.count(b"FLAG") == 1 and read_png(data)[3][b"Comment"].endswith(FLAG.encode())

# Wrong Label: a picture of the flag, saved as recipe.txt.
FLAG = "FLAG{NOT_A_TEXT_FILE}"
INK, PAPER = (40, 40, 40), (250, 246, 235)
width, height, pixels = text_image(FLAG, 4, INK, PAPER, 24)
data = png(width, height, pixels)
write("wrong-label", "recipe.txt", data)
assert data[1:4] == b"PNG" and b"FLAG" not in data
assert read_text(width, read_png(data)[2], 4, INK, 24, len(FLAG)) == FLAG

# Broken Header: a picture of the flag whose first four bytes (89 50 4E 47)
# were wiped to zeros, so nothing opens it until they're written back.
FLAG = "FLAG{MAGIC_BYTES_FIXED}"
INK, PAPER = (20, 60, 120), (235, 242, 250)
width, height, pixels = text_image(FLAG, 4, INK, PAPER, 24)
good = png(width, height, pixels)
broken = b"\x00\x00\x00\x00" + good[4:]
write("broken-header", "postcard.png", broken)
assert broken[:8] == b"\x00\x00\x00\x00\r\n\x1a\n" and b"FLAG" not in broken
fixed = bytes.fromhex("89504E47") + broken[4:]
assert fixed == good and read_text(width, read_png(fixed)[2], 4, INK, 24, len(FLAG)) == FLAG

# Blacked Out: a "redacted" PDF whose black boxes sit on top of real text.
FLAG = "FLAG{bl4ck_b0x3s_d0nt_d3l3t3}"
stream = b"\n".join(
    [
        b"BT /F1 20 Tf 72 720 Td (Office Incident Report) Tj ET",
        b"BT /F1 12 Tf 72 690 Td (Subject: The missing birthday cake) Tj ET",
        b"BT /F1 12 Tf 72 670 Td (On Friday afternoon, the cake in the office fridge disappeared.) Tj ET",
        # The name is its own piece of text with a gap before it, so its box
        # covers it whatever font a viewer substitutes for Helvetica.
        b"BT /F1 12 Tf 72 650 Td (Person responsible:) Tj ET",
        b"BT /F1 12 Tf 200 650 Td (Jordan from Accounts) Tj ET",
        b"BT /F1 12 Tf 72 620 Td (Case number: " + FLAG.encode() + b") Tj ET",
        b"BT /F1 12 Tf 72 600 Td (A new cake has been ordered. Please label your food.) Tj ET",
        b"BT /F1 12 Tf 72 570 Td (End of report. Redacted before sharing with all staff.) Tj ET",
        # The "redactions": black rectangles drawn over the name and the case number.
        b"0 0 0 rg 194 646 140 16 re f",
        b"0 0 0 rg 70 616 330 16 re f",
    ]
)
data = pdf(stream)
write("blacked-out", "incident_report.pdf", data)
assert FLAG.encode() in data and data.index(FLAG.encode()) < data.index(b"re f")

# File Properties: the flag is in the PDF's metadata (its Subject), not on the
# page. The metadata is written as hex, so searching the file for FLAG fails.
FLAG = "FLAG{m3t4d4t4_kn0ws_m0r3}"
stream = b"\n".join(
    [
        b"BT /F1 20 Tf 72 720 Td (Board Game Club: Meeting Minutes) Tj ET",
        b"BT /F1 12 Tf 72 690 Td (Present: 9 members, 2 cats.) Tj ET",
        b"BT /F1 12 Tf 72 670 Td (Next month's game: a very long game of Monopoly.) Tj ET",
        b"BT /F1 12 Tf 72 650 Td (Snacks: everyone brings one. No more glitter.) Tj ET",
        b"BT /F1 12 Tf 72 620 Td (End of minutes.) Tj ET",
    ]
)
info = b"<< /Title %s /Author %s /Subject %s /Keywords %s >>" % (
    pdf_hex("Board Game Club: Meeting Minutes"),
    pdf_hex("Club Secretary"),
    pdf_hex(f"Secret word: {FLAG}"),
    pdf_hex("club, minutes, games"),
)
data = pdf(stream, info)
write("file-properties", "club_minutes.pdf", data)
assert b"FLAG" not in data and pdf_hex(f"Secret word: {FLAG}") in data
assert bytes.fromhex(pdf_hex(f"Secret word: {FLAG}")[1:-1].decode()).decode().endswith(FLAG)

# Too Fast: a loading spinner GIF with one frame shown for 20 milliseconds.
FLAG = "FLAG{BLINK_AND_YOU_MISS_IT}"
PALETTE = [(24, 26, 32), (70, 74, 86), (120, 200, 255), (255, 255, 255)]
W, H = 360, 200
DOTS = 8


def spinner(lit):
    indices = [0] * (W * H)
    for dot in range(DOTS):
        angle = 2 * math.pi * dot / DOTS
        cx, cy = W / 2 + 50 * math.cos(angle), H / 2 + 50 * math.sin(angle)
        for y in range(int(cy) - 9, int(cy) + 10):
            for x in range(int(cx) - 9, int(cx) + 10):
                if math.hypot(x - cx, y - cy) <= 8:
                    indices[y * W + x] = 2 if dot == lit else 1
    return indices


text_w, text_h, text_pixels = text_image(FLAG, 2, (255, 255, 255), PALETTE[0], 0)
flag_frame = [0] * (W * H)
left, top = (W - text_w) // 2, (H - text_h) // 2
for y in range(text_h):
    for x in range(text_w):
        if text_pixels[(y * text_w + x) * 3 : (y * text_w + x) * 3 + 3] == b"\xff\xff\xff":
            flag_frame[(top + y) * W + left + x] = 3
frames = [(spinner(lit), 10) for lit in range(DOTS)]
frames.insert(5, (flag_frame, 2))  # 2 hundredths of a second: too fast to read
data = gif(W, H, PALETTE, [(bytes(f), d) for f, d in frames])
write("too-fast", "loading.gif", data)
_, _, decoded = read_gif(data)
assert [d for _, d in decoded] == [10] * 5 + [2] + [10] * 3
assert all(decoded[i][0] == bytes(frames[i][0]) for i in range(len(frames)))
rgb = bytearray(b"".join(bytes(PALETTE[i]) for i in decoded[5][0]))
assert read_text(W, rgb, 2, (255, 255, 255), 0, len(FLAG), left, top) == FLAG

# === Medium ====================================================================

# Dark Room: a black picture with the flag written one shade brighter than
# black. Paint's fill bucket only fills the exact colour clicked, so it shows.
FLAG = "FLAG{TURN_THE_LIGHTS_ON}"
WIDTH, HEIGHT, SCALE = 960, 540, 4
TEXT = (8, 8, 8)
text_width = len(FLAG) * 6 * SCALE
left, top = (WIDTH - text_width) // 2, (HEIGHT - 7 * SCALE) // 2
_, _, ink = text_image(FLAG, SCALE, TEXT, (0, 0, 0), 0)
ink_width = len(FLAG) * 6 * SCALE - SCALE
pixels = bytearray(WIDTH * HEIGHT * 3)
for y in range(7 * SCALE):
    for x in range(ink_width):
        if ink[(y * ink_width + x) * 3 : (y * ink_width + x) * 3 + 3] == bytes(TEXT):
            pixels[((top + y) * WIDTH + left + x) * 3 : ((top + y) * WIDTH + left + x) * 3 + 3] = bytes(TEXT)
# A few dust specks, kept clear of the text so they can't hide a letter.
rng = random.Random("dark-room")
for _ in range(140):
    x, y = rng.randrange(WIDTH), rng.randrange(HEIGHT)
    if top - 12 <= y <= top + 7 * SCALE + 12 and left - 12 <= x <= left + text_width + 12:
        continue
    level = rng.randint(90, 230)
    pixels[(y * WIDTH + x) * 3 : (y * WIDTH + x) * 3 + 3] = bytes((level, level, level))
data = png(WIDTH, HEIGHT, pixels)
write("dark-room", "dark_room.png", data)
decoded = read_png(data)[2]
assert read_text(WIDTH, decoded, SCALE, TEXT, 0, len(FLAG), left, top) == FLAG
assert max(decoded[((top + 3) * WIDTH + left) * 3: ((top + 3) * WIDTH + left + ink_width) * 3]) == 8

# Inside the Doc: a Word document is a zip; the flag is a picture left inside.
FLAG = "FLAG{A_DOCX_IS_A_ZIP}"
INK, PAPER = (30, 30, 40), (245, 245, 240)
width, height, pixels = text_image(FLAG, 4, INK, PAPER, 24)
picture = png(width, height, pixels)
assert read_text(width, read_png(picture)[2], 4, INK, 24, len(FLAG)) == FLAG
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
paragraphs = [
    "Surprise Party Plan",
    "The party is on Saturday at 7 pm. Everyone arrives at 6:30 and hides behind the sofa.",
    "Bring snacks, but not the spicy chips again.",
    "The photo of the secret party code has been removed from this plan, just in case.",
    "Shh!",
]
document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    f'<w:document xmlns:w="{W_NS}"><w:body>'
    + "".join(f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>" for text in paragraphs)
    + "</w:body></w:document>"
)
parts = {
    "[Content_Types].xml": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    ),
    "_rels/.rels": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/></Relationships>'
    ),
    "word/document.xml": document,
    # The picture is still listed here, so Word doesn't complain, but no
    # paragraph shows it any more.
    "word/_rels/document.xml.rels": (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
        'Target="media/party_code.png"/></Relationships>'
    ),
    "word/media/party_code.png": picture,
}
data = plain_zip(parts, (2026, 3, 6, 18, 0, 0))
write("inside-the-doc", "party_plan.docx", data)
with zipfile.ZipFile(io.BytesIO(data)) as bundle:
    assert bundle.read("word/media/party_code.png") == picture
    assert b"party_code.png" not in bundle.read("word/document.xml")

# Stowaway: a zip file appended after the end of a holiday photo.
FLAG = "FLAG{st0w4w4y_z1p_f0und}"
LIST = f"""PACKING LIST
- sunscreen
- 3 books I won't read
- charger (don't forget it this time)
- secret: {FLAG}
"""
pixels = scene(960, 600, "stowaway", (70, 140, 220), (180, 220, 250), (60, 130, 80),
               horizon=0.55, sun=(180, 110, 40, (255, 250, 220)))
image = png(960, 600, pixels)
data = image + plain_zip({"packing_list.txt": LIST}, (2026, 4, 1, 8, 0, 0))
write("stowaway", "holiday.png", data)
assert read_png(data)[4] == len(image) and b"FLAG" not in data
with zipfile.ZipFile(io.BytesIO(data)) as bundle:
    assert bundle.namelist() == ["packing_list.txt"] and FLAG in bundle.read("packing_list.txt").decode()

# Plain Login: HTTP Basic authentication in a capture. Two attempts: the first
# password is wrong (401), the second works (200), and it's the flag.
FLAG = "FLAG{b4s1c_4uth_1s_just_b4s364}"


def basic_login(password):
    import base64
    token = base64.b64encode(f"sam:{password}".encode()).decode()
    return http_get("/admin", extra=f"Authorization: Basic {token}\r\n")


frames = []
frames += conversation(50101, 80, [(True, http_get("/")), (False, http_reply("200 OK", "text/plain", "Office intranet home"))])
frames += conversation(50102, 80, [(True, http_get("/lunch-menu")), (False, http_reply("200 OK", "text/plain", "Today: noodles"))])
frames += conversation(50103, 80, [(True, basic_login("password123")), (False, http_reply("401 Unauthorized", "text/plain", "Wrong password"))])
frames += conversation(50104, 80, [(True, basic_login(FLAG)), (False, http_reply("200 OK", "text/plain", "Welcome back, Sam"))])
frames += conversation(50105, 80, [(True, http_get("/admin/settings")), (False, http_reply("200 OK", "text/plain", "Settings"))])
data = pcap(frames)
write("plain-login", "login_capture.pcap", data)
assert b"FLAG" not in data and data.count(b"Authorization: Basic ") == 2

# Old School: two FTP logins in plain text. The first fails, the second works,
# and its password is the flag.
FLAG = "FLAG{ftp_n3v3r_h1d3s_p4ssw0rds}"
ftp = [
    (False, b"220 Office file server ready.\r\n"),
    (True, b"USER alex\r\n"),
    (False, b"331 Password required for alex.\r\n"),
    (True, b"PASS letmein\r\n"),
    (False, b"530 Login incorrect.\r\n"),
    (True, b"USER alex\r\n"),
    (False, b"331 Password required for alex.\r\n"),
    (True, b"PASS " + FLAG.encode() + b"\r\n"),
    (False, b"230 User alex logged in.\r\n"),
    (True, b"PWD\r\n"),
    (False, b'257 "/home/alex" is the current directory.\r\n'),
    (True, b"QUIT\r\n"),
    (False, b"221 Goodbye.\r\n"),
]
frames = []
frames += conversation(50201, 80, [(True, http_get("/")), (False, http_reply("200 OK", "text/plain", "Office intranet home"))])
frames += conversation(50202, 21, ftp)
frames += conversation(50203, 80, [(True, http_get("/calendar")), (False, http_reply("200 OK", "text/plain", "No meetings today"))])
data = pcap(frames, start=1795100000)
write("old-school", "ftp_capture.pcap", data)
assert data.count(b"PASS ") == 2 and (b"PASS " + FLAG.encode()) in data

# Seeing Sound: the flag drawn in sound, visible in a spectrogram. Time runs
# left to right through the text, and each of the font's 7 rows is a band of
# frequencies, top row highest. Each band is a few close tones, so the letters
# look solid.
FLAG = "FLAG{LOOK_DONT_LISTEN}"
RATE = 22050
COLUMN = 0.08  # seconds per font column
LOW, HIGH = 2000, 8000
band = (HIGH - LOW) / 7
columns = []
for char in FLAG:
    for column in range(5):
        columns.append([FONT[char][row][column] == "1" for row in range(7)])
    columns.append([False] * 7)
per_column = int(RATE * COLUMN)
OFFSETS = (-300, -180, -60, 60, 180, 300)  # six close tones make each row a solid bar
TONE = 0.045
ramp = int(RATE * 0.015)
rng = random.Random("seeing-sound")
lead = int(RATE * 0.5)
total = lead * 2 + per_column * len(columns)
# Each row fades in and out on its own, and only when it changes, so the sound
# doesn't click (a click shows up as a line across the whole spectrogram).
envelopes = []
for row in range(7):
    target = [0.0] * total
    for index, lit in enumerate(columns):
        if lit[row]:
            for n in range(lead + index * per_column, lead + (index + 1) * per_column):
                target[n] = 1.0
    envelope, level, step = [0.0] * total, 0.0, 1.0 / ramp
    for n in range(total):
        level = min(target[n], level + step) if target[n] > level else max(target[n], level - step)
        envelope[n] = level
    envelopes.append(envelope)
samples = []
for n in range(total):
    t = n / RATE
    value = rng.uniform(-0.004, 0.004)
    for row in range(7):
        if envelopes[row][n]:
            centre = HIGH - (row + 0.5) * band
            value += envelopes[row][n] * TONE * sum(math.sin(2 * math.pi * (centre + o) * t) for o in OFFSETS)
    samples.append(value)
peak = max(abs(v) for v in samples)
samples = [v * 0.95 / peak for v in samples]  # as loud as possible without clipping
pcm = struct.pack(f"<{len(samples)}h", *(int(max(-1.0, min(1.0, s)) * 30000) for s in samples))
sound = io.BytesIO()
with wave.open(sound, "wb") as out:
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(RATE)
    out.writeframes(pcm)
write("seeing-sound", "mystery.wav", sound.getvalue())


def strength(chunk_samples, frequency):
    """Goertzel: how much of one frequency is in a run of samples."""
    k = 2 * math.cos(2 * math.pi * frequency / RATE)
    a = b = 0.0
    for sample in chunk_samples:
        a, b = sample + k * a - b, a
    return a * a + b * b - k * a * b


levels = []
for index in range(len(columns)):
    middle = samples[lead + index * per_column + per_column // 4 : lead + index * per_column + 3 * per_column // 4]
    levels.append([strength(middle, HIGH - (row + 0.5) * band + 60) for row in range(7)])
loudest = max(max(row) for row in levels)
assert [[level > loudest * 0.1 for level in row] for row in levels] == columns
assert max(abs(v) for v in samples) < 1.0  # no clipping

# === Hard ======================================================================

# Wire Tap: a capture with an FTP login and an HTTP download. The download is a
# password-locked zip, and the password is the one the same person used for FTP
# (the second, working one). The flag is in the zip.
FLAG = "FLAG{s4m3_p4ssw0rd_tw1c3}"
PASSWORD = "sunflower42"
NOTE = f"""Q3 bonus list - CONFIDENTIAL

Everyone gets a bonus this year, and pizza on Friday.

{FLAG}
"""
locked = locked_zip("bonus_list.txt", NOTE.encode(), PASSWORD, (2026, 9, 30, 17, 45, 0), "wire-tap")
with zipfile.ZipFile(io.BytesIO(locked)) as bundle:
    assert bundle.read("bonus_list.txt", pwd=PASSWORD.encode()).decode() == NOTE
    for wrong in (b"autumn2026", b"sunflower"):
        try:
            bundle.read("bonus_list.txt", pwd=wrong)
            raise AssertionError("a wrong password opened the zip")
        except RuntimeError:
            pass
        except zipfile.BadZipFile:
            pass
# File names in a zip are never locked, but the note's contents are.
assert b"FLAG" not in locked and b"pizza" not in locked
ftp = [
    (False, b"220 Office file server ready.\r\n"),
    (True, b"USER jamie\r\n"),
    (False, b"331 Password required for jamie.\r\n"),
    (True, b"PASS autumn2026\r\n"),
    (False, b"530 Login incorrect.\r\n"),
    (True, b"USER jamie\r\n"),
    (False, b"331 Password required for jamie.\r\n"),
    (True, b"PASS " + PASSWORD.encode() + b"\r\n"),
    (False, b"230 User jamie logged in.\r\n"),
    (True, b"QUIT\r\n"),
    (False, b"221 Goodbye.\r\n"),
]
INK, PAPER = (60, 60, 60), (255, 255, 255)
w2, h2, p2 = text_image("OFFICE LUNCH MENU", 3, INK, PAPER, 20)
menu_png = png(w2, h2, p2)
page = (
    "<html><head><title>Files</title></head><body><h1>Shared files</h1>"
    "<img src=/images/menu.png><ul><li><a href=/files/bonus_list.zip>bonus_list.zip</a></li></ul>"
    "<p>Zips are locked with your usual password.</p></body></html>"
)
frames = []
frames += conversation(50301, 80, [(True, http_get("/files/")), (False, http_reply("200 OK", "text/html", page))])
frames += conversation(50302, 80, [(True, http_get("/images/menu.png")), (False, http_reply("200 OK", "image/png", menu_png))])
frames += conversation(50303, 21, ftp)
frames += conversation(50304, 80, [(True, http_get("/files/bonus_list.zip")), (False, http_reply("200 OK", "application/zip", locked))])
data = pcap(frames, start=1795200000)
write("wire-tap", "office_capture.pcap", data)
assert data.count(b"PASS ") == 2 and locked in data and b"FLAG" not in data

# Least Significant: the flag is in the lowest bit of each BLUE value, read
# left to right and top to bottom, highest bit of each byte first, ending with a
# zero byte. The description doesn't say which colour.
FLAG = "FLAG{blu3_b1ts_t3ll_t4l3s}"
pixels = scene(480, 300, "least-significant", (120, 190, 240), (210, 235, 250), (70, 150, 60),
               horizon=0.5, sun=(90, 70, 22, (255, 245, 200)))
bits = [(byte >> shift) & 1 for byte in FLAG.encode() + b"\x00" for shift in range(7, -1, -1)]
for index, bit in enumerate(bits):
    pixels[index * 3 + 2] = (pixels[index * 3 + 2] & 0xFE) | bit
data = png(480, 300, pixels)
write("least-significant", "garden.png", data)
decoded = read_png(data)[2]


def lsb_text(values):
    out = bytearray()
    for i in range(0, len(values) - 7, 8):
        value = 0
        for v in values[i : i + 8]:
            value = (value << 1) | (v & 1)
        if value == 0:
            break
        out.append(value)
    return bytes(out)


assert lsb_text(decoded[2::3]).decode() == FLAG
assert not lsb_text(decoded[0::3]).startswith(b"FLAG") and not lsb_text(decoded[1::3]).startswith(b"FLAG")
assert b"FLAG" not in data

# Bit Planes: the flag is a picture, drawn into the lowest bit of the RED
# values. Shown on its own (CyberChef's View Bit Plane), that bit draws the
# flag; the picture itself looks unchanged.
FLAG = "FLAG{HIDDEN_IN_A_BIT_PLANE}"
WIDTH, HEIGHT, SCALE, MARGIN = 600, 300, 3, 30
pixels = scene(WIDTH, HEIGHT, "bit-planes", (20, 24, 60), (90, 60, 120), (30, 30, 40),
               horizon=0.7, sun=(480, 80, 16, (250, 250, 230)), noise=6)
_, _, ink = text_image(FLAG, SCALE, (1, 1, 1), (0, 0, 0), 0)
ink_width = len(FLAG) * 6 * SCALE - SCALE
left, top = (WIDTH - ink_width) // 2, (HEIGHT - 7 * SCALE) // 2
for y in range(HEIGHT):
    for x in range(WIDTH):
        inside = left <= x < left + ink_width and top <= y < top + 7 * SCALE
        bit = ink[((y - top) * ink_width + (x - left)) * 3] if inside else 0
        offset = (y * WIDTH + x) * 3
        pixels[offset] = (pixels[offset] & 0xFE) | bit
data = png(WIDTH, HEIGHT, pixels)
write("bit-planes", "city_lights.png", data)
decoded = read_png(data)[2]
assert read_text(WIDTH, decoded, SCALE, lambda rgb: rgb[0] & 1 == 1, 0, len(FLAG), left, top) == FLAG
# The other colours' lowest bits are noise, not text.
assert read_text(WIDTH, decoded, SCALE, lambda rgb: rgb[1] & 1 == 1, 0, len(FLAG), left, top) != FLAG
assert read_text(WIDTH, decoded, SCALE, lambda rgb: rgb[2] & 1 == 1, 0, len(FLAG), left, top) != FLAG
assert not lsb_text(decoded[0::3]).startswith(b"FLAG")

print("SITS Forensics downloads written and checked.")
