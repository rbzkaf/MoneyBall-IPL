import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


matches = pd.read_csv("matches.csv")
matches.head()

deliveries = pd.read_csv("deliveries.csv")
deliveries.head()


player_data = pd.read_csv("DIM_PLAYER.csv")
player_data = player_data.drop(["PLAYER_SK", "Player_Id", "DOB", "Batting_hand"], axis=1)
player_data.replace( 'Right-arm medium fast', 'Right-arm medium-fast',inplace = True)

player_data.rename(columns={'Player_Name':'bowler'}, inplace=True)
deliveries = pd.merge(player_data, deliveries, on='bowler')
print(deliveries.columns)


grouped = pd.DataFrame(deliveries.groupby(['batsman','Bowling_skill']).agg({'batsman_runs' : 'sum', 'ball' :'count'}))
grouped = grouped.reset_index()
grouped.columns=np.where(grouped.columns==0, 'count', grouped.columns)

print(grouped.head())

rt_arm_med = grouped[grouped['Bowling_skill'] == 'Right-arm medium']
rt_arm_med.rename(columns={'batsman_runs':'rt_arm_med_runs'}, inplace=True)
rt_arm_med.rename(columns={'ball':'rt_arm_med_balls'}, inplace=True)
rt_arm_med = rt_arm_med.drop(['Bowling_skill'], axis=1)


rt_arm_off = grouped[grouped['Bowling_skill'] == 'Right-arm offbreak']
rt_arm_off.rename(columns={'batsman_runs':'rt_arm_off_runs'}, inplace=True)
rt_arm_off.rename(columns={'ball':'rt_arm_off_balls'}, inplace=True)
rt_arm_off = rt_arm_off.drop(['Bowling_skill'], axis=1)

rt_arm_fm = grouped[grouped['Bowling_skill'] == 'Right-arm fast-medium']
rt_arm_fm.rename(columns={'batsman_runs':'rt_arm_fm_runs'}, inplace=True)
rt_arm_fm.rename(columns={'ball':'rt_arm_fm_balls'}, inplace=True)
rt_arm_fm = rt_arm_fm.drop(['Bowling_skill'], axis=1)

rt_arm_mf = grouped[grouped['Bowling_skill'] == 'Right-arm medium-fast']
rt_arm_mf.rename(columns={'batsman_runs':'rt_arm_mf_runs'}, inplace=True)
rt_arm_mf.rename(columns={'ball':'rt_arm_mf_balls'}, inplace=True)
rt_arm_mf = rt_arm_mf.drop(['Bowling_skill'], axis=1)

leg_break_googly = grouped[grouped['Bowling_skill'] == 'Legbreak googly']
leg_break_googly.rename(columns={'batsman_runs':'leg_break_googly_runs'}, inplace=True)
leg_break_googly.rename(columns={'ball':'leg_break_googly_balls'}, inplace=True)
leg_break_googly = leg_break_googly.drop(['Bowling_skill'], axis=1)

lt_arm_fm = grouped[grouped['Bowling_skill'] == 'Left-arm fast-medium']
lt_arm_fm.rename(columns={'batsman_runs':'lt_arm_fm_runs'}, inplace=True)
lt_arm_fm.rename(columns={'ball':'lt_arm_fm_balls'}, inplace=True)
lt_arm_fm = lt_arm_fm.drop(['Bowling_skill'], axis=1)



lt_arm_mf = grouped[grouped['Bowling_skill'] == 'Left-arm medium-fast']
lt_arm_mf.rename(columns={'batsman_runs':'lt_arm_mf_runs'}, inplace=True)
lt_arm_mf.rename(columns={'ball':'lt_arm_mf_balls'}, inplace=True)
lt_arm_mf = lt_arm_mf.drop(['Bowling_skill'], axis=1)

leg_break = grouped[grouped['Bowling_skill'] == 'Legbreak']
leg_break.rename(columns={'batsman_runs':'leg_break_runs'}, inplace=True)
leg_break.rename(columns={'ball':'leg_break_balls'}, inplace=True)
leg_break = leg_break.drop(['Bowling_skill'], axis=1)

