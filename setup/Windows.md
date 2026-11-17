# Installing Apptainer on Windows

Apptainer requires a Linux environment. On Windows, we will use the Windows Subsystem for Linux (WSL2), which allows Linux applications to run on Windows.

**Note:** These instructions are based on the official Apptainer and Microsoft documentation. This setup has not been directly tested with gSeaGen by the hands-on session organisers. Please complete the installation and test gSeaGen before the school.

## 1. System requirements

- Windows 11 or Windows 10 (Build 19044 or later).
- An Intel or AMD 64-bit processor.
- Administrator privileges to install WSL2.

The gSeaGen container is built for the x86_64 architecture. If you have a Windows computer with an ARM processor, please contact us before proceeding.

## 2. Install WSL2 and Ubuntu

Open PowerShell as Administrator and run:

```powershell
wsl --install -d Ubuntu-22.04
```

Restart your computer if requested.

Open Ubuntu 22.04 from the Windows Start menu and follow the instructions to create a Linux username and password.

Check that Ubuntu is running under WSL2 by executing the following command in PowerShell:

```powershell
wsl -l -v
```

The Ubuntu distribution should have `VERSION` equal to `2`.

If WSL is already installed, make sure it is up to date:

```powershell
wsl --update
```

For further information, refer to the [official WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install).

## 3. Install Apptainer

Open the Ubuntu terminal.

Check your system architecture:

```bash
uname -m
```

The expected output is:

```text
x86_64
```

Install Apptainer:

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:apptainer/ppa
sudo apt update
sudo apt install -y apptainer
```

## 4. Test your installation

Check the installed version:

```bash
apptainer --version
```

Run a small test container:

```bash
apptainer exec docker://alpine:latest uname -m
```

The expected output is:

```text
x86_64
```

If the command runs successfully, your Apptainer installation is ready.

## 5. Graphical applications

During the hands-on sessions, we will use ROOT to analyse simulated events and produce plots.

Recent versions of WSL2 support Linux graphical applications through WSLg.

From the Ubuntu terminal, check that the DISPLAY environment variable is set:

```bash
echo $DISPLAY
```

The output should be similar to:

```text
:0
```

For further information and troubleshooting, refer to the [Microsoft guide to running Linux GUI applications with WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

## 6. Create a working directory

We recommend keeping the hands-on files in the Linux filesystem rather than in the Windows filesystem.

From the Ubuntu terminal:

```bash
mkdir -p ~/gseagen
cd ~/gseagen
```

To access this directory from Windows File Explorer, run:

```bash
explorer.exe .
```

## 7. Download and test gSeaGen

From the Ubuntu terminal, proceed to the [gSeaGen setup instructions](gSeaGen.md).

Please report any installation or execution problems before the school.

## Useful links

- [Apptainer installation guide](https://apptainer.org/docs/admin/latest/installation.html)
- [WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Linux graphical applications on Windows](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)

---

[Back to the main page](../README.md)
