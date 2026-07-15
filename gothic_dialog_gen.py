#!/usr/bin/env python3
"""
Gothic Dialog Generator — Minimal Edition
All visual design is defined in the THEME block below. Nothing else in the
file contains hard-coded colors, font names, or sizes.
"""

import sys
import os
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QScrollArea,
    QSpinBox, QCheckBox, QComboBox, QSplitter, QTabWidget,
    QMessageBox, QFileDialog, QGroupBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat, QPalette


# ═════════════════════════════════════════════════════════════════════════════=
#  THEME  —  change everything visual here, nowhere else
# ═════════════════════════════════════════════════════════════════════════════=
from theme import THEME

# ── Derived stylesheet fragments (built once from THEME, used everywhere) ─────

def _ss_field():
    t = THEME
    return (
        f"QLineEdit {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:5px 8px; "
        f"  selection-background-color:{t['accent_primary']}; "
        f"  font-family:{t['font_ui']}; }}"
        f"QLineEdit:focus {{ border:{t['border_width']} solid {t['accent_primary']}; }}"
        f"QLineEdit::placeholder {{ color:{t['text_muted']}; }}"
    )

def _ss_spin():
    t = THEME
    return (
        f"QSpinBox {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:2px 4px; }}"
        f"QSpinBox:focus {{ border:{t['border_width']} solid {t['accent_primary']}; }}"
    )

def _ss_combo():
    t = THEME
    return (
        f"QComboBox {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:3px 6px; }}"
        f"QComboBox::drop-down {{ border:none; }}"
        f"QComboBox QAbstractItemView {{ background:{t['bg_panel']}; color:{t['text_primary']}; "
        f"  selection-background-color:{t['accent_primary']}; "
        f"  selection-color:{t['bg_main']}; }}"
    )

def _ss_check():
    t = THEME
    return (
        f"QCheckBox {{ color:{t['text_secondary']}; spacing:6px; }}"
        f"QCheckBox::indicator {{ width:13px; height:13px; "
        f"  border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:3px; background:{t['bg_input']}; }}"
        f"QCheckBox::indicator:checked {{ background:{t['accent_primary']}; "
        f"  border-color:{t['accent_primary']}; }}"
    )

def _ss_group():
    t = THEME
    return (
        f"QGroupBox {{ color:{t['accent_gold']}; font-weight:600; font-size:{t['font_size_small']}; "
        f"  letter-spacing:0.3px; border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:{t['radius_lg']}; margin-top:10px; padding-top:6px; "
        f"  background:{t['bg_panel']}; font-family:{t['font_ui']}; }}"
        f"QGroupBox::title {{ subcontrol-origin:margin; left:10px; "
        f"  background:{t['bg_panel']}; padding:0 4px; }}"
    )

def _ss_add_btn():
    t = THEME
    return (
        f"QPushButton {{ background:{t['bg_bar']}; color:{t['text_secondary']}; "
        f"  border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:5px 12px; "
        f"  font-size:{t['font_size_small']}; font-weight:600; }}"
        f"QPushButton:hover {{ background:{t['bg_input_border']}; color:{t['text_primary']}; }}"
    )

def _ss_rm_btn():
    t = THEME
    return (
        f"QPushButton {{ background:transparent; color:{t['text_muted']}; border:none; }}"
        f"QPushButton:hover {{ color:{t['accent_hover']}; }}"
    )

def _ss_global():
    t = THEME
    return f"""
        QMainWindow, QWidget {{
            background: {t['bg_main']};
            color: {t['text_primary']};
            font-family: {t['font_ui']};
            font-size: {t['font_size_ui']};
        }}
        QLabel {{ color: {t['text_secondary']}; }}
        QScrollBar:vertical {{
            background: {t['bg_panel']}; width: 8px; border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {t['bg_border']}; border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QSplitter::handle {{ background: {t['bg_border']}; }}
        QTabWidget::pane {{
            border: {t['border_width']} solid {t['bg_border']};
            background: {t['bg_main']};
            border-radius: {t['radius_md']};
            top: -1px;
        }}
        QTabBar::tab {{
            background: transparent;
            color: {t['text_secondary']};
            padding: 6px 14px;
            border: none;
            margin-right: 2px;
            font-family: {t['font_ui']};
        }}
        QTabBar::tab:selected {{
            color: {t['accent_primary']};
            font-weight: 700;
            border-bottom: 2px solid {t['accent_primary']};
        }}
        QMessageBox {{ background: {t['bg_main']}; }}
    """

# Build all sheets once at import time
SS = {
    "field":    _ss_field(),
    "spin":     _ss_spin(),
    "combo":    _ss_combo(),
    "check":    _ss_check(),
    "group":    _ss_group(),
    "add_btn":  _ss_add_btn(),
    "rm_btn":   _ss_rm_btn(),
    "global":   _ss_global(),
}

# ══════════════════════════════════════════════════════════════════════════════
#  END OF THEME
# ══════════════════════════════════════════════════════════════════════════════


