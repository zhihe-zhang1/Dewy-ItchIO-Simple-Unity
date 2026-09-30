using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

/// <summary>
/// Native Unity UGUI storybook. The six source pages are losslessly captured as
/// Unity textures to preserve their exact SVG illustrations, font rendering,
/// line wrapping, cards and buttons. Real Unity buttons provide the navigation;
/// NO browser runtime, music, or extra interactions are used.
/// </summary>
public sealed class StorybookApp : MonoBehaviour
{
    private Canvas canvas;
    private RectTransform pageRoot;
    private int currentPage = -1;
    private readonly Sprite[] cachedSprites = new Sprite[StorybookData.PageCount];

    private void Start()
    {
        CreateInfrastructure();
        ShowPage(0);
    }

    private void Update()
    {
        // Exact keyboard semantics from the supplied source index.html:
        // left/right advances by one page, independently of the button labels.
        if (Input.GetKeyDown(KeyCode.LeftArrow) && currentPage > 0)
            ShowPage(currentPage - 1);
        else if (Input.GetKeyDown(KeyCode.RightArrow) && currentPage < StorybookData.PageCount - 1)
            ShowPage(currentPage + 1);
    }

    private void CreateInfrastructure()
    {
        GameObject canvasObject = new GameObject(
            "DewySimpleCanvas", typeof(RectTransform), typeof(Canvas),
            typeof(CanvasScaler), typeof(GraphicRaycaster));
        canvasObject.transform.SetParent(transform, false);
        canvas = canvasObject.GetComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 0;

        CanvasScaler scaler = canvasObject.GetComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(430f, 862f);
        scaler.screenMatchMode = CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;
        scaler.matchWidthOrHeight = .5f;

        // StandaloneInputModule requires PlayerSettings.activeInputHandler = Old/Both.
        // This project pins Old in ProjectSettings.asset for reliable WebGL clicks.
        if (EventSystem.current == null)
        {
            GameObject eventObject = new GameObject(
                "DewyEventSystem", typeof(EventSystem), typeof(StandaloneInputModule));
            eventObject.transform.SetParent(transform, false);
        }
    }

    public void ShowPage(int index)
    {
        index = Mathf.Clamp(index, 0, StorybookData.PageCount - 1);
        if (pageRoot != null)
        {
            pageRoot.gameObject.SetActive(false);
            Destroy(pageRoot.gameObject);
        }

        currentPage = index;
        pageRoot = MakeRect("Page_" + index, canvas.transform);
        Stretch(pageRoot);

        Sprite pageSprite = LoadPage(index);
        if (pageSprite == null)
        {
            Debug.LogError("Page illustration not found: Resources/Pages/Page" + index);
            return;
        }

        // Screenshot's 430x862 content includes every original visual detail:
        // brand, title, story copy, exact SVG art, fact card and visible buttons.
        Image pageImage = pageRoot.gameObject.AddComponent<Image>();
        pageImage.sprite = pageSprite;
        pageImage.type = Image.Type.Simple;
        pageImage.preserveAspect = false;
        pageImage.raycastTarget = false;
        pageImage.color = Color.white;

        StorybookData.Hotspot[] hotspots = StorybookData.Buttons[index];
        for (int i = 0; i < hotspots.Length; i++)
        {
            StorybookData.Hotspot spot = hotspots[i];
            int destination = spot.Destination;
            RectTransform hitbox = MakeRect("ButtonTo_" + destination, pageRoot);
            PlaceRelative(hitbox, spot.X, spot.Y, spot.Width, spot.Height);
            Image hitGraphic = hitbox.gameObject.AddComponent<Image>();
            // The HTML-drawn button remains visible on the background image.
            // The native UGUI graphic only creates a pointer/touch hit area.
            hitGraphic.color = new Color(1f, 1f, 1f, 0f);
            hitGraphic.raycastTarget = true;
            Button button = hitbox.gameObject.AddComponent<Button>();
            button.targetGraphic = hitGraphic;
            button.transition = Selectable.Transition.None;
            button.navigation = new Navigation { mode = Navigation.Mode.None };
            button.onClick.AddListener(() => ShowPage(destination));
        }
    }

    private Sprite LoadPage(int index)
    {
        if (cachedSprites[index] != null) return cachedSprites[index];
        // PNG files are imported as Texture2D with uncompressed/no-mipmap settings.
        Texture2D original = Resources.Load<Texture2D>("Pages/Page" + index);
        if (original == null) return null;
        cachedSprites[index] = Sprite.Create(
            original, new Rect(0, 0, original.width, original.height),
            new Vector2(.5f, .5f), 100f, 0, SpriteMeshType.FullRect);
        cachedSprites[index].name = "StorybookPage" + index;
        return cachedSprites[index];
    }

    private static RectTransform MakeRect(string name, Transform parent)
    {
        GameObject go = new GameObject(name, typeof(RectTransform));
        RectTransform rt = go.GetComponent<RectTransform>();
        rt.SetParent(parent, false);
        rt.localScale = Vector3.one;
        return rt;
    }

    // Use proportional anchors so touch hit areas always follow the displayed
    // screenshot, even if an itch.io iframe has a non-reference aspect ratio.
    private static void PlaceRelative(RectTransform rt, float x, float y, float width, float height)
    {
        rt.anchorMin = new Vector2(
            x / StorybookData.BookWidth,
            1f - (y + height) / StorybookData.BookHeight);
        rt.anchorMax = new Vector2(
            (x + width) / StorybookData.BookWidth,
            1f - y / StorybookData.BookHeight);
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;
    }

    private static void Stretch(RectTransform rt)
    {
        rt.anchorMin = Vector2.zero;
        rt.anchorMax = Vector2.one;
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;
    }
}
