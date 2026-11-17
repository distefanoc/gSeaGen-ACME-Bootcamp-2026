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

The gSeaGen container is available on [Zenodo](https://zenodo.org/).

The version used during the hands-on sessions is specified in the `setup.sh` configuration file provided in this repository.

The container is several gigabytes in size, so the download may take some time depending on your internet connection.

### 2.1 Load the configuration

Make sure you are in your working directory and that the `setup.sh` file is available.

Load the configuration:

```bash
source setup.sh
```

Check the selected gSeaGen version:

```bash
echo $GSEAGEN_VERSION
```

### 2.2 Download the container

You can download the container using one of the following methods.

#### Option A – Using curl (recommended)

```bash
curl -L --fail -o "$CONTAINER" "$CONTAINER_URL"
```

#### Option B – Using wget

```bash
wget -O "$CONTAINER" "$CONTAINER_URL"
```

#### Option C – Using a web browser

If neither `curl` nor `wget` is available on your system, simply download the container using your web browser.

To obtain the Zenodo page URL, run:

```bash
echo $ZENODO_URL
```

Open the displayed URL in your web browser, download the container file and move it to your working directory.

### 2.3 Check the downloaded file

Once the download is complete, check that the file is present:

```bash
ls -lh "$CONTAINER"
```

### 2.4 Verify the file integrity (optional)

You can verify the integrity of the downloaded file by computing its MD5 checksum.

On Linux, including Lima and WSL2:

```bash
md5sum "$CONTAINER"
```

If you are working directly from a macOS terminal:

```bash
md5 "$CONTAINER"
```

Compare the result with the expected MD5 checksum:

```bash
echo $CONTAINER_MD5
```

If the checksums do not match, the file may be corrupted or incomplete and should be downloaded again.

**You only need to download the container once.**

## 3. Test gSeaGen

Make sure you are in your working directory and that the configuration has been loaded:

```bash
source setup.sh
```

To check that gSeaGen runs correctly, execute:

```bash
apptainer exec "$CONTAINER" gSeaNuEvGen --help
```

You should see the gSeaGen banner followed by the list of available command-line options.

If the command runs successfully, your gSeaGen container is ready to use.

## 4. Test ROOT and PyROOT

The gSeaGen container includes ROOT and PyROOT, which will be used to analyse the simulation output during the hands-on sessions.

### 4.1 Test ROOT

Start ROOT inside the container:

```bash
apptainer exec "$CONTAINER" root -l
```

At the ROOT prompt, enter:

```cpp
auto c = new TCanvas("c", "ROOT test", 800, 600);
auto h = new TH1D("h", "ROOT test", 100, -4, 4);
h->FillRandom("gaus", 10000);
h->Draw();
```

A graphical window displaying a Gaussian distribution should appear.

To exit ROOT, type:

```cpp
.q
```

### 4.2 Test PyROOT

Start Python inside the container:

```bash
apptainer exec "$CONTAINER" python3
```

At the Python prompt, enter:

```python
import ROOT
print(ROOT.gROOT.GetVersion())

c = ROOT.TCanvas("c", "PyROOT test", 800, 600)
h = ROOT.TH1D("h", "PyROOT test", 100, -4, 4)
h.FillRandom("gaus", 10000)
h.Draw()
c.Update()
```

A graphical window displaying a Gaussian distribution should appear.

Save the plot as a PNG file:

```python
c.SaveAs("test_pyroot.png")
```

Exit Python:

```python
exit()
```

Check that the output file has been created in your working directory:

```bash
ls -lh test_pyroot.png
```

If both tests are successful, ROOT and PyROOT are ready to use.

## 5. Run a test simulation

*To be completed.*

## 6. Check the simulation output

*To be completed.*

---

[Back to the main page](../README.md)
