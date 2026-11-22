"""Regenerates the player downloads for every Lyra star, using only the standard library.

Run this after changing a flag, then push the files with ctfcli challenge sync.
"""
import base64
import io
import pathlib
import random
import struct
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


# Sheliak: the flag is in a PNG text chunk
FLAG = "STARS{sh3l14k_m3t4d4t4_sp34ks}"
pixels = starfield(480, 300, "sheliak")
comment = chunk(b"tEXt", b"Comment\x00Observer note. Archive key: " + FLAG.encode())
write("sheliak", "sheliak.png", png(480, 300, pixels, comment))

# Sulafat: a picture of the flag, saved with the wrong extension. The text is in
# capitals with no look-alike characters, because players read it off an image.
FLAG = "STARS{SULAFAT_WRONG_EXTENSION}"
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "{": ["00110", "00100", "00100", "01000", "00100", "00100", "00110"],
    "}": ["01100", "00100", "00100", "00010", "00100", "00100", "01100"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
}
SCALE = 4
MARGIN = 24
width = MARGIN * 2 + len(FLAG) * 6 * SCALE
height = MARGIN * 2 + 7 * SCALE
pixels = bytearray(bytes((10, 16, 32)) * (width * height))
for index, char in enumerate(FLAG):
    for row, bits in enumerate(FONT[char]):
        for column, bit in enumerate(bits):
            if bit == "1":
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        x = MARGIN + index * 6 * SCALE + column * SCALE + dx
                        y = MARGIN + row * SCALE + dy
                        pixels[(y * width + x) * 3 : (y * width + x) * 3 + 3] = bytes((220, 230, 245))
write("sulafat", "notes.txt", png(width, height, pixels))

# Aladfar: white text on a white PDF page
FLAG = "STARS{4l4df4r_wh1t3_1nk}"
stream = b"\n".join(
    [
        b"BT /F1 20 Tf 72 720 Td (Lyra Survey: Observation Report) Tj ET",
        b"BT /F1 12 Tf 72 690 Td (Target: Aladfar \\(Eta Lyrae\\)) Tj ET",
        b"BT /F1 12 Tf 72 670 Td (Aladfar is a blue-white star in the constellation Lyra.) Tj ET",
        b"BT /F1 12 Tf 72 650 Td (Viewing was good all night, with no cloud cover.) Tj ET",
        b"1 1 1 rg BT /F1 12 Tf 72 620 Td (Archive key: " + FLAG.encode() + b") Tj ET 0 0 0 rg",
        b"BT /F1 12 Tf 72 590 Td (End of report.) Tj ET",
    ]
)
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
    b"/Resources << /Font << /F1 5 0 R >> >> >>",
    b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
]
pdf = b"%PDF-1.4\n"
offsets = []
for number, body in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf += b"%d 0 obj\n%s\nendobj\n" % (number, body)
xref = len(pdf)
pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
for offset in offsets:
    pdf += b"%010d 00000 n \n" % offset
pdf += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
write("aladfar", "aladfar_report.pdf", pdf)

# Vega: a zip file appended after the end of the PNG
FLAG = "STARS{v3g4_h1d3s_1n_th3_d33p_f13ld}"
LOG = f"""RIGHT ASCENSION  18h 36m 56s
DECLINATION      +38 47' 01"
TARGET           Vega (Alpha Lyrae)
STATUS           Exposure complete
ARCHIVE KEY      {FLAG}
"""
pixels = starfield(960, 600, "lyra", LYRA)
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
    bundle.writestr("observation_log.txt", LOG)
write("vega", "vega_deep_field.png", png(960, 600, pixels) + archive.getvalue())

# Alathfar: a network capture of an HTTP login with Basic authentication
FLAG = "STARS{4l4thf4r_sn1ff3d_th3_w1r3}"
CLIENT = bytes((10, 20, 30, 40))
SERVER = bytes((10, 20, 30, 1))
CLIENT_MAC = bytes.fromhex("02aabbcc0028")
SERVER_MAC = bytes.fromhex("02aabbcc0001")


def checksum(data):
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF


def frame(from_client, port, seq, ack, flags, payload=b"", ident=[1000]):
    src, dst = (CLIENT, SERVER) if from_client else (SERVER, CLIENT)
    sport, dport = (port, 80) if from_client else (80, port)
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


def session(port, request, response):
    c, s = 1000, 5000
    frames = [frame(True, port, c, 0, 0x02), frame(False, port, s, c + 1, 0x12)]
    c += 1
    s += 1
    frames.append(frame(True, port, c, s, 0x10))
    frames.append(frame(True, port, c, s, 0x18, request))
    c += len(request)
    frames.append(frame(False, port, s, c, 0x10))
    frames.append(frame(False, port, s, c, 0x18, response))
    s += len(response)
    frames.append(frame(True, port, c, s, 0x10))
    frames.append(frame(True, port, c, s, 0x11))
    c += 1
    frames.append(frame(False, port, s, c, 0x11))
    s += 1
    frames.append(frame(True, port, c, s, 0x10))
    return frames


def http_get(path, extra=""):
    return f"GET {path} HTTP/1.1\r\nHost: observatory.lyra.local\r\n{extra}\r\n".encode()


def http_login(password):
    token = base64.b64encode(f"astronomer:{password}".encode()).decode()
    return (
        "POST /login HTTP/1.1\r\nHost: observatory.lyra.local\r\n"
        f"Authorization: Basic {token}\r\nContent-Length: 0\r\n\r\n"
    ).encode()


def http_response(status, body):
    return f"HTTP/1.1 {status}\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()


frames = []
frames += session(49201, http_get("/"), http_response("200 OK", "Lyra Observatory home page"))
frames += session(49202, http_get("/sky/tonight.html"), http_response("200 OK", "Clear skies tonight"))
frames += session(49203, http_login("polaris1"), http_response("401 Unauthorized", "Wrong password"))
frames += session(49204, http_login(FLAG), http_response("200 OK", "Welcome back, astronomer"))
frames += session(49205, http_get("/archive"), http_response("200 OK", "Archive index"))

capture = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
for index, data in enumerate(frames):
    capture += struct.pack("<IIII", 1790000000 + index // 10, index * 10000 % 1000000, len(data), len(data))
    capture += data
write("alathfar", "alathfar_capture.pcap", capture)

# Double Double: the flag is in the lowest bit of each red value, read left to
# right and top to bottom, highest bit of each byte first, ending with a zero byte
FLAG = "STARS{d0ubl3_d0ubl3_b1ts_1n_th3_r3d}"
pixels = starfield(480, 300, "double-double")
bits = [(byte >> shift) & 1 for byte in FLAG.encode() + b"\x00" for shift in range(7, -1, -1)]
for index, bit in enumerate(bits):
    pixels[index * 3] = (pixels[index * 3] & 0xFE) | bit
write("double-double", "double_double.png", png(480, 300, pixels))
