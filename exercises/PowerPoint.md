# Generating a PowerPoint summary

You can automatically generate a PowerPoint presentation containing the plots produced during the hands-on exercises.

First, make sure you have installed `python-pptx` by following the [installation instructions](../setup/PowerPoint.md).

From the main directory of the repository, run the following command **outside the Apptainer container**:

```bash
python3 scripts/create_summary_pptx.py
```

The script creates `gseagen_hands_on_results.pptx` in the main directory of the repository.

Only the available plots in `plots/` are included, so you can run the script at any time and rerun it as you complete more exercises.

---

[Back to the main page](../README.md#hands-on-exercises)
