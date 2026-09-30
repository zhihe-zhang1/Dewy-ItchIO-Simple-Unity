# Dewy's Wonderful Water Journey — Simple Unity Edition

This is a **new and independent native Unity UGUI project** converted from the
user-supplied `Dewy_ItchIO_Zhihe_Zhang(1).zip` (one self-contained `index.html`).
It is intentionally NOT the earlier six-interaction-scene Dewy project.

## Source parity

- Exactly **6 pages**: Home, four scenes, Credits.
- Exact story copy, colors, SVG illustrations, page frames and visible buttons are
  preserved as **lossless 430×862 browser page captures** under `Assets/Resources/Pages/`.
  The page captures are Unity-native Texture2D resources, not embedded HTML.
- All visible navigation has **real Unity UGUI Buttons** with hit areas measured
  from the supplied HTML (`SourceReference/navigation.json`).
- Button mapping: Home→1; 1↔0/2; 2↔1/3; 3↔2/4; 4↔3/5; Credits→4 or Restart→0.
- The original **ArrowLeft / ArrowRight** page navigation is implemented in C#.
- There is no audio, drag game, scene unlocking, or music button in the uploaded source;
  none has been invented here.
- Canvas reference: **430 × 862**, matching the original desktop book capture
  including its 1px top and bottom border.

### Editing guide

Navigation logic: `Assets/Scripts/StorybookApp.cs`.
Navigation coordinates: `Assets/Scripts/StorybookData.cs`.
Original HTML and measured button rectangles: `SourceReference/`.
To change a source illustration/copy, edit the HTML and re-capture corresponding
PNG via `tools/capture_source_pages.py` (requires Python + Playwright + Chromium).

## Open in Unity

Use Unity Editor **6000.3.23f1** with WebGL Build Support, or another compatible
Unity 6.3 release. From Unity Hub, choose **Add project from disk** and select
this folder (the one containing `Assets`, `Packages`, `ProjectSettings`).
Open `Assets/Scenes/Main.unity` and press Play.

## WebGL / itch.io build

Unity menu: **Dewy Simple → Build WebGL for itch.io**.
For **Unity Build Automation**: repository branch `main`, platform `WebGL`,
scene `Assets/Scenes/Main.unity`. Use Unity's **standard WebGL build**, not the
local manual build method. In Advanced Settings you may set the optional
**Pre-Export Method** to `StorybookBuild.PreExport` to configure the template,
Gzip + decompression fallback and 430×862 dimensions before export.
**Do not set `StorybookBuild.BuildWebGL` as the Pre-Export Method.** Do not
override the Cloud export/output directory with `Builds/WebGL`; Unity Build
Automation assigns its own export path, which its publisher subsequently reads.
The local editor menu `Dewy Simple → Build WebGL for itch.io` still outputs
to `Builds/WebGL` for builds you run on your own computer.

If Cloud reports `Build failed - export directory is empty`, download the Unity
Editor log and inspect the FIRST earlier compilation/build error as well; the
Publishing-stage `Could not find index.html` warning is downstream of the
missing export and is not by itself a diagnosis.

After compiling, ZIP the **contents** of `Builds/WebGL` so `index.html` is at
ZIP root. Upload that ZIP to itch.io and tick *This file will be played in the browser*.
Suggested itch.io embed viewport: 430 × 862 (larger iframe may be needed for
external chrome on desktop).

> The project has been structurally and source-parity tested, but the current
> working environment does not contain Unity Editor. An actual Unity/WebGL
> compile must be performed on your Unity installation or Unity Cloud Build.
