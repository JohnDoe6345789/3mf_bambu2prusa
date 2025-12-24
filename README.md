# 3mf_bambu2prusa
This application converts Bambu Studio 3mf files (including painted/colored models) into PrusaSlicer-compatible 3mf files. The project was built by reverse-engineering 3mf archives rather than relying on an official specification.

## Architecture

The project is now split into two main domains:

### Backend (Core Logic)
- **`bambu_to_prusa/`** - Core conversion logic
  - `converter.py` - Main conversion orchestration
  - `model_processing.py` - Model file processing
  - `model_injection.py` - Prusa model building
  - `package_builder.py` - Package assembly
  - `file_ops.py` - File operations
  - `settings.py` - Settings management
  - `theme_engine.py` - UI theming support

### Frontend (User Interfaces)
- **`frontends/`** - Modular frontend implementations
  - `cli/` - Command-line interface
  - `tkinter/` - Tkinter GUI (default)
  - `pyqt6/` - PyQt6 GUI (optional)
  - `common/` - Shared frontend utilities

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

# Ubuntu (Linux)
sudo apt install python3 python3-pip
pipx install .
```

If you prefer a virtual environment, `pip install .` works as well.

## Launch the GUI
The packaged entrypoint launches the Tkinter GUI by default:

```
bambu2prusa
```

### Alternative Frontends

**Tkinter GUI** (default):
```
bambu2prusa-tkinter
```

**Command-line interface**:
```
bambu2prusa-cli input.3mf output.3mf
```

**PyQt6 GUI** (requires PyQt6):
```
# Install PyQt6 first
pip install bambu2prusa[pyqt6]

# Then launch
bambu2prusa-pyqt6
```

The legacy launcher remains available if you want to pick an interpreter explicitly:

```
python scripts/launch_gui.py
```
