#Player Related

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

matches = pd.read_csv("matches.csv")
matches.head()

deliveries = pd.read_csv("deliveries.csv")
deliveries.head()

batsmen_score = pd.DataFrame(deliveries.groupby(['match_id','batsman']).sum()['batsman_runs'])
batsmen_score.head()

def hist_runs_scored():
    plt.rcParams['figure.figsize'] = 10, 5
    batsmen_score.plot(kind='hist', fontsize=20)
    plt.xlabel('Runs Scored', fontsize=20)
    plt.ylabel('Number of Times', fontsize=20)
    plt.title('Histogram for Runs Scored', fontsize=20)
    plt.show()

batsmen_score_20 = pd.DataFrame(deliveries.groupby(['match_id','batsman']).agg({'batsman_runs' : 'sum', 'ball' :'count'}))

batsmen_strikerate = batsmen_score_20[batsmen_score_20['ball'] >= 15]
batsmen_strikerate['Strike Rate'] = (batsmen_strikerate['batsman_runs']/batsmen_strikerate['ball'])*100
batsmen_strikerate.head()

def inning_progression():
    ax = batsmen_strikerate.plot(kind='scatter', x='batsman_runs', y='Strike Rate')
    plt.xlabel('Runs Scored', fontsize=20)
    plt.ylabel('Strike Rate', fontsize=20)
    plt.title('Innings Progression with Runs', fontsize=20)
    plt.show()

def strike_rate_prog():
    ax = batsmen_strikerate.plot(kind='scatter', x='ball', y='Strike Rate', color='y')
    batsmen_strikerate.groupby(['ball']).max().plot(kind='line', y='Strike Rate', ax=ax, color='green',
                                                    label='Max Strike Rate')
    batsmen_strikerate.groupby(['ball']).min().plot(kind='line', y='Strike Rate', ax=ax, color='red',
                                                    label='Min Strike Rate')
    plt.xlabel('Ball Faced', fontsize=20)
    plt.ylabel('Strike Rate', fontsize=20)
    plt.title('Strike Rate Progression with Balls', fontsize=20)
    plt.show()


batsmen_strikerate_season = pd.DataFrame(deliveries.groupby(['batsman']).agg({'batsman_runs' : 'sum','ball' : 'count'}))
batsmen_strikerate_season['Strike Rate'] = batsmen_strikerate_season['batsman_runs']/batsmen_strikerate_season['ball']*100
batsmen_strikerate_season = batsmen_strikerate_season.sort_values(by ='Strike Rate' , ascending = False)
batsmen_strikerate_season[batsmen_strikerate_season['batsman_runs'] > 2500]

def top_strike_rate():
    colors = cm.rainbow(
        np.linspace(0, 1, len(batsmen_strikerate_season[batsmen_strikerate_season['batsman_runs'] > 2500])))
    batsmen_strikerate_season[batsmen_strikerate_season['batsman_runs'] > 2500].plot(kind='bar', y='Strike Rate',
                                                                                     color=colors, legend='',
                                                                                     fontsize=10)
    plt.xlabel('Batsman Name', fontsize=20)
    plt.ylabel('Strike Rate', fontsize=20)
    plt.show()

batsmen_average = pd.DataFrame(deliveries.groupby(['batsman']).agg({'batsman_runs' : 'sum','player_dismissed' : 'count'}))
batsmen_average['Average'] = batsmen_average['batsman_runs']/batsmen_average['player_dismissed']
batsmen_average = batsmen_average.sort_values(by = 'Average',ascending = False)
batsmen_average[batsmen_average['batsman_runs'] > 2500]

def top_avg():
    plt.rcParams['figure.figsize'] = 15, 10
    colors = cm.rainbow(np.linspace(0, 1, len(batsmen_average[batsmen_average['batsman_runs'] > 2500])))
    batsmen_average[batsmen_average['batsman_runs'] > 2500].plot(kind='bar', y='Average',
                                                                 color=colors, legend='', fontsize=10)
    plt.xlabel('Batsman Name', fontsize=20)
    plt.ylabel('Average', fontsize=20)
    plt.show()


#hist_runs_scored()
#inning_progression()
#strike_rate_prog()
#top_strike_rate()
#top_avg()
