"""
widgets.py — All custom Qt widgets: the chat-style line input, choice rows,
the per-scene editor, and the sidebar list item.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QScrollArea, QSpinBox, QCheckBox, QComboBox, QTabWidget,
)
from PyQt6.QtCore import Qt, QTimer

from theme import THEME, SS
from daedalus_gen import DialogLine, DialogChoice, DialogBlock, is_hero_speaker, speaker_display_name


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
    """Shows one dialog line. Double-click the text to edit it in place."""
    def __init__(self, line: DialogLine, on_remove=None, on_edit=None):
        super().__init__()
        self.line = line
        self.on_remove = on_remove
        self.on_edit = on_edit
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

        self.text_lbl = QLabel(line.text)
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setStyleSheet(f"color:{fg}; background:transparent; font-family:{THEME['font_ui']};")
        self.text_lbl.setMaximumWidth(340)
        self.text_lbl.setCursor(Qt.CursorShape.IBeamCursor)
        self.text_lbl.setToolTip("Double-click to edit")
        self.text_lbl.mouseDoubleClickEvent = lambda e: self._enter_edit()

        self.text_edit = QLineEdit(line.text)
        self.text_edit.setStyleSheet(
            f"QLineEdit {{ background:{THEME['bg_input']}; color:{THEME['text_primary']}; "
            f"border:{THEME['border_width']} solid {THEME['accent_primary']}; "
            f"border-radius:{THEME['radius_sm']}; padding:2px 4px; }}")
        self.text_edit.setMaximumWidth(340)
        self.text_edit.hide()
        self.text_edit.editingFinished.connect(self._commit_edit)

        col = QVBoxLayout(); col.setSpacing(1)
        col.addWidget(tag); col.addWidget(self.text_lbl); col.addWidget(self.text_edit)
        bl.addLayout(col, 1)

        rm = QPushButton("✕"); rm.setFixedSize(16, 16); rm.setStyleSheet(SS["rm_btn"])
        rm.clicked.connect(lambda: self.on_remove(self) if self.on_remove else None)
        bl.addWidget(rm, 0, Qt.AlignmentFlag.AlignTop)

        outer.addWidget(bubble)
        if not is_hero: outer.addStretch(1)

    def _enter_edit(self):
        self.text_edit.setText(self.line.text)
        self.text_lbl.hide(); self.text_edit.show()
        self.text_edit.setFocus(); self.text_edit.selectAll()

    def _commit_edit(self):
        new_text = self.text_edit.text().strip()
        if new_text:
            self.line.text = new_text
            self.text_lbl.setText(new_text)
        self.text_edit.hide(); self.text_lbl.show()
        if self.on_edit: self.on_edit()


class ChatLinesWidget(QWidget):
    def __init__(self, on_change=None):
        super().__init__()
        self.on_change = on_change
        self.lines: list[DialogLine] = []
        self.current_speaker = "self"   # NPC speaks first, as is typical
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
        self.scroll.setWidgetResizable(True); self.scroll.setMinimumHeight(230)
        self.scroll.setStyleSheet(
            f"QScrollArea {{ border:{THEME['border_width']} solid {THEME['bg_border']}; "
            f"border-radius:{THEME['radius_md']}; background:{THEME['bg_main']}; }}")
        root.addWidget(self.scroll, 1)

        inrow = QHBoxLayout(); inrow.setSpacing(6)
        self.speaker_btn = QPushButton()
        self.speaker_btn.setFixedWidth(64)
        self.speaker_btn.clicked.connect(self._toggle_speaker)
        self.input = ChatInput(on_submit=self._submit, on_toggle=self._toggle_speaker)
        self.input.setPlaceholderText("Type a line, Enter to add  ·  ↑↓ switch speaker  ·  double-click a line to edit")
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
        bubble = ChatBubble(line, on_remove=self._remove_bubble, on_edit=self._on_edit)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self._bubble_map[bubble] = line

    def _on_edit(self):
        if self.on_change: self.on_change()

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


# ── Choices ───────────────────────────────────────────────────────────────────
class ChoiceWidget(QFrame):
    def __init__(self, parent=None, on_remove=None):
        super().__init__(parent)
        self.on_remove = on_remove
        self.linked_block = None   # the auto-created follow-up DialogBlock, if any
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
        self.func = QLineEdit(); self.func.setPlaceholderText("Handler func")
        self.func.setFixedWidth(210); self.func.setStyleSheet(SS["field"])
        rm = QPushButton("✕"); rm.setFixedSize(22, 22); rm.setStyleSheet(SS["rm_btn"])
        rm.clicked.connect(lambda: self.on_remove(self) if self.on_remove else None)
        lay.addWidget(self.label, 2); lay.addWidget(self.func, 1); lay.addWidget(rm)

    def lock_func(self, name):
        """Called once a follow-up scene has been auto-created for this choice —
        the function name is now managed by that scene, not free text."""
        self.func.setText(name)
        self.func.setReadOnly(True)
        self.func.setStyleSheet(SS["field_readonly"])

    def get_choice(self): return DialogChoice(self.label.text(), self.func.text())


class BlockEditor(QWidget):
    def __init__(self, parent=None, on_change=None, on_choice_added=None,
                 on_choice_removed=None, is_followup=False):
        super().__init__(parent)
        self.on_change = on_change
        self.on_choice_added = on_choice_added
        self.on_choice_removed = on_choice_removed
        self.is_followup = is_followup
        self.setStyleSheet(f"QWidget {{ background:{THEME['bg_main']}; }}")
        self._suppress_emit = True
        self._build()
        self._suppress_emit = False

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(14, 12, 14, 12); root.setSpacing(8)

        def lbl(text, width=60):
            w = QLabel(text)
            w.setFixedWidth(width)
            w.setStyleSheet(f"color:{THEME['text_secondary']}; font-weight:600; font-size:{THEME['font_size_small']};")
            return w

        if self.is_followup:
            hint = QLabel("↳  Follow-up scene, shown after a choice is picked")
            hint.setStyleSheet(
                f"color:{THEME['accent_secondary']}; font-weight:600; "
                f"font-size:{THEME['font_size_small']}; padding-bottom:2px;")
            root.addWidget(hint)

        name_row = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(
            "Choice reply name  ·  e.g. GiveRingOfStrength" if self.is_followup
            else "Scene name  ·  e.g. Hello · WannaJoin · KalomsRecipe")
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
        choices_scroll.setWidgetResizable(True); choices_scroll.setMinimumHeight(160)
        choices_scroll.setMaximumHeight(260)
        choices_scroll.setStyleSheet(f"QScrollArea {{ border:none; background:{THEME['bg_main']}; }}")
        dt.addWidget(choices_scroll)

        tabs.addTab(dialog_tab, "Dialog")

        # ── Advanced tab: everything else, tucked away ─────────────────────────
        adv_tab = QWidget()
        av = QVBoxLayout(adv_tab); av.setContentsMargins(10, 10, 10, 10); av.setSpacing(10)

        if not self.is_followup:
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
        else:
            # Follow-up scenes don't have instance metadata — keep placeholders
            # so get_block()/load_block() stay uniform across both kinds.
            self.desc_edit = QLineEdit(); self.perm_cb = QCheckBox(); self.imp_cb = QCheckBox()
            self.trade_cb = QCheckBox(); self.cond_edit = QLineEdit()

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

        if not self.is_followup:
            self.stop_cb = QCheckBox("AI_StopProcessInfos at end")
            self.stop_cb.setChecked(True); self.stop_cb.setStyleSheet(SS["check"])
            sr = QHBoxLayout(); sr.addWidget(self.stop_cb); sr.addStretch()
            av.addLayout(sr)
        else:
            self.stop_cb = QCheckBox()
            note = QLabel("This reply closes back to the main dialog automatically.")
            note.setStyleSheet(f"color:{THEME['text_muted']}; font-size:{THEME['font_size_small']}; font-style:italic;")
            av.addWidget(note)
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
        if getattr(self, "_suppress_emit", False): return
        if self.on_change: self.on_change()

    def _add_choice(self, choice=None, is_loaded=False):
        cw = ChoiceWidget(on_remove=self._rm_choice)
        if choice:
            cw.label.setText(choice.label); cw.func.setText(choice.func_name)
        cw.label.textChanged.connect(self._emit); cw.func.textChanged.connect(self._emit)
        self.choices_layout.addWidget(cw)
        if not is_loaded and self.on_choice_added:
            self.on_choice_added(cw)   # lets MainWindow auto-create the follow-up scene
        self._emit()
        return cw

    def _rm_choice(self, w):
        if self.on_choice_removed: self.on_choice_removed(w)
        w.setParent(None); w.deleteLater(); self._emit()

    def _clear_choices(self):
        while self.choices_layout.count():
            item = self.choices_layout.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()

    def get_block(self):
        b = DialogBlock()
        b.name = self.name_edit.text().strip()
        b.is_followup = self.is_followup
        if not self.is_followup:
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

    def load_block(self, b):
        self._suppress_emit = True
        self.name_edit.setText(b.name)
        if not self.is_followup:
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
            self._add_choice(ch, is_loaded=True)
        self._suppress_emit = False

    def get_choice_widgets(self):
        return [self.choices_layout.itemAt(i).widget() for i in range(self.choices_layout.count())]


class BlockListItem(QFrame):
    def __init__(self, idx, name, parent=None, on_select=None, on_remove=None, is_followup=False):
        super().__init__(parent)
        self.idx = idx; self.on_select = on_select; self.on_remove = on_remove; self._active = False
        self.is_followup = is_followup
        self.setFixedHeight(34); self.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(24 if is_followup else 10, 4, 6, 4)
        prefix = "↳ " if is_followup else ""
        self.lbl = QLabel(prefix + (name or f"Scene {idx+1}"))
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
            color = THEME['text_muted'] if self.is_followup else THEME['text_secondary']
            self.lbl.setStyleSheet(f"color:{color}; font-size:{THEME['font_size_ui']};")

    def set_active(self, v): self._active = v; self._update_style()
    def update_name(self, n):
        prefix = "↳ " if self.is_followup else ""
        self.lbl.setText(prefix + (n or f"Scene {self.idx+1}"))
    def mousePressEvent(self, e):
        if self.on_select: self.on_select(self.idx)
