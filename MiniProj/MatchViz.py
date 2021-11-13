import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

matches_data = pd.read_csv("matches.csv")
matches_data.head(5)

matches_data.drop('umpire3', axis=1, inplace=True)
matches_data.replace( 'Rising Pune Supergiant', 'Rising Pune Supergiants',inplace = True)
matches_data['city'].fillna( matches_data['venue'].apply(lambda x: x[:5]),inplace = True)
matches_data[matches_data['city']== 'Dubai']
matches_data[matches_data['winner'].isnull()]
matches_data.replace('Bengaluru', 'Bangalore',inplace = True)

def best_defend_team():
    plt.figure(figsize=(8,5))
    sns.swarmplot(y='win_by_runs',x='winner',data=matches_data)
    plt.tight_layout()
    plt.xticks(rotation=90)
    plt.title('Best Defending Teams')
    plt.show()

def best_chase_team():
    plt.figure(figsize=(8, 5))
    sns.swarmplot(y='win_by_wickets', x='winner', data=matches_data)
    plt.xticks(rotation=80)
    plt.title('Best Chasing Team')
    plt.show()

def annot_plot(ax,w,h):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for p in ax.patches:
        ax.annotate('{0:.1f}'.format(p.get_height()), (p.get_x()+w, p.get_height()+h))

def man_of_match():
    plt.figure(figsize=(5, 3))

    ax = matches_data['player_of_match'].value_counts()[:10].plot.bar()
    plt.title('Top 10 high performing Players')
    annot_plot(ax, 0.08, 1)
    plt.show()

#best_chase_team()
#best_defend_team()
#man_of_match()