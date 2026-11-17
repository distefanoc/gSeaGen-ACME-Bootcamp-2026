# Downloading and testing gSeaGen

These instructions apply to all operating systems once Apptainer has been successfully installed.

We will use gSeaGen distributed as an Apptainer container that includes GENIE, ROOT, PyROOT and all the required dependencies.

The gSeaGen version used during the hands-on sessions is specified in the `setup.sh` configuration file provided in this repository.

## 1. Working directory

### 1.1 Open a terminal

- **Linux:** Open a terminal.
- **macOS:** Connect to your Lima virtual machine using SSH with X11 forwarding, as described in the [macOS setup instructions](macOS.md).
- **Windows:** Open the Ubuntu terminal.

### 1.2 Create your working directory

On Linux and Windows:

```bash
mkdir -p ~/gseagen
cd ~/gseagen
```

On macOS, access the shared working directory created during the setup:

```bash
cd /Users/<your-mac-username>/gseagen
```

### 1.3 Download the hands-on material

Download this GitHub repository using the **Code → Download ZIP** option on the [main repository page](../README.md).

Extract the archive and copy its contents into your working directory.

### 1.4 Create the output directories

From your working directory, run:

```bash
mkdir -p files plots
```

The working directory will have the following structure:

```text
gseagen/
├── README.md
├── setup.sh
├── setup/
├── scripts/
├── files/
└── plots/
```

- `setup.sh`: gSeaGen release configuration.
- `setup/`: installation and setup instructions.
- `scripts/`: simulation and analysis scripts.
- `files/`: simulation output files.
- `plots/`: plots produced during the analysis.

The gSeaGen container will also be stored in the main working directory.

**Always execute the simulation and analysis commands from the main working directory, not from the scripts directory.**

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
c.SaveAs("plots/test_pyroot.png")
```

Exit Python:

```python
exit()
```

Check that the output file has been created in your working directory:

```bash
ls -lh plots/test_pyroot.png
```

If both tests are successful, ROOT and PyROOT are ready to use.

## 5. Run a test simulation

We will now run a short simulation to verify that gSeaGen and all its dependencies work correctly.

The simulation generates muon neutrinos with energies between 100 GeV and 1 PeV, using charged-current interactions.

From your working directory, run:

```bash
bash scripts/run_test.sh
```

The script generates 1000 neutrinos and saves the simulation output in the `files/` directory.

Once the simulation is complete, check the output files:

```bash
ls -lh files/test*
```

You should find the following files:

```text
files/test.1.binstat
files/test.1.et.root
files/test.1.geo-mu.root
```

The main simulation output is `files/test.1.et.root`, which contains the simulated events and the generation parameters.

We will use this file to test the analysis in the next section.

## 6. Check the simulation output

We will now analyse the simulation output using PyROOT.

Make sure you are in your working directory and that the configuration has been loaded:

```bash
source setup.sh
```

Run the analysis script:

```bash
apptainer exec "$CONTAINER" python3 -i scripts/plot_neutrino.py files/test.1.et.root
```

The script reads the simulation output and produces both unweighted and weighted distributions of the neutrino energy and the cosine of the neutrino zenith angle.

Two graphical windows should appear, and the corresponding plots will be saved in the `plots/` directory:

```text
plots/test.1_nu_energy.png
plots/test.1_nu_costheta.png
```

The script also prints the generation parameters and the integrated results. For example:

```text
Generation parameters:
  Mean number of neutrinos to simulate: 1000
  Energy range: 1.00e+02 - 1.00e+06 GeV
  Cosine of zenith range: -1.0 - 1.0
  Number of energy bins: 1
  Number of saved events: 47
Total MC events: 47
Total event rate: 2.7024e-06 Hz
Expected events per year: 85.28
```

The output shown above is an example. The number of saved events and the estimated event rate may differ from the values reported here.

To exit Python, type:

```python
exit()
```

Check that the plots have been created:

```bash
ls -lh plots/test*
```

### Verify the generation statistics

You can check the generation statistics by inspecting the `.binstat` file:

```bash
cat files/test.1.binstat
```

Check the following columns:

- `NEvBin`: mean number of neutrinos to be simulated in the energy bin, used for event weight normalisation.
- `NEvBinScal`: actual number of simulated neutrinos, obtained by applying a Poisson fluctuation to `NEvBin` to account for statistical fluctuations.
- `NEvBinGen`: number of events accepted and saved in the output file.

The value of `NEvBinGen` should match both `Number of saved events` and `Total MC events` printed by the analysis script.

**Congratulations! If all the tests have been completed successfully, your software environment is ready for the hands-on sessions.**

---

[Back to the main page](../README.md)

