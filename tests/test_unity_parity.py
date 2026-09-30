import json
import re
import unittest
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

class UnityParityTests(unittest.TestCase):
    def test_original_has_six_pages_and_no_audio_or_drag(self):
        html = (ROOT/'SourceReference/index.html').read_text(encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        self.assertEqual(6, len(soup.select('section.page')))
        self.assertEqual(0, len(soup.select('audio')))
        self.assertNotIn('addEventListener(\'drag', html)

    def test_each_page_has_exact_browser_capture(self):
        for i in range(6):
            with Image.open(ROOT/f'Assets/Resources/Pages/Page{i}.png') as img:
                self.assertEqual((430,862), img.size)

    def test_button_rects_and_destinations_match_source(self):
        nav = json.loads((ROOT/'SourceReference/navigation.json').read_text(encoding='utf-8'))
        self.assertEqual([[1],[0,2],[1,3],[2,4],[3,5],[4,0]],
                         [[button['go'] for button in nav[str(i)]] for i in range(6)])
        ui = (ROOT/'Assets/Scripts/StorybookData.cs').read_text()
        for i in range(6):
            for button in nav[str(i)]:
                self.assertIn(f"new Hotspot({button['go']}, {button['x']}f, {button['y']}f, {button['w']}f, {button['h']}f)", ui)

    def test_unity_is_native_ugui_with_keyboard_and_real_buttons(self):
        app = (ROOT/'Assets/Scripts/StorybookApp.cs').read_text()
        self.assertIn('new Vector2(430f, 862f)', app)
        self.assertIn('typeof(Canvas)', app)
        self.assertIn('typeof(StandaloneInputModule)', app)
        self.assertIn('Input.GetKeyDown(KeyCode.LeftArrow)', app)
        self.assertIn('Input.GetKeyDown(KeyCode.RightArrow)', app)
        self.assertIn('button.onClick.AddListener', app)
        self.assertIn('PlaceRelative(hitbox, spot.X, spot.Y, spot.Width, spot.Height)', app)
        self.assertIn('x / StorybookData.BookWidth', app)
        self.assertIn('Resources.Load<Texture2D>("Pages/Page" + index)', app)
        self.assertNotIn('WebView', app)
        self.assertNotIn('Application.OpenURL', app)

    def test_unity_scene_and_webgl_template(self):
        scene=(ROOT/'Assets/Scenes/Main.unity').read_text()
        meta=(ROOT/'Assets/Scripts/StorybookBootstrap.cs.meta').read_text()
        guid=re.search(r'guid: ([a-f0-9]{32})',meta).group(1)
        self.assertIn(guid,scene)
        build=(ROOT/'Assets/Editor/StorybookBuild.cs').read_text()
        self.assertIn('Assets/Scenes/Main.unity',build)
        self.assertIn('defaultWebScreenWidth = 430',build)
        self.assertIn('defaultWebScreenHeight = 862',build)
        self.assertIn('WebGLCompressionFormat.Gzip',build)
        html=(ROOT/'Assets/WebGLTemplates/DewySimple/index.html').read_text()
        self.assertIn('JSON.stringify(PRODUCT_NAME)',html)
        manifest=(ROOT/'Packages/manifest.json').read_text()
        self.assertIn('"com.unity.ugui"',manifest)
        settings=(ROOT/'ProjectSettings/ProjectSettings.asset').read_text()
        self.assertIn('activeInputHandler: 0',settings)

if __name__=='__main__': unittest.main()
