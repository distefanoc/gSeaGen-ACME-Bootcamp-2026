# Installing Apptainer on macOS

Apptainer requires a Linux environment. On macOS, we will use [Lima](https://lima-vm.io/), which provides a lightweight Linux virtual machine.

The installation procedure depends on your Mac processor.

## 1. Check your system architecture

Open a terminal and run:

```bash
uname -m
```

- `x86_64`: Intel processor.
- `arm64`: Apple Silicon processor (M1, M2, M3, etc.).

## 2. Install Homebrew and Lima

If Homebrew is not already installed, follow the instructions at [https://brew.sh/](https://brew.sh/).

Install Lima:

```bash
brew install lima
```

Check the installation:

```bash
limactl --version
```

## 3. Create a Linux virtual machine

Follow **only one** of the two procedures below, depending on your processor.

### 3.1 Intel Macs

Create a Linux virtual machine with Apptainer already installed:

```bash
limactl start --name=apptainer --mount-writable template:apptainer
```
The --mount-writable option allows the virtual machine to read and write files in the shared macOS home directory.

If prompted, proceed with the default configuration.

Enter the virtual machine:

```bash
limactl shell apptainer
```

Check that Apptainer is available:

```bash
apptainer --version
```

Test the installation:

```bash
apptainer exec docker://alpine:latest uname -m
```

The expected output is:

```text
x86_64
```

Exit the virtual machine:

```bash
exit
```

### 3.2 Apple Silicon Macs

The gSeaGen container is built for the x86_64 architecture. Rosetta allows us to run x86_64 Linux applications on Apple Silicon.

Install Rosetta:

```bash
softwareupdate --install-rosetta --agree-to-license
```

Create an Ubuntu 22.04 virtual machine with Rosetta support:

```bash
limactl start --name=apptainer2204 \
    --vm-type=vz \
    --rosetta \
    --mount-writable \
    template:ubuntu-22.04
```

If prompted, proceed with the default configuration.

Enter the virtual machine:

```bash
limactl shell apptainer2204
```

Install Apptainer inside the virtual machine:

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:apptainer/ppa
sudo apt update
sudo apt install -y apptainer
```

Check the installation:

```bash
apptainer --version
```

Download a small x86_64 test container:

```bash
apptainer pull --arch amd64 alpine_amd64.sif \
    docker://alpine:latest
```

Test its execution:

```bash
apptainer exec alpine_amd64.sif uname -m
```

The expected output is:

```text
x86_64
```

Exit the virtual machine:

```bash
exit
```

## 4. Enable graphical applications

During the hands-on sessions, we will use ROOT to analyse simulated events and produce plots.

To display graphical windows on macOS, install XQuartz:

```bash
brew install --cask xquartz
```

Alternatively, download it from [https://www.xquartz.org/](https://www.xquartz.org/).

After installation, you may need to log out and log back in to macOS.

Start XQuartz:

```bash
open -a XQuartz
```

Connect to the virtual machine using SSH with X11 forwarding.

### Intel Macs

```bash
ssh -Y -o ControlPath=none \
    -F ~/.lima/apptainer/ssh.config \
    lima-apptainer
```

### Apple Silicon Macs

```bash
ssh -Y -o ControlPath=none \
    -F ~/.lima/apptainer2204/ssh.config \
    lima-apptainer2204
```

Inside the virtual machine, check that X11 forwarding is enabled:

```bash
echo $DISPLAY
```

The output should be similar to:

```text
localhost:10.0
```

## 5. Create a working directory

We recommend keeping the hands-on files in a directory shared between macOS and the Linux virtual machine.

Open a macOS terminal and create a directory:

```bash
mkdir -p ~/gseagen
```

From inside the virtual machine, access the same directory:

```bash
cd /Users/<your-mac-username>/gseagen
```

Replace `<your-mac-username>` with your macOS username.

## 6. Download and test gSeaGen

From inside the Linux virtual machine, proceed to the [gSeaGen setup instructions](gSeaGen.md).

## 7. Managing the virtual machine

The following commands must be executed from a macOS terminal, outside the virtual machine.

List the available virtual machines and their status:

```bash
limactl list
```

### Intel Macs

Start the virtual machine:

```bash
limactl start apptainer
```

Stop the virtual machine:

```bash
limactl stop apptainer
```

### Apple Silicon Macs

Start the virtual machine:

```bash
limactl start apptainer2204
```

Stop the virtual machine:

```bash
limactl stop apptainer2204
```

The virtual machine does not need to be recreated each time. All installed software and files are preserved when it is stopped.

---

[Back to the main page](../README.md)
