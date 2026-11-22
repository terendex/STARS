"""Regenerates the player downloads for every Lyra star, using only the standard library.

Run this after changing a flag, then push the files with ctfcli challenge sync.
Each star checks its own download where Python can: the flag has to come back
out the way a player would get it. Flags drawn as pictures (Sulafat, Ring Nebula,
Kepler-62, M56, Zeta Lyrae) use capital letters only, from FONT below, so there
are no look-alike characters, and CTFd accepts them in any case.
"""
import base64
import io
import math
import pathlib
import random
import struct
import wave
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parent
STAR_COLORS = [(255, 255, 255), (190, 215, 255), (255, 235, 200), (255, 205, 170)]
# Lyra's main stars, with Vega at the top
LYRA = [
    (470, 130, 5.0),
    (530, 190, 2.2),
    (440, 205, 2.0),
    (505, 275, 2.2),
    (415, 290, 2.3),
    (455, 395, 2.8),
    (555, 375, 2.6),
]


def write(star, name, data):
    path = ROOT / star / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def starfield(width, height, seed, named_stars=()):
    rng = random.Random(seed)
    pixels = bytearray(width * height * 3)

    def add_light(x, y, color, strength):
        if 0 <= x < width and 0 <= y < height:
            offset = (y * width + x) * 3
            for i in range(3):
                pixels[offset + i] = min(255, pixels[offset + i] + int(color[i] * strength))

    def draw_star(cx, cy, radius, color, strength=1.0):
        reach = int(radius * 4)
        for y in range(cy - reach, cy + reach + 1):
            for x in range(cx - reach, cx + reach + 1):
                distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                add_light(x, y, color, strength / (1 + (distance / radius) ** 4))

    # Faint background sky
    for y in range(height):
        for x in range(width):
            offset = (y * width + x) * 3
            glow = max(0, 1 - abs(x / width - y / height) * 2.2)
            noise = rng.randint(0, 5)
            pixels[offset] = 4 + noise + int(16 * glow)
            pixels[offset + 1] = 5 + noise + int(10 * glow)
            pixels[offset + 2] = 14 + noise + int(30 * glow)

    scale = width * height / (960 * 600)
    for _ in range(int(1400 * scale)):
        add_light(
            rng.randrange(width),
            rng.randrange(height),
            rng.choice(STAR_COLORS),
            rng.uniform(0.15, 0.9),
        )
    for _ in range(int(120 * scale)):
        draw_star(
            rng.randrange(width),
            rng.randrange(height),
            rng.uniform(0.7, 1.8),
            rng.choice(STAR_COLORS),
            rng.uniform(0.5, 1.0),
        )
    for cx, cy, radius in named_stars:
        draw_star(cx, cy, radius, (205, 225, 255))
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


def read_text(width, pixels, scale, fg, margin, length):
    """Reads FONT text back out of a text_image, to check a drawn flag."""
    glyphs = {"".join(rows): char for char, rows in FONT.items()}
    out = ""
    for index in range(length):
        rows = []
        for row in range(7):
            bits = ""
            for column in range(5):
                x = margin + index * 6 * scale + column * scale
                y = margin + row * scale
                bits += "1" if pixels[(y * width + x) * 3 : (y * width + x) * 3 + 3] == bytes(fg) else "0"
            rows.append(bits)
        out += glyphs["".join(rows)]
    return out


def pdf(stream):
    """A one-page PDF with Helvetica, drawing the given content stream."""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    return out


# --- Sheliak: the flag is in a PNG text chunk ---------------------------------
FLAG = "STARS{sh3l14k_s4ys_ch3ck_th3_m3t4d4t4}"
pixels = starfield(480, 300, "sheliak-second")
comment = chunk(b"tEXt", b"Comment\x00Observer note. Archive key: " + FLAG.encode())
data = png(480, 300, pixels, comment)
write("sheliak", "sheliak.png", data)
assert FLAG.encode() in data and read_png(data)[3][b"Comment"].endswith(FLAG.encode())

