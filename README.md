# MT-assignment2

## Introduction
Phrase-based machine translation is to build a model which memorizes multi-symbol strings, and
translates this string as a single segment. 

One target is to build a WFST. In order to get the
WFST, a previous step should be taken which is phrase extraction. In order to get those German-
English phrase pairs, we need to first get the alignments for each translation instance. To get
the alignment, ibm model is one of the appropriate choices. Therefore, it becomes clear that this
assignment can be divided into 3 main tasks: ibm model training, phrase extraction and finite
state machine creation.

## How to run:
- python phase-extract.py
- python create-phase-fst.py
- python train-model1.py
