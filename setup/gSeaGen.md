# Downloading and testing gSeaGen

These instructions apply to all operating systems once Apptainer has been successfully installed.

We will use **gSeaGen v7.7.1**, distributed as an Apptainer container that includes GENIE, ROOT, PyROOT and all the required dependencies.

## 1. Working directory

- **Linux:** Open a terminal.
- **macOS:** Connect to your Lima virtual machine using SSH with X11 forwarding, as described in the [macOS setup instructions](macOS.md).
- **Windows:** Open the Ubuntu terminal.

On Linux and Windows, create and enter your working directory:

```bash
mkdir -p ~/gseagen
cd ~/gseagen
```

On macOS, access the shared working directory created during the setup:

```bash
cd /Users/<your-mac-username>/gseagen
```

## 2. Download the gSeaGen container

The container file `gseagen_open_v7.7.1.sif` is available on [Zenodo – gSeaGen v7.7.1](https://doi.org/10.5281/zenodo.24232207).

The container is approximately **4.1 GB** in size, so the download may take some time depending on your internet connection.

Make sure you are in your working directory before proceeding.

You can download the container using one of the following methods.

### Option A – Using curl (recommended)

```bash
curl -L --fail -o gseagen_open_v7.7.1.sif \
    "https://zenodo.org/records/24232207/files/gseagen_open_v7.7.1.sif?download=1"
```

### Option B – Using wget

```bash
wget -O gseagen_open_v7.7.1.sif \
    "https://zenodo.org/records/24232207/files/gseagen_open_v7.7.1.sif?download=1"
```

### Option C – Using a web browser

If neither `curl` nor `wget` is available on your system, simply open the [Zenodo page](https://doi.org/10.5281/zenodo.24232207) in your web browser and download the file `gseagen_open_v7.7.1.sif`.

Move the downloaded file to your working directory.

### Check the downloaded file

Once the download is complete, check that the file is present:

```bash
ls -lh gseagen_open_v7.7.1.sif
```

### Verify the file integrity (optional)

You can verify the integrity of the downloaded file by computing its MD5 checksum.

On Linux, including Lima and WSL2:

```bash
md5sum gseagen_open_v7.7.1.sif
```

If you are working directly from a macOS terminal:

```bash
md5 gseagen_open_v7.7.1.sif
```

The expected MD5 checksum is:

```text
78a42495dbc5b42eb1aa83cb04bc7a84
```

If the checksum does not match, the file may be corrupted or incomplete and should be downloaded again.

**You only need to download the container once.**

## 3. Test gSeaGen

*To be completed.*

## 4. Test ROOT and PyROOT

*To be completed.*

## 5. Run a test simulation

*To be completed.*

## 6. Check the simulation output

*To be completed.*

---

[Back to the main page](../README.md)
