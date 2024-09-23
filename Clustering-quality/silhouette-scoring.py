# This file is for the analysis of the quality of clustering given different types and number of questions 
# We consider yes and no questions, integer type questions and slider questions (continuous rating scale)

from k_means_constrained import KMeansConstrained
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import copy
from sklearn.metrics import silhouette_score

def main(df):

    df_numeric = df.replace({'Yes': 5, 'No': 1}, inplace=False)
    df_allocations = copy.deepcopy(df)
    headers = list(df.columns)
    survey_questions = headers[1:]

    preferences = df_numeric[survey_questions].values
    X = preferences

    # Apply Constrained K-Means Clustering
    clusters = KMeansConstrained(
        n_clusters=8,
        size_min=8,
        size_max=12,
        random_state=0
    )
    predict = clusters.fit_predict(X) + 1
    centers = clusters.cluster_centers_
    labels = clusters.labels_ + 1
    df_allocations['Flat Allocation'] = labels

    # Calculate Silhouette Score
    silhouette_avg = silhouette_score(X, clusters.labels_)
    print(f'Silhouette Score: {silhouette_avg}')
    
    # Output predictions and allocations
    print("The students are allocated to the following flats:")
    print(predict)

###

# Silhouette scoring results for yes-and-no questions: 
dfyn4 = pd.read_csv('toydatayn4.csv')
print("A four-question yes or no questionnaire gets the following results: ")
main(dfyn4)
dfyn3 = pd.read_csv('toydatayn3.csv')
print("A three-question yes or no questionnaire gets the following results: ")
main(dfyn3)
dfyn2 = pd.read_csv('toydatayn2.csv')
print("A two-question yes or no questionnaire gets the following results: ")
main(dfyn2)

# It is observable that the 3-dimensional y/n survey gets the best score in the y/n surveys. This is because 4dim suffers from the curse of dimensionality, and the 2dim is not enough to capture different enough personalities and hence leads to poor clustering 
# We now have integer type questions:
dfint3= pd.read_csv('toydata3int.csv')
print("A three-question integer response (1 to 5) questionnaire gets the following results: ")
main(dfint3)
dfint2= pd.read_csv('toydata2int.csv')
print("A two-question integer response (1 to 5) questionnaire gets the following results: ")
main(dfint2)
dfint1= pd.read_csv('toydata1int.csv')
print("A one-question integer response (1 to 5) questionnaire gets the following results: ")
main(dfint1)

# Slider questions: 
dfnum3= pd.read_csv('toydatanum3.csv')
print("A three-question slider scale (1 to 5) questionnaire gets the following results: ")
main(dfnum3)
dfnum2= pd.read_csv('toydatanum2.csv')
print("A two-question slider scale (1 to 5) questionnaire gets the following results: ")
main(dfnum2)
dfnum1= pd.read_csv('toydatanum1.csv')
print("A one-question slider scale (1 to 5) questionnaire gets the following results: ")
main(dfnum1)

# Clearly, the 3 question y/n questionnaire still gives us the best results. This is due to the expected number of people per flat being 10, and the total number of people being 80.
# 8 different "personality types" are obtained with the 3 y/n questionnaire. This allows the best clustering as one flat getting a single "type" of person aligns with the expected value