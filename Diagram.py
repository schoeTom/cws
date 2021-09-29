import numpy as np

from main import get_data_for_nation
from main import get_average_over_time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from enum import Enum
class Type(Enum):
    SCATTER = 0
    BAR = 1
    LINE = 2
    MAP = 3



class Diagram:

    def __init__(self, type: Type):
        self.type = type

    # creates a plot showing one variable for one country over time
    def print_single_variable_of_single_country_over_time(variable: str, country: str):
        dfs = get_data_for_nation(variable=variable, nation=country)
        xAxis = dfs[dfs.iloc[:, 0] == country]
        yAxis = xAxis
        xAxis = xAxis.iloc[:, 2]
        print("printing xAxis")
        print(xAxis)
        print("printing yAxis")
        print(yAxis)
        plt.title(country)
        plt.ylabel(variable)
        plt.xlabel("Year")
        plt.xticks(range(2000, 2021))
        plt.plot(xAxis, yAxis)
        plt.show()

    # creates and returns a dataframe containing all the data for one specific variable for multiple countries
    def create_dataframe(self, variable: str, nations: [str]):
        dataframes = []
        for nation in nations:
            if nation == "average":
                dataframes.append(get_average_over_time(variable))
            else:
                dataframes.append(get_data_for_nation(variable, nation))
        result = pd.concat(dataframes)
        return result


    # creates a plot comparing one variable of one country against the average over time
    def lineplot_single_variable_over_time(self, variable: str, nations: [str]):
        dataframe = Diagram.create_dataframe(self, variable, nations)
        sns.lineplot(data=dataframe, x="year", y=variable, hue="country").set_xticks(range(2000, 2021))
        plt.show()

    # creates a barplot of a single variable on y-Axis and years on x-Axis
    def barplot_variable_over_time(self, variable: str, nations: [str]):
        dataframe = Diagram.create_dataframe(self, variable, nations)
        sns.barplot(data=dataframe, x="year", y=variable, hue="country")
        plt.show()

    def scatterplot_two_variables(self,
                                  varX: str,
                                  varY: str,
                                  nations: [str]):
        xAxis  = Diagram.create_dataframe(self, varX, nations)
        yAxis = Diagram.create_dataframe(self, varY, nations)
        sns.scatterplot(x=xAxis.iloc[:, 0], y=yAxis.iloc[:, 0])
        if (varX == "Year"):
            plt.xticks(range(2000, 2021))
        plt.title(nations)
        plt.show()

    def scatterplot_three_variables(self, varX: str, varY: str, varZ: str, nations: [str]):
        xAxis = Diagram.create_dataframe(self, varX, nations)
        yAxis = Diagram.create_dataframe(self, varY, nations)
        zAxis = Diagram.create_dataframe(self, varZ, nations)
        sns.scatterplot(x=xAxis.iloc[:, 0], y=yAxis.iloc[:, 0], size=zAxis.iloc[:, 0])
        if (varX == "Year"):
            plt.xticks(range(2000, 2021))
        plt.title(nations)
        plt.show()

    def create_plot(self, type: Type, variable: [str], nations: [str]):
        if(type == Type.SCATTER):
            if(len(variable) == 2 & np.unique(variable) == 2 & len(nations) > 0):
                Diagram.scatterplot_two_variables(self, variable[0], variable[1], nations)
            elif(len(variable) == 3 & np.unique(variable) == 3 & len(nations) > 0):
                Diagram.scatterplot_three_variables(self, variable[0], variable[1], variable[2], nations)
            else:
                print("Scatterplots require 2-3 different variables, aswell as at least one country!")
        elif(type == Type.LINE):
            if(len(variable == 1) & len(nations) > 0):
                Diagram.lineplot_single_variable_over_time(self, variable[0], nations)
            else:
                print("Lineplots require one variable, aswell as at least one country!")
        elif(type == Type.BAR):
            if(len(variable) == 1 & len(nations) > 0):
                Diagram.barplot_variable_over_time(self, variable[0], nations)
            else:
                print("Barplots require one variable, aswell as at least one country!")
        elif(type == Type.MAP):
            print("Yeah, I dont really do anything right now. Try some other type of Diagram!")

