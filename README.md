# Two Force Choice N-back Paradigm

Features:
    Stand-alone trial generator
    
    Three condtions: 1-back, 0-back, recognition
    
    New project structure!

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

