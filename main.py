import sys
import openpyxl as xl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt        #folium for maps
import dash                            #bokeh for virtualization
import dash_html_components as html
import plotly.express as px
import math
import seaborn as sns

#initializes all variables, that are needed throughout a lot of functions
def initialize_global_variables():
    global country
    global sheet
    global year
    global countryISO3
    countryISO3 = {'DEU', 'GHA', 'GIB', 'MDG'}

    #variables_sanitation is a dictionary mapping each variable from the sanitation datasheet to
    #its column index in the datasheet, to have easy integerbased access to the column
    global variables_sanitation
    variables_sanitation = {"Country":0, "ISO3":1, "Year":2, "Population (thousands)":3,
                            "% urban population":4, "% at least basic national sanitation":5,
                            "limited (shared) national sanitation":6, "unimproved national sanitation":7,
                            "open defecation national sanitation":8, "annual rate of change in basic national sanitation":9,
                            "annual rate of change in open national defecation":10, "at least basic rural sanitation":11,
                            "limited (shared) rural sanitation":12, "unimproved rural sanitation":13,
                            "open defecation rural sanitation":14, "annual rate of change in basic rural sanitation":15,
                            "annual rate of change in open rural defecation":16, "at least basic urban sanitation":17,
                            "limited (shared) urban sanitation":18, "unimproved urban sanitation":19,
                            "open defecation urban sanitation":20, "annual rate of change in basic urban sanitation":21,
                            "annual rate of change in open urban defecation":22,
                            "Safely managed national Proportion of population using improved sanitation facilities (excluding shared)":23,
                            "Disposed in situ national Proportion of population using improved sanitation facilities (excluding shared)":24,
                            "Emptied and treated national Proportion of population using improved sanitation facilities (excluding shared)":25,
                            "Wastewater treated national Proportion of population using improved sanitation facilities (excluding shared)":26,
                            "annual rate of change in safely mangaged national Proportion of population using improved sanitation facilities (excluding shared)":27,
                            "Latriness and other national Proportion of population using improved sanitation facilities (including shared)":28,
                            "Septic tanks national Proportion of population using improved sanitation facilities (including shared)":29,
                            "Sewer connections national Proportion of population using improved sanitation facilities (including shared)":30,
                            "Safely managed rural Proportion of population using improved sanitation facilities (excluding shared)":31,
                            "Disposed in situ rural Proportion of population using improved sanitation facilities (excluding shared)":32,
                            "Emptied and treated rural Proportion of population using improved sanitation facilities (excluding shared)":33,
                            "Wastewater treated rural Proportion of population using improved sanitation facilities (excluding shared)":34,
                            "Annual rate of change in safely managed rural Proportion of population using improved sanitation facilities (excluding shared)":35,
                            "Latriness and other rural Proportion of population using improved sanitation facilities (including shared)":36,
                            "Septic tanks rural Proportion of population using improved sanitation facilities (including shared)":37,
                            "Sewer connections rural Proportion of population using improved sanitation facilities (including shared)":38,
                            "Safely managed urban Proportion of population using improved sanitation facilities (excluding shared)":39,
                            "Disposed in situ urban Proportion of population using improved sanitation facilities (excluding shared)":40,
                            "Emptied and treated urban Proportion of population using improved sanitation facilities (excluding shared)":41,
                            "Wastewater treated urban Proportion of population using improved sanitation facilities (excluding shared)":42,
                            "Annual rate of change in safely managed urban Proportion of population using improved sanitation facilities (excluding shared)":43,
                            "Latriness and other urban Proportion of population using improved sanitation facilities (including shared)":44,
                            "Septic tanks urban Proportion of population using improved sanitation facilities (including shared)":45,
                            "Sewer connections urban Proportion of population using improved sanitation facilities (including shared)":46,
                            "SDG region":47, "WHO region":48, "UNICEF Programming region":49, "UNICEF Reporting region":50}

    read_data()

#reads all the necessary data from csv files
def read_data():
    global dfWater
    global dfSanitation
    global dfHygiene
    dfWater = pd.read_csv("Water_12_08_2021.csv", header=0)
    dfSanitation = pd.read_csv("Sanitation_12_08_2021.csv", header=1, index_col=0)
    dfSanitation = dfSanitation.fillna(0)
    dfHygiene = pd.read_csv("Hygiene_12_08_2021.csv", header=0)

#copies excel sheets to single excel files
def copy_excel_file():
    path1 = "JMP_2021_WLD.xlsx"
    path2 = "WHS_11_08_2021.xlsx"
    wb1 = xl.load_workbook(filename=path1)
    ws1 = wb1.worksheets[3]
    wb2 = xl.load_workbook(filename=path2)
    ws2 = wb2.create_sheet(ws1.title)
    for row in ws1:
        for cell in row:
            ws2[cell.coordinate].value = cell.value
    wb2.save(path2)

#manages textbased user input to use this program
def get_user_input():
    global country
    global sheet
    global year
    country = input("Enter ISO3: ").upper()
    sheet = input("Choose Datasheet (Water/Sanitation/Hygiene): ").capitalize()
    year = int(input("Select the year (2000-2020): "))
    if(country == "END" or country == "EXIT"):
        print("Stopping the program. Seems like it worked!")
        sys.exit()
    while(not(countryISO3.__contains__(country))):
        print("Country ISO3 not recognized. Try one of these countries.")
        print(countryISO3)
        country = input("Enter ISO3: ").upper()
    while(not(sheet == "Water" or sheet == "Sanitation" or sheet == "Hygiene")):
        if (country == "END" or country == "EXIT"):         #to give an exit option if you cant select sheet
            print("Stopping the program. Seems like it worked!")
            sys.exit()
        print("Datasheet not recognized. Go and try again!")
        sheet = input("Choose Datasheet (Water/Sanitation/Hygiene): ")
    while(year<2000 or year>2020):
        print("Invalid year! Please choose a year between 2000 and 2020.")
        year = int(input("Select the year (2000-2020): "))

