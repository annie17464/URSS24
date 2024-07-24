from k_means_constrained import KMeansConstrained
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import copy

df = pandas.read_csv('toydata3.csv')
df_numeric = df.replace({'Yes': 5, 'No': 1}, inplace= False)
df_allocations = copy.deepcopy(df)
headers= list(df.columns)
survey_questions= headers[1:]

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