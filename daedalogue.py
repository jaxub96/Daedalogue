"""
Gothic Dialog Generator — Minimal Edition
Visual design lives in theme.py. Data model + code generation live in
daedalus_gen.py. Custom widgets live in widgets.py. This file is just the
main window that wires them together.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QScrollArea,
    QMessageBox, QFileDialog, QSplitter,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

from theme import THEME, SS, DaedalusHighlighter, mono_font
from daedalus_gen import (
    DialogBlock, sanitize, export_block_name,
    generate_dia_file, generate_constants_file, export_plain_dialog, parse_dia_file,export_followup_name
)
from widgets import BlockEditor, BlockListItem


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

        def flat_btn(text):
            b = QPushButton(text)
            b.setStyleSheet(
                f"QPushButton {{ background:{THEME['bg_panel']}; color:{THEME['text_secondary']}; "
                f"border:{THEME['border_width']} solid {THEME['bg_border']}; "
                f"border-radius:{THEME['radius_md']}; padding:6px 14px; font-weight:600; }}"
                f"QPushButton:hover {{ background:{THEME['bg_input_border']}; color:{THEME['text_primary']}; }}")
            return b

        open_btn = flat_btn("Open")
        open_btn.clicked.connect(self._open)

        text_btn = flat_btn("Export Text")
        text_btn.clicked.connect(self._export_text)

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
        tb.addWidget(open_btn); tb.addWidget(text_btn); tb.addWidget(save_btn)
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

        self.dia_preview = QTextEdit(); self.dia_preview.setReadOnly(True); self.dia_preview.setFont(mono_font())
        self.dia_preview.setStyleSheet(
            f"QTextEdit {{ background:{THEME['bg_panel']}; color:{THEME['text_primary']}; "
            f"border:none; padding:10px; }}")
        DaedalusHighlighter(self.dia_preview.document())
        pv.addWidget(self.dia_preview)

        splitter.addWidget(preview_panel)
        splitter.setSizes(THEME["splitter_sizes"])
        root.addWidget(splitter, 1)

        self.npc_name_edit.textChanged.connect(self._refresh_preview)
        self.npc_id_edit.textChanged.connect(self._refresh_preview)

    # ── Scene tree management ───────────────────────────────────────────────

    def _make_editor(self, is_followup):
        return BlockEditor(
            on_change=self._refresh_preview,
            on_choice_added=self._on_choice_added,
            on_choice_removed=self._on_choice_removed,
            is_followup=is_followup,
        )

    def _find_insert_pos_after(self, parent_idx):
        parent_block = self.blocks[parent_idx]
        pos = parent_idx + 1
        while pos < len(self.blocks) and self._is_descendant(self.blocks[pos], parent_block):
            pos += 1
        return pos

    def _is_descendant(self, block, ancestor):
        cur = block.parent_block
        while cur is not None:
            if cur is ancestor: return True
            cur = cur.parent_block
        return False

    def _add_block(self, block=None, parent_idx=None):
        b = block if block is not None else DialogBlock()
        insert_pos = self._find_insert_pos_after(parent_idx) if parent_idx is not None else len(self.blocks)

        self.blocks.insert(insert_pos, b)
        ed = self._make_editor(is_followup=b.is_followup)
        if block is not None:
            ed.load_block(b)
        self.block_editors.insert(insert_pos, ed)
        self.editor_stack.addWidget(ed)

        item = BlockListItem(insert_pos, b.name, on_select=self._select_block,
                              on_remove=self._remove_block, is_followup=b.is_followup)
        self.block_items.insert(insert_pos, item)
        self.block_list_layout.insertWidget(insert_pos, item)
        self._reindex()
        self._select_block(insert_pos)
        return b, ed

    def _reindex(self):
        for i, it in enumerate(self.block_items):
            it.idx = i

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
        target = self.blocks[idx]
        # cascade: remove this block and every descendant follow-up scene
        doomed = [i for i, b in enumerate(self.blocks) if b is target or self._is_descendant(b, target)]
        for i in sorted(doomed, reverse=True):
            self.blocks.pop(i)
            self.block_editors.pop(i).deleteLater()
            item = self.block_items.pop(i); item.setParent(None); item.deleteLater()
        self._reindex()
        self.current_block_idx = min(self.current_block_idx, len(self.blocks) - 1)
        if self.current_block_idx >= 0: self._select_block(self.current_block_idx)
        else: self.editor_stack.setCurrentWidget(self.placeholder)
        self._refresh_preview()

    # ── Choice ↔ follow-up scene linking ────────────────────────────────────

    def _on_choice_added(self, cw):
        parent_idx = self._editor_idx_containing(cw)
        if parent_idx is None: return
        parent_block = self.blocks[parent_idx]
        ni = self.npc_id_edit.text().strip()   or "NPC_ID"
        parent_name = self.block_editors[parent_idx].name_edit.text().strip() or parent_block.name or f"Scene{parent_idx+1}"
        if parent_block.is_followup and parent_block.func_name:
            parent_bn = parent_block.func_name
        else:
            parent_bn = export_block_name(ni, parent_name)

        existing_children = [b for b in self.blocks if b.parent_block is parent_block]
        n = len(existing_children) + 1
        func_name = f"{parent_bn}_Choice{n}"

        nb = DialogBlock()
        nb.is_followup = True
        nb.name = f"Choice {n}"
        nb.func_name = func_name
        nb.parent_block = parent_block

        cw.linked_block = nb
        cw.lock_func(func_name)

        self._add_block(nb, parent_idx=parent_idx)

    def _on_choice_removed(self, cw):
        if getattr(cw, "linked_block", None) is None: return
        for i, b in enumerate(self.blocks):
            if b is cw.linked_block:
                self._remove_block(i)
                break

    def _editor_idx_containing(self, choice_widget):
        for i, ed in enumerate(self.block_editors):
            if choice_widget in ed.get_choice_widgets():
                return i
        return None

    # ── Generation / persistence ────────────────────────────────────────────

    def _collect_blocks(self):
        for i, ed in enumerate(self.block_editors):
            b = self.blocks[i]
            fresh = ed.get_block()
            b.name = fresh.name or (f"Choice{i+1}" if b.is_followup else f"Scene{i+1}")
            b.description = fresh.description
            b.permanent = fresh.permanent
            b.important = fresh.important
            b.is_trade = fresh.is_trade
            b.condition_expr = fresh.condition_expr
            b.stop_after = fresh.stop_after
            b.entries = fresh.entries
            b.choices = fresh.choices
            self.block_items[i].update_name(b.name)

        
        # nr is assigned automatically from top-level scene order
        n = 1
        for b in self.blocks:
            if not b.is_followup:
                b.nr = n; n += 1

        nn = self.npc_name_edit.text().strip() or "NPC"
        ni = self.npc_id_edit.text().strip()   or "NPC_ID"
        for b in self.blocks:
            if b.is_followup:
                parent_bn = b.parent_block.func_name if b.parent_block.is_followup \
                    else export_block_name(ni, b.parent_block.name)
                b.func_name = export_followup_name(parent_bn, b.name)
        for ed in self.block_editors:
            for cw in ed.get_choice_widgets():
                if cw.linked_block is not None:
                    cw.func.setText(cw.linked_block.func_name)
        return self.blocks

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
        default = self.current_file_path or f"DIA_{sanitize(ni)}.d"
        path, _ = QFileDialog.getSaveFileName(self, "Save Dialog File", default, "Daedalus Dialog Files (*.d)")
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write(generate_dia_file(nn, ni, bl))
        self.current_file_path = path
        self.setWindowTitle(f"Gothic Dialog Generator — {os.path.basename(path)}")
        QMessageBox.information(self, "Saved", f"Dialog file saved:\n  {path}")

    def _export_text(self):
        bl = self._collect_blocks()
        if not any(b.lines() for b in bl):
            QMessageBox.information(self, "Nothing to Export", "Add some dialog lines first.")
            return
        ni = self.npc_id_edit.text().strip()   or "NPC_ID"
        default = f"{sanitize(ni)}_dialog.txt"
        path, _ = QFileDialog.getSaveFileName(self, "Export Plain Dialog Text", default, "Text Files (*.txt)")
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write(export_plain_dialog(bl))
        QMessageBox.information(self, "Exported", f"Dialog reference text saved:\n  {path}")

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
            # parsed blocks arrive in pre-order (parent, then its children) —
            # a plain append reproduces the correct nesting automatically.
            _, ed = self._add_block(b)
            # re-link each parsed choice row to its follow-up scene, if any
            if not b.is_followup:
                for cw in ed.get_choice_widgets():
                    child = next((c for c in blocks if c.is_followup and c.func_name == cw.func.text()
                                  and c.parent_block is b), None)
                    if child is not None:
                        cw.linked_block = child
                        cw.lock_func(child.func_name)
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