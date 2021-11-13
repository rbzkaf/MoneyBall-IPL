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
player_data=player_data.drop(["PLAYER_SK", "Player_Id", "DOB","Batting_hand"], axis=1)
print(player_data.head())

matches = deliveries.groupby(by='bowler', as_index=False).agg({'match_id': pd.Series.nunique})


# Aggregate Functions result in missing columns
# Additional steps with Join to circumvent this issue
# bowler_score = pd.DataFrame(deliveries.groupby('bowler').agg({'batsman_runs' : 'sum', 'ball':'count'}))
runs = pd.DataFrame(deliveries.groupby(['bowler'], as_index=False, sort=False)['batsman_runs'].sum())
balls = pd.DataFrame(deliveries.groupby(['bowler'], as_index=False, sort=False)['ball'].count())
extras = pd.DataFrame(deliveries.groupby(['bowler'], as_index=False, sort=False)['extra_runs'].sum())
bowler_score = pd.merge(runs, balls, on='bowler', how='inner')
bowler_score = pd.merge(runs, balls, on='bowler', how='inner')
bowler_score = pd.merge(bowler_score, extras, on='bowler', how='inner')

no_match = deliveries.groupby(by='bowler', as_index=False).agg({'match_id': pd.Series.nunique})
no_match.rename(columns={'match_id':'Matches_bowled'}, inplace=True)
bowler_score = pd.merge(bowler_score, no_match, on='bowler', how='inner')

bowler_score['Economy_Rate'] = ((bowler_score['batsman_runs']+bowler_score['extra_runs'])/bowler_score['ball'])*6

# Inner Join to get a differnt data set to get Bowling Style
bowler_score.rename(columns={'bowler':'Player_Name'}, inplace=True)
bowler_score = pd.merge(player_data, bowler_score, on='Player_Name', how='inner')
print(bowler_score.columns)



boundaries4 = deliveries.groupby('bowler')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
boundaries4.rename(columns={'bowler':'Player_Name'}, inplace=True)
boundaries4.rename(columns={'batsman_runs':'No_of_4'}, inplace=True)
print(boundaries4.head())

#Bounaries and other Parameters
boundaries6 = deliveries.groupby('bowler')['batsman_runs'].agg(lambda x: (x==6).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
boundaries6.rename(columns={'bowler':'Player_Name'}, inplace=True)
boundaries6.rename(columns={'batsman_runs':'No_of_6'}, inplace=True)
print(boundaries6.head())

dotballs = deliveries.groupby('bowler')['batsman_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
dotballs.rename(columns={'bowler':'Player_Name'}, inplace=True)
dotballs.rename(columns={'batsman_runs':'Percent_dot_balls'}, inplace=True)

wicket = deliveries[['bowler','player_dismissed']]
wicket.dropna(subset=['player_dismissed'], inplace=True)
fin_wickets = pd.DataFrame(wicket.groupby(['bowler'], as_index=False, sort=False)['player_dismissed'].count())
fin_wickets.rename(columns={'bowler':'Player_Name'}, inplace=True)
fin_wickets.rename(columns={'player_dismissed':'Wickets_per_match'}, inplace=True)

bowler_score = pd.merge(boundaries4, bowler_score, on='Player_Name', how='inner')
bowler_score = pd.merge(boundaries6, bowler_score, on='Player_Name', how='inner')
bowler_score = pd.merge(dotballs, bowler_score, on='Player_Name', how='inner')
bowler_score = pd.merge(fin_wickets, bowler_score, on='Player_Name', how='inner')

bowler_score['Percent_dot_balls'] = (bowler_score['Percent_dot_balls'] / bowler_score['ball'])
bowler_score['No_of_4'] = (bowler_score['No_of_4'] / bowler_score['Matches_bowled'])
bowler_score['No_of_6'] = (bowler_score['No_of_6'] / bowler_score['Matches_bowled'])
bowler_score['extra_runs'] = (bowler_score['extra_runs'] / bowler_score['Matches_bowled'])
bowler_score['Wickets_per_match'] = (bowler_score['Wickets_per_match'] / bowler_score['Matches_bowled'])

print(bowler_score.columns)


#Changing Column Names to better Represent
bowler_score.rename(columns={'batsman_runs':'Runs_Conceded'}, inplace=True)

#bowler_score.to_csv('NewBowl.csv')