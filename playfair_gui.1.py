"""
╔══════════════════════════════════════════════════════╗
║   PLAYFAIR SHIFR  —  Hacker Terminal + Animatsiya    ║
║   Tugma bosganda ishlaydi                             ║
╚══════════════════════════════════════════════════════╝
"""

import sys
from PyQt5.QtWidgets import (  # type: ignore
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QTimer  # type: ignore
from PyQt5.QtGui import QColor, QPalette, QPainter, QPen  # type: ignore

# ─── Algorithm ────────────────────────────────────────────────────────────────

# Matritsa 1: har doim standart alifbo (o'zgarmaydi)
ALPHA_DISPLAY = [
    ['A','B','C','D','E'],
    ['F','G','H','I/J','K'],
    ['L','M','N','O','P'],
    ['Q','R','S','T','U'],
    ['V','W','X','Y','Z'],
]
ALPHA_CALC = [
    ['A','B','C','D','E'],
    ['F','G','H','I','K'],
    ['L','M','N','O','P'],
    ['Q','R','S','T','U'],
    ['V','W','X','Y','Z'],
]

def build_key_display(key):
    """Ko'rsatish uchun matritsa — I/J bitta katakda."""
    alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    seen = set()
    chars = []  # type: ignore
    for ch in key.upper().replace('J','I') + alpha:
        if ch.isalpha() and ch not in seen:
            seen.add(ch); chars.append(ch)
    result = []
    for r in range(5):
        row = [('I/J' if ch == 'I' else ch) for ch in chars[r*5:r*5+5]]  # type: ignore
        result.append(row)
    return result

def build_key_calc(key):
    """Hisoblash uchun matritsa — oddiy harflar."""
    alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    seen = set()
    chars = []  # type: ignore
    for ch in key.upper().replace('J','I') + alpha:
        if ch.isalpha() and ch not in seen:
            seen.add(ch); chars.append(ch)
    return [chars[r*5:r*5+5] for r in range(5)]  # type: ignore

def get_pos(matrix, ch):
    ch = ch.replace('J','I')
    for r in range(5):
        for c in range(5):
            if matrix[r][c].replace('J','I') == ch: return r, c  # type: ignore
    raise ValueError(f"Not found: {ch}")

def prepare_text(text):
    clean = ''.join(c for c in text.upper().replace('J','I') if c.isalpha())
    pairs, i = [], 0
    while i < len(clean):
        a = clean[i]
        b = clean[i+1] if i+1 < len(clean) else 'X'
        if a == b: pairs.append((a,'X')); i += 1
        else:      pairs.append((a,b));   i += 2
    return pairs

def encrypt_pair(m1, m2, a, b):
    r1,c1 = get_pos(m1, a)
    r2,c2 = get_pos(m2, b)
    if r1 == r2:
        # Bir xil qatorda → o'ngga siljish (aylanib)
        return m1[r1][(c1+1)%5], m2[r2][(c2+1)%5]
    else:
        # Turli qator → to'rtburchak: M1 b ning qatori, M2 a ning qatori
        return m1[r2][c1], m2[r1][c2]

def decrypt_pair(m1, m2, a, b):
    r1,c1 = get_pos(m1, a)
    r2,c2 = get_pos(m2, b)
    if r1 == r2:
        # Bir xil qatorda → chapga siljish (aylanib)
        return m1[r1][(c1-1)%5], m2[r2][(c2-1)%5]
    else:
        # Turli qator → to'rtburchak (shifrlash bilan bir xil, o'z-o'ziga teskari)
        return m1[r2][c1], m2[r1][c2]

def remove_padding(text):
    result = list(text)
    i = 0
    cleaned = []
    while i < len(result):
        if result[i] == 'X':
            if i == len(result) - 1:
                i += 1; continue
            if i > 0 and i+1 < len(result) and cleaned and cleaned[-1] == result[i+1]:
                i += 1; continue
        cleaned.append(result[i])
        i += 1
    return ''.join(cleaned)

def run_cipher(text, key, mode):
    m1 = ALPHA_CALC
    m2 = build_key_calc(key)
    pairs = prepare_text(text)
    out = []
    for a,b in pairs:
        ea,eb = (encrypt_pair if mode=='encrypt' else decrypt_pair)(m1, m2, a, b)
        out.append(ea+eb)
    raw = ''.join(out)
    if mode == 'decrypt':
        return remove_padding(raw)
    return ' '.join(out)

# ─── Colors ───────────────────────────────────────────────────────────────────

BG    = "#070b07"
BG2   = "#0a0f0a"
G     = "#00ff41"
G3    = "#005020"
G4    = "#002a0d"
BLUE  = "#00bfff"
BLUE3 = "#003040"
DIM   = "#003010"
GOLD  = "#ffd700"
MONO  = "Courier New"

# ─── Matrix Cell ─────────────────────────────────────────────────────────────

class MatrixCell(QLabel):
    def __init__(self, letter, accent=G):
        super().__init__(letter)  # type: ignore
        self.letter = letter
        self.accent = accent
        self.lit    = False
        self.is_ij  = (letter == 'I/J')
        self._fsize = 10 if self.is_ij else 16
        self._ft = QTimer(self); self._ft.timeout.connect(self._fstep)
        self._fc = 0; self._fon = True
        self.setFixedSize(54, 50)
        self.setAlignment(Qt.AlignCenter)
        self._draw(False)

    def _draw(self, lit):
        self.lit = lit
        bc = GOLD if self.is_ij else self.accent
        if lit:
            self.setStyleSheet(f"""
                background:{bc}; color:#060b06;
                font-family:'{MONO}'; font-size:{self._fsize}pt; font-weight:bold;
                border:2px solid {bc};
            """)
        else:
            fg = GOLD if self.is_ij else self.accent
            brd = f"2px solid {GOLD}55" if self.is_ij else "1px solid #001a08"
            self.setStyleSheet(f"""
                background:#080d08; color:{fg};
                font-family:'{MONO}'; font-size:{self._fsize}pt; font-weight:bold;
                border:{brd};
            """)

    def set_lit(self, lit):
        self._ft.stop(); self._draw(lit)

    def flicker(self, cycles=6, interval=45):
        self._fc = cycles*2; self._fon = True; self._ft.start(interval)

    def _fstep(self):
        if self._fc <= 0:
            self._ft.stop(); self._draw(self.lit); return
        self._fc -= 1; self._fon = not self._fon
        c = GOLD if self.is_ij else self.accent
        if self._fon:
            self.setStyleSheet(f"background:rgba(0,255,65,0.18); color:{c}; font-family:'{MONO}'; font-size:{self._fsize}pt; font-weight:bold; border:1px solid {c};")
        else:
            self.setStyleSheet(f"background:#080d08; color:{G3}; font-family:'{MONO}'; font-size:{self._fsize}pt; font-weight:bold; border:1px solid #001208;")

    def enterEvent(self, e):
        if not self.lit:
            c = GOLD if self.is_ij else self.accent
            self.setStyleSheet(f"background:rgba(0,255,65,0.14); color:{c}; font-family:'{MONO}'; font-size:{self._fsize}pt; font-weight:bold; border:1px solid {c};")

    def leaveEvent(self, e):
        if not self.lit: self._draw(False)


# ─── Matrix Widget ────────────────────────────────────────────────────────────

class MatrixWidget(QFrame):
    def __init__(self, matrix, title, subtitle, accent=G):
        super().__init__()
        self.accent = accent
        self.cells  = {}
        self.setStyleSheet(f"background:{BG2}; border:1px solid {G4};")
        vlay = QVBoxLayout(self)
        vlay.setContentsMargins(10,10,10,10); vlay.setSpacing(4)

        self._tlbl = QLabel(title); self._tlbl.setAlignment(Qt.AlignCenter)
        self._tlbl.setStyleSheet(f"color:{accent}; font-family:'{MONO}'; font-size:10pt; letter-spacing:4px;")
        vlay.addWidget(self._tlbl)

        self._slbl = QLabel(subtitle); self._slbl.setAlignment(Qt.AlignCenter)
        self._slbl.setStyleSheet(f"color:{accent}55; font-family:'{MONO}'; font-size:8pt; letter-spacing:2px;")
        vlay.addWidget(self._slbl)

        ij = QLabel("★  I  va  J  →  bitta katakda"); ij.setAlignment(Qt.AlignCenter)
        ij.setStyleSheet(f"color:{GOLD}55; font-family:'{MONO}'; font-size:7pt;")
        vlay.addWidget(ij)

        cr = QHBoxLayout(); cr.setSpacing(0); cr.addSpacing(24)
        for n in range(1,6):
            l = QLabel(str(n)); l.setFixedWidth(54); l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet(f"color:{accent}33; font-family:'{MONO}'; font-size:8pt;")
            cr.addWidget(l)
        vlay.addLayout(cr)

        for ri, row in enumerate(matrix):
            rl = QHBoxLayout(); rl.setSpacing(2)
            rn = QLabel(str(ri+1)); rn.setFixedWidth(22)
            rn.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            rn.setStyleSheet(f"color:{accent}33; font-family:'{MONO}'; font-size:8pt;")
            rl.addWidget(rn)
            for ci, ch in enumerate(row):
                cell = MatrixCell(ch, accent)
                self.cells[(ri,ci)] = cell
                rl.addWidget(cell)
            vlay.addLayout(rl)

    def set_subtitle(self, t): self._slbl.setText(t)

    def update_letters(self, matrix):
        for (r,c), cell in self.cells.items():
            new_ch = matrix[r][c]
            if cell.letter != new_ch:
                cell.letter = new_ch; cell.is_ij = (new_ch=='I/J')
                cell._fsize = 10 if cell.is_ij else 16
                cell.setText(new_ch); cell.flicker(4,40)

    def highlight_char(self, ch):
        if not ch: self.highlight(set()); return
        ch_n = ch.upper().replace('J','I')
        pos = next(
            ((r,c) for (r,c),cell in self.cells.items()
             if cell.letter.replace('/','').replace('J','I') == ch_n
             or (ch_n in ('I','J') and cell.letter=='I/J')),
            None
        )
        if not pos: self.highlight(set()); return
        r0,c0 = pos
        self.highlight({(r0,i) for i in range(5)} | {(i,c0) for i in range(5)})

    def highlight(self, pos):
        for (r,c), cell in self.cells.items(): cell.set_lit((r,c) in pos)

    def clear_highlight(self): self.highlight(set())

    def flash_all(self, iv=35):
        for i,cell in enumerate(self.cells.values()):
            QTimer.singleShot(i*iv, lambda c=cell: c.flicker(3,40))

    def flash_chars(self, chars):
        for cell in self.cells.values():
            if cell.letter.replace('J','').replace('/','') in chars or cell.letter in chars:
                cell.flicker(5,50)


# ─── Glow Title ──────────────────────────────────────────────────────────────

class GlowLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)  # type: ignore
        self._ph = 0
        self.setAlignment(Qt.AlignCenter)
        t = QTimer(self); t.timeout.connect(self._pulse); t.start(80)

    def _pulse(self):
        import math
        self._ph = (self._ph + 5) % 360
        v = int(200 + 55*abs(math.sin(math.radians(self._ph))))
        self.setStyleSheet(f"color:rgb(0,{v},65); font-family:'{MONO}'; font-size:28pt; font-weight:bold; letter-spacing:10px;")


