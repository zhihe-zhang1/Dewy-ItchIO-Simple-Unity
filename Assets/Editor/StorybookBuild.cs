#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;

/// <summary>Use WebGL compression fallback for static hosts such as itch.io.</summary>
public sealed class StorybookBuild : IPreprocessBuildWithReport
{
    public int callbackOrder => -1000;

    public void OnPreprocessBuild(BuildReport report)
    {
        if (report.summary.platform == BuildTarget.WebGL)
            ApplyWebGLSettings();
    }

    [MenuItem("Dewy Simple/Apply WebGL Settings")]
    public static void ApplyWebGLSettings()
    {
        PlayerSettings.defaultWebScreenWidth = 430;
        PlayerSettings.defaultWebScreenHeight = 862;
        PlayerSettings.WebGL.template = "PROJECT:DewySimple";
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Gzip;
        PlayerSettings.WebGL.decompressionFallback = true;
        EditorUserBuildSettings.SetBuildLocation(BuildTarget.WebGL, "Builds/WebGL");
        EditorBuildSettings.scenes = new [] {
            new EditorBuildSettingsScene("Assets/Scenes/Main.unity", true)
        };
    }

    [MenuItem("Dewy Simple/Build WebGL for itch.io")]
    public static void BuildWebGL()
    {
        ApplyWebGLSettings();
        const string output = "Builds/WebGL";
        if (Directory.Exists(output)) Directory.Delete(output, true);
        Directory.CreateDirectory(output);
        BuildReport result = BuildPipeline.BuildPlayer(new BuildPlayerOptions {
            scenes = new [] { "Assets/Scenes/Main.unity" },
            locationPathName = output,
            target = BuildTarget.WebGL,
            options = BuildOptions.None
        });
        if (result.summary.result != BuildResult.Succeeded)
            throw new BuildFailedException("Dewy Simple WebGL failed: " + result.summary.result);
        Debug.Log("Dewy Simple WebGL created at: " + Path.GetFullPath(output));
    }
}
#endif
