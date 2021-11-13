import pandas as pd



matches = pd.read_csv("matches.csv")
matches.head()

deliveries = pd.read_csv("deliveries.csv")
deliveries.head()

"""
# Initial PreProcessing
>Umpire 3 has too many NULL values
>Pune's team has 2 names for the same entity
>Change of Name of City: Bangalore --> Bengaluru
"""

matches.drop('umpire3', axis=1, inplace=True)
matches.replace( 'Rising Pune Supergiant', 'Rising Pune Supergiants',inplace = True)
matches.replace( 'Bengaluru', 'Bangalore',inplace = True)

player_data = pd.read_csv("DIM_PLAYER.csv")
player_data=player_data.drop(["PLAYER_SK", "Player_Id", "DOB","Bowling_skill"], axis=1)
print(player_data.head())

matches = deliveries.groupby(by='batsman', as_index=False).agg({'match_id': pd.Series.nunique})


# Aggregate Functions result in missing columns
# Additional steps with Join to circumvent this issue
# batsman_score = pd.DataFrame(deliveries.groupby('batsman').agg({'batsman_runs' : 'sum', 'ball':'count'}))
runs = pd.DataFrame(deliveries.groupby(['batsman'], as_index=False, sort=False)['batsman_runs'].sum())
balls = pd.DataFrame(deliveries.groupby(['batsman'], as_index=False, sort=False)['ball'].count())
batsman_score = pd.merge(runs, balls, on='batsman', how='inner')

no_match = deliveries.groupby(by='batsman', as_index=False).agg({'match_id': pd.Series.nunique})
no_match.rename(columns={'match_id':'Matches_batted'}, inplace=True)
batsman_score = pd.merge(batsman_score, no_match, on='batsman', how='inner'

batsman_score['Strike_Rate'] = ((batsman_score['batsman_runs'])/batsman_score['ball'])*100
batsman_score['Avg_run_per_match'] = ((batsman_score['batsman_runs'])/batsman_score['Matches_batted'])

# Inner Join to get a differnt data set to get Bowling Style
batsman_score.rename(columns={'batsman':'Player_Name'}, inplace=True)
batsman_score = pd.merge(player_data, batsman_score, on='Player_Name', how='inner')
print(batsman_score.columns)



boundaries4 = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
boundaries4.rename(columns={'batsman':'Player_Name'}, inplace=True)
boundaries4.rename(columns={'batsman_runs':'No_of_4'}, inplace=True)
print(boundaries4.head())

#Bounaries and other Parameters
boundaries6 = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==6).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
boundaries6.rename(columns={'batsman':'Player_Name'}, inplace=True)
boundaries6.rename(columns={'batsman_runs':'No_of_6'}, inplace=True)
print(boundaries6.head())



dotballs = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
dotballs.rename(columns={'batsman':'Player_Name'}, inplace=True)
dotballs.rename(columns={'batsman_runs':'Percent_dot_balls'}, inplace=True)


batsman_score = pd.merge(boundaries4, batsman_score, on='Player_Name', how='inner')
batsman_score = pd.merge(boundaries6, batsman_score, on='Player_Name', how='inner')
batsman_score = pd.merge(dotballs, batsman_score, on='Player_Name', how='inner')

batsman_score['Percent_dot_balls'] = (batsman_score['Percent_dot_balls'] / batsman_score['ball'])
batsman_score['No_of_4'] = (batsman_score['No_of_4'] / batsman_score['Matches_batted'])
batsman_score['No_of_6'] = (batsman_score['No_of_6'] / batsman_score['Matches_batted'])

print(batsman_score.columns)

#print(batsman_score.loc[batsman_score['Avg_run_per_match'].idxmax()])

#Changing Column Names to better Represent
#batsman_score.rename(columns={'batsman_runs':'Runs_Conceded'}, inplace=True)

#batsman_score.to_csv('NewBowl.csv')