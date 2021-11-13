from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

import pandas as pd

neighbour_count = 3

data = pd.read_csv("NewBat.csv")
data_dup = pd.read_csv("NewBat.csv")

data = data[data['ball'] >= 300]

data = data.drop(['Batting_hand','Country_Name','batsman_runs','ball','Matches_batted'], axis=1)

print("Enter Name to find Similar Player:")
inp = input()
finding = data[data['Player_Name'].str.contains(inp)]
print(finding)


data.set_index('Player_Name',inplace=True)
finding.set_index('Player_Name',inplace=True)
#data = StandardScaler().fit_transform(data)

print(data)

neigh = NearestNeighbors(n_neighbors=neighbour_count, radius=0.4)
neigh.fit(data)

ind = neigh.kneighbors(finding, 3, return_distance=False)

print("Similar Player:\n")
for i in range(neighbour_count-1):
    print(data_dup.loc[ind[0][i+1]],"\n\n")

