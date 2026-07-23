import pathlib
import unittest

from daedalus_gen import parse_dia_file


class ParseDiaFileTests(unittest.TestCase):
    def test_parses_reference_gothic_dialog_file(self):
        text = pathlib.Path("REFERENCE/DIA_Addon_BAU_4300_Cavalorn.d").read_text(
            encoding="utf-8", errors="ignore"
        )

        npc_name, npc_id, blocks = parse_dia_file(text)

        self.assertEqual(npc_id, "bau_4300_addon_cavalorn")
        self.assertGreater(len(blocks), 0)

        hallo = next(b for b in blocks if b.name == "DIA_ADDON_CAVALORN_HALLO")
        self.assertEqual(hallo.nr, 5)
        self.assertGreater(len(hallo.entries), 0)
        self.assertEqual(len(hallo.choices), 2)
        self.assertTrue(any(getattr(e, "text", "") for e in hallo.entries))


if __name__ == "__main__":
    unittest.main()
