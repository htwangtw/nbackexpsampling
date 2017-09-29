# Two Force Choice N-back Paradigm
Based on the task developed by Konish et al., I am working on a enhanced verison of the task.
The task uses a n-back memory paradigm intending to induce mind-wandering.

Reference:

Konishi, M., McLaren, D. G., Engen, H., & Smallwood, J. (2015). Shaped by the past: the default mode network supports cognition that is independent of immediate perceptual input. PloS One, 10(6), e0132209. http://doi.org/10.1371/journal.pone.0132209



Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── settings.py        <- Enviromnetal setting of the task.
    ├── run.py             <- The main experiment program.   
    ├── examples           <- Examples.
    ├── instructions       <- Instructions .txt files. '#' used as page breaker   
    ├── data               <- Data generated from the task. Read-only.
    ├── parameters         <- Trial generation specification files.
    ├── references         <- Manuals, plans for this experiemnt
    ├── src                <- Source code for use in this project.
    │   │
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── datastructure  <- Scripts to generate trials
    │   │    ├── __init__.py 
    │   │    ├── datastructure.py 
    │   │    ├── stimulus.py 
    │   │    └── trialtype.py
    │   │
    │   ├── experiment.py  <- experiment deatails
    │   └── fileIO.py      <- file input/output
    │   
    └── stimuli            <- stimulus photos

