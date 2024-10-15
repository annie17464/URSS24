# This file plots the clusters formed when k-means-constrained is applied to data based on the 2-dimensional slider type (1 to 5) questionnaire. 

from k_means_constrained import KMeansConstrained
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import copy

# to visualise 
import seaborn as sns
import matplotlib.pyplot as plt

df = pandas.read_csv('toydata2dim.csv')
df_numeric = df.replace({'Yes': 5, 'No': 1}, inplace= False)
df_allocations = copy.deepcopy(df)
headers= list(df.columns)
survey_questions= headers[1:]
print(df)
print(headers[1:])
preferences = df_numeric[survey_questions].values
X=preferences

clusters = KMeansConstrained(
     n_clusters=8,
     size_min=8,
     size_max=12,
     random_state=0
 )
predict= clusters.fit_predict(X) + 1
centers= clusters.cluster_centers_
labels= clusters.labels_ + 1
print(predict)
df_allocations['Flat Allocation']= labels
print(df_allocations)


# Plotting
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_allocations, x='Social', y='Quiet hours', hue='Flat Allocation', palette='Set1')
plt.title('Scatter plot of students with colours representing different flats')
plt.show()