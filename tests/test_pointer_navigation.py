"""Regression coverage for itch.io WebGL mouse/touch navigation fallbacks."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PointerNavigationTests(unittest.TestCase):
    def test_unity_mouse_touch_and_browser_pointer_are_supported(self):
        app = (ROOT / 'Assets/Scripts/StorybookApp.cs').read_text(encoding='utf-8')
        for token in [
            'Input.GetMouseButtonDown(0)',
            'Input.GetMouseButtonUp(0)',
            'Input.touchCount > 0',
            'TouchPhase.Began',
            'TouchPhase.Ended',
            'RegisterPointerDown(',
            'RegisterPointerUp(',
            'RectTransformUtility.ScreenPointToLocalPointInRectangle(',
            '[UnityEngine.Scripting.Preserve]',
            'public void BrowserPointer(string normalizedPosition)',
            'DestinationAtBookPosition('
        ]:
            self.assertIn(token, app)

    def test_home_left_is_disabled_and_all_original_hotspots_still_work(self):
        app = (ROOT / 'Assets/Scripts/StorybookApp.cs').read_text(encoding='utf-8')
        self.assertIn('return currentPage > 0 ? currentPage - 1 : -1;', app)
        self.assertIn('page == StorybookData.PageCount - 1 ? 0 : page + 1', app)
        self.assertIn('StorybookData.Buttons[currentPage]', app)
        self.assertIn('button.Destination;', app)

    def test_one_gesture_cannot_advance_twice(self):
        app = (ROOT / 'Assets/Scripts/StorybookApp.cs').read_text(encoding='utf-8')
        self.assertIn('Time.unscaledTime - lastNavigationAt < .18f', app)
        self.assertIn('pointerDownPage == currentPage', app)
        self.assertIn('destination == pointerDownDestination', app)
        self.assertIn('button.onClick.AddListener(() => NavigateTo(destination));', app)

    def test_webgl_template_forwards_browser_pointer_to_scene_bootstrap(self):
        html = (ROOT / 'Assets/WebGLTemplates/DewySimple/index.html').read_text(encoding='utf-8')
        self.assertIn("document.addEventListener('pointerup'", html)
        self.assertIn("canvas.getBoundingClientRect()", html)
        self.assertIn("unityInstance.SendMessage('StorybookBootstrap', 'BrowserPointer'", html)
        self.assertIn("unityInstance = instance;", html)

if __name__ == '__main__':
    unittest.main()
