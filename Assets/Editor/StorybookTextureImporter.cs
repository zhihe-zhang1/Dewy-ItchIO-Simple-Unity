#if UNITY_EDITOR
using UnityEditor;

/// <summary>Keep the captured source book pages crisp; avoid mipmap text blur.</summary>
public sealed class StorybookTextureImporter : AssetPostprocessor
{
    private void OnPreprocessTexture()
    {
        if (!assetPath.StartsWith("Assets/Resources/Pages/")) return;
        TextureImporter importer = (TextureImporter)assetImporter;
        importer.textureType = TextureImporterType.Default;
        importer.mipmapEnabled = false;
        importer.npotScale = TextureImporterNPOTScale.None;
        importer.textureCompression = TextureImporterCompression.Uncompressed;
        importer.alphaIsTransparency = true;
        importer.sRGBTexture = true;
        importer.maxTextureSize = 2048;
    }
}
#endif
