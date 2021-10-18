import geojson
import webbrowser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

from enum import Enum
import webbrowser
from enum import Enum

import folium
import geojson
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Type(Enum):
    SCATTER = 0
    BAR = 1
    LINE = 2
    MAP = 3



class Diagram:

    def __init__(self, type: Type, df_s, df_w, df_h, var_s, var_w, var_h):
        self.type = type
        self.dfSanitation = df_s
        self.dfWater = df_w
        self.dfHygiene = df_h
        self.variables_sanitation = var_s
        self.variables_water = var_w
        self.variables_hygiene = var_h

    # returns a dataframe containing the average worldwide values per year
    def get_average_over_time(self, variable="Population (thousands)"):
        dfs = self.dfSanitation
        averages = []
        for year in range(2000, 2021):
            tempAverages = dfs[dfs.iloc[:, 2] == year]
            tempAverages = tempAverages.iloc[:, self.variables_sanitation[variable]]
            tempAverages = sum(tempAverages) / len(tempAverages)
            averages.append(tempAverages)
        list = ["average" for i in range(0, 21)]
        dfAverages = pd.DataFrame(data=averages)
        dfAverages["line"] = list
        dfAverages["year"] = range(2000, 2021)
        dfAverages.columns = [variable, 'country', 'year']
        return dfAverages

    # returns the iso of a single country
    def get_iso(self, country):
        df = self.dfSanitation.iloc[:, 0:2]
        iso = ""
        index = 0
        while iso == "":
            if df.iloc[index, 0] == country:
                iso = df.iloc[index, 1]
            index = index+1
        return iso


    # return a dataframe containing the data for a single nation for a single variable over time
    def get_data_for_nation(self, variable="Population (thousands)", nation="Madagascar"):
        if self.variables_water[variable]:
            df = self.dfWater
        elif self.variables_hygiene[variable]:
            df = self.dfHygiene
        elif self.variables_sanitation[variable]:
            df = self.dfSanitation
        else:
            print("ERROR: variable not found!")
        data = df[df.iloc[:, 0] == nation]
        if variable in self.variables_water:
            data = data.iloc[:, self.variables_water[variable]]
        elif variable in self.variables_hygiene:
            data = data.iloc[:, self.variables_hygiene[variable]]
        elif variable in self.variables_hygiene:
            data = data.iloc[:, self.variables_sanitation[variable]]
        else:
            print("ERROR: variable not found!")

        list_countries = [nation for i in range(0, 21)]
        iso = self.get_iso(nation)
        list_iso = [iso for i in range(0, 21)]
        result = pd.DataFrame(data)
        result["country"] = list_countries
        result["year"] = range(2000, 2021)
        result["ISO_A3"] = list_iso
        result.columns = [variable, "country", "year", "ISO_A3"]
        return result

    def get_world_data(self, variable="Population (thousands)", year=2020):
        countries = self.dfSanitation.iloc[:, 0].unique().tolist()
        df = self.create_dataframe(variable=variable, nations=countries)
        result = df[df.iloc[:, 2] == year]
        return result

    # creates a plot showing one variable for one country over time
    def print_single_variable_of_single_country_over_time(self, variable: str, country: str):
        dfs = Diagram.get_data_for_nation(self, variable=variable, nation=country)
        xAxis = dfs[dfs.iloc[:, 0] == country]
        yAxis = xAxis
        xAxis = xAxis.iloc[:, 2]
        plt.title(country)
        plt.ylabel(variable)
        plt.xlabel("Year")
        plt.xticks(range(2000, 2021))
        plt.plot(xAxis, yAxis)
        plt.show()

    # creates and returns a dataframe containing all the data for one specific variable for multiple countries
    def create_dataframe(self, variable, nations):
        dataframes = []
        for nation in nations:
            if nation == "average":
                dataframes.append(Diagram.get_average_over_time(self, variable))
            else:
                dataframes.append(Diagram.get_data_for_nation(self, variable, nation))
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

    def create_plot(self, type: Type, variable: [str], nations: [str], year = 2000):
        if type == Type.SCATTER:
            if len(variable) == 2 & np.unique(variable) == 2 & len(nations) > 0:
                Diagram.scatterplot_two_variables(self, variable[0], variable[1], nations)
            elif len(variable) == 3 & np.unique(variable) == 3 & len(nations) > 0:
                Diagram.scatterplot_three_variables(self, variable[0], variable[1], variable[2], nations)
            else:
                print("Scatterplots require 2-3 different variables, aswell as at least one country!")
        elif type == Type.LINE:
            if len(variable == 1) & len(nations) > 0:
                Diagram.lineplot_single_variable_over_time(self, variable[0], nations)
            else:
                print("Lineplots require one variable, aswell as at least one country!")
        elif type == Type.BAR:
            if len(variable) == 1 & len(nations) > 0:
                Diagram.barplot_variable_over_time(self, variable[0], nations)
            else:
                print("Barplots require one variable, aswell as at least one country!")
        elif type == Type.MAP:
            Diagram.folium_experiments(self, year)

    # for experiments with folium
    def folium_experiments(self, variable='% urban population', year=2000):
        data = self.get_world_data(variable, year)
        #data = data.to_numpy()
        world_geo = geojson.load(open('countries.geojson'))
        #url = ('https://github.com/python-visualization/folium/tree/master/examples/data')
        #world_geo = f"{url}/world-counties.json"
        m = folium.Map(location=[35, 0], zoom_start=2.6)
        folium.Choropleth(
            geo_data=world_geo,
            name="choropleth",
            data=data,
            columns=["ISO_A3", variable],
            key_on='feature.properties.ISO_A3',
            fill_color='YlOrRd',
            legend_name=variable
        ).add_to(m)

        print("I created a map!")
        m.save('map.html')
        webbrowser.open_new('map.html')

