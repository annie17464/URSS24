# This file plots the clusters formed when k-means-constrained is applied to data based on the 3-dimensional yes/no questionnaire. 
# We first cluster the data and then apply principal component analysis to reduce our dimension to 2 in order to plot data for visualization. 

from k_means_constrained import KMeansConstrained
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import numpy as np

# to standardize data 
from sklearn.preprocessing import StandardScaler

# to visualise 
import seaborn as sns
import matplotlib.pyplot as plt

df = pandas.read_csv('toydatayn3.csv')
df_numeric = df.replace({'Yes': 5, 'No': 1}, inplace= False)

features= ['Social', 'Quiet hours', 'Shared Bathrooms']
x= df_numeric.loc[:, features].values
x= StandardScaler().fit_transform(x)
from sklearn.decomposition import PCA
# we want 2 components in this visualization, so we choose n_components=2 
pca= PCA(n_components=2)

headers= list(df_numeric.columns)
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

principalComponents= pca.fit_transform(x)
principalDf= pandas.DataFrame(data= principalComponents, columns= ['Principal Component 1', 'Principal Component 2'])
principalDf['Flat Allocation'] = labels

# This data is binary in each dimension, and thus a lot of the points lie on top of each other. To visualise the clusters, we add random noise and jitter the points
principalDf['Principal Component 1'] += np.random.normal(0, 0.2, size=principalDf['Principal Component 1'].shape)
principalDf['Principal Component 2'] += np.random.normal(0, 0.2, size=principalDf['Principal Component 2'].shape)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=principalDf, x='Principal Component 1', y='Principal Component 2', hue='Flat Allocation', palette='Set1', s= 80)
plt.title('Scatter plot of students with colours representing different flats')
plt.show()