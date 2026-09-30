import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class VisibleNavigationTests(unittest.TestCase):
    def test_real_visible_previous_and_next_buttons_on_every_page(self):
        code = (ROOT/'Assets/Scripts/StorybookApp.cs').read_text(encoding='utf-8')
        self.assertIn('AddVisibleNavigationArrows(index);', code)
        self.assertIn('"PreviousArrow"', code)
        self.assertIn('"NextArrow"', code)
        self.assertIn('button.interactable = enabled;', code)
        self.assertIn('page == StorybookData.PageCount - 1 ? 0 : page + 1', code)
        self.assertIn('AddChevronStroke(root, "ArrowUpper"', code)
        self.assertIn('AddChevronStroke(root, "ArrowLower"', code)
        self.assertIn('PlaceRelative(root, x, y, 42f, 42f);', code)
        self.assertIn('GetNavigationDisc()', code)
        self.assertIn('button.onClick.AddListener(() => ShowPage(destination));', code)

if __name__ == '__main__': unittest.main()
