"""Regression checks for Unity Build Automation's managed export directory."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CloudBuildExportTests(unittest.TestCase):
    def test_cloud_preprocessing_cannot_redirect_export_folder(self):
        code = (ROOT / 'Assets/Editor/StorybookBuild.cs').read_text(encoding='utf-8')
        config = code.split('public static void ApplyWebGLSettings()', 1)[1].split('public static void PreExport()', 1)[0]
        self.assertNotRegex(config, r'(?m)^\\s*EditorUserBuildSettings\\.SetBuildLocation\\s*\\(')
        self.assertNotRegex(config, r'(?m)^\\s*EditorBuildSettings\\.scenes\\s*=')
        self.assertIn('public void OnPreprocessBuild(BuildReport report)', code)

    def test_cloud_hook_only_configures_settings(self):
        code = (ROOT / 'Assets/Editor/StorybookBuild.cs').read_text(encoding='utf-8')
        hook = code.split('public static void PreExport()', 1)[1].split('[MenuItem("Dewy Simple/Build WebGL for itch.io")]', 1)[0]
        self.assertIn('ApplyWebGLSettings();', hook)
        self.assertNotIn('BuildPipeline.BuildPlayer(', hook)
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('StorybookBuild.PreExport', readme)
        self.assertIn('Unity Build Automation assigns its own export path', readme)

    def test_local_manual_build_still_uses_own_output(self):
        code = (ROOT / 'Assets/Editor/StorybookBuild.cs').read_text(encoding='utf-8')
        local_build = code.split('public static void BuildWebGL()', 1)[1]
        self.assertIn('const string output = "Builds/WebGL";', local_build)
        self.assertIn('locationPathName = output', local_build)
        self.assertIn('BuildPipeline.BuildPlayer(', local_build)

if __name__ == '__main__':
    unittest.main()
