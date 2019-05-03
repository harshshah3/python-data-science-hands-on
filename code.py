# --------------
#Importing header files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Path of the file
path

#Code starts here
data = pd.read_csv(path)

data.rename(columns = {'Total': 'Total_Medals'}, inplace = True)
print(data.head(10))


# --------------
data['Better_Event'] = np.where(data['Total_Summer'] > data['Total_Winter'], 'Summer', 'Winter')
data['Better_Event'] = np.where(data['Total_Summer'] == data['Total_Winter'], 'Both', data['Better_Event'])
better_event = data['Better_Event'].value_counts().idxmax()
print("Better event with respect to all the performing countries: ", better_event)



# --------------
#Creating subset dataframe of data
top_countries = data[['Country_Name', 'Total_Summer', 'Total_Winter', 'Total_Medals']]

#Dropping 'Toal_Medals' column from to_countries
top_countries.drop(top_countries.Total_Medals.index[-1], inplace = True)

#define func--> top_ten
def top_ten(top_countries, col_name):
    country_list = []
    country_list = list(top_countries.nlargest(10, col_name)['Country_Name'])
    return country_list

#Calling func for 3 different columns of DataFrame
top_10_summer = top_ten(top_countries, col_name = 'Total_Summer')
top_10_winter = top_ten(top_countries, col_name = 'Total_Winter')
top_10 = top_ten(top_countries, col_name = 'Total_Medals')

#Finding Common elements between 3 lists above
common = list(set(top_10_summer) & set(top_10_winter) & set(top_10))
print(common)




# --------------
#creating subset DataFrames for 3 Bar plots
summer_df = data[data['Country_Name'].isin(top_10_summer)]
winter_df = data[data['Country_Name'].isin(top_10_winter)]
top_df = data[data['Country_Name'].isin(top_10)]

#Initializing figure with 3 subplots
fig, axs = plt.subplots(1, 3, figsize = (15,10), sharey = True)
#1st Subplot for SUMMER
axs[0].bar(summer_df['Country_Name'], summer_df['Total_Summer'], color = 'red')
axs[0].set_title('SUMMER event')
axs[0].set_xlabel('Countries')
axs[0].set_ylabel('No of Medals', fontsize = 13)

#2nd Subplot for WINTER
axs[1].bar(winter_df['Country_Name'], winter_df['Total_Summer'], color = 'blue')
axs[1].set_title('WINTER event')
axs[1].set_xlabel('Countries')
#axs[1].set_ylabel('No of Medals')

#3rd Subplot for BOTH event
axs[2].bar(top_df['Country_Name'], top_df['Total_Summer'])
axs[2].set_title('BOTH event')
axs[2].set_xlabel('Countries')
#axs[2].set_ylabel('No of Medals')

#Setting up properties of main figure
fig.tight_layout()
fig.subplots_adjust(top = 0.88)
fig.suptitle('Total Medal Count in different events for top 10 countries', fontsize = 16)

#For xticks rotation
for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation=45)

#Display Plot    
plt.show()


# --------------
#Adding new column to all 3 DataFrames
#Finding Max value of Gold Ratio among coutries for each kind of event
 
summer_df['Gold_Ratio'] = summer_df.apply(lambda x: x.Gold_Summer / x.Total_Summer, axis = 1)
summer_max_index = summer_df['Gold_Ratio'].argmax()
summer_max_ratio = summer_df.Gold_Ratio.loc[summer_max_index]
summer_country_gold = summer_df.Country_Name.loc[summer_max_index]
print(summer_max_ratio, summer_country_gold)


winter_df['Gold_Ratio'] = winter_df.apply(lambda x: x.Gold_Winter / x.Total_Winter, axis = 1)
winter_max_index = winter_df['Gold_Ratio'].argmax()
winter_max_ratio = winter_df.Gold_Ratio.loc[winter_max_index]
winter_country_gold = winter_df.Country_Name.loc[winter_max_index]
print(winter_max_ratio, winter_country_gold)

top_df['Gold_Ratio'] = top_df.apply(lambda x: x.Gold_Total / x.Total_Medals, axis = 1)
top_max_index = top_df['Gold_Ratio'].argmax()
top_max_ratio = top_df.Gold_Ratio.loc[top_max_index]
top_country_gold = top_df.Country_Name.loc[top_max_index]
print(top_max_ratio, top_country_gold)


# --------------
#Removing last row and subsetting DataFrame --> data
data_1 = data.drop(data.index[-1], axis = 0)
#Adding new columns-->'Total_Points' having weighted value of types of medals
weights = pd.Series([3, 2, 1], index = ['Gold_Total', 'Silver_Total', 'Bronze_Total'])
data_1['Total_Points'] = (data_1[['Gold_Total', 'Silver_Total', 'Bronze_Total']] * weights).sum(1)

#Finding maxiimun point holder country and their points
most_points_index = data_1.Total_Points.idxmax()
most_points = data_1.loc[[most_points_index], 'Total_Points'].values[0]
best_country = data_1.loc[[most_points_index], 'Country_Name'].values[0]
print(most_points, best_country, sep = '\n')


# --------------
#Creating single row DataFrame for best_country value
best = data[data['Country_Name'] == best_country]
#Filtering df with only 3 columns
best = best[['Gold_Total','Silver_Total','Bronze_Total']].copy()

#Plotting Stacked Bar plot
best.plot.bar(stacked = False)
plt.xlabel('United States')
plt.legend(labels = ['Total Gold', 'Total Silver', 'Total Bronze'])
plt.title("Best Country's overall Olympic Performance")

#Removing xticks
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

#Display Plot
plt.show()


