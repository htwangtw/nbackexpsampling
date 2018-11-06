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
    ├── example_trial_generator.py
    |                      <- The example of the trial generator.
    ├── instructions       <- Instructions .txt files.
    ├── data               <- Data generated from the task. Read-only.
    ├── parameters         <- Trial generation specification files.
    ├── src                <- Source code for use in this project.
    └── stimuli            <- stimulus photos and experience sampling questions


## Dependency
The current version was tested on:
Python 2.7.15
Psychopy 1.85.6

## Running the task
Execute run.py


## Modifying experience sampling questions

Change the questions/scales/lable in `stimuli/ES_questions.csv`.
Please leave the headers untouch.

## Modifying instructions
'#' is used as page breaker. 
The text in between curly breackates {} changes in the experiment. Please do not modify the text inside the breakets.

## Modifying MRI related setting
This script supports the buttom boxes set-up in York Neuroimaging Centre.
The two buttom boxes are mapped to number 1 to 4 and 6 to 9 on a regular keyboard.
Number 5 is linked to MRI trigger setting.

If your neuroimaging centre uses the same set up, there's no need to modify the code.
If you use parallel port, please contact your local support to find out the setting and modify the code yourself.

The dummy volumes are accounted for in the scanner used at York.
If you require manual set up, please modify the variable in `run.py` accordingly.