# ── Syntax Highlighter ────────────────────────────────────────────────────────
class DaedalusHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        t = THEME
        self.rules = []

        def fmt(color, bold=False, italic=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:   f.setFontWeight(QFont.Weight.Bold)
            if italic: f.setFontItalic(True)
            return f

        kw = fmt(t["syn_keyword"], bold=True)
        for w in ["instance","func","void","int","var","return","if","else",
                  "INSTANCE","FUNC","VOID","INT","VAR"]:
            self.rules.append((re.compile(r'\b' + w + r'\b'), kw))

        tp = fmt(t["syn_type"], bold=True)
        for w in ["C_INFO","TRUE","FALSE","LOG_MISSION","LOG_NOTE",
                  "LOG_RUNNING","LOG_SUCCESS","DIALOG_ENDE"]:
            self.rules.append((re.compile(r'\b' + w + r'\b'), tp))

        fn = fmt(t["syn_function"])
        for w in ["AI_Output","AI_StopProcessInfos","B_GiveXP","B_GiveInvItems",
                  "CreateInvItems","Log_CreateTopic","Log_SetTopicStatus","B_LogEntry",
                  "Info_ClearChoices","Info_AddChoice","Npc_KnowsInfo",
                  "Npc_GetTrueGuild","Npc_IsInState"]:
            self.rules.append((re.compile(r'\b' + w + r'\b'), fn))

        self.rules.append((re.compile(r'"[^"]*"'),   fmt(t["syn_string"])))
        self.rules.append((re.compile(r'//[^\n]*'),   fmt(t["syn_comment"], italic=True)))
        self.rules.append((re.compile(r'\b\d+\b'),    fmt(t["syn_number"])))

    def highlightBlock(self, text):
        for pat, fmt in self.rules:
            for m in pat.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ── Data models ───────────────────────────────────────────────────────────────
def is_hero_speaker(speaker):
    return speaker == "other"


def speaker_display_name(speaker):
    return "Hero" if is_hero_speaker(speaker) else "NPC"


class DialogLine:
    def __init__(self, speaker="self", text=""):
        self.speaker = speaker   # "self" = NPC, "other" = Hero
        self.text = text

class DialogChoice:
    def __init__(self, label="", func_name=""):
        self.label = label
        self.func_name = func_name

class DialogBlock:
    def __init__(self):
        self.name = ""; self.description = ""; self.nr = 1
        self.permanent = 0; self.important = 0; self.condition_expr = ""
        self.lines: list[DialogLine] = []
        self.choices: list[DialogChoice] = []
        self.give_xp = ""; self.give_item = ""; self.give_item_count = 1
        self.take_item = ""; self.take_item_count = 1
        self.log_topic = ""; self.log_entry = ""; self.log_status = "LOG_RUNNING"
        self.stop_after = True; self.is_exit = False; self.is_trade = False


# ── Code generator ────────────────────────────────────────────────────────────
def sanitize(n): return re.sub(r'[^A-Za-z0-9_]', '_', n)

def voice_code(bname, idx, speaker):
    return f"{bname}_{'15' if speaker == 'other' else '10'}_{idx:02d}"

def _log_type(s): return "LOG_MISSION" if ("RUNNING" in s or "SUCCESS" in s) else "LOG_NOTE"

def generate_dia_file(npc_name, npc_id, blocks):
    safe = sanitize(npc_name)
    out = [f"// Dialog file for {npc_name} ({npc_id})",
           "// Generated by Gothic Dialog Generator", ""]
    en = f"DIA_{safe}_EXIT"
    out += ["// " + "="*60, "// \t\t\t\t\tEXIT", "// " + "="*60,
            f"instance {en} (C_INFO)",
            f"\tnpc\t\t\t= {npc_id};", f"\tnr\t\t\t= 999;",
            f"\tcondition\t= {en}_Condition;", f"\tinformation\t= {en}_Info;",
            f"\tpermanent\t= 1;", f"\tdescription = DIALOG_ENDE;", f"}};", "",
            f"FUNC int {en}_Condition()", f"\treturn 1;",
            f"FUNC VOID {en}_Info()", f"\tAI_StopProcessInfos\t(self);", ""]
    for b in blocks:
        if b.is_exit: continue
        bn = sanitize(b.name) if b.name else f"DIA_{safe}_Block"
        if not bn.startswith("DIA_"): bn = f"DIA_{safe}_{bn}"
        out += ["// " + "="*60, f"// \t\t\t{b.description or b.name}", "// " + "="*60,
                f"instance {bn} (C_INFO)",
                f"\tnpc\t\t\t= {npc_id};", f"\tnr\t\t\t= {b.nr};",
                f"\tcondition\t= {bn}_Condition;", f"\tinformation\t= {bn}_Info;",
                f"\tpermanent\t= {b.permanent};"]
        if b.important: out.append(f"\timportant\t= 1;")
        if b.description and not b.important: out.append(f'\tdescription\t= "{b.description}";')
        if b.is_trade: out.append(f"\tTrade\t\t= 1;")
        out += [f"}};", "", f"FUNC int {bn}_Condition()"]
        if b.condition_expr.strip():
            for cl in b.condition_expr.strip().splitlines(): out.append(f"\t{cl}")
        else: out.append("\treturn 1;")
        out += ["", f"FUNC VOID {bn}_Info()"]
        if b.choices: out.append(f"\tInfo_ClearChoices\t({bn});")
        for i, dl in enumerate(b.lines):
            sf = "other" if dl.speaker == "other" else "self"
            st = "self"  if dl.speaker == "other" else "other"
            out.append(f'\tAI_Output ({sf}, {st},"{voice_code(bn, i, dl.speaker)}"); //{dl.text}')
        if b.choices:
            for ch in b.choices:
                cf = sanitize(ch.func_name) if ch.func_name else sanitize(ch.label)
                if not cf.startswith("DIA_"): cf = f"{bn}_{cf}"
                out.append(f'\tInfo_AddChoice\t({bn},"{ch.label}",{cf});')
        if b.give_xp:    out.append(f"\tB_GiveXP({b.give_xp});")
        if b.give_item:  out.append(f"\tB_GiveInvItems(self, other, {b.give_item}, {b.give_item_count});")
        if b.take_item:  out.append(f"\tB_GiveInvItems(other, self, {b.take_item}, {b.take_item_count});")
        if b.log_topic:
            out.append(f"\tLog_CreateTopic\t({b.log_topic}, {_log_type(b.log_status)});")
            out.append(f"\tLog_SetTopicStatus\t({b.log_topic}, {b.log_status});")
        if b.log_entry:
            out.append(f'\tB_LogEntry\t({b.log_topic or "LOG_TOPIC"},"{b.log_entry}");')
        if b.stop_after and not b.choices: out.append("\tAI_StopProcessInfos\t(self);")
        out.append("")
    return "\n".join(out)

def generate_constants_file(npc_name, blocks):
    topics = sorted({b.log_topic for b in blocks if b.log_topic})
    if not topics: return f"// No log constants needed for {npc_name}\n"
    out = [f"// Log constants for {npc_name} dialogs",
           "// Add to Constants.d or a dedicated _CONST.d", "",
           "// ── Log Topic IDs ──────────────────────────────────"]
    for i, t in enumerate(topics, 100): out.append(f"const int {t} = {i};")
    out.append("")
    return "\n".join(out)


# ── Parser (round-trips files produced by this tool) ───────────────────────────
def parse_dia_file(text):
    header_m = re.search(r'//\s*Dialog file for\s+(.*?)\s*\((.*?)\)', text)
    npc_name = header_m.group(1).strip() if header_m else ""
    npc_id   = header_m.group(2).strip() if header_m else ""
    prefix = f"DIA_{sanitize(npc_name)}_"

    blocks = []
    segments = re.split(r'\binstance\s+', text)
    for seg in segments[1:]:
        seg = "instance " + seg
        name_m = re.match(r'instance\s+(\w+)\s*\(C_INFO\)', seg)
        if not name_m:
            continue
        bn = name_m.group(1)
        if bn.endswith("_EXIT"):
            continue  # the EXIT block is regenerated automatically, skip it

        body_m = re.search(r'\{(.*?)\}\s*;', seg, re.S)
        body = body_m.group(1) if body_m else ""

        def field(pat, default=""):
            m = re.search(pat, body)
            return m.group(1).strip() if m else default

        b = DialogBlock()
        b.name = bn[len(prefix):] if bn.startswith(prefix) else bn
        try: b.nr = int(field(r'nr\s*=\s*(\d+)\s*;', "1"))
        except ValueError: b.nr = 1
        perm = field(r'permanent\s*=\s*(\d+)\s*;', "0")
        b.permanent = int(perm) if perm.isdigit() else 0
        b.important = 1 if re.search(r'important\s*=\s*1\s*;', body) else 0
        b.description = field(r'description\s*=\s*"([^"]*)"\s*;', "")
        b.is_trade = bool(re.search(r'Trade\s*=\s*1\s*;', body))

        cond_m = re.search(rf'FUNC int {re.escape(bn)}_Condition\(\)(.*?)FUNC VOID', seg, re.S)
        cond_body = cond_m.group(1).strip() if cond_m else ""
        if cond_body and cond_body != "return 1;":
            b.condition_expr = cond_body

        info_m = re.search(rf'FUNC VOID {re.escape(bn)}_Info\(\)(.*)', seg, re.S)
        info_body = info_m.group(1) if info_m else ""
        cut = re.search(r'\n//\s=+', info_body)
        if cut: info_body = info_body[:cut.start()]

        for m in re.finditer(r'AI_Output\s*\((\w+),\s*(\w+),\s*"[^"]*"\);\s*//(.*)', info_body):
            sf, txt = m.group(1), m.group(3).strip()
            speaker = "other" if sf == "other" else "self"
            b.lines.append(DialogLine(speaker=speaker, text=txt))

        for m in re.finditer(r'Info_AddChoice\s*\(\s*\w+\s*,\s*"([^"]*)"\s*,\s*(\w+)\s*\);', info_body):
            b.choices.append(DialogChoice(label=m.group(1), func_name=m.group(2)))

        xp_m = re.search(r'B_GiveXP\(([^)]*)\);', info_body)
        if xp_m: b.give_xp = xp_m.group(1).strip()

        gi_m = re.search(r'B_GiveInvItems\(self,\s*other,\s*([^,]+),\s*(\d+)\);', info_body)
        if gi_m: b.give_item = gi_m.group(1).strip(); b.give_item_count = int(gi_m.group(2))

        ti_m = re.search(r'B_GiveInvItems\(other,\s*self,\s*([^,]+),\s*(\d+)\);', info_body)
        if ti_m: b.take_item = ti_m.group(1).strip(); b.take_item_count = int(ti_m.group(2))

        status_m = re.search(r'Log_SetTopicStatus\s*\(([^,]+),\s*(\w+)\);', info_body)
        if status_m:
            b.log_topic = status_m.group(1).strip(); b.log_status = status_m.group(2).strip()
        else:
            topic_m = re.search(r'Log_CreateTopic\s*\(([^,]+),', info_body)
            if topic_m: b.log_topic = topic_m.group(1).strip()

        entry_m = re.search(r'B_LogEntry\s*\([^,]+,\s*"([^"]*)"\);', info_body)
        if entry_m: b.log_entry = entry_m.group(1)

        b.stop_after = bool(re.search(r'AI_StopProcessInfos\s*\(self\);', info_body))
        blocks.append(b)

    blocks.sort(key=lambda x: x.nr)
    return npc_name, npc_id, blocks


# ── Chat-based dialog line input ────────────────────────────────────────────────
class ChatInput(QLineEdit):
    """Enter submits the current line. Up/Down always switch speaker; Left/Right
    switch speaker only when the field is empty, so normal text editing still works."""
    def __init__(self, on_submit=None, on_toggle=None, parent=None):
        super().__init__(parent)
        self.on_submit = on_submit
        self.on_toggle = on_toggle

    def keyPressEvent(self, e):
        k = e.key()
        if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            text = self.text().strip()
            if text and self.on_submit:
                self.on_submit(text)
                self.clear()
            e.accept()
            return
        if k in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            if self.on_toggle: self.on_toggle()
            e.accept()
            return
        if k in (Qt.Key.Key_Left, Qt.Key.Key_Right) and not self.text():
            if self.on_toggle: self.on_toggle()
            e.accept()
            return
        super().keyPressEvent(e)


class ChatBubble(QFrame):
    def __init__(self, line: DialogLine, on_remove=None):
        super().__init__()
        self.on_remove = on_remove
        is_hero = is_hero_speaker(line.speaker)
        bg = THEME["bubble_hero_bg"] if is_hero else THEME["bubble_npc_bg"]
        fg = THEME["bubble_hero_text"] if is_hero else THEME["bubble_npc_text"]

        outer = QHBoxLayout(self); outer.setContentsMargins(2, 1, 2, 1); outer.setSpacing(0)
        if is_hero: outer.addStretch(1)

        bubble = QFrame()
        bubble.setStyleSheet(f"QFrame {{ background:{bg}; border-radius:{THEME['radius_lg']}; }}")
        bl = QHBoxLayout(bubble); bl.setContentsMargins(10, 6, 6, 6); bl.setSpacing(4)

        tag = QLabel(speaker_display_name(line.speaker))
        tag.setStyleSheet(
            f"color:{fg}; background:transparent; font-weight:700; "
            f"font-size:{THEME['font_size_tiny']}; letter-spacing:1px;")

        text_lbl = QLabel(line.text)
        text_lbl.setWordWrap(True)
        text_lbl.setStyleSheet(f"color:{fg}; background:transparent; font-family:{THEME['font_ui']};")
        text_lbl.setMaximumWidth(340)

        col = QVBoxLayout(); col.setSpacing(1)
        col.addWidget(tag); col.addWidget(text_lbl)
        bl.addLayout(col, 1)

        rm = QPushButton("✕"); rm.setFixedSize(16, 16); rm.setStyleSheet(SS["rm_btn"])
        rm.clicked.connect(lambda: self.on_remove(self) if self.on_remove else None)
        bl.addWidget(rm, 0, Qt.AlignmentFlag.AlignTop)

        outer.addWidget(bubble)
        if not is_hero: outer.addStretch(1)


class ChatLinesWidget(QWidget):
    def __init__(self, on_change=None):
        super().__init__()
        self.on_change = on_change
        self.lines: list[DialogLine] = []
        self.current_speaker = "self"   # self = NPC, other = Hero
        self._bubble_map = {}
        self._build()

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(0, 0, 0, 0); root.setSpacing(6)

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet(f"background:{THEME['bg_main']};")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(6, 6, 6, 6); self.chat_layout.setSpacing(3)
        self.chat_layout.addStretch()

        self.scroll = QScrollArea(); self.scroll.setWidget(self.chat_container)
        self.scroll.setWidgetResizable(True); self.scroll.setMinimumHeight(150)
        self.scroll.setStyleSheet(
            f"QScrollArea {{ border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; background:{THEME['bg_main']}; }}")
        root.addWidget(self.scroll, 1)

        inrow = QHBoxLayout(); inrow.setSpacing(6)
        self.speaker_btn = QPushButton()
        self.speaker_btn.setFixedWidth(64)
        self.speaker_btn.clicked.connect(self._toggle_speaker)
        self.input = ChatInput(on_submit=self._submit, on_toggle=self._toggle_speaker)
        self.input.setPlaceholderText("Type a line, press Enter  ·  ↑ ↓ switches speaker")
        self.input.setStyleSheet(SS["field"])
        inrow.addWidget(self.speaker_btn); inrow.addWidget(self.input, 1)
        root.addLayout(inrow)

        self._update_speaker_style()

    def _toggle_speaker(self):
        self.current_speaker = "other" if self.current_speaker == "self" else "self"
        self._update_speaker_style()
        self.input.setFocus()

    def _update_speaker_style(self):
        is_hero = is_hero_speaker(self.current_speaker)
        self.speaker_btn.setText(speaker_display_name(self.current_speaker))
        color = THEME["accent_primary"] if is_hero else THEME["accent_secondary"]
        self.speaker_btn.setStyleSheet(
            f"QPushButton {{ background:{color}; color:{THEME['bg_main']}; border:none; "
            f"border-radius:{THEME['radius_md']}; font-weight:700; padding:7px 0; }}"
            f"QPushButton:hover {{ background:{THEME['accent_hover']}; }}")

    def _submit(self, text):
        line = DialogLine(speaker=self.current_speaker, text=text)
        self.lines.append(line)
        self._add_bubble(line)
        if self.on_change: self.on_change()
        QTimer.singleShot(0, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()))

    def _add_bubble(self, line):
        bubble = ChatBubble(line, on_remove=self._remove_bubble)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self._bubble_map[bubble] = line

    def _remove_bubble(self, bubble):
        line = self._bubble_map.pop(bubble, None)
        if line in self.lines: self.lines.remove(line)
        bubble.setParent(None); bubble.deleteLater()
        if self.on_change: self.on_change()

    def load_lines(self, lines):
        for b in list(self._bubble_map.keys()):
            b.setParent(None); b.deleteLater()
        self._bubble_map = {}
        self.lines = []
        for l in lines:
            self.lines.append(l)
            self._add_bubble(l)

    def get_lines(self):
        return list(self.lines)


