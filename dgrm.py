import sys
import webbrowser
from enum import Enum
import folium
import geojson
import matplotlib.pyplot as plt
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
        index = -1
        if variable in self.variables_water:
            df = self.dfWater
            index = self.variables_water[variable]
        elif variable in self.variables_hygiene:
            df = self.dfHygiene
            index = self.variables_hygiene[variable]
        elif variable in self.variables_sanitation:
            df = self.dfSanitation
            index = self.variables_sanitation[variable]
        else:
            print("ERROR: variable not found!")
        if index == -1:
            print("ERROR: variables index out of bound.")
        averages = []
        for year in range(2000, 2021):
            temp_averages = df[df.iloc[:, 2] == year]
            temp_averages = temp_averages.iloc[:, index]
            temp_averages = sum(temp_averages) / len(temp_averages)
            averages.append(temp_averages)
        list = ["average" for i in range(0, 21)]
        df_averages = pd.DataFrame(data=averages)
        df_averages["country"] = list
        df_averages["year"] = range(2000, 2021)
        df_averages.columns = [variable, 'country', 'year']
        return df_averages

    # returns the iso of a single country
    def get_iso(self, country):
        if country == "average":
            return "AVG"
        df = self.dfSanitation.iloc[:, 0:2]
        iso = ""
        index = 0
        while iso == "":
            if df.iloc[index, 0] == country:
                iso = df.iloc[index, 1]
            index = index + 1
        return iso

    # returns a dataframe containing only the values requested from a single variable and nation
    def get_data(self, variable, nation):
        if variable in self.variables_water:
            df = self.dfWater
        elif variable in self.variables_hygiene:
            df = self.dfHygiene
        elif variable in self.variables_sanitation:
            df = self.dfSanitation
        #else:
        #    print("ERROR: variable " + variable + " not found! Did you maybe misspell it?")
        #    sys.exit()
        data = df[df.iloc[:, 0] == nation]
        if variable in self.variables_water:
            data = data.iloc[:, self.variables_water[variable]]
        elif variable in self.variables_hygiene:
            data = data.iloc[:, self.variables_hygiene[variable]]
        elif variable in self.variables_sanitation:
            data = data.iloc[:, self.variables_sanitation[variable]]
        else:
            print("ERROR: variable not found!")
        return data

    # return a dataframe containing the data for a single nation for a single variable over time
    def get_data_for_nation(self, variable="Population (thousands)", nation="Madagascar"):
        data = self.get_data(variable=variable, nation=nation)
        list_countries = [nation for i in range(0, 21)]
        iso = self.get_iso(nation)
        list_iso = [iso for i in range(0, 21)]
        result = pd.DataFrame(data)
        result["country"] = list_countries
        result["year"] = range(2000, 2021)
        result["ISO_A3"] = list_iso
        result.columns = [variable, "country", "year", "ISO_A3"]
        return result

    # returns a dataframe containing only the values requested from a two variable and nation
    # NOTE: needs two variables, less will throw an error, more variables will be ignored
    def get_double_data(self, variables, nation):
        values_a = self.get_data(variable=variables[0], nation=nation)
        values_b = self.get_data(variable=variables[1], nation=nation)
        list_countries = [nation for i in range(0, 21)]
        iso = self.get_iso(nation)
        list_iso = [iso for i in range(0, 21)]
        result = pd.concat([values_a, values_b], axis=1, join='inner')
        result["country"] = list_countries
        result["year"] = range(2000, 2021)
        result["ISO_A3"] = list_iso
        result.columns = [variables[0], variables[1], "country", "year", "ISO_A3"]
        return result

    # returns all the data from every country for a specific variable and year
    # needed for the data for maps
    def get_world_data(self, variable="Population (thousands)", year=2020):
        countries = self.dfSanitation.iloc[:, 0].unique().tolist()
        df = self.create_dataframe(variable=variable, nations=countries)
        result = df[df.iloc[:, 2] == year]
        return result

    # creates a plot showing one variable for one country over time
    def print_single_variable_of_single_country_over_time(self, variable: str, country: str):
        dfs = Diagram.get_data_for_nation(self, variable=variable, nation=country)
        x_axis = dfs[dfs.iloc[:, 0] == country]
        y_axis = x_axis
        x_axis = x_axis.iloc[:, 2]
        plt.title(country)
        plt.ylabel(variable)
        plt.xlabel("Year")
        plt.xticks(range(2000, 2021))
        plt.plot(x_axis, y_axis)
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

    # creates and returns a dataframe containing all the data for multiple of variables and countries
    def multi_dataframe(self, variables, nations):
        dataframes = []
        for index in range(0, len(variables)):
            dataframes.append(pd.DataFrame())
        frame = pd.DataFrame()
        for index in range(0, len(dataframes)):
            for nation in nations:
                if nation == "average":
                    df = self.get_average_over_time(variables[index])
                    if frame.empty:
                        frame = df
                    else:
                        frame = pd.concat([frame, df], axis=1, join='inner', copy=False)
                    frame = frame.loc[:, ~frame.columns.duplicated()]
                    if dataframes[index].size == 0:
                        dataframes[index] = frame
                    else:
                        dataframes[index] = pd.concat([dataframes[index].append(frame)])
                else:
                    if dataframes[index].size == 0:
                        dataframes[index] = self.get_double_data(variables, nation)
                    else:
                        df = self.get_double_data(variables, nation)
                        dataframes[index] = pd.concat([dataframes[index].append(df)])
        result = pd.concat(dataframes)
        return result

    # creates a plot comparing one variable of one country against the average over time
    def lineplot_single_variable_over_time(self, variable, nations: [str]):
        dataframe = Diagram.create_dataframe(self, variable, nations)
        sns.lineplot(data=dataframe, x="year", y=variable, hue="country")
        plt.xticks(range(2000, 2021))
        plt.show()

    # creates a barplot of a single variable on y-Axis and years on x-Axis
    def barplot_variable_over_time(self, variable: str, nations: [str]):
        dataframe = Diagram.create_dataframe(self, variable, nations)
        sns.barplot(data=dataframe, x="year", y=variable, hue="country")
        plt.show()

    def scatterplot_two_variables(self, var_x: str, var_y: str, nations: [str]):
        df = self.multi_dataframe((var_x, var_y), nations)
        sns.scatterplot(x=df.iloc[:, 0], y=df.iloc[:, 1], data=df, hue="country", legend=True)
        if var_x == "Year":
            plt.xticks(range(2000, 2021))
        plt.title(var_x + " vs " + var_y)
        plt.show()

    def scatterplot_three_variables(self, var_x: str, var_y: str, var_z: str, nations: [str]):
        df = self.multi_dataframe((var_x, var_y, var_z), nations)
        sns.scatterplot(x=df.iloc[:, 0], y=df.iloc[:, 1], size=df.iloc[:, 2], data=df, hue="country", legend=True)
        if var_x == "Year":
            plt.xticks(range(2000, 2021))
        plt.title(var_x + " vs " + var_y + " with size: " + var_z)
        plt.show()

    # this function is called only from the main file to create the diagram.
    # every information needed to create any diagram is given with the parameters
    # this function also checks if the given parameters fit in the requested diagram
    def create_plot(self, type: Type, variable, nations: [str], year=2000):
        if type == Type.SCATTER:
            if len(variable) == 2 and len(nations) > 0:
                Diagram.scatterplot_two_variables(self, variable[0], variable[1], nations)
            elif len(variable) == 3 and len(nations) > 0:
                Diagram.scatterplot_three_variables(self, variable[0], variable[1], variable[2], nations)
            else:
                print("Scatterplots require 2-3 different variables, aswell as at least one country!")
        elif type == Type.LINE:
            if len(variable) == 1 and len(nations) > 0:
                Diagram.lineplot_single_variable_over_time(self, variable=variable[0], nations=nations)
            else:
                print("Lineplots require one variable, aswell as at least one country!")
        elif type == Type.BAR:
            if len(variable) == 1 and len(nations) > 0:
                Diagram.barplot_variable_over_time(self, variable=variable[0], nations=nations)
            else:
                print("Barplots require one variable, aswell as at least one country!")
        elif type == Type.MAP:
            year = int(year)
            if 2000 <= year <= 2020 and len(nations) == 0:
                print("Creating map. This might take a moment.")
                Diagram.create_map(self, variable, year)
            else:
                print("Maps require one variable and a year from 2000-2020!")

    # creates a Choropleth map for the given variable and year
    # maps is saved before it's shown in a new browser window
    def create_map(self, variable='% urban population', year=2000):
        data = self.get_world_data(variable, year)
        world_geo = geojson.load(open('countries.geojson'))
        color4 = 'YlOrBr'
        m = folium.Map(location=[35, 0], zoom_start=2.6)
        folium.Choropleth(
            geo_data=world_geo,
            name="choropleth",
            data=data,
            columns=["ISO_A3", variable],
            key_on='feature.properties.ISO_A3',
            fill_color=color4,
            legend_name=variable
        ).add_to(m).geojson.add_child(folium.features.GeoJsonTooltip(['ADMIN'], labels=False))
        m.save('map.html')
        webbrowser.open_new('map.html')
