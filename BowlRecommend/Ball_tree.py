from sklearn.neighbors import NearestNeighbors,KDTree,BallTree
import pandas as pd

neighbour_count = 3

data = pd.read_csv("NewBat.csv")
data_dup = pd.read_csv("NewBat.csv")

data=data.drop(['Batting_hand', 'Country_Name'], axis=1)
print(data.head())

print("Enter Name to find Similar Player:")
inp = input()
finding = data[data['Player_Name'].str.contains(inp)]
print(finding)

data.set_index('Player_Name' , inplace=True)
finding.set_index('Player_Name',inplace=True)


model = BallTree(data, leaf_size=3, metric='minkowski')

dist, ind = model.query(finding, k=neighbour_count)

print("Similar Player:\n")
for i in range(neighbour_count-1):
    print(data_dup.loc[ind[0][i+1]])
    print("Distance from Player: ", dist[0][i+1], "\n\n")
# print(data[])