# ─── Typing Output ────────────────────────────────────────────────────────────

class TypingOutput(QTextEdit):
    def __init__(self):
        super().__init__(); self.setReadOnly(True)
        self._target=""; self._pos=0
        self._t = QTimer(self); self._t.timeout.connect(self._step)
        self.setMaximumHeight(110)
        self.setStyleSheet(f"QTextEdit {{ background:#050a05; border:1px solid {BLUE3}; color:{BLUE}; font-family:'{MONO}'; font-size:12pt; padding:8px; letter-spacing:3px; }}")

    def animate(self, text):
        self._target=text; self._pos=0; self.clear()
        self._t.stop()
        if text: self._t.start(30)

    def _step(self):
        if self._pos >= len(self._target): self._t.stop(); return
        self.insertPlainText(self._target[self._pos]); self._pos += 1


# ─── Scanlines ────────────────────────────────────────────────────────────────

class ScanlineWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)  # type: ignore
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self._off = 0
        t = QTimer(self); t.timeout.connect(lambda: (setattr(self,'_off',(self._off+2)%8), self.update())[1]); t.start(40)

    def paintEvent(self, e):
        p = QPainter(self); p.setOpacity(0.05)
        p.setPen(QPen(QColor(0,0,0),1))
        y = self._off
        while y < self.height(): p.drawLine(0,y,self.width(),y); y += 4
        p.end()

    def resizeEvent(self, e): self.setGeometry(self.parent().rect())


