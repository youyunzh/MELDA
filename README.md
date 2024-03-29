**Automatic Summarization System for LING573 Sp19**<br>
June 10, 2019

MELDA is a summarization system based on MEAD with content selection boosted by LDA topic modeling. The final version of MELDA incorporates information ordering and content realization modules. The final report is `doc/D4.pdf` and its presentation slides is `doc/D4_slides.pdf`.

MELDA can be run by executing `run_all.sh` from inside `src/`, either directly or by submitting `D4.cmd` to Condor. 
It is run with default parameters: 3 topics, 5 sentences per topic, MEAD score weights: 1, 1, 1; Brown Corpus (from NLTK) for IDF score; max threshhold value; and information ordering led by top MEAD score.

Additionally we include two baseline systems - Lead Sentence (hereafter LEAD) and MEAD, which are also run by executing `run_all.sh` from inside `src/`. In order to run MEAD or LEAD, the corresponding lines in `run_all.sh` script must be uncommented. The lines include flags for the version parameters: 'mead' for MEAD and 'lead for LEAD. (The other parameters for MEAD are the parallel parameters for MELDA: MEAD score weights: 1, 1, 1; Brown Corpus (from NLTK) for IDF score; max threshhold value; and information ordering led by top MEAD score.)


**Developers:**<br>
Claude Zhang<br>
Julia McAnallen<br>
Genevieve Peaslee<br>
Zoe Winkworth<br>
