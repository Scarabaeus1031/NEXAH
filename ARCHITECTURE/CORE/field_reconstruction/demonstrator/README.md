# NEXAH Field Reconstruction Demonstrator

This package presents the existing `field_reconstruction` scripts and generated
frames as one inspectable sequence:

`delay embedding → sheet → mesh → boundary → gradient → stability → channels → trajectory → target → IEEE field → resolution test → return`

The two historical sheet frames are copied byte-for-byte into `outputs/demo/`
so the browser package remains self-contained. Their producing scripts remain
the registered authority.

Open `../NEXAH_FIELD_RECONSTRUCTION_DEMONSTRATOR.html` directly in a browser.
It has no server or build dependency.

Controls:

- `PREV`, `PLAY`, `NEXT`: traverse the sixteen source-bound stages;
- `U / I WINDOW`: show the optional open-U, I/seam and `C | RIS | T` reading layer;
- `ORANGE SPARK`: mark the two candidate source/edge regions for inspection;
- `COMPARE`: split the current frame against its registered comparator;
- `EXPORT RECEIPT`: save the current source, producer, boundary and display state.

The overlays are annotations, not measurements. They never modify the source
frames. The orange regions remain an open diagnostic question: support density,
interpolation, edge handling and resolution sensitivity must be checked before
any physical interpretation.

Validate the package with:

```bash
python3 demonstrator/validate_demonstrator.py
```
