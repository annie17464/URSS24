# Application of Clustering Methods to the Student Experience of Accommodation.
2023/24 Undergraduate Research Support Scheme  - The University of Warwick

This repository allocates a set of students to suitable accommodation from preference data using matching algorithms and clustering methods in the following order: 

1. Block Allocation: allocate students to a 'preliminary accommodation' based on their ranking of accommodations using different matching and probabilistic algorithms for comparison. 

2. Flat Allocation: Further segment students within each block into smaller 'flats' by clustering based on student profile data (e.g., social preferences, sleep schedules, etc.).


## Directory structure

The repository content is organized in the following directories:

- `Matching-algorithms/`: hosts the code of the matching algorithms 'Stable Marriage' (UserSM), 'Maximum Matching' (UserA1) and 'Hungarian' (UserHungarian)

- `Variance-demo/`: directory hosts code and toy data to analyse incorporating variance into a flat by filtering students by an attribute. 

- `Clustering-Visualisation/`: hosts toy data based on two different questionnaires and code clustering this data (using k-means) into 'flats' and plots these to provide visual intuition.  

- `Clustering-quality/`: hosts toy data having different types and number of questions, and code clustering it (using k-means), and reports quality of clustering using silhoutte scoring for analysis. 

## Loose Files

- `weighted_b_matching.py`: File containing the code for the weighted-b-matching algorithm. 

- `flatpref.csv`: File containing the student preferences required for step 1 (allocation to blocks).  

- `flatcluster.csv`: File containing the student profile data to required for step 2 (clustering to flats).  

- `README.md`

- `requirements.txt`: File outlining the libraries and packages required for this project. 

Step 1: 

- `RSD.py`: File containing the first step as done by Random Serial Dictatorship. 

- `PS.py`: File containing the first step as done by Probabilistic Serial Mechanism. 

- `Hungarian_step1.py`: File containing the first step as done by the Hungarian algorithm. 

- `WbBM_step1.py`: File containing the first step as done by the Weighted-B-Matching algorithm. 

Step 2: 

- `step2.py`: File containing the second step as done by the constrained k-means algorithm. 


## Requirements

Python 3.11

All libraries and packages from 'requirements.txt' file

It is recommended to create a virtual environment in which to install the above dependencies.

## Installation and Running

1. Create a virtual environment (must have python3 already installed on the computer):

 <code> python3 -m venv environment_name</code>

2. Activate the virtual environment:

<code>  source environment_name/bin/activate</code>

3. Install the required libraries and packages from requirements.txt file using PIP (must install if you do not have):

<code>  pip install -r requirements.txt </code>

1. From command line, go to the directory of the required folder:

<code> cd file_path/folder </code>

5. Run the code ("code" in example here)

<code>  environment_name/bin/python3.11 "code" </code>


## Contributors

Main contributor: Ananya Garg 

Supervisor: Dr Martyn Parker