# --- Sulafat: a picture of the flag whose PNG signature was wiped -------------
# The first four bytes (89 50 4E 47) are zeros, so nothing will open it until a
# player writes them back in a hex editor.
FLAG = "STARS{FIX_THE_MAGIC_BYTES}"
INK, PAPER = (220, 230, 245), (10, 16, 32)
width, height, pixels = text_image(FLAG, 4, INK, PAPER, 24)
good = png(width, height, pixels)
broken = b"\x00\x00\x00\x00" + good[4:]
write("sulafat", "sulafat.png", broken)
assert broken[:8] == b"\x00\x00\x00\x00\r\n\x1a\n"
fixed = b"\x89PNG" + broken[4:]
assert read_text(width, read_png(fixed)[2], 4, INK, 24, len(FLAG)) == FLAG

# --- Aladfar: a "redacted" PDF whose black boxes sit on top of real text ------
FLAG = "STARS{4l4df4r_r3d4ct3d_b4dly}"
stream = b"\n".join(
    [
        b"BT /F1 20 Tf 72 720 Td (Lyra Survey: Observation Report) Tj ET",
        b"BT /F1 12 Tf 72 690 Td (Target: Aladfar \\(Eta Lyrae\\)) Tj ET",
        b"BT /F1 12 Tf 72 670 Td (Aladfar is a blue-white star in the constellation Lyra.) Tj ET",
        b"BT /F1 12 Tf 72 650 Td (Observer on duty: Dr. M. Reyes) Tj ET",
        b"BT /F1 12 Tf 72 620 Td (Archive key: " + FLAG.encode() + b") Tj ET",
        b"BT /F1 12 Tf 72 600 Td (Viewing was good all night, with no cloud cover.) Tj ET",
        b"BT /F1 12 Tf 72 570 Td (End of report. Redacted before public release.) Tj ET",
        # The "redactions": black rectangles drawn over the observer's name and the key.
        b"0 0 0 rg 182 646 140 16 re f",
        b"0 0 0 rg 70 616 330 16 re f",
    ]
)
data = pdf(stream)
write("aladfar", "aladfar_report.pdf", data)
assert FLAG.encode() in data and data.index(FLAG.encode()) < data.index(b"re f")

# --- Ring Nebula: an animated GIF with one frame shown for 20 milliseconds ----


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


FLAG = "STARS{ONE_FRAME_TOO_FAST}"
PALETTE = [(4, 6, 16), (40, 20, 70), (90, 40, 140), (150, 70, 200), (230, 120, 90), (255, 200, 140), (210, 225, 255), (255, 255, 255)]
W, H = 360, 220
rng = random.Random("ring-nebula")
sky = [0] * (W * H)
for _ in range(220):
    sky[rng.randrange(W * H)] = rng.choice([6, 7])


def ring_frame(glow):
    indices = list(sky)
    for y in range(H):
        for x in range(W):
            dx, dy = (x - W / 2) / 120, (y - H / 2) / 80
            r = math.hypot(dx, dy)
            if 0.55 < r < 1.0:
                band = abs(r - 0.78)
                indices[y * W + x] = [glow + 2, glow + 1, 2, 1][min(3, int(band * 18))]
            elif r <= 0.55:
                indices[y * W + x] = 1 if r > 0.12 else 6
    return indices


# The flag frame: the flag in white, on the same dark sky, no nebula.
text_w, text_h, text_pixels = text_image(FLAG, 2, (255, 255, 255), (4, 6, 16), 0)
flag_frame = list(sky)
left, top = (W - text_w) // 2, (H - text_h) // 2
for y in range(text_h):
    for x in range(text_w):
        if text_pixels[(y * text_w + x) * 3 : (y * text_w + x) * 3 + 3] == b"\xff\xff\xff":
            flag_frame[(top + y) * W + left + x] = 7
frames = [(ring_frame(g), 40) for g in (2, 3, 2, 3, 2)]
frames.insert(3, (flag_frame, 2))  # 2 hundredths of a second: too fast to read
data = gif(W, H, PALETTE, [(bytes(f), d) for f, d in frames])
write("ring-nebula", "ring_nebula.gif", data)
_, _, decoded = read_gif(data)
assert [d for _, d in decoded] == [40, 40, 40, 2, 40, 40]
assert decoded[3][0] == bytes(flag_frame) and all(decoded[i][0] == bytes(frames[i][0]) for i in range(6))

