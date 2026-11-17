# Installing Apptainer on Linux

Apptainer runs natively on Linux. No virtual machine is required.

The gSeaGen container provided for the hands-on sessions is built for the x86_64 architecture.

## 1. Check your system architecture

Open a terminal and run:

```bash
uname -m
```

The expected output is:

```text
x86_64
```

If your system uses a different architecture, please contact us before proceeding.

## 2. Check whether Apptainer is already installed

```bash
apptainer --version
```

If Apptainer is already installed, skip to Section 4.

## 3. Install Apptainer

### Ubuntu

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:apptainer/ppa
sudo apt update
sudo apt install -y apptainer
```

### Fedora

```bash
sudo dnf install -y apptainer
```

### Rocky Linux / AlmaLinux

```bash
sudo dnf install -y epel-release
sudo dnf install -y apptainer
```

For other Linux distributions, please refer to the [official Apptainer installation guide](https://apptainer.org/docs/admin/latest/installation.html).

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

## 5. Download and test gSeaGen

Once Apptainer is working, proceed to the [gSeaGen setup instructions](gSeaGen.md).

---

[Back to the main page](../README.md)
