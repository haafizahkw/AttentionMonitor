STYLESHEET = """
/* ═══════════════════════════════════════════
   GLOBAL
═══════════════════════════════════════════ */
* {
    font-family: 'Courier New', 'Consolas', monospace;
    color: #C8F0FF;
}

QMainWindow, QWidget {
    background-color: #050D14;
}

/* ═══════════════════════════════════════════
   HEADER
═══════════════════════════════════════════ */
QLabel#titleLabel {
    font-family: 'Courier New', monospace;
    font-size: 20px;
    font-weight: bold;
    color: #00E5FF;
    letter-spacing: 6px;
    padding: 4px 0px;
}

QLabel#subtitleLabel {
    font-family: 'Courier New', monospace;
    font-size: 10px;
    color: #2A6F8A;
    letter-spacing: 4px;
}

/* ═══════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════ */
QFrame#divider {
    background-color: #00E5FF;
    border: none;
    max-height: 1px;
}

/* ═══════════════════════════════════════════
   FACE CARDS
═══════════════════════════════════════════ */
QWidget#faceCard {
    background-color: #071520;
    border: 1px solid #0A3A52;
    border-left: 3px solid #00E5FF;
    border-radius: 4px;
    padding: 8px;
}

QWidget#faceCard:hover {
    border-left: 3px solid #00FFCC;
    background-color: #091C2A;
}

QLabel#cardTitle {
    font-size: 13px;
    font-weight: bold;
    color: #00E5FF;
    letter-spacing: 3px;
    padding-bottom: 4px;
}

QLabel#cardStat {
    font-size: 11px;
    color: #7ECFEA;
    letter-spacing: 1px;
    padding: 1px 0px;
}

QFrame#cardDivider {
    background-color: #0A3A52;
    border: none;
    max-height: 1px;
    margin: 4px 0px;
}

/* ═══════════════════════════════════════════
   AWARENESS BAR
═══════════════════════════════════════════ */
QProgressBar {
    background-color: #071520;
    border: 1px solid #0A3A52;
    border-radius: 3px;
    text-align: center;
    font-size: 10px;
    color: #C8F0FF;
    letter-spacing: 1px;
}

QProgressBar::chunk {
    border-radius: 3px;
    background-color: #00E5FF;
}

/* ═══════════════════════════════════════════
   LOG AREA
═══════════════════════════════════════════ */
QTextEdit {
    background-color: #030C12;
    border: 1px solid #0A3A52;
    border-radius: 4px;
    font-size: 10px;
    color: #3A9BBF;
    padding: 6px;
    selection-background-color: #00E5FF;
    selection-color: #050D14;
}

QScrollBar:vertical {
    background: #050D14;
    width: 6px;
    border: none;
}

QScrollBar::handle:vertical {
    background: #0A3A52;
    border-radius: 3px;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ═══════════════════════════════════════════
   CAMERA VIEW
═══════════════════════════════════════════ */
CameraView {
    background-color: #030C12;
    border: 1px solid #0A3A52;
    border-radius: 4px;
}

/* ═══════════════════════════════════════════
   GENERIC LABELS (log title etc)
═══════════════════════════════════════════ */
QLabel {
    font-size: 11px;
    color: #7ECFEA;
    letter-spacing: 1px;
}
"""