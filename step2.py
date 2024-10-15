# this file contains the solution for the second step of the problem, the flat clustering, through k means constrained. 

from k_means_constrained import KMeansConstrained
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import copy

blockdata = pandas.read_csv('preliminary_accommodations.csv')
df = pandas.read_csv('flatcluster.csv')

students_in_block = {f'b{i+1}': 0 for i in range(6)}
block_indices = {f'b{i+1}': [] for i in range(6)}

for index, row in blockdata.iterrows():
    block = row['Preliminary Accommodation']
    if block in block_indices:
        block_indices[block].append(index)
        students_in_block[block] += 1

print("Students in each block:")
for block, count in students_in_block.items():
    print(f"{block}: {count}")


df_numeric = df.replace({'Yes': 5, 'No': 1}, inplace=False)
df_allocations = copy.deepcopy(df)
headers = list(df.columns)
survey_questions = headers[1:]

df_allocations['Block'] = None

# Perform clustering on each block
for block, indices in block_indices.items():
    if indices:  # Check if the block has any students
        # Extract the subset of df_numeric for the current block
        df_allocations.loc[indices, 'Block'] = block
        block_data = df_numeric.iloc[indices]
        preferences = block_data[survey_questions].values
        num_students = len(indices)
        num_clusters = max(1, round(num_students / 10))  # Ensure at least 1 cluster
        
        # Apply KMeansClustering to this block
        clusters = KMeansConstrained(
            n_clusters=num_clusters,
            size_min=8,
            size_max=12,
            random_state=0
        )
        predict = clusters.fit_predict(preferences) + 1
        centers = clusters.cluster_centers_
        labels = clusters.labels_ + 1
        
        print(f"\nCluster predictions for {block}:")
        print(predict)
        
        # Add the cluster labels to the df_allocations DataFrame
        df_allocations.loc[indices, 'Flat Allocation'] = labels

print(df_allocations)