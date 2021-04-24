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

def compose_name(x_label, y_label, category_label = None):
    """
    Creates a name for a plot file based on X, Y, and categorial variables.

    Parameters
    ----------
    x_label : X variable label

    y_label : Y variable label

    category_label: categorial variable

    Returns
    -------
    The file name (string)

    """
    category_str = ""
    if category_label:
        category_str = "-by-{0}".format(category_label)
    plot_path = "{0}-v-{1}{2}.pdf".format(x_label, y_label,
            category_str)
    return plot_path


def regression_scatter(dataframe, x_column_name, y_column_name,
        category_column_name = None,
        plot_path = None):

    if not plot_path:
        plot_path = compose_name(x_column_name, y_column_name,
                category_column_name)

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


def main_cli():
    parser = argparse.ArgumentParser(
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('path',
            type = str,
            help = 'A path to a CSV file.')
    parser.add_argument('x', '--x',
            type = str,
            default = "petal_length_cm",
            help = 'The column name to plot along the X axis.')
    parser.add_argument('y', '--y',
            type = str,
            default = "sepal_length_cm",
            help = 'The column name to plot along the Y axis.')
    parser.add_argument('-c', '--category',
            type = str,
            default = "species",
            help = 'The column name to treat as a cetegorical variable.')
    parser.add_argument('-o', '--output-plot-path',
            type = str,
            default = "",
            help = 'The desired path of the output plot.')

    args = parser.parse_arg()

    if not os.path.exists(args.path):
        msg = "ERROR: YOU'RE WRONG... The path {0} does not exist.".format(args.path)
        sys.exit(msg)
    elif not os.path.isfile(args.path):
        msg = "ERROR YOU'RE WRONG... The path {0} is not a file.".format(arg.path)
        sys.exit(msg)

    try:
        dataframe = pd.read_csv(args.path)
    except Exception as e:
        msg = "Pandas couldn't read {0}\n".format(args.path)
        sys.stderr.write(msg)
        raise e

    regression_scatter(dataframe, args.x, args.y,
            args.category, arg.output_plot_path)


if __name__ == '__main__':
    main_cli()