lt_arm_ortdx = grouped[grouped['Bowling_skill'] == 'Slow left-arm orthodox']
lt_arm_ortdx.rename(columns={'batsman_runs':'lt_arm_ortdx_runs'}, inplace=True)
lt_arm_ortdx.rename(columns={'ball':'lt_arm_ortdx_balls'}, inplace=True)
lt_arm_ortdx = lt_arm_ortdx.drop(['Bowling_skill'], axis=1)


rt_arm_fast = grouped[grouped['Bowling_skill'] == 'Right-arm fast']
rt_arm_fast.rename(columns={'batsman_runs':'rt_arm_fast_runs'}, inplace=True)
rt_arm_fast.rename(columns={'ball':'rt_arm_fast_balls'}, inplace=True)
rt_arm_fast = rt_arm_fast.drop(['Bowling_skill'], axis=1)

lt_arm_fast = grouped[grouped['Bowling_skill'] == 'Left-arm fast']
lt_arm_fast.rename(columns={'batsman_runs':'lt_arm_fast_runs'}, inplace=True)
lt_arm_fast.rename(columns={'ball':'lt_arm_fast_balls'}, inplace=True)
lt_arm_fast = lt_arm_fast.drop(['Bowling_skill'], axis=1)

lt_arm_med = grouped[grouped['Bowling_skill'] == 'Left-arm medium']
lt_arm_med.rename(columns={'batsman_runs':'lt_arm_med_runs'}, inplace=True)
lt_arm_med.rename(columns={'ball':'lt_arm_med_balls'}, inplace=True)
lt_arm_med = lt_arm_med.drop(['Bowling_skill'], axis=1)

lt_arm_china = grouped[grouped['Bowling_skill'] == 'Slow left-arm chinaman']
lt_arm_china.rename(columns={'batsman_runs':'lt_arm_china_runs'}, inplace=True)
lt_arm_china.rename(columns={'ball':'lt_arm_china_balls'}, inplace=True)
lt_arm_china = lt_arm_china.drop(['Bowling_skill'], axis=1)

bat_bowl_style = pd.merge(rt_arm_fast, rt_arm_fm, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, rt_arm_mf, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, rt_arm_med, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, lt_arm_fast, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, lt_arm_fm, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, lt_arm_mf, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, lt_arm_med, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, leg_break, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, leg_break_googly, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, rt_arm_off, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, lt_arm_ortdx, on='batsman')
bat_bowl_style = pd.merge(bat_bowl_style, lt_arm_china, on='batsman')

print(bat_bowl_style.columns)
#Averages are better measures
bat_bowl_style['rt_arm_fast_avg']=(bat_bowl_style['rt_arm_fast_runs']/bat_bowl_style['rt_arm_fast_balls'])*6
bat_bowl_style['rt_arm_mf_avg']=(bat_bowl_style['rt_arm_mf_runs']/bat_bowl_style['rt_arm_mf_balls'])*6
bat_bowl_style['rt_arm_fm_avg']=(bat_bowl_style['rt_arm_fm_runs']/bat_bowl_style['rt_arm_fm_balls'])*6
bat_bowl_style['rt_arm_med_avg']=(bat_bowl_style['rt_arm_med_runs']/bat_bowl_style['rt_arm_med_balls'])*6

bat_bowl_style['lt_arm_fast_avg']=(bat_bowl_style['lt_arm_fast_runs']/bat_bowl_style['lt_arm_fast_balls'])*6
bat_bowl_style['lt_arm_fm_avg']=(bat_bowl_style['lt_arm_fm_runs']/bat_bowl_style['lt_arm_fm_balls'])*6
bat_bowl_style['lt_arm_mf_avg']=(bat_bowl_style['lt_arm_mf_runs']/bat_bowl_style['lt_arm_mf_balls'])*6
bat_bowl_style['lt_arm_med_avg']=(bat_bowl_style['lt_arm_med_runs']/bat_bowl_style['lt_arm_med_balls'])*6

