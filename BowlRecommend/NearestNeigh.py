from sklearn.neighbors import NearestNeighbors
import pandas as pd

neighbour_count = 3

data = pd.read_csv("NewBowl.csv")
data_dup = pd.read_csv("NewBowl.csv")

data = data.drop(['Bowling_skill','Country_Name'], axis=1)

print("Enter Name to find Similar Player:")
inp = input()
finding = data[data['Player_Name'].str.contains(inp)]
print(finding)

data.set_index('Player_Name',inplace=True)
finding.set_index('Player_Name',inplace=True)

neigh = NearestNeighbors(n_neighbors=3 ,radius=0.4)
neigh.fit(data)

ind = neigh.kneighbors(finding, neighbour_count, return_distance=False)

print("Similar Player:\n")
for i in range(neighbour_count-1):
    print(data_dup.loc[ind[0][i+1]],"\n\n")
