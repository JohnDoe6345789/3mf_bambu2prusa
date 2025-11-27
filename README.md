# 3mf_bambu2prusa
This application converts Bambu Studio 3mf files (including painted/colored models) into PrusaSlicer-compatible 3mf files. The project was built by reverse-engineering 3mf archives rather than relying on an official specification.

## Setup
Run the helper script to create a virtual environment, install the package in editable mode, and expose the `bambu2prusa` command inside the venv:

```
python scripts/setup.py

# Then launch from the venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
bambu2prusa
```

## Install globally (PATH-friendly)
With Python already installed, install from the repository root using your preferred tooling. The generated `bambu2prusa` command is placed on your PATH automatically by pipx/pip:

```
# macOS (Homebrew Python)
brew install python-tk
pipx install .

# Windows (Chocolatey)
choco install python
pipx install .
```

If you prefer a virtual environment, `pip install .` works as well.

## Launch the GUI
The packaged entrypoint is the quickest way to start the converter:

```
bambu2prusa
```

The legacy launcher remains available if you want to pick an interpreter explicitly:

```
python scripts/launch_gui.py
```

An experimental XML-based workflow remains available in `bambu_to_prusa_xml.py`.