#prints all the data for one country
def print_single_country_single_year(country ="Madagascar", year = 2020):
    dfs = dfSanitation
    dfs = dfs[dfs.iloc[:, 0] == country]
    dfs = dfs[dfs.iloc[:, 2] == year]
    print(dfs)

#creates a plot showing one variable for one country over time
def print_single_variable_of_single_country_over_time(variable ="Population (thousands)", country ="Madagascar"):
    dfs = dfSanitation
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

#creates a plot comparing one variable of one country against the average over time
def lineplotSingleVariableOverTime(variable ="Population (thousands)", nations =['Madagascar']):
    averages = getAverageOverTime(variable=variable)
    frames = [averages]
    for nation in nations:
        frames.append(getDataForNation(variable=variable, nation=nation))
    result = pd.concat(frames)
    sns.lineplot(data=result, x="year", y=variable, hue="country").set_xticks(range(2000, 2021))
    plt.show()

def barplotSingleVariableOverTime(variable="Popluation (thousands)", nations=["Madagascar"]):
    averages = getAverageOverTime(variable=variable)
    frames = [averages]
    for nation in nations:
        frames.append(getDataForNation(variable=variable, nation=nation))
    result = pd.concat(frames)
    sns.barplot(data=result, x="year", y=variable, hue="country")
    plt.show()

def scatterplotDifferentVariables(varX="Population (thousands)", varY="% at least basic national sanitation", nation="Madagascar"):
    xAxis = getDataForNation(variable=varX, nation=nation)
    yAxis = getDataForNation(variable=varY, nation=nation)
    sns.scatterplot(x=xAxis.iloc[:, 0], y=yAxis.iloc[:, 0])
    if(varX=="Year"):
        plt.xticks(range(2000, 2021))
    plt.title(nation)
    plt.show()

def scatterplotThreeVariables(varX="Population (thousands)",
                              varY="% at least basic national sanitation",
                              varZ="Sewer connections urban Proportion of population using improved sanitation facilities (including shared)",
                              nation="Madagascar"):
    xAxis = getDataForNation(variable=varX, nation=nation)
    yAxis = getDataForNation(variable=varY, nation=nation)
    zAxis = getDataForNation(variable=varZ, nation=nation)
    sns.scatterplot(x=xAxis.iloc[:, 0], y=yAxis.iloc[:, 0], size=zAxis.iloc[:, 0])
    if(varX=="Year"):
        plt.xticks(range(2000, 2021))
    plt.title(nation)
    plt.show()


#returns a dataframe containing the average worldwide values per year
def getAverageOverTime(variable = "Population (thousands)"):
    dfs = dfSanitation
    averages = []
    for year in range(2000, 2021):
        tempAverages = dfs[dfs.iloc[:, 2] == year]
        tempAverages = tempAverages.iloc[:, variables_sanitation[variable]]
        tempAverages = sum(tempAverages)/len(tempAverages)
        averages.append(tempAverages)
    list = ["average" for i in range(0, 21)]
    dfAverages = pd.DataFrame(data=averages)
    dfAverages["line"] = list
    dfAverages["year"] = range(2000, 2021)
    dfAverages.columns = [variable, 'country', 'year']
    return dfAverages

#return a dataframe containing the data for a single nation for a single variable over time
def getDataForNation(variable="Population (thousands)", nation="Madagascar"):
    dfs = dfSanitation
    data = dfs[dfs.iloc[:, 0] == nation]
    data = data.iloc[:, variables_sanitation[variable]]
    list = [nation for i in range(0, 21)]
    df = pd.DataFrame(data=data)
    df["country"] = list
    df["year"] = range(2000, 2021)
    df.columns = [variable, 'country', 'year']
    return df

#creates csv files from excelfiles
def excel_to_csv():
    read_file = pd.read_excel('WHS_11_08_2021.xlsx', sheet_name='Sanitation')
    read_file.to_csv(r'C:\Users\schoe\PycharmProjects\testing\Sanitation_12_08_2021.csv', index = None, header=True)


#currently cleans sanitation, dont use unless new copy of sanitation
def clean_data():
    global dfSanitation
    dfSanitation = dfSanitation.replace("<1", "0.1")
    dfSanitation = dfSanitation.replace(">99", "99.9")
    dfSanitation = dfSanitation.replace("-", "0")
    dfSanitation.to_csv("Sanitation_12_08_2021.csv")

#pretty much the main function, but havent googled yet on how to do it properly
def run_program():
    initialize_global_variables()
    #copy_excel_file()
    #get_user_input()
    #print_single_country(year=2005)
    #print_single_variable_over_time()
    lineplotSingleVariableOverTime(nations=["Germany", "Switzerland", "Madagascar", "Russian Federation"], variable="Population (thousands)")
    #barplotSingleVariableOverTime(nations=["Germany", "Switzerland", "Madagascar", "Russian Federation"], variable="Population (thousands)")
    #scatterplotDifferentVariables(varX="Year",varY="Sewer connections urban Proportion of population using improved sanitation facilities (including shared)",nation="Madagascar")
    #scatterplotThreeVariables()
    #getAverageOverTime()
    #excel_to_csv()
    #clean_data()
    #dfs = dfSanitation
    #print(type(dfs.iloc[38][6]))

run_program()