# ─── Alpha Bar ────────────────────────────────────────────────────────────────

class AlphaBar(QWidget):
    def __init__(self, on_hover, on_leave):
        super().__init__()
        lay = QHBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(3)
        for ch in list("ABCDEFGH") + ["I/J"] + list("KLMNOPQRSTUVWXYZ"):
            b = QPushButton(ch); w = 36 if ch=='I/J' else 27; b.setFixedSize(w,25)
            ij = ch=='I/J'
            b.setStyleSheet(f"""
                QPushButton {{ background:transparent;
                    border:1px solid {GOLD+'44' if ij else '#001508'};
                    color:{GOLD+'88' if ij else DIM};
                    font-family:'{MONO}'; font-size:{'7' if ij else '8'}pt; padding:0; }}
                QPushButton:hover {{ background:rgba(0,255,65,0.16);
                    border:1px solid {GOLD if ij else G}; color:{GOLD if ij else G}; }}
            """)
            b.enterEvent = lambda e, c=ch: on_hover(c)
            b.leaveEvent = lambda e: on_leave()
            lay.addWidget(b)
        lay.addStretch()


# ─── Main Window ─────────────────────────────────────────────────────────────

class PlayfairWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLAYFAIR SHIFR — Hacker Terminal")
        self.setMinimumSize(1020, 880)
        self._last_key = ""
        self._word_lengths = []

        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(BG))
        self.setPalette(pal)

        central = QWidget(); central.setStyleSheet(f"background:{BG};")
        self.setCentralWidget(central)
        self._scan = ScanlineWidget(central)

        main = QVBoxLayout(central)
        main.setContentsMargins(20,14,20,14); main.setSpacing(10)

        # Header
        hdr = QVBoxLayout(); hdr.setSpacing(3)
        hdr.addWidget(self._lbl("◄  K R I P T O G R A F I Y A   T I Z I M I  ►", G4, 8, True))
        hdr.addWidget(GlowLabel("PLAYFAIR  SHIFR"))
        hdr.addWidget(self._lbl("───  STANDART ALIFBO  ×  KALIT MATRITSA  ───", G4, 8, True))
        main.addLayout(hdr)

        # Row1: Key + Mode
        r1 = QHBoxLayout(); r1.setSpacing(12)

        kf = self._frame(G4)
        kl = QVBoxLayout(kf); kl.setContentsMargins(12,10,12,10); kl.setSpacing(5)
        kl.addWidget(self._lbl("► KALIT SO'Z  (Matritsa 2 uchun)", G))
        self.key_input = QLineEdit("UZBEKISTON")
        self.key_input.setStyleSheet(self._css_line(G))
        self.key_input.textChanged.connect(self._update_matrix2)
        kl.addWidget(self.key_input)
        kl.addWidget(self._lbl("Matritsa 1 — har doim standart alifbo  ·  Matritsa 2 — kalit asosida", G4, 7))
        r1.addWidget(kf, 3)

        # Rejim
        mf = self._frame(G4)
        ml = QVBoxLayout(mf); ml.setContentsMargins(12,10,12,10); ml.setSpacing(6)
        ml.addWidget(self._lbl("► SHIFRLASH REJIMI", G))
        br = QHBoxLayout(); br.setSpacing(8)

        self.btn_enc = QPushButton("🔒  SHIFRLASH")
        self.btn_dec = QPushButton("🔓  DESHIFRLASH")
        self.btn_enc.setCursor(Qt.PointingHandCursor)
        self.btn_dec.setCursor(Qt.PointingHandCursor)
        self.btn_enc.clicked.connect(self.do_encrypt)
        self.btn_dec.clicked.connect(self.do_decrypt)
        br.addWidget(self.btn_enc); br.addWidget(self.btn_dec)
        ml.addLayout(br); ml.addStretch()
        r1.addWidget(mf, 2)
        self._set_btn_active(None)
        main.addLayout(r1)

        # Row2: In / Out
        r2 = QHBoxLayout(); r2.setSpacing(12)

        inf = self._frame(G4)
        il = QVBoxLayout(inf); il.setContentsMargins(12,10,12,10); il.setSpacing(5)
        il.addWidget(self._lbl("► KIRUVCHI MATN", G))
        self.text_in = QTextEdit("HELLO WORLD")
        self.text_in.setMaximumHeight(105)
        self.text_in.setStyleSheet(self._css_edit(G))
        # Matn o'zgarganda faqat juftlar ko'rsatiladi
        self.text_in.textChanged.connect(self._update_pairs)
        il.addWidget(self.text_in)
        self.pairs_lbl = QLabel("Tayyorlangan juftlar: —")
        self.pairs_lbl.setStyleSheet(f"color:{G3}; font-family:'{MONO}'; font-size:7pt;")
        il.addWidget(self.pairs_lbl)
        r2.addWidget(inf)

        outf = self._frame(BLUE3)
        ol = QVBoxLayout(outf); ol.setContentsMargins(12,10,12,10); ol.setSpacing(5)
        oh = QHBoxLayout()
        oh.addWidget(self._lbl("► CHIQUVCHI MATN", BLUE)); oh.addStretch()
        cb = QPushButton("[ NUSXA ]")
        cb.setStyleSheet(f"QPushButton {{ background:transparent; border:none; color:{BLUE3}; font-family:'{MONO}'; font-size:8pt; letter-spacing:2px; padding:0 4px; }} QPushButton:hover {{ color:{BLUE}; }}")
        cb.setCursor(Qt.PointingHandCursor); cb.clicked.connect(self.copy_out)
        oh.addWidget(cb); ol.addLayout(oh)
        self.text_out = TypingOutput()
        ol.addWidget(self.text_out)
        self.step_lbl = QLabel("")
        self.step_lbl.setStyleSheet(f"color:{BLUE3}; font-family:'{MONO}'; font-size:7pt;")
        self.step_lbl.setWordWrap(True)
        ol.addWidget(self.step_lbl)
        r2.addWidget(outf)
        main.addLayout(r2)

        # Matrices
        mf2 = self._frame(G4)
        mfl = QVBoxLayout(mf2); mfl.setContentsMargins(14,12,14,12); mfl.setSpacing(8)
        mfl.addWidget(self._lbl("► 5 × 5  M A T R I T S A L A R", G, 9, True))
        mfl.addWidget(self._lbl("Harfga sichqonchani olib keling — ikki matritsada pozitsiyani ko'ring", G3, 7, True))



        ab_w = QWidget()
        ab_l = QHBoxLayout(ab_w); ab_l.setContentsMargins(0,0,0,0)
        ab_l.addStretch(); ab_l.addWidget(AlphaBar(self.on_hover, self.on_leave)); ab_l.addStretch()
        mfl.addWidget(ab_w)

        mr = QHBoxLayout(); mr.setSpacing(20); mr.addStretch()
        self.mw1 = MatrixWidget(ALPHA_DISPLAY, "MATRITSA  1", "STANDART ALIFBO", G)
        mr.addWidget(self.mw1)

        div = QVBoxLayout(); div.setAlignment(Qt.AlignCenter)
        for s in ["⊕","×","⊕"]:
            l = QLabel(s); l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet(f"color:{G4}; font-family:'{MONO}'; font-size:14pt;")
            div.addWidget(l)
        mr.addLayout(div)

        self.mw2 = MatrixWidget(build_key_display("UZBEKISTON"), "MATRITSA  2", '"UZBEKISTON" kaliti', BLUE)
        mr.addWidget(self.mw2)
        mr.addStretch()
        mfl.addLayout(mr)

        self.hover_lbl = QLabel("")
        self.hover_lbl.setAlignment(Qt.AlignCenter)
        self.hover_lbl.setStyleSheet(f"color:{G3}; font-family:'{MONO}'; font-size:8pt;")
        mfl.addWidget(self.hover_lbl)
        main.addWidget(mf2)

        # Boot animation
        QTimer.singleShot(300,  lambda: self.mw1.flash_all(30))
        QTimer.singleShot(1000, lambda: self.mw2.flash_all(30))

        self._last_key = "UZBEKISTON"
        self._update_pairs()

    # ── Helpers ──────────────────────────────────────────────

    def _frame(self, b):
        f = QFrame(); f.setStyleSheet(f"background:{BG2}; border:1px solid {b};"); return f

    def _lbl(self, t, c=G, s=8, center=False):
        l = QLabel(t)
        l.setStyleSheet(f"color:{c}; font-family:'{MONO}'; font-size:{s}pt; letter-spacing:3px;")
        if center: l.setAlignment(Qt.AlignCenter)
        return l

    def _css_line(self, c):
        return f"QLineEdit {{ background:#050a05; border:1px solid {G4}; color:{c}; font-family:'{MONO}'; font-size:11pt; padding:6px 8px; }} QLineEdit:focus {{ border:1px solid {c}; }}"

    def _css_edit(self, c):
        return f"QTextEdit {{ background:#050a05; border:1px solid {G4}; color:{c}; font-family:'{MONO}'; font-size:11pt; padding:6px 8px; }} QTextEdit:focus {{ border:1px solid {c}; }}"

    def _set_btn_active(self, mode):
        """mode='encrypt' yoki 'decrypt' yoki None"""
        ac  = f"QPushButton {{ background:rgba(0,255,65,0.12); border:2px solid {G}; color:{G}; font-family:'{MONO}'; font-size:10pt; letter-spacing:3px; padding:8px 16px; }}"
        in_ = f"QPushButton {{ background:transparent; border:1px solid {G4}; color:{DIM}; font-family:'{MONO}'; font-size:10pt; letter-spacing:3px; padding:8px 16px; }} QPushButton:hover {{ border:1px solid {G}; color:{G}; background:rgba(0,255,65,0.05); }}"
        self.btn_enc.setStyleSheet(ac  if mode=='encrypt' else in_)
        self.btn_dec.setStyleSheet(ac  if mode=='decrypt' else in_)

    # ── Matritsa 2 yangilanadi (kalit o'zgarganda) ──────────

    def _update_matrix2(self):
        key = self.key_input.text().strip()
        if key and key != self._last_key:
            self._last_key = key
            self.mw2.update_letters(build_key_display(key))
            self.mw2.set_subtitle(f'"{key.upper()}" kaliti')

    # ── Juftlar ko'rsatiladi (matn o'zgarganda) ─────────────

    def _update_pairs(self):
        text = self.text_in.toPlainText().strip()
        if text:
            pairs = prepare_text(text)
            self.pairs_lbl.setText("Tayyorlangan juftlar: " + "  ".join(a+b for a,b in pairs))
        else:
            self.pairs_lbl.setText("Tayyorlangan juftlar: —")

    # ── SHIFRLASH tugmasi ────────────────────────────────────

    def do_encrypt(self):
        self._set_btn_active('encrypt')
        self._run('encrypt')

    # ── DESHIFRLASH tugmasi ──────────────────────────────────

    def do_decrypt(self):
        self._set_btn_active('decrypt')
        self._run('decrypt')

    # ── Umumiy ishlov ────────────────────────────────────────

    def _run(self, mode):
        key  = self.key_input.text().strip()
        text = self.text_in.toPlainText().strip()

        if not key:
            self.text_out.animate("⚠  Kalit so'z kiriting!")
            self.step_lbl.setText(""); return
        if not text:
            self.text_out.animate("⚠  Matn kiriting!")
            self.step_lbl.setText(""); return

        try:
            result = run_cipher(text, key, mode)

            if mode == 'encrypt':
                self._word_lengths = [
                    len(''.join(c for c in w.upper().replace('J','I') if c.isalpha()))
                    for w in text.split()
                ]
                display = result
            else:
                display = self._restore_spaces(result, self._word_lengths)

            self.text_out.animate(display)

            rchars = set(result.replace(' ',''))
            QTimer.singleShot(100, lambda: self.mw1.flash_chars(rchars))
            QTimer.singleShot(200, lambda: self.mw2.flash_chars(rchars))

            # Step trace — birinchi juft
            pairs = prepare_text(text)
            if pairs:
                a, b = pairs[0]
                m2c = build_key_calc(key)
                p1  = get_pos(ALPHA_CALC, a)
                p2  = get_pos(m2c, b)
                if p1 and p2:
                    r1,c1 = p1; r2,c2 = p2
                    ea,eb = encrypt_pair(ALPHA_CALC, m2c, a, b)
                    rule = "Bir qatorda → o'ngga siljish" if r1==r2 else "To'rtburchak → ustunlar almashadi"
                    lbl = "SHIFRLASH" if mode=='encrypt' else "DESHIFRLASH"
                    self.step_lbl.setText(
                        f"[{lbl}]  {a}({r1+1},{c1+1}) × {b}({r2+1},{c2+1}) → {ea+eb}  [{rule}]"
                    )
        except Exception as ex:
            self.text_out.animate(f"XATO: {ex}")

    def _restore_spaces(self, text, word_lengths):
        """Deshifrlangan matnni asl so'z bo'shliqlariga qaytaradi."""
        if not word_lengths:
            return text
        words = []
        pos = 0
        for length in word_lengths:
            chunk = text[pos:pos + length]
            if chunk:
                words.append(chunk)
            pos += length
        # Qolgan harflar bo'lsa (agar uzunlik to'g'ri kelmasa)
        if pos < len(text):
            words.append(text[pos:])
        return ' '.join(words)

    def on_hover(self, ch):
        self.mw1.highlight_char(ch)
        self.mw2.highlight_char(ch)
        note = "  ·  I va J bir xil katak" if ch in ('I','J','I/J') else ""
        self.hover_lbl.setText(f"«{ch}» —  Yashil: Matritsa 1  ·  Ko'k: Matritsa 2{note}")

    def on_leave(self):
        self.mw1.clear_highlight(); self.mw2.clear_highlight(); self.hover_lbl.setText("")

    def copy_out(self):
        QApplication.clipboard().setText(self.text_out.toPlainText())
        orig = self.text_out.styleSheet()
        self.text_out.setStyleSheet(orig.replace(BLUE, G))
        QTimer.singleShot(500, lambda: self.text_out.setStyleSheet(orig))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self,'_scan'): self._scan.setGeometry(self.centralWidget().rect())


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dark = QPalette()
    dark.setColor(QPalette.Window,          QColor(BG))
    dark.setColor(QPalette.WindowText,      QColor(G))
    dark.setColor(QPalette.Base,            QColor("#050a05"))
    dark.setColor(QPalette.AlternateBase,   QColor(BG2))
    dark.setColor(QPalette.Text,            QColor(G))
    dark.setColor(QPalette.Button,          QColor(BG2))
    dark.setColor(QPalette.ButtonText,      QColor(G))
    dark.setColor(QPalette.Highlight,       QColor(G4))
    dark.setColor(QPalette.HighlightedText, QColor(G))
    app.setPalette(dark)
    win = PlayfairWindow()
    win.show()
    sys.exit(app.exec_())
