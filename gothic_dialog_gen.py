#!/usr/bin/env python3
"""
Gothic Dialog Generator — Parchment Edition
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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat, QPalette


# ══════════════════════════════════════════════════════════════════════════════
#  THEME  —  change everything visual here, nowhere else
# ══════════════════════════════════════════════════════════════════════════════

THEME = {
    # ── Colors ────────────────────────────────────────────────────────────────
    # Backgrounds (light → dark)
    "bg_main":          "#f5edd6",   # window / editor background
    "bg_panel":         "#ede0c0",   # sidebar, group boxes
    "bg_bar":           "#e0ceaa",   # top bar, item hover
    "bg_border":        "#c9b68a",   # borders, separators, scrollbar handle
    "bg_input":         "#d8ccb8",   # text field / spinbox background
    "bg_input_border":  "#c8bca0",   # text field border
    "bg_code":          "#faf4e4",   # code preview background
    "bg_choice":        "#eee8d0",   # choice row background
    "bg_choice_input":  "#f0ead8",   # choice label input

    # Text
    "text_primary":     "#2e1f0e",   # main body text
    "text_secondary":   "#5a3e28",   # labels, secondary
    "text_muted":       "#9a7d5a",   # placeholders, inactive

    # Accents
    "accent_primary":   "#8b3a1a",   # rust red  — active, selected, export btn
    "accent_hover":     "#c05a30",   # lighter rust for hover
    "accent_secondary": "#4a5e35",   # moss green — choices, log
    "accent_gold":      "#a07820",   # gold       — group box titles

    # Syntax highlighting (code preview only)
    "syn_keyword":      "#7a2010",   # instance / func / void …
    "syn_type":         "#5a3e80",   # C_INFO / TRUE / LOG_* …
    "syn_function":     "#1a5a30",   # AI_Output / B_GiveXP …
    "syn_string":       "#7a5010",   # "quoted strings"
    "syn_comment":      "#9a8060",   # // comments
    "syn_number":       "#1a407a",   # numeric literals

    # ── Typography ────────────────────────────────────────────────────────────
    "font_ui":          "Georgia, serif",          # all UI chrome
    "font_code":        "Cascadia Code, Consolas, monospace",  # code preview
    "font_size_ui":     "12px",
    "font_size_small":  "11px",
    "font_size_tiny":   "9px",
    "font_size_title":  "16px",
    "font_size_placeholder": "17px",
    "font_size_code":   10,          # pt, used for QFont object

    # ── Geometry ──────────────────────────────────────────────────────────────
    "radius_sm":        "3px",
    "radius_md":        "4px",
    "radius_lg":        "6px",
    "border_width":     "1px",
    "topbar_height":    56,
    "sidebar_width":    204,
    "splitter_sizes":   [204, 530, 480],
    "window_size":      (1280, 840),

    # ── Spacing ───────────────────────────────────────────────────────────────
    "label_col_width":  "44px",      # left-column label width in editor rows
}

# ── Derived stylesheet fragments (built once from THEME, used everywhere) ─────
# These are the only place that translates THEME values into Qt stylesheet text.

def _ss_field():
    t = THEME
    return (
        f"QLineEdit {{ background:{t['bg_input']}; color:{t['text_primary']}; "
        f"  border:{t['border_width']} solid {t['bg_input_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:4px 8px; "
        f"  selection-background-color:{t['accent_hover']}; "
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
        f"  border-radius:{t['radius_sm']}; padding:2px 6px; }}"
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
        f"  border-radius:2px; background:{t['bg_input']}; }}"
        f"QCheckBox::indicator:checked {{ background:{t['accent_primary']}; "
        f"  border-color:{t['accent_primary']}; }}"
    )

def _ss_group(title_color=None):
    t = THEME
    c = title_color or t["accent_gold"]
    return (
        f"QGroupBox {{ color:{c}; font-weight:700; font-size:{t['font_size_small']}; "
        f"  letter-spacing:0.5px; border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:{t['radius_lg']}; margin-top:10px; padding-top:6px; "
        f"  background:{t['bg_panel']}; font-family:{t['font_ui']}; }}"
        f"QGroupBox::title {{ subcontrol-origin:margin; left:10px; "
        f"  background:{t['bg_panel']}; padding:0 4px; }}"
    )

def _ss_add_btn(color=None):
    t = THEME
    c = color or t["accent_primary"]
    return (
        f"QPushButton {{ background:{t['bg_bar']}; color:{c}; "
        f"  border:{t['border_width']} solid {t['bg_border']}; "
        f"  border-radius:{t['radius_sm']}; padding:4px 12px; "
        f"  font-size:{t['font_size_small']}; font-weight:600; }}"
        f"QPushButton:hover {{ background:{t['bg_input_border']}; color:{t['text_primary']}; }}"
    )

def _ss_rm_btn():
    t = THEME
    return (
        f"QPushButton {{ background:transparent; color:{t['text_muted']}; border:none; }}"
        f"QPushButton:hover {{ color:{t['accent_primary']}; }}"
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
        }}
        QTabBar::tab {{
            background: {t['bg_bar']};
            color: {t['text_secondary']};
            padding: 6px 16px;
            border-top-left-radius: {t['radius_md']};
            border-top-right-radius: {t['radius_md']};
            border: {t['border_width']} solid {t['bg_border']};
            margin-right: 2px;
            font-family: {t['font_ui']};
        }}
        QTabBar::tab:selected {{
            background: {t['bg_main']};
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
    "group_rust": _ss_group(THEME["accent_primary"]),
    "group_moss": _ss_group(THEME["accent_secondary"]),
    "group_mid":  _ss_group(THEME["text_secondary"]),
    "add_btn":    _ss_add_btn(),
    "add_btn_rust": _ss_add_btn(THEME["accent_primary"]),
    "add_btn_moss": _ss_add_btn(THEME["accent_secondary"]),
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
class DialogLine:
    def __init__(self, speaker="other", text=""):
        self.speaker = speaker
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


# ── Widgets ───────────────────────────────────────────────────────────────────
class LineWidget(QFrame):
    def __init__(self, parent=None, on_remove=None):
        super().__init__(parent)
        self.on_remove = on_remove
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(
            f"QFrame {{ background:{THEME['bg_input']}; "
            f"border:{THEME['border_width']} solid {THEME['bg_input_border']}; "
            f"border-radius:{THEME['radius_md']}; margin:1px; }}")
        lay = QHBoxLayout(self); lay.setContentsMargins(6, 4, 6, 4); lay.setSpacing(6)
        self.speaker = QComboBox(); self.speaker.addItems(["Hero", "NPC"])
        self.speaker.setFixedWidth(68); self.speaker.setStyleSheet(SS["combo"])
        self.text = QLineEdit(); self.text.setPlaceholderText("Dialog line…")
        self.text.setStyleSheet(SS["field"])
        rm = QPushButton("✕"); rm.setFixedSize(22, 22); rm.setStyleSheet(SS["rm_btn"])
        rm.clicked.connect(lambda: self.on_remove(self) if self.on_remove else None)
        lay.addWidget(self.speaker); lay.addWidget(self.text, 1); lay.addWidget(rm)

    def get_line(self):
        return DialogLine(
            speaker="other" if self.speaker.currentIndex() == 0 else "self",
            text=self.text.text())


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
            f"QLineEdit {{ background:{THEME['bg_choice_input']}; color:{THEME['accent_secondary']}; "
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
        root = QVBoxLayout(self); root.setContentsMargins(12, 12, 12, 12); root.setSpacing(10)

        def lbl(text):
            w = QLabel(text)
            w.setFixedWidth(44)
            w.setStyleSheet(f"color:{THEME['text_secondary']}; font-weight:600;")
            return w

        def scrolled(container, min_h):
            sc = QScrollArea(); sc.setWidget(container); sc.setWidgetResizable(True)
            sc.setMinimumHeight(min_h)
            sc.setStyleSheet(f"QScrollArea {{ border:none; background:{THEME['bg_main']}; }}")
            return sc

        # Settings group
        mg = QGroupBox("Block Settings"); mg.setStyleSheet(SS["group"])
        ml = QVBoxLayout(mg); ml.setSpacing(7)

        r1 = QHBoxLayout()
        self.name_edit = QLineEdit(); self.name_edit.setPlaceholderText("e.g. Hello  ·  WannaJoin  ·  KalomsRecipe"); self.name_edit.setStyleSheet(SS["field"])
        self.nr_spin = QSpinBox(); self.nr_spin.setRange(1, 998); self.nr_spin.setValue(1); self.nr_spin.setFixedWidth(62); self.nr_spin.setStyleSheet(SS["spin"])
        nr_lbl = QLabel("  nr"); nr_lbl.setStyleSheet(f"color:{THEME['text_secondary']}; font-weight:600;")
        r1.addWidget(lbl("Name")); r1.addWidget(self.name_edit, 1); r1.addWidget(nr_lbl); r1.addWidget(self.nr_spin)
        ml.addLayout(r1)

        r2 = QHBoxLayout()
        self.desc_edit = QLineEdit(); self.desc_edit.setPlaceholderText("Player-visible choice text  (blank for auto/important dialogs)"); self.desc_edit.setStyleSheet(SS["field"])
        r2.addWidget(lbl("Desc")); r2.addWidget(self.desc_edit, 1)
        ml.addLayout(r2)

        r3 = QHBoxLayout()
        self.perm_cb  = QCheckBox("Permanent");            self.perm_cb.setStyleSheet(SS["check"])
        self.imp_cb   = QCheckBox("Important (auto)");     self.imp_cb.setStyleSheet(SS["check"])
        self.trade_cb = QCheckBox("Trade");                self.trade_cb.setStyleSheet(SS["check"])
        r3.addWidget(self.perm_cb); r3.addWidget(self.imp_cb); r3.addWidget(self.trade_cb); r3.addStretch()
        ml.addLayout(r3)

        r4 = QHBoxLayout()
        self.cond_edit = QLineEdit(); self.cond_edit.setPlaceholderText("e.g.  if (Kapitel < 3) { return 1; }"); self.cond_edit.setStyleSheet(SS["field"])
        r4.addWidget(lbl("Cond")); r4.addWidget(self.cond_edit, 1)
        ml.addLayout(r4)
        root.addWidget(mg)

        # Lines group
        lg = QGroupBox("Dialog Lines"); lg.setStyleSheet(SS["group_rust"])
        lv = QVBoxLayout(lg); lv.setSpacing(4)
        self.lines_container = QWidget(); self.lines_container.setStyleSheet(f"background:{THEME['bg_main']};")
        self.lines_layout = QVBoxLayout(self.lines_container); self.lines_layout.setContentsMargins(0,0,0,0); self.lines_layout.setSpacing(3)
        lv.addWidget(scrolled(self.lines_container, 200))
        ab = QPushButton("＋  Add Line"); ab.setStyleSheet(SS["add_btn_rust"]); ab.clicked.connect(self._add_line)
        lv.addWidget(ab)
        root.addWidget(lg)

        # Choices group
        cg = QGroupBox("Dialog Choices  —  optional branching"); cg.setStyleSheet(SS["group_moss"])
        cv = QVBoxLayout(cg); cv.setSpacing(4)
        self.choices_container = QWidget(); self.choices_container.setStyleSheet(f"background:{THEME['bg_main']};")
        self.choices_layout = QVBoxLayout(self.choices_container); self.choices_layout.setContentsMargins(0,0,0,0); self.choices_layout.setSpacing(3)
        cv.addWidget(scrolled(self.choices_container, 80))
        cb = QPushButton("＋  Add Choice"); cb.setStyleSheet(SS["add_btn_moss"]); cb.clicked.connect(self._add_choice)
        cv.addWidget(cb)
        root.addWidget(cg)

        # Effects group
        fg = QGroupBox("Effects  —  optional"); fg.setStyleSheet(SS["group_mid"])
        fv = QVBoxLayout(fg); fv.setSpacing(7)

        def row(label_text, *widgets):
            rw = QHBoxLayout(); rw.setSpacing(6)
            lb = QLabel(label_text); lb.setFixedWidth(70)
            lb.setStyleSheet(f"color:{THEME['text_secondary']}; font-weight:600; font-size:{THEME['font_size_small']};")
            rw.addWidget(lb)
            for w in widgets: rw.addWidget(w)
            return rw

        self.xp_edit = QLineEdit(); self.xp_edit.setPlaceholderText("XP constant  e.g. XP_KilledBandit"); self.xp_edit.setStyleSheet(SS["field"])
        fv.addLayout(row("Give XP:", self.xp_edit))

        self.give_item_edit = QLineEdit(); self.give_item_edit.setPlaceholderText("Item  e.g. ItAm_Prot_Fire_01"); self.give_item_edit.setStyleSheet(SS["field"])
        self.give_count = QSpinBox(); self.give_count.setRange(1,999); self.give_count.setValue(1); self.give_count.setFixedWidth(54); self.give_count.setStyleSheet(SS["spin"])
        x1 = QLabel("×"); x1.setStyleSheet(f"color:{THEME['text_muted']};")
        fv.addLayout(row("Give Item:", self.give_item_edit, x1, self.give_count))

        self.take_item_edit = QLineEdit(); self.take_item_edit.setPlaceholderText("Item  e.g. ItWr_SomeScroll"); self.take_item_edit.setStyleSheet(SS["field"])
        self.take_count = QSpinBox(); self.take_count.setRange(1,999); self.take_count.setValue(1); self.take_count.setFixedWidth(54); self.take_count.setStyleSheet(SS["spin"])
        x2 = QLabel("×"); x2.setStyleSheet(f"color:{THEME['text_muted']};")
        fv.addLayout(row("Take Item:", self.take_item_edit, x2, self.take_count))

        self.log_topic_edit = QLineEdit(); self.log_topic_edit.setPlaceholderText("Log topic  e.g. CH1_JoinPsi"); self.log_topic_edit.setStyleSheet(SS["field"])
        self.log_status_cmb = QComboBox(); self.log_status_cmb.addItems(["LOG_RUNNING","LOG_SUCCESS","LOG_FAILED","LOG_NOTE"]); self.log_status_cmb.setFixedWidth(130); self.log_status_cmb.setStyleSheet(SS["combo"])
        fv.addLayout(row("Log Topic:", self.log_topic_edit, self.log_status_cmb))

        self.log_entry_edit = QLineEdit(); self.log_entry_edit.setPlaceholderText("Log entry text — shown in quest log…"); self.log_entry_edit.setStyleSheet(SS["field"])
        fv.addLayout(row("Log Entry:", self.log_entry_edit))

        self.stop_cb = QCheckBox("AI_StopProcessInfos at end"); self.stop_cb.setChecked(True); self.stop_cb.setStyleSheet(SS["check"])
        sr = QHBoxLayout(); sr.addWidget(self.stop_cb); sr.addStretch()
        fv.addLayout(sr)
        root.addWidget(fg)
        root.addStretch()

        for w in [self.name_edit, self.desc_edit, self.cond_edit, self.xp_edit,
                  self.give_item_edit, self.take_item_edit, self.log_topic_edit, self.log_entry_edit]:
            w.textChanged.connect(self._emit)
        for w in [self.perm_cb, self.imp_cb, self.trade_cb, self.stop_cb]:
            w.stateChanged.connect(self._emit)
        self.nr_spin.valueChanged.connect(self._emit)
        self.log_status_cmb.currentTextChanged.connect(self._emit)

    def _emit(self, *_):
        if self.on_change: self.on_change()

    def _add_line(self):
        lw = LineWidget(on_remove=self._rm)
        lw.text.textChanged.connect(self._emit); lw.speaker.currentIndexChanged.connect(self._emit)
        self.lines_layout.addWidget(lw); self._emit()

    def _add_choice(self):
        cw = ChoiceWidget(on_remove=self._rm)
        cw.label.textChanged.connect(self._emit); cw.func.textChanged.connect(self._emit)
        self.choices_layout.addWidget(cw); self._emit()

    def _rm(self, w): w.setParent(None); w.deleteLater(); self._emit()

    def get_block(self):
        b = DialogBlock()
        b.name = self.name_edit.text().strip(); b.nr = self.nr_spin.value()
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
        for i in range(self.lines_layout.count()):
            w = self.lines_layout.itemAt(i).widget()
            if isinstance(w, LineWidget): b.lines.append(w.get_line())
        for i in range(self.choices_layout.count()):
            w = self.choices_layout.itemAt(i).widget()
            if isinstance(w, ChoiceWidget): b.choices.append(w.get_choice())
        return b


class BlockListItem(QFrame):
    def __init__(self, idx, name, parent=None, on_select=None, on_remove=None):
        super().__init__(parent)
        self.idx = idx; self.on_select = on_select; self.on_remove = on_remove; self._active = False
        self.setFixedHeight(36); self.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QHBoxLayout(self); lay.setContentsMargins(10, 4, 6, 4)
        self.lbl = QLabel(name or f"Block {idx+1}")
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
                f"color:{THEME['accent_primary']}; font-weight:700; font-size:{THEME['font_size_ui']};")
        else:
            self.setStyleSheet(
                f"QFrame {{ background:{THEME['bg_panel']}; border-left:3px solid transparent; "
                f"border-radius:{THEME['radius_sm']}; margin:1px; }}")
            self.lbl.setStyleSheet(
                f"color:{THEME['text_secondary']}; font-size:{THEME['font_size_ui']};")

    def set_active(self, v): self._active = v; self._update_style()
    def update_name(self, n): self.lbl.setText(n or f"Block {self.idx+1}")
    def mousePressEvent(self, e):
        if self.on_select: self.on_select(self.idx)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.blocks = []; self.block_editors = []; self.block_items = []; self.current_block_idx = -1
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
            f"border-bottom:2px solid {THEME['bg_border']}; }}")
        tb = QHBoxLayout(topbar); tb.setContentsMargins(18, 10, 18, 10); tb.setSpacing(10)

        crown = QLabel("⚔")
        crown.setStyleSheet(f"color:{THEME['accent_primary']}; font-size:20px;")

        title = QLabel("Gothic  Dialog  Generator")
        title.setStyleSheet(
            f"color:{THEME['text_primary']}; font-size:{THEME['font_size_title']}; font-weight:700; "
            f"font-family:{THEME['font_ui']}; letter-spacing:2px;")

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"color:{THEME['bg_border']}; margin:4px 6px;")

        def hdr_lbl(text):
            w = QLabel(text)
            w.setStyleSheet(f"color:{THEME['text_secondary']}; font-size:{THEME['font_size_small']}; font-weight:600;")
            return w

        self.npc_name_edit = QLineEdit(); self.npc_name_edit.setPlaceholderText("Gomez")
        self.npc_name_edit.setFixedWidth(140); self.npc_name_edit.setStyleSheet(SS["field"])

        self.npc_id_edit = QLineEdit(); self.npc_id_edit.setPlaceholderText("Ebr_100_Gomez")
        self.npc_id_edit.setFixedWidth(180); self.npc_id_edit.setStyleSheet(SS["field"])

        refresh_btn = QPushButton("↺  Refresh")
        refresh_btn.setStyleSheet(
            f"QPushButton {{ background:{THEME['bg_panel']}; color:{THEME['text_secondary']}; "
            f"border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; padding:6px 14px; font-weight:600; }}"
            f"QPushButton:hover {{ background:{THEME['bg_input_border']}; color:{THEME['text_primary']}; }}")
        refresh_btn.clicked.connect(self._refresh_preview)

        export_btn = QPushButton("📜  Export Files")
        export_btn.setStyleSheet(
            f"QPushButton {{ background:{THEME['accent_primary']}; color:{THEME['bg_main']}; "
            f"border:{THEME['border_width']} solid {THEME['accent_hover']}; "
            f"border-radius:{THEME['radius_md']}; padding:6px 16px; "
            f"font-weight:700; font-family:{THEME['font_ui']}; }}"
            f"QPushButton:hover {{ background:{THEME['accent_hover']}; }}")
        export_btn.clicked.connect(self._export)

        tb.addWidget(crown); tb.addWidget(title); tb.addWidget(sep); tb.addStretch()
        tb.addWidget(hdr_lbl("NPC Name")); tb.addWidget(self.npc_name_edit)
        tb.addWidget(hdr_lbl("NPC ID"));   tb.addWidget(self.npc_id_edit)
        tb.addWidget(refresh_btn); tb.addWidget(export_btn)
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
            f"QPushButton {{ background:{THEME['bg_bar']}; color:{THEME['accent_primary']}; "
            f"border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; padding:7px; "
            f"font-weight:700; font-family:{THEME['font_ui']}; }}"
            f"QPushButton:hover {{ background:{THEME['bg_input_border']}; }}")
        add_block_btn.clicked.connect(self._add_block)
        lv.addWidget(add_block_btn)
        splitter.addWidget(left)
        self.placeholder = QLabel("Select or create a dialog scene  →")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet(
            f"color:{THEME['bg_border']}; font-size:{THEME['font_size_placeholder']}; "
            f"font-family:{THEME['font_ui']}; font-style:italic;")
        # Editor
        self.editor_stack = QStackedWidget()
        self.editor_stack.setStyleSheet(f"QWidget {{ background:{THEME['bg_main']}; }}")
        self.editor_stack.addWidget(self.placeholder)

        self.placeholder = QLabel("Select or create a dialog scene  →")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet(
            f"color:{THEME['bg_border']}; font-size:{THEME['font_size_placeholder']}; "
            f"font-family:{THEME['font_ui']}; font-style:italic;")
        self.editor_stack.setCurrentWidget(self.placeholder)
        splitter.addWidget(self.editor_stack)

        # Preview
        preview_panel = QWidget()
        preview_panel.setStyleSheet(f"background:{THEME['bg_main']};")
        pv = QVBoxLayout(preview_panel); pv.setContentsMargins(0, 0, 0, 0)
        tabs = QTabWidget()

        mono = QFont(THEME["font_code"].split(",")[0].strip(), THEME["font_size_code"])
        mono.setStyleHint(QFont.StyleHint.Monospace)

        def make_preview():
            te = QTextEdit(); te.setReadOnly(True); te.setFont(mono)
            te.setStyleSheet(
                f"QTextEdit {{ background:{THEME['bg_code']}; color:{THEME['text_primary']}; "
                f"border:none; padding:10px; }}")
            DaedalusHighlighter(te.document())
            return te

        self.dia_preview   = make_preview()
        self.const_preview = make_preview()
        tabs.addTab(self.dia_preview, "DIA_.d")
        tabs.addTab(self.const_preview, "_CONST.d")
        pv.addWidget(tabs)
        splitter.addWidget(preview_panel)
        splitter.setSizes(THEME["splitter_sizes"])
        root.addWidget(splitter, 1)

        self.npc_name_edit.textChanged.connect(self._refresh_preview)
        self.npc_id_edit.textChanged.connect(self._refresh_preview)

    def _add_block(self):
        idx = len(self.blocks); self.blocks.append(DialogBlock())
        ed = BlockEditor(on_change=self._refresh_preview)
        self.block_editors.append(ed)
        self.editor_stack.addWidget(ed) 
        print("ADDING", ed)
        item = BlockListItem(idx, "", on_select=self._select_block, on_remove=self._remove_block)
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
            print("EDITOR", i, ed)

            try:
                print("NAME WIDGET", ed.name_edit)
                print("TEXT", ed.name_edit.text())
            except Exception as e:
                print("BROKEN EDITOR:", i, e)
            b = ed.get_block()
            if not b.name: b.name = f"Block{i+1}"
            blocks.append(b)
            if i < len(self.block_items): self.block_items[i].update_name(b.name)
        return blocks

    def _refresh_preview(self, *_):
        nn = self.npc_name_edit.text().strip() or "NPC"
        ni = self.npc_id_edit.text().strip()   or "NPC_ID"
        bl = self._collect_blocks()
        self.dia_preview.setPlainText(generate_dia_file(nn, ni, bl))
        self.const_preview.setPlainText(generate_constants_file(nn, bl))

    def _export(self):
        nn = self.npc_name_edit.text().strip()
        ni = self.npc_id_edit.text().strip()
        if not nn or not ni:
            QMessageBox.warning(self, "Missing Info", "Please enter both NPC Name and NPC ID.")
            return
        folder = QFileDialog.getExistingDirectory(self, "Select export folder")
        if not folder: return
        bl = self._collect_blocks(); safe = sanitize(nn)
        dia_path   = os.path.join(folder, f"DIA_{safe}.d")
        const_path = os.path.join(folder, f"DIA_{safe}_CONST.d")
        with open(dia_path,   "w", encoding="utf-8") as f: f.write(generate_dia_file(nn, ni, bl))
        with open(const_path, "w", encoding="utf-8") as f: f.write(generate_constants_file(nn, bl))
        QMessageBox.information(self, "Scrolls Inscribed",
            f"Files saved:\n  {dia_path}\n  {const_path}")


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
