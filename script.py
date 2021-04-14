#! /usr/bin/env python3

"""
A script to plot two variables stored in columns of a table data file.
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

"""
notes to remember for writing the script:
dataframe = pd.read_csv("iris.csv") #define dataframe
print(dataframe) #print it out
dataframe.sepal_length_cm #access the column "sepal_length_cm"
dataframe.iloc[0] #use "iloc" to access the row number specified
    dataframe.iloc[0:3] #for first 3 rows (doesnt include line 3, 0 is first)
dataframe.iloc[0, 0] #get a specific value @ first row and column
dataframe.iloc[0:3, 0] #first 3 rows of first column
    OR dataframe.sepal_length_cm[0:3]
long_flowers = dataframe[dataframe.petal_length_cm > 5.9] #filter data
    print(long_flowers)
versicolor = dataframe[dataframe.species == "Iris_versicolor"]
    print(versicolor)

plt.scatter(dataframe.petal_length_cm, dataframe.sepal_length_cm)
    #OR specify x and y explicitly:
x = dataframe.petal_length_cm
y = dataframe.sepal_length_cm
regression = stats.linregress(x, y)
slope = regression.slope
intercept = regression.intercept
plt.scatter(x, y, label = 'Data')
plt.plot(x, slope * x + intercept, color = "orange", label = 'Fitted line')
plt.xlabel("Petal length (cm)")
plt.ylabel("Sepal length (cm)")
plt.legend()
plt.savefig("petal_v_sepal_length_regress.png")

"""

def regression_scatter(dataframe, x_column_name, y_column_name,
        category_column_name = None,
        plot_path = None):
    if category_column_name:
        grouped_dataframes = dataframe.groupby(category_column_name)
    else:
        grouped_dataframes = ('all', dataframe),
    x_min = min(dataframe[x_column_name])
    x_max = max(dataframe[x_column_name])

    color_index = 0
    for category, df in grouped_dataframes:
        x = df[x_column_name]
        y = df[y_column_name]
        regression = stats.linregress(x, y)
        slope = regression.slope
        intercept = regression.intercept
        plt.scatter(x, y, label = category, color = 'C' + str(color_index))

        y1 = slope * x_min + intercept
        y2 = slope * x_max + intercept
        plt.plot((x_min, x_max), (y1, y2),
                color = 'C' + str(color_index))
        color_index += 1

    plt.xlabel(x_column_name)
    plt.ylabel(y_column_name)
    plt.legend()
    plt.savefig(plot_path)



if __name__ == '__main__':
    regression_scatter()
