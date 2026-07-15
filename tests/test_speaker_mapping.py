import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from gothic_dialog_gen import ChatLinesWidget, is_hero_speaker, speaker_display_name

app = QApplication.instance() or QApplication([])


def test_default_speaker_is_npc():
    widget = ChatLinesWidget()
    assert widget.current_speaker == "self"


def test_speaker_helpers_follow_npc_hero_mapping():
    assert is_hero_speaker("other") is True
    assert is_hero_speaker("self") is False
    assert speaker_display_name("self") == "NPC"
    assert speaker_display_name("other") == "Hero"
