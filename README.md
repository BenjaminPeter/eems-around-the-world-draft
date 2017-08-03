# EEMS-AROUND-THE-WORLD

## Goal
This is a workflow that allows easily using a number of population
structure analysis tools, with the goal to streamline workflows that 
allow easy comparison between methods and approaches. The original reason
was to compare EEMS with other methods.

## Implemented methods
- [EEMS](http://github.com/dipetkov/eems)
- [flashpca](https://github.com/gabraham/flashpca)
- [admixture](https://www.genetics.ucla.edu/software/admixture/)
- [pong](https://pypi.python.org/pypi/pong) visualization of admixture
- [TESS3](https://github.com/cayek/TESS3/)
- [treemix](https://bitbucket.org/nygcresearch/treemix/wiki/Home)
- [Spacemix](https://github.com/gbradburd/SpaceMix)
- FST


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

However, the relevant bit is the following:
the folder `sfiles/` contains rules for specific tools. `sfiles/pca.snake`, for
example, controlls input formatting, managing options, running and plotting
for PCA plots, `sfiles/eems.snake` does the same for EEMS.