# --- Kepler-62: a Word document is a zip; the flag is a picture left inside ---
FLAG = "STARS{DOCX_IS_JUST_A_ZIP}"
INK, PAPER = (30, 30, 40), (245, 245, 240)
width, height, pixels = text_image(FLAG, 4, INK, PAPER, 24)
picture = png(width, height, pixels)
assert read_text(width, read_png(picture)[2], 4, INK, 24, len(FLAG)) == FLAG
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
paragraphs = [
    "Kepler-62 Survey Report",
    "Kepler-62 is a star in Lyra with five known planets. Two of them, Kepler-62e and "
    "Kepler-62f, orbit in the zone where liquid water could exist.",
    "Figure 1 (the archive photo of Kepler-62f) has been removed from this report "
    "before release.",
    "End of report.",
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
        'Target="media/kepler-62f.png"/></Relationships>'
    ),
    "word/media/kepler-62f.png": picture,
}
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
    for name, content in parts.items():
        info = zipfile.ZipInfo(name, date_time=(2025, 6, 2, 21, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        bundle.writestr(info, content)
data = archive.getvalue()
write("kepler-62", "kepler-62_report.docx", data)
with zipfile.ZipFile(io.BytesIO(data)) as bundle:
    assert bundle.read("word/media/kepler-62f.png") == picture
    assert b"kepler-62f.png" not in bundle.read("word/document.xml")

# --- Vega: a zip file appended after the end of the PNG -----------------------
FLAG = "STARS{v3g4_c4rr13s_4_st0w4w4y}"
LOG = f"""RIGHT ASCENSION  18h 36m 56s
DECLINATION      +38 47' 01"
TARGET           Vega (Alpha Lyrae)
STATUS           Exposure complete
ARCHIVE KEY      {FLAG}
"""
pixels = starfield(960, 600, "lyra-second", LYRA)
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
    info = zipfile.ZipInfo("vega_log.txt", date_time=(2025, 8, 12, 22, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    bundle.writestr(info, LOG)
image = png(960, 600, pixels)
data = image + archive.getvalue()
write("vega", "vega_deep_field.png", data)
assert read_png(data)[4] == len(image)
with zipfile.ZipFile(io.BytesIO(data)) as bundle:
    assert FLAG in bundle.read("vega_log.txt").decode()

# --- Network captures: Alathfar (FTP login) and Zeta Lyrae (HTTP download) -----
CLIENT = bytes((10, 20, 30, 40))
SERVER = bytes((10, 20, 30, 1))
CLIENT_MAC = bytes.fromhex("02aabbcc0028")
SERVER_MAC = bytes.fromhex("02aabbcc0001")
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


def pcap(frames, start=1790000000):
    out = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    for index, data in enumerate(frames):
        out += struct.pack("<IIII", start + index // 10, index * 10000 % 1000000, len(data), len(data))
        out += data
    return out


def http_get(path):
    return f"GET {path} HTTP/1.1\r\nHost: observatory.lyra.local\r\nUser-Agent: Mozilla/5.0\r\n\r\n".encode()


def http_ok(content_type, body):
    if isinstance(body, str):
        body = body.encode()
    head = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\n\r\n"
    return head.encode() + body


# Alathfar: two FTP logins in plain text. The first fails, the second works.
FLAG = "STARS{4l4thf4r_ftp_s3nds_1t_pl41n}"
ftp = [
    (False, b"220 Lyra Observatory FTP server ready.\r\n"),
    (True, b"USER astronomer\r\n"),
    (False, b"331 Password required for astronomer.\r\n"),
    (True, b"PASS vega-2025\r\n"),
    (False, b"530 Login incorrect.\r\n"),
    (True, b"USER astronomer\r\n"),
    (False, b"331 Password required for astronomer.\r\n"),
    (True, b"PASS " + FLAG.encode() + b"\r\n"),
    (False, b"230 User astronomer logged in.\r\n"),
    (True, b"PWD\r\n"),
    (False, b'257 "/home/astronomer" is the current directory.\r\n'),
    (True, b"QUIT\r\n"),
    (False, b"221 Goodbye.\r\n"),
]
frames = []
frames += conversation(49301, 80, [(True, http_get("/")), (False, http_ok("text/plain", "Lyra Observatory home page"))])
frames += conversation(49302, 80, [(True, http_get("/sky/tonight.html")), (False, http_ok("text/plain", "Clear skies tonight"))])
frames += conversation(49303, 21, ftp)
frames += conversation(49304, 80, [(True, http_get("/archive")), (False, http_ok("text/plain", "Archive index"))])
data = pcap(frames)
write("alathfar", "alathfar_capture.pcap", data)
assert data.count(b"PASS ") == 2 and (b"PASS " + FLAG.encode()) in data

# Zeta Lyrae: a web page and its pictures, sent over HTTP. One picture is the flag.
FLAG = "STARS{CARVED_FROM_THE_WIRE}"
INK, PAPER = (255, 230, 150), (12, 14, 30)
width, height, pixels = text_image(FLAG, 3, INK, PAPER, 20)
# Faint stars behind the text, which also make the picture big enough to need
# several packets, as real downloads do.
rng = random.Random("zeta-lyrae")
for _ in range(1800):
    spot = rng.randrange(width * height) * 3
    if pixels[spot : spot + 3] == bytes(PAPER):
        level = rng.randint(40, 160)
        pixels[spot : spot + 3] = bytes((level, level, min(255, level + 30)))
flag_png = png(width, height, pixels)
assert read_text(width, read_png(flag_png)[2], 3, INK, 20, len(FLAG)) == FLAG
w2, h2, p2 = text_image("TELESCOPE CAM OFFLINE", 3, (180, 180, 190), PAPER, 20)
decoy_png = png(w2, h2, p2)
page = (
    "<html><head><title>Zeta Lyrae</title><link rel=stylesheet href=/style.css></head>"
    "<body><h1>Zeta Lyrae tonight</h1><img src=/images/telescope.png>"
    "<p>Tonight's photo is only for staff.</p></body></html>"
)
frames = []
frames += conversation(49401, 80, [(True, http_get("/")), (False, http_ok("text/html", page))])
frames += conversation(49402, 80, [(True, http_get("/style.css")), (False, http_ok("text/css", "body { background: #000; color: #eee; }"))])
frames += conversation(49403, 80, [(True, http_get("/images/telescope.png")), (False, http_ok("image/png", decoy_png))])
frames += conversation(49404, 80, [(True, http_get("/staff/zeta_lyrae_tonight.png")), (False, http_ok("image/png", flag_png))])
data = pcap(frames, start=1790100000)
write("zeta-lyrae", "zeta_lyrae_capture.pcap", data)
assert len(flag_png) > 1460  # sent in more than one segment, as real downloads are

# --- M56: the flag drawn in sound, visible in a spectrogram ---------------------
# Time runs left to right through the text, and each of the font's 7 rows is a
# band of frequencies, top row highest. Each band is a few close tones, so the
# letters look solid.
FLAG = "STARS{SEE_THE_SOUND}"
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
rng = random.Random("m56")
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
write("m56", "m56_signal.wav", sound.getvalue())


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

# --- Double Double: the flag is in the lowest bit of each GREEN value, read left
# to right and top to bottom, highest bit of each byte first, ending with a zero byte
FLAG = "STARS{d0ubl3_d0ubl3_gr33n_b1ts}"
pixels = starfield(480, 300, "double-double-second")
bits = [(byte >> shift) & 1 for byte in FLAG.encode() + b"\x00" for shift in range(7, -1, -1)]
for index, bit in enumerate(bits):
    pixels[index * 3 + 1] = (pixels[index * 3 + 1] & 0xFE) | bit
data = png(480, 300, pixels)
write("double-double", "double_double.png", data)
green = read_png(data)[2][1::3]
recovered = bytearray()
for i in range(0, len(green), 8):
    value = 0
    for g in green[i : i + 8]:
        value = (value << 1) | (g & 1)
    if value == 0:
        break
    recovered.append(value)
assert recovered.decode() == FLAG

print("Lyra downloads written and checked.")
