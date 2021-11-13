import pandas as pd

from sklearn.neighbors import KDTree
from sklearn import preprocessing




matches = pd.read_csv("matches.csv")
matches.head()

deliveries = pd.read_csv("deliveries.csv")
deliveries.head()

targname = 'SP Narine'

deliveries = deliveries[deliveries['bowler'] == targname]

runs = pd.DataFrame(deliveries.groupby(['batsman'], as_index=False, sort=False)['batsman_runs'].sum())
balls = pd.DataFrame(deliveries.groupby(['batsman'], as_index=False, sort=False)['ball'].count())
bat_against_targ = pd.merge(runs, balls, on='batsman', how='inner')

no_match = deliveries.groupby(by='batsman', as_index=False).agg({'match_id': pd.Series.nunique})
no_match.rename(columns={'match_id':'Matches_batted'}, inplace=True)
bat_against_targ = pd.merge(bat_against_targ, no_match, on='batsman', how='inner')

bat_against_targ['Strike_Rate'] = ((bat_against_targ['batsman_runs'])/bat_against_targ['ball'])*100
bat_against_targ['Avg_run_per_match'] = ((bat_against_targ['batsman_runs'])/bat_against_targ['Matches_batted'])

# Inner Join to get a differnt data set to get Bowling Style
bat_against_targ.rename(columns={'batsman':'Player_Name'}, inplace=True)




boundaries4 = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
boundaries4.rename(columns={'batsman':'Player_Name'}, inplace=True)
boundaries4.rename(columns={'batsman_runs':'No_of_4'}, inplace=True)


#Bounaries and other Parameters
boundaries6 = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==6).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
boundaries6.rename(columns={'batsman':'Player_Name'}, inplace=True)
boundaries6.rename(columns={'batsman_runs':'No_of_6'}, inplace=True)


dotballs = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
dotballs.rename(columns={'batsman':'Player_Name'}, inplace=True)
dotballs.rename(columns={'batsman_runs':'Percent_dot_balls'}, inplace=True)


bat_against_targ = pd.merge(boundaries4, bat_against_targ, on='Player_Name', how='inner')
bat_against_targ = pd.merge(boundaries6, bat_against_targ, on='Player_Name', how='inner')
bat_against_targ = pd.merge(dotballs, bat_against_targ, on='Player_Name', how='inner')

bat_against_targ['Percent_dot_balls'] = (bat_against_targ['Percent_dot_balls'] / bat_against_targ['ball'])
bat_against_targ['No_of_4'] = (bat_against_targ['No_of_4'] / bat_against_targ['Matches_batted'])
bat_against_targ['No_of_6'] = (bat_against_targ['No_of_6'] / bat_against_targ['Matches_batted'])
bat_against_targ['percent_boundaries'] = (0.6*bat_against_targ['No_of_6'] + 0.4*bat_against_targ['No_of_4'])

print(bat_against_targ.columns)

# Finding the best player
idealPlayer = [[0,1,1,1]]
data = bat_against_targ
data = data[data['ball'] >= 30]
data.set_index('Player_Name',inplace=True)
data.reset_index(inplace=True)
data_dup = data



data = data.drop(["Player_Name", "Matches_batted", "ball", "batsman_runs","No_of_4","No_of_6"], axis=1)
data = preprocessing.normalize(data)
print(data)
tree = KDTree(data, leaf_size=3)
dist, ind = tree.query(idealPlayer, k=2)



print("Best Player:\n")
for i in range(2):
    print(data_dup.loc[ind[0][i]])
    print("Distance from Player: ", dist[0][i], "\n\n")




Best Player:

Player_Name           KL Rahul
Percent_dot_balls       0.3125
No_of_6                    1.5
No_of_4                    1.5
batsman_runs                70
ball                        32
Matches_batted               4
Strike_Rate             218.75
Avg_run_per_match         17.5
percent_boundaries         1.5
Name: 21, dtype: object
Distance from Player:  1.3539797641056206


Player_Name           CH Gayle
Percent_dot_balls     0.537037
No_of_6               0.142857
No_of_4               0.714286
batsman_runs                46
ball                        54
Matches_batted               7
Strike_Rate            85.1852
Avg_run_per_match      6.57143
percent_boundaries    0.371429
Name: 4, dtype: object
Distance from Player:  1.357742328797376
