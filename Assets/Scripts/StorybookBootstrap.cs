using UnityEngine;

/// <summary>Single-scene startup for the user's original six-page storybook.</summary>
public sealed class StorybookBootstrap : MonoBehaviour
{
    private void Awake()
    {
        if (FindFirstObjectByType<StorybookApp>() == null)
            gameObject.AddComponent<StorybookApp>();
    }
}
