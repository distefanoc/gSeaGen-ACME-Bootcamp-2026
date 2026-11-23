# Installing python-pptx

The hands-on exercises include an optional script that creates a PowerPoint presentation from your plots. To use it, install the `python-pptx` package **outside the Apptainer container**.

## 1. Open a Linux terminal

- **Linux:** Use a terminal on your computer.
- **macOS:** Open a terminal inside your Lima virtual machine.
- **Windows:** Open the Ubuntu terminal in WSL2.

## 2. Check whether pip is installed

```bash
python3 -m pip --version
```

If the command works, continue to Step 3.

If you see `No module named pip`, install it using your Linux distribution's package manager. On Ubuntu (including Ubuntu in Lima and WSL2):

```bash
sudo apt update
sudo apt install python3-pip
```

## 3. Install python-pptx

```bash
python3 -m pip install python-pptx
```

This also installs the required Python dependencies.

If your system reports an `externally-managed-environment` error, create a virtual environment instead (install `python3-venv` first if needed):

```bash
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install python-pptx
```

Create the virtual environment from the repository's main directory. Whenever you want to run the presentation script, activate it again with `source .venv/bin/activate`.

You only need to install the package once. Instructions for generating the presentation are provided in the [hands-on exercises section](../README.md#hands-on-exercises).

---

[Back to the main page](../README.md)