# ── Widgets ───────────────────────────────────────────────────────────────────
class ChoiceWidget(QFrame):
    def __init__(self, parent=None, on_remove=None):
        super().__init__(parent)
        self.on_remove = on_remove
        self.setStyleSheet(
            f"QFrame {{ background:{THEME['bg_choice']}; "
            f"border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; margin:1px; "
            f"border-left:3px solid {THEME['accent_secondary']}; }}")
        lay = QHBoxLayout(self); lay.setContentsMargins(6, 4, 6, 4); lay.setSpacing(6)
        self.label = QLineEdit(); self.label.setPlaceholderText("Choice shown to player…")
        self.label.setStyleSheet(
            f"QLineEdit {{ background:{THEME['bg_choice_input']}; color:{THEME['accent_hover']}; "
            f"border:none; border-radius:2px; padding:4px 6px; font-weight:500; }}")
        self.func = QLineEdit(); self.func.setPlaceholderText("Handler func (optional)")
        self.func.setFixedWidth(190); self.func.setStyleSheet(SS["field"])
        rm = QPushButton("✕"); rm.setFixedSize(22, 22); rm.setStyleSheet(SS["rm_btn"])
        rm.clicked.connect(lambda: self.on_remove(self) if self.on_remove else None)
        lay.addWidget(self.label, 2); lay.addWidget(self.func, 1); lay.addWidget(rm)

    def get_choice(self): return DialogChoice(self.label.text(), self.func.text())


