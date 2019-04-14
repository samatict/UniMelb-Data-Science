
======
  
This file describes the various data files associated with Project 1 for COMP30027 Machine Learning in Semester 1 2019. References for the data files are listed in the accompanying Project specifications.

The archive contains eleven files, of which nine are data files in (approximately) CSV format, headers.txt is a text file contains the corresponding CSV headers (if you require them), and README.txt is this file.

The data files are formatted as follows:
  - one instance per line;
  - each line is comprised of a list of attribute values separated by commas --- all attributes are categorical, but no attribute value contains the comma character or any space character, and consequently are not surrounded by quotation marks;
  - the final attribute is the class of the corresponding instance.


Detailed descriptions of the various datafiles:

anneal.csv
==========
This file is derived from the Annealing dataset (https://archive.ics.uci.edu/ml/datasets/Annealing). It is comprised of 989 instances, with 35 attributes (36 including the class). Hypothetically, there are six possible class labels, however, only five are attested in the dataset: {1, 2, 3, 4, U}. Some continuous attributes were removed from the original dataset. By convention, there are no missing attribute values in this dataset.

breast-cancer.csv
=================
This file is derived from the Breast Cancer dataset (https://archive.ics.uci.edu/ml/datasets/Breast+Cancer). It is comprised of 286 instances, with 9 attributes (10 including the class). There are two possible class labels: {recurrence-events, no-recurrence-events}. There are a small number of missing values in this dataset, which are indicated by a question mark ("?").

car.csv
=======
This file is derived from the Car Evaluation dataset (https://archive.ics.uci.edu/ml/datasets/Car+Evaluation). It is comprised of 1728 instances, with 6 attributes (7 including the class). There are four possible class labels: {unacc, acc, good, vgood}. There are no missing values in this dataset.

cmc.csv
=======
This file is derived from the Contraceptive Method Choice dataset (https://archive.ics.uci.edu/ml/datasets/Contraceptive+Method+Choice). It is comprised of 1473 instances, with 8 attributes (9 including the class). There are three possible class labels: {No-use, Short-term, Long-term}. There are no missing values in this dataset.

hepatitis.csv
=============
This file is derived from the Hepatitis dataset (https://archive.ics.uci.edu/ml/datasets/Hepatitis). It is comprised of 155 instances, with 13 attributes (14 including the class). There are two possible class labels: {LIVE, DIE}. Some continuous attributes were removed from the original dataset. There are a moderate number of missing values in this dataset, which are indicated by a question mark ("?").

hypothyroid.csv
===============
This file is derived from the Thyroid Disease dataset (https://archive.ics.uci.edu/ml/datasets/Thyroid+Disease). It is comprised of 3163 instances, with 18 attributes (19 including the class). There are two possible class labels: {hypothyroid, negative}. Some continuous attributes were removed from the original dataset. There are a moderate number of missing values in this dataset, which are indicated by a question mark ("?").

mushroom.csv
============
This file is derived from the Mushroom dataset (https://archive.ics.uci.edu/ml/datasets/Mushroom). It is comprised of 8124 instances, with 22 attributes (23 including the class). There are two possible class labels: {e, p}. There are a large number of missing values in this dataset, which are indicated by a question mark ("?").

nursery.csv
===========
This file is derived from the Nursery dataset (https://archive.ics.uci.edu/ml/datasets/Nursery). It is comprised of 12960 instances, with 8 attributes (9 including the class). There are five possible class labels: {not_recom, recommend, very_recom, priority, spec_prior}. There are no missing values in this dataset.

primary-tumor.csv
=================
This file is derived from the Primary Tumor dataset (https://archive.ics.uci.edu/ml/datasets/Primary+Tumor). It is comprised of 339 instances, with 17 attributes (18 including the class). Hypothetically, there are twenty-two possible class labels, however, only twenty-one are attested in the dataset: {A, B, C, D, E, F, G, H, J, K, L, M, N, O, P, Q, R, S, T, U, V}. The class labels have been abstracted away from more meaningful labels. There are a large number of missing values in this dataset, which are indicated by a question mark ("?").