bat_bowl_style['leg_break_avg']=(bat_bowl_style['leg_break_runs']/bat_bowl_style['leg_break_balls'])*6
bat_bowl_style['leg_break_googly_avg']=(bat_bowl_style['leg_break_googly_runs']/bat_bowl_style['leg_break_googly_balls'])*6
bat_bowl_style['rt_arm_off_avg']=(bat_bowl_style['rt_arm_off_runs']/bat_bowl_style['rt_arm_off_balls'])*6
bat_bowl_style['lt_arm_ortdx_avg']=(bat_bowl_style['lt_arm_ortdx_runs']/bat_bowl_style['lt_arm_ortdx_balls'])*6
bat_bowl_style['lt_arm_china_avg']=(bat_bowl_style['lt_arm_china_runs']/bat_bowl_style['lt_arm_china_balls'])*6

def right_fast():
    bat_bowl_style.sort_values(by=['rt_arm_fast_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'rt_arm_fast_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen againt right arm Fast ',fontsize = 20)
    plt.show()

def right_fastmed():
    bat_bowl_style.sort_values(by=['rt_arm_fm_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'rt_arm_fm_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen against right arm Fast Medium ',fontsize = 20)
    plt.show()

def right_medfast():
    bat_bowl_style.sort_values(by=['rt_arm_mf_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'rt_arm_mf_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen against right arm MediumFast ',fontsize = 20)
    plt.show()

def right_med():
    bat_bowl_style.sort_values(by=['rt_arm_med_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'rt_arm_med_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen against right arm Medium ',fontsize = 20)
    plt.show()

def left_fast():
    bat_bowl_style.sort_values(by=['lt_arm_fast_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'lt_arm_fast_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen againt left arm Fast ',fontsize = 20)
    plt.show()

def left_fastmed():
    bat_bowl_style.sort_values(by=['lt_arm_fm_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'lt_arm_fm_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen against left arm Fast Medium ',fontsize = 20)
    plt.show()

def right_medfast():
    bat_bowl_style.sort_values(by=['lt_arm_mf_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0,1,10))
    plt.rcParams['figure.figsize'] = 10,5
    bat_bowl_style.plot(x = 'batsman',y = 'lt_arm_mf_avg',kind = 'bar',legend = '',color = colors,fontsize = 10)
    plt.xlabel('Batsman Name',fontsize = 20)
    plt.ylabel('Average per Over',fontsize = 20)
    plt.title('Top Batsmen against left arm MediumFast ',fontsize = 20)
    plt.show()


def left_med():
    bat_bowl_style.sort_values(by=['lt_arm_med_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0, 1, 10))
    plt.rcParams['figure.figsize'] = 10, 5
    bat_bowl_style.plot(x='batsman', y='lt_arm_med_avg', kind='bar', legend='', color=colors, fontsize=10)
    plt.xlabel('Batsman Name', fontsize=20)
    plt.ylabel('Average per Over', fontsize=20)
    plt.title('Top Batsmen against left arm Medium ', fontsize=20)
    plt.show()


def leg_break():
    bat_bowl_style.sort_values(by=['leg_break_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0, 1, 10))
    plt.rcParams['figure.figsize'] = 10, 5
    bat_bowl_style.plot(x='batsman', y='leg_break_avg', kind='bar', legend='', color=colors, fontsize=10)
    plt.xlabel('Batsman Name', fontsize=20)
    plt.ylabel('Average per Over', fontsize=20)
    plt.title('Top Batsmen against Legbreak ', fontsize=20)
    plt.show()

def leg_break_googly():
    bat_bowl_style.sort_values(by=['leg_break_googly_avg'], inplace=True, ascending=False)
    colors = cm.rainbow(np.linspace(0, 1, 10))
    plt.rcParams['figure.figsize'] = 10, 5
    bat_bowl_style.plot(x='batsman', y='leg_break_googly_avg', kind='bar', legend='', color=colors, fontsize=10)
    plt.xlabel('Batsman Name', fontsize=20)
    plt.ylabel('Average per Over', fontsize=20)
    plt.title('Top Batsmen against Legbreak Googly ', fontsize=20)
    plt.show()

right_fast()
#right_fastmed()
#right_medfast()
right_med()

#left_fast()
#left_fastmed()
#left_medfast()
#left_med()

#leg_break()
#leg_break_googly()