class BlockEditor(QWidget):
    def __init__(self, parent=None, on_change=None):
        super().__init__(parent)
        self.on_change = on_change
        self.setStyleSheet(f"QWidget {{ background:{THEME['bg_main']}; }}")
        self._build()

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(14, 12, 14, 12); root.setSpacing(8)

        def lbl(text, width=60):
            w = QLabel(text)
            w.setFixedWidth(width)
            w.setStyleSheet(f"color:{THEME['text_secondary']}; font-weight:600; font-size:{THEME['font_size_small']};")
            return w

        # Scene name — always visible, it's how the scene is identified in the list
        name_row = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Scene name  ·  e.g. Hello · WannaJoin · KalomsRecipe")
        self.name_edit.setStyleSheet(SS["field"])
        name_row.addWidget(lbl("Name")); name_row.addWidget(self.name_edit, 1)
        root.addLayout(name_row)

        tabs = QTabWidget()

        # ── Dialog tab: the chat + choices, the primary work surface ──────────
        dialog_tab = QWidget()
        dt = QVBoxLayout(dialog_tab); dt.setContentsMargins(10, 10, 10, 10); dt.setSpacing(8)

        self.chat = ChatLinesWidget(on_change=self._emit)
        dt.addWidget(self.chat, 1)

        choices_hdr = QHBoxLayout()
        choices_hdr.addWidget(lbl("Choices", 60))
        add_choice_btn = QPushButton("＋  Add choice")
        add_choice_btn.setStyleSheet(SS["add_btn"])
        add_choice_btn.clicked.connect(lambda: self._add_choice())
        choices_hdr.addStretch(); choices_hdr.addWidget(add_choice_btn)
        dt.addLayout(choices_hdr)

        self.choices_container = QWidget()
        self.choices_container.setStyleSheet(f"background:{THEME['bg_main']};")
        self.choices_layout = QVBoxLayout(self.choices_container)
        self.choices_layout.setContentsMargins(0, 0, 0, 0); self.choices_layout.setSpacing(3)
        choices_scroll = QScrollArea(); choices_scroll.setWidget(self.choices_container)
        choices_scroll.setWidgetResizable(True); choices_scroll.setMaximumHeight(110)
        choices_scroll.setStyleSheet(f"QScrollArea {{ border:none; background:{THEME['bg_main']}; }}")
        dt.addWidget(choices_scroll)

        tabs.addTab(dialog_tab, "Dialog")

        # ── Advanced tab: everything else, tucked away ─────────────────────────
        adv_tab = QWidget()
        av = QVBoxLayout(adv_tab); av.setContentsMargins(10, 10, 10, 10); av.setSpacing(10)

        r2 = QHBoxLayout()
        self.desc_edit = QLineEdit(); self.desc_edit.setPlaceholderText("Player-visible choice text  (blank for auto/important)")
        self.desc_edit.setStyleSheet(SS["field"])
        r2.addWidget(lbl("Desc")); r2.addWidget(self.desc_edit, 1)
        av.addLayout(r2)

        r3 = QHBoxLayout()
        self.perm_cb  = QCheckBox("Permanent");        self.perm_cb.setStyleSheet(SS["check"])
        self.imp_cb   = QCheckBox("Important (auto)"); self.imp_cb.setStyleSheet(SS["check"])
        self.trade_cb = QCheckBox("Trade");             self.trade_cb.setStyleSheet(SS["check"])
        r3.addWidget(self.perm_cb); r3.addWidget(self.imp_cb); r3.addWidget(self.trade_cb); r3.addStretch()
        av.addLayout(r3)

        r4 = QHBoxLayout()
        self.cond_edit = QLineEdit(); self.cond_edit.setPlaceholderText("e.g.  if (Kapitel < 3) { return 1; }")
        self.cond_edit.setStyleSheet(SS["field"])
        r4.addWidget(lbl("Cond")); r4.addWidget(self.cond_edit, 1)
        av.addLayout(r4)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"color:{THEME['bg_border']};")
        av.addWidget(div)

        def row(label_text, *widgets):
            rw = QHBoxLayout(); rw.setSpacing(6)
            rw.addWidget(lbl(label_text, 74))
            for w in widgets: rw.addWidget(w)
            return rw

        self.xp_edit = QLineEdit(); self.xp_edit.setPlaceholderText("XP constant  e.g. XP_KilledBandit")
        self.xp_edit.setStyleSheet(SS["field"])
        av.addLayout(row("Give XP", self.xp_edit))

        self.give_item_edit = QLineEdit(); self.give_item_edit.setPlaceholderText("Item  e.g. ItAm_Prot_Fire_01")
        self.give_item_edit.setStyleSheet(SS["field"])
        self.give_count = QSpinBox(); self.give_count.setRange(1, 999); self.give_count.setValue(1)
        self.give_count.setFixedWidth(54); self.give_count.setStyleSheet(SS["spin"])
        av.addLayout(row("Give Item", self.give_item_edit, self.give_count))

        self.take_item_edit = QLineEdit(); self.take_item_edit.setPlaceholderText("Item  e.g. ItWr_SomeScroll")
        self.take_item_edit.setStyleSheet(SS["field"])
        self.take_count = QSpinBox(); self.take_count.setRange(1, 999); self.take_count.setValue(1)
        self.take_count.setFixedWidth(54); self.take_count.setStyleSheet(SS["spin"])
        av.addLayout(row("Take Item", self.take_item_edit, self.take_count))

        self.log_topic_edit = QLineEdit(); self.log_topic_edit.setPlaceholderText("Log topic  e.g. CH1_JoinPsi")
        self.log_topic_edit.setStyleSheet(SS["field"])
        self.log_status_cmb = QComboBox()
        self.log_status_cmb.addItems(["LOG_RUNNING", "LOG_SUCCESS", "LOG_FAILED", "LOG_NOTE"])
        self.log_status_cmb.setFixedWidth(130); self.log_status_cmb.setStyleSheet(SS["combo"])
        av.addLayout(row("Log Topic", self.log_topic_edit, self.log_status_cmb))

        self.log_entry_edit = QLineEdit(); self.log_entry_edit.setPlaceholderText("Log entry text — shown in quest log…")
        self.log_entry_edit.setStyleSheet(SS["field"])
        av.addLayout(row("Log Entry", self.log_entry_edit))

        self.stop_cb = QCheckBox("AI_StopProcessInfos at end")
        self.stop_cb.setChecked(True); self.stop_cb.setStyleSheet(SS["check"])
        sr = QHBoxLayout(); sr.addWidget(self.stop_cb); sr.addStretch()
        av.addLayout(sr)
        av.addStretch()

        tabs.addTab(adv_tab, "Advanced")
        root.addWidget(tabs, 1)

        for w in [self.name_edit, self.desc_edit, self.cond_edit, self.xp_edit,
                  self.give_item_edit, self.take_item_edit, self.log_topic_edit, self.log_entry_edit]:
            w.textChanged.connect(self._emit)
        for w in [self.perm_cb, self.imp_cb, self.trade_cb, self.stop_cb]:
            w.stateChanged.connect(self._emit)
        self.log_status_cmb.currentTextChanged.connect(self._emit)

    def _emit(self, *_):
        if self.on_change: self.on_change()

    def _add_choice(self, choice=None):
        cw = ChoiceWidget(on_remove=self._rm_choice)
        if choice:
            cw.label.setText(choice.label); cw.func.setText(choice.func_name)
        cw.label.textChanged.connect(self._emit); cw.func.textChanged.connect(self._emit)
        self.choices_layout.addWidget(cw)
        self._emit()

    def _rm_choice(self, w): w.setParent(None); w.deleteLater(); self._emit()

    def _clear_choices(self):
        while self.choices_layout.count():
            item = self.choices_layout.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()

    def get_block(self):
        b = DialogBlock()
        b.name = self.name_edit.text().strip()
        b.description = self.desc_edit.text().strip()
        b.permanent = 1 if self.perm_cb.isChecked() else 0
        b.important = 1 if self.imp_cb.isChecked() else 0
        b.is_trade = self.trade_cb.isChecked()
        b.condition_expr = self.cond_edit.text().strip()
        b.stop_after = self.stop_cb.isChecked()
        b.give_xp = self.xp_edit.text().strip()
        b.give_item = self.give_item_edit.text().strip(); b.give_item_count = self.give_count.value()
        b.take_item = self.take_item_edit.text().strip(); b.take_item_count = self.take_count.value()
        b.log_topic = self.log_topic_edit.text().strip(); b.log_entry = self.log_entry_edit.text().strip()
        b.log_status = self.log_status_cmb.currentText()
        b.lines = self.chat.get_lines()
        for i in range(self.choices_layout.count()):
            w = self.choices_layout.itemAt(i).widget()
            if isinstance(w, ChoiceWidget): b.choices.append(w.get_choice())
        return b

    def load_block(self, b: DialogBlock):
        self.name_edit.setText(b.name)
        self.desc_edit.setText(b.description)
        self.perm_cb.setChecked(bool(b.permanent))
        self.imp_cb.setChecked(bool(b.important))
        self.trade_cb.setChecked(bool(b.is_trade))
        self.cond_edit.setText(b.condition_expr)
        self.stop_cb.setChecked(bool(b.stop_after))
        self.xp_edit.setText(b.give_xp)
        self.give_item_edit.setText(b.give_item); self.give_count.setValue(b.give_item_count or 1)
        self.take_item_edit.setText(b.take_item); self.take_count.setValue(b.take_item_count or 1)
        self.log_topic_edit.setText(b.log_topic); self.log_entry_edit.setText(b.log_entry)
        idx = self.log_status_cmb.findText(b.log_status)
        if idx >= 0: self.log_status_cmb.setCurrentIndex(idx)
        self.chat.load_lines(b.lines)
        self._clear_choices()
        for ch in b.choices:
            self._add_choice(ch)


class BlockListItem(QFrame):
    def __init__(self, idx, name, parent=None, on_select=None, on_remove=None):
        super().__init__(parent)
        self.idx = idx; self.on_select = on_select; self.on_remove = on_remove; self._active = False
        self.setFixedHeight(34); self.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QHBoxLayout(self); lay.setContentsMargins(10, 4, 6, 4)
        self.lbl = QLabel(name or f"Scene {idx+1}")
        rm = QPushButton("✕"); rm.setFixedSize(18, 18); rm.setStyleSheet(SS["rm_btn"])
        rm.clicked.connect(lambda: on_remove(self.idx) if on_remove else None)
        lay.addWidget(self.lbl, 1); lay.addWidget(rm)
        self._update_style()

    def _update_style(self):
        if self._active:
            self.setStyleSheet(
                f"QFrame {{ background:{THEME['bg_bar']}; border-left:3px solid {THEME['accent_primary']}; "
                f"border-radius:{THEME['radius_sm']}; margin:1px; }}")
            self.lbl.setStyleSheet(
                f"color:{THEME['accent_hover']}; font-weight:700; font-size:{THEME['font_size_ui']};")
        else:
            self.setStyleSheet(
                f"QFrame {{ background:{THEME['bg_panel']}; border-left:3px solid transparent; "
                f"border-radius:{THEME['radius_sm']}; margin:1px; }}")
            self.lbl.setStyleSheet(
                f"color:{THEME['text_secondary']}; font-size:{THEME['font_size_ui']};")

    def set_active(self, v): self._active = v; self._update_style()
    def update_name(self, n): self.lbl.setText(n or f"Scene {self.idx+1}")
    def mousePressEvent(self, e):
        if self.on_select: self.on_select(self.idx)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.blocks = []; self.block_editors = []; self.block_items = []; self.current_block_idx = -1
        self.current_file_path = None
        self.setWindowTitle("Gothic Dialog Generator")
        w, h = THEME["window_size"]
        self.resize(w, h)
        self.setStyleSheet(SS["global"])
        self._build_ui()

    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central); root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)

        # Top bar
        topbar = QFrame(); topbar.setFixedHeight(THEME["topbar_height"])
        topbar.setStyleSheet(
            f"QFrame {{ background:{THEME['bg_bar']}; "
            f"border-bottom:{THEME['border_width']} solid {THEME['bg_border']}; }}")
        tb = QHBoxLayout(topbar); tb.setContentsMargins(18, 8, 18, 8); tb.setSpacing(10)

        title = QLabel("Gothic Dialog Generator")
        title.setStyleSheet(
            f"color:{THEME['text_primary']}; font-size:{THEME['font_size_title']}; font-weight:700; "
            f"font-family:{THEME['font_ui']}; letter-spacing:0.5px;")

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"color:{THEME['bg_border']}; margin:4px 6px;")

        def hdr_lbl(text):
            w = QLabel(text)
            w.setStyleSheet(f"color:{THEME['text_secondary']}; font-size:{THEME['font_size_small']}; font-weight:600;")
            return w

        self.npc_name_edit = QLineEdit(); self.npc_name_edit.setPlaceholderText("Gomez")
        self.npc_name_edit.setFixedWidth(130); self.npc_name_edit.setStyleSheet(SS["field"])

        self.npc_id_edit = QLineEdit(); self.npc_id_edit.setPlaceholderText("Ebr_100_Gomez")
        self.npc_id_edit.setFixedWidth(160); self.npc_id_edit.setStyleSheet(SS["field"])

        open_btn = QPushButton("Open")
        open_btn.setStyleSheet(
            f"QPushButton {{ background:{THEME['bg_panel']}; color:{THEME['text_secondary']}; "
            f"border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; padding:6px 14px; font-weight:600; }}"
            f"QPushButton:hover {{ background:{THEME['bg_input_border']}; color:{THEME['text_primary']}; }}")
        open_btn.clicked.connect(self._open)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(
            f"QPushButton {{ background:{THEME['accent_primary']}; color:{THEME['bg_main']}; "
            f"border:{THEME['border_width']} solid {THEME['accent_hover']}; "
            f"border-radius:{THEME['radius_md']}; padding:6px 16px; "
            f"font-weight:700; font-family:{THEME['font_ui']}; }}"
            f"QPushButton:hover {{ background:{THEME['accent_hover']}; }}")
        save_btn.clicked.connect(self._save)

        tb.addWidget(title); tb.addWidget(sep); tb.addStretch()
        tb.addWidget(hdr_lbl("NPC Name")); tb.addWidget(self.npc_name_edit)
        tb.addWidget(hdr_lbl("NPC ID"));   tb.addWidget(self.npc_id_edit)
        tb.addWidget(open_btn); tb.addWidget(save_btn)
        root.addWidget(topbar)

        splitter = QSplitter(Qt.Orientation.Horizontal); splitter.setHandleWidth(2)

        # Sidebar
        left = QWidget(); left.setFixedWidth(THEME["sidebar_width"])
        left.setStyleSheet(f"QWidget {{ background:{THEME['bg_panel']}; }}")
        lv = QVBoxLayout(left); lv.setContentsMargins(6, 10, 6, 8); lv.setSpacing(4)

        sc_title = QLabel("SCENES")
        sc_title.setStyleSheet(
            f"color:{THEME['text_muted']}; font-size:{THEME['font_size_tiny']}; "
            f"font-weight:700; letter-spacing:3px; padding:2px 4px;")
        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"color:{THEME['bg_border']}; margin-bottom:4px;")
        lv.addWidget(sc_title); lv.addWidget(div)

        self.block_list_widget = QWidget()
        self.block_list_widget.setStyleSheet(f"background:{THEME['bg_panel']};")
        self.block_list_layout = QVBoxLayout(self.block_list_widget)
        self.block_list_layout.setContentsMargins(0, 0, 0, 0)
        self.block_list_layout.setSpacing(2); self.block_list_layout.addStretch()

        bl_scroll = QScrollArea(); bl_scroll.setWidget(self.block_list_widget); bl_scroll.setWidgetResizable(True)
        bl_scroll.setStyleSheet(f"QScrollArea {{ border:none; background:{THEME['bg_panel']}; }}")
        lv.addWidget(bl_scroll, 1)

        add_block_btn = QPushButton("＋  New Scene")
        add_block_btn.setStyleSheet(
            f"QPushButton {{ background:{THEME['bg_bar']}; color:{THEME['accent_hover']}; "
            f"border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; padding:7px; "
            f"font-weight:700; font-family:{THEME['font_ui']}; }}"
            f"QPushButton:hover {{ background:{THEME['bg_input_border']}; }}")
        add_block_btn.clicked.connect(lambda: self._add_block())
        lv.addWidget(add_block_btn)
        splitter.addWidget(left)

        # Editor
        self.editor_stack = QStackedWidget()
        self.editor_stack.setStyleSheet(f"QWidget {{ background:{THEME['bg_main']}; }}")

        self.placeholder = QLabel("Select or create a dialog scene  →")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet(
            f"color:{THEME['bg_border']}; font-size:{THEME['font_size_placeholder']}; "
            f"font-family:{THEME['font_ui']}; font-style:italic;")
        self.editor_stack.addWidget(self.placeholder)
        self.editor_stack.setCurrentWidget(self.placeholder)
        splitter.addWidget(self.editor_stack)

        # Preview — single DIA_.d preview, kept quiet
        preview_panel = QWidget()
        preview_panel.setStyleSheet(f"background:{THEME['bg_main']};")
        pv = QVBoxLayout(preview_panel); pv.setContentsMargins(0, 0, 0, 0); pv.setSpacing(0)

        pv_hdr = QLabel("  DIA_.d preview")
        pv_hdr.setFixedHeight(28)
        pv_hdr.setStyleSheet(
            f"color:{THEME['text_muted']}; font-size:{THEME['font_size_tiny']}; "
            f"font-weight:700; letter-spacing:2px; background:{THEME['bg_bar']}; "
            f"border-bottom:{THEME['border_width']} solid {THEME['bg_border']};")
        pv.addWidget(pv_hdr)

        mono = QFont(THEME["font_code"].split(",")[0].strip(), THEME["font_size_code"])
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self.dia_preview = QTextEdit(); self.dia_preview.setReadOnly(True); self.dia_preview.setFont(mono)
        self.dia_preview.setStyleSheet(
            f"QTextEdit {{ background:{THEME['bg_code']}; color:{THEME['text_primary']}; "
            f"border:none; padding:10px; }}")
        DaedalusHighlighter(self.dia_preview.document())
        pv.addWidget(self.dia_preview)

        splitter.addWidget(preview_panel)
        splitter.setSizes(THEME["splitter_sizes"])
        root.addWidget(splitter, 1)

        self.npc_name_edit.textChanged.connect(self._refresh_preview)
        self.npc_id_edit.textChanged.connect(self._refresh_preview)

    def _add_block(self, block=None):
        idx = len(self.blocks)
        b = block if block is not None else DialogBlock()
        self.blocks.append(b)
        ed = BlockEditor(on_change=self._refresh_preview)
        if block is not None:
            ed.load_block(b)
        self.block_editors.append(ed)
        self.editor_stack.addWidget(ed)
        item = BlockListItem(idx, b.name, on_select=self._select_block, on_remove=self._remove_block)
        self.block_items.append(item)
        self.block_list_layout.insertWidget(self.block_list_layout.count() - 1, item)
        self._select_block(idx)

    def _select_block(self, idx):
        if idx < 0 or idx >= len(self.blocks): return
        if 0 <= self.current_block_idx < len(self.block_items):
            self.block_items[self.current_block_idx].set_active(False)
        self.current_block_idx = idx
        self.block_items[idx].set_active(True)
        self.editor_stack.setCurrentWidget(self.block_editors[idx])
        self._refresh_preview()

    def _remove_block(self, idx):
        if idx < 0 or idx >= len(self.blocks): return
        self.blocks.pop(idx); self.block_editors.pop(idx).deleteLater()
        item = self.block_items.pop(idx); item.setParent(None); item.deleteLater()
        for i, it in enumerate(self.block_items): it.idx = i
        self.current_block_idx = min(self.current_block_idx, len(self.blocks) - 1)
        if self.current_block_idx >= 0: self._select_block(self.current_block_idx)
        else: self.editor_stack.setCurrentWidget(self.placeholder)
        self._refresh_preview()

    def _collect_blocks(self):
        blocks = []
        for i, ed in enumerate(self.block_editors):
            b = ed.get_block()
            if not b.name: b.name = f"Scene{i+1}"
            b.nr = i + 1  # nr is assigned automatically from scene order
            blocks.append(b)
            if i < len(self.block_items): self.block_items[i].update_name(b.name)
        return blocks

    def _refresh_preview(self, *_):
        nn = self.npc_name_edit.text().strip() or "NPC"
        ni = self.npc_id_edit.text().strip()   or "NPC_ID"
        bl = self._collect_blocks()
        self.dia_preview.setPlainText(generate_dia_file(nn, ni, bl))

    def _save(self):
        nn = self.npc_name_edit.text().strip()
        ni = self.npc_id_edit.text().strip()
        if not nn or not ni:
            QMessageBox.warning(self, "Missing Info", "Please enter both NPC Name and NPC ID.")
            return
        bl = self._collect_blocks()
        default = self.current_file_path or f"DIA_{sanitize(nn)}.d"
        path, _ = QFileDialog.getSaveFileName(self, "Save Dialog File", default, "Daedalus Dialog Files (*.d)")
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write(generate_dia_file(nn, ni, bl))
        self.current_file_path = path
        self.setWindowTitle(f"Gothic Dialog Generator — {os.path.basename(path)}")
        QMessageBox.information(self, "Saved", f"Dialog file saved:\n  {path}")

    def _open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Dialog File", "", "Daedalus Dialog Files (*.d)")
        if not path: return
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            npc_name, npc_id, blocks = parse_dia_file(text)
        except Exception as e:
            QMessageBox.critical(self, "Could Not Open File", f"This file could not be read:\n{e}")
            return
        self._load_project(npc_name, npc_id, blocks)
        self.current_file_path = path
        self.setWindowTitle(f"Gothic Dialog Generator — {os.path.basename(path)}")

    def _load_project(self, npc_name, npc_id, blocks):
        for ed in self.block_editors:
            self.editor_stack.removeWidget(ed); ed.deleteLater()
        for item in self.block_items:
            item.setParent(None); item.deleteLater()
        self.blocks = []; self.block_editors = []; self.block_items = []; self.current_block_idx = -1

        self.npc_name_edit.setText(npc_name)
        self.npc_id_edit.setText(npc_id)

        if not blocks:
            self.editor_stack.setCurrentWidget(self.placeholder)
        for b in blocks:
            self._add_block(b)
        if blocks:
            self._select_block(0)
        self._refresh_preview()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,          QColor(THEME["bg_main"]))
    pal.setColor(QPalette.ColorRole.WindowText,      QColor(THEME["text_primary"]))
    pal.setColor(QPalette.ColorRole.Base,            QColor(THEME["bg_input"]))
    pal.setColor(QPalette.ColorRole.AlternateBase,   QColor(THEME["bg_panel"]))
    pal.setColor(QPalette.ColorRole.Text,            QColor(THEME["text_primary"]))
    pal.setColor(QPalette.ColorRole.Button,          QColor(THEME["bg_bar"]))
    pal.setColor(QPalette.ColorRole.ButtonText,      QColor(THEME["text_secondary"]))
    pal.setColor(QPalette.ColorRole.Highlight,       QColor(THEME["accent_primary"]))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor(THEME["bg_main"]))
    app.setPalette(pal)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()