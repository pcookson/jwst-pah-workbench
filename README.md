# JWST PAH Workbench

Epic 0 scaffold for a Linux desktop workbench built with PySide6.

## Features in this scaffold

- Dockable panels:
  - Left: Project Explorer
  - Right: Inspector
  - Bottom: Logs
- Central tab workspace:
  - Spectrum tab (mock matplotlib plot)
  - Image tab (mock grayscale QGraphicsView)
- File menu stubs for project actions
- Working FITS import via file dialog (`.fits`, `.fit`)
- Drag-and-drop FITS import onto the main window
- Persistent window geometry and dock layout via `QSettings`
- In-memory imported file list and inspector placeholders

## Setup (Ubuntu / Linux)

```bash
make install
```

This project is configured to use a repo-local virtual environment at `.venv/`.
Use `.venv/bin/python` (or `make` targets) so dependencies never install into system Python.

## Run

```bash
make run
```

## Test

```bash
make test
```
