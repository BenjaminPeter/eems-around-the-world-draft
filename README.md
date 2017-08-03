# EEMS-AROUND-THE-WORLD

## Goal
This is a workflow that allows easily using a number of population
structure analysis tools, with the goal to streamline workflows that 
allow easy comparison between methods and approaches. The original reason
was to compare EEMS with other methods.

The ultimate goal is to be able to use a comand of the form
```snakemake figures/pca/2d/europe0_pc1.png
```

to *automatically and reproducibly* create a figure of a 2D-pca plot 
for a subset of the data
called "europe0", with sensible choices for display; the command
```snakemake all_subsets_pca
```
to generate pca-plots for all defined subsets of the data,
and e.g.

```snakemake figures/pca/2d/poster/europe0_pc1.png
```
to automatically generate a version appropriate for a poster.

The first two
commands
are currently implemented, (and will automatically create the subset, do some
basic QC, run PCA and plot the result).

## Repo Overview
- the `Snakefile` is the main file that is used to call all analyses
- `sfiles/` contains rules for specific tools. `sfiles/pca.snake`, for
example, controlls input formatting, managing options, running and plotting
for PCA plots, `sfiles/eems.snake` does the same for EEMS.
- `scripts/` contains scripts that are called from rules specified in `sfiles`.
- `config/` contains the configuration files that specify the analyses. 
- `subsetter` contains a python module that handles subsetting data. This is
currently done using plink, but another tool (e.g. vcftools or angst) could possibly 
be developed.

Thus, ideally a user of the pipeline would only need to change some config 
files, whereas a developer of a new method would need to write rules 
(in sfiles/) and modify the Snakefile to link this file. This modular approach
has the advantage that the developer has full freedom of how he wants to 
implement his approach, as long as he specifies the files required, and the
files generated.



## Implemented methods
These methods are all implemented in various degrees of completeness. EEMS,
flashpca are well implemented, admixture and pong are as well, with the caveat
that the ordering of samples is at times strange.
- [EEMS](http://github.com/dipetkov/eems)
- [flashpca](https://github.com/gabraham/flashpca)
- [admixture](https://www.genetics.ucla.edu/software/admixture/)
- [pong](https://pypi.python.org/pypi/pong) visualization of admixture
- [TESS3](https://github.com/cayek/TESS3/)
- [treemix](https://bitbucket.org/nygcresearch/treemix/wiki/Home)
- [Spacemix](https://github.com/gbradburd/SpaceMix)
- FST

## Config file details
- `cluster.yaml` contains job-specific info for cluster resources
- `config.yaml` contains data and server specific info, in particular
paths to the data and executables 
- `subset.yaml` contains info for subsets, i.e. which samples should be 
included in a run
- `eems.yaml` contains specification for different types of eems runs
- `plots.yaml` contains info about options for different EEMS plots

The major limitation of the repo currently is that all the options are
undocumented and will therefore be unusable without digging through the files.


## Implementation
Genotypic data is stored in [plink](https://www.cog-genomics.org/plink2) format.
Metadata/location data is stored using John Novembre's
[PopGenStructures](https://docs.google.com/document/d/1wPlI1hLr19JIdM2EzYKlPnzzbR6L2ZOgOGkC6kbhHE4/edit)
data format, with some minor (recommended) changes.
The pipeline is implemented using [Snakemake](https://bitbucket.org/snakemake),
using `python` for most data wrangling and `R` for most plotting

## Status
This is a draft intended at showcasing the intended structure of the project.
This is **NOT** a working version (as the version I use handles sensitive data,
I cannot just push it to github).

