# USD Updater

## What is this ?

This tool gives an interactive way to update USD files on a Prism-based pipeline.
For a given USD, it will check if there is a new version available for each dependency
Then allow their update.

Given a specific shot USD export, it will be to retrieve a given list of layers and will also parse them.

<img width="1198" height="830" alt="image" src="https://github.com/user-attachments/assets/2b8728b8-fa39-41bb-84bd-35716321afd2" />

## Packages

The GUI part relies mainly on `Qt` framework, we are using `pyqt` as an abstraction layer
to have an UI working with different PySide versions such as: PySide2, PySide6, PyQt5 or PyQt6.
This is useful to have an UI working on different DCC with unknown `Qt` implementation.

The USD scan and update are handle using the official USD API in Python `usd-core`.

Debug is done through DCC via `debugpy`, purely optional in production settings.

## Quick Start

First, you need to use a Python environment with the correct packages.
These packages are specified in the `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

A `quickstart.py` is available as an example.

```bash
python quickstart.py
```

The only method needed is `startUpdateAssetsUSD(openType, tmpfile=None, ar_context=None)`:
 - openType can be either "prism", "houdini" or "maya". It will define the starting behaviour of the interface. Prism is the default setting.
 - tmpfile is an USD file that can be provided directly.
 - ar_context is the context of the USD asset resolver as a Python list.

### Environment variables

Here is a list of useful environment variable:
 - `UD_LOG_DIR` sets the location of logs, by default they go in `logs` directory in this repository.
 - `UD_DEBUG` (0 or 1) tells if the debug mode should be enabled.
 - `UD_DEBUG_PYTHON_EXEC` path to a custom Python executable, useful for specific DCC.
 - `UD_DEBUGPY_PATH` path to `debugpy` lib, needed if debugpy is not installed in current environment.
 - `PYTHONPATH` classic python path variable, needed to hold repository root path to be able to start test.
  
## Notes

There is currently 3 modes, one for Prism, one for Maya and one for Houdini.

Prism and Houdini are very similar as they start with a given USD filepath.
The only differnce is that the Houdini modes will also look for path in selected 
Prism Import LOP nodes.

While these 2 modes use standard USD API to parse depedencies ([https://openusd.org/dev/api/dependencies_8h.html](https://openusd.org/dev/api/dependencies_8h.html)).
The Maya mode is more rough as it just parsed the current work layer as an USDA and use regular expression to get dependencies.

## Where to use it

### Prism Mode :

This mode is started from Prism Project browser product windows and is added with a prism plugin [https://prism-pipeline.com/docs/latest/development/developingPlugins/](https://prism-pipeline.com/docs/latest/development/developingPlugins/)

### Houdini and Maya :

Located as custom button in both DCC shelves.
