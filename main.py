import pandas as pd
import dgrm

from enum import Enum

class Sheet(Enum):
    WATER = 0
    SANITATION = 1
    HYGIENE = 2


# initializes all variables, that are needed throughout a lot of functions
def initialize_global_variables():
    # variables_sanitation is a dictionary mapping each variable from the sanitation datasheet to
    # its column index in the datasheet, to have easy integerbased access to the column
    global variables_sanitation
    variables_sanitation = {
        "Country": 0, "ISO3": 1, "Year": 2, "Population (thousands)": 3,
        "% urban population": 4, "% at least basic national sanitation": 5,
        "limited (shared) national sanitation": 6, "unimproved national sanitation": 7,
        "open defecation national sanitation": 8, "annual rate of change in basic national sanitation": 9,
        "annual rate of change in open national defecation": 10, "at least basic rural sanitation": 11,
        "limited (shared) rural sanitation": 12, "unimproved rural sanitation": 13,
        "open defecation rural sanitation": 14, "annual rate of change in basic rural sanitation": 15,
        "annual rate of change in open rural defecation": 16, "at least basic urban sanitation": 17,
        "limited (shared) urban sanitation": 18, "unimproved urban sanitation": 19,
        "open defecation urban sanitation": 20, "annual rate of change in basic urban sanitation": 21,
        "annual rate of change in open urban defecation": 22,
        "Safely managed national Proportion of population using improved sanitation facilities (excluding shared)": 23,
        "Disposed in situ national Proportion of population using improved sanitation facilities (excluding shared)": 24,
        "Emptied and treated national Proportion of population using improved sanitation facilities (excluding shared)": 25,
        "Wastewater treated national Proportion of population using improved sanitation facilities (excluding shared)": 26,
        "annual rate of change in safely mangaged national Proportion of population using improved sanitation facilities (excluding shared)": 27,
        "Latriness and other national Proportion of population using improved sanitation facilities (including shared)": 28,
        "Septic tanks national Proportion of population using improved sanitation facilities (including shared)": 29,
        "Sewer connections national Proportion of population using improved sanitation facilities (including shared)": 30,
        "Safely managed rural Proportion of population using improved sanitation facilities (excluding shared)": 31,
        "Disposed in situ rural Proportion of population using improved sanitation facilities (excluding shared)": 32,
        "Emptied and treated rural Proportion of population using improved sanitation facilities (excluding shared)": 33,
        "Wastewater treated rural Proportion of population using improved sanitation facilities (excluding shared)": 34,
        "Annual rate of change in safely managed rural Proportion of population using improved sanitation facilities (excluding shared)": 35,
        "Latriness and other rural Proportion of population using improved sanitation facilities (including shared)": 36,
        "Septic tanks rural Proportion of population using improved sanitation facilities (including shared)": 37,
        "Sewer connections rural Proportion of population using improved sanitation facilities (including shared)": 38,
        "Safely managed urban Proportion of population using improved sanitation facilities (excluding shared)": 39,
        "Disposed in situ urban Proportion of population using improved sanitation facilities (excluding shared)": 40,
        "Emptied and treated urban Proportion of population using improved sanitation facilities (excluding shared)": 41,
        "Wastewater treated urban Proportion of population using improved sanitation facilities (excluding shared)": 42,
        "Annual rate of change in safely managed urban Proportion of population using improved sanitation facilities (excluding shared)": 43,
        "Latriness and other urban Proportion of population using improved sanitation facilities (including shared)": 44,
        "Septic tanks urban Proportion of population using improved sanitation facilities (including shared)": 45,
        "Sewer connections urban Proportion of population using improved sanitation facilities (including shared)": 46,
        "SDG region": 47, "WHO region": 48, "UNICEF Programming region": 49, "UNICEF Reporting region": 50
    }

    # variables_water is a dictionary mapping each variable from the water datasheet to
    # its column index in the datasheet, to have easy integerbased access to the column
    global variables_water
    variables_water = {"Country": 0, "ISO3": 1, "Year": 2, "Population (thousands)": 3, "% urban population": 4,
                       "at least basic national water": 5, "limited national water": 6, "unimproved national water": 7,
                       "surface water national": 8, "annual rate of change in basic national water": 9,
                       "at least basic rural water": 10, "limited rural water": 11, "unimproved rural water": 12,
                       "surface water rural": 13, "annual rate of change in basic rural water": 14,
                       "at least basic urban water": 15, "limited urban water": 16, "unimproved urban water": 17,
                       "surface water urban": 18, "annual rate of change in basic urban water": 19,
                       "safely managed national proportion of population using improved water supplies": 20,
                       "accessible on premises national proportion of population using improved water supplies": 21,
                       "available when needed national proportion of population using improved water supplies": 22,
                       "free from contamination national proportion of population using improved water supplies": 23,
                       "annual rate of change in safely managed national proportion of population using improved water supplies": 24,
                       "piped national proportion of population using improved water supplies": 25,
                       "non-piped national proportion of population using improved water supplies": 26,
                       "safely managed rural proportion of population using improved water supplies": 27,
                       "accessible on premises rural proportion of population using improved water supplies": 28,
                       "available when needed rural proportion of population using improved water supplies": 29,
                       "free from contamination rural proportion of population using improved water supplies": 30,
                       "annual rate of change in safely managed rural proportion of population using improved water supplies": 31,
                       "piped rural proportion of population using improved water supplies": 32,
                       "non-piped rural proportion of population using improved water supplies": 33,
                       "safely managed urban proportion of population using improved water supplies": 34,
                       "accessible on premises urban proportion of population using improved water supplies": 35,
                       "available when needed urban proportion of population using improved water supplies": 36,
                       "free from contamination urban proportion of population using improved water supplies": 37,
                       "annual rate of change in safely managed urban proportion of population using improved water supplies": 38,
                       "piped urban proportion of population using improved water supplies": 39,
                       "non-piped urban proportion of population using improved water supplies": 40,
                       "SDG region": 41, "WHO region": 42, "UNICEF programming region": 43,
                       "UNICEF reporting region": 44
                       }

    # variables_hygiene is a dictionary mapping each variable from the hygiene datasheet to
    # its column index in the datasheet, to have easy integerbased access to the column
    global variables_hygiene
    variables_hygiene = {"Country": 0, "ISO3": 1, "Year": 2, "Population (thousands)": 3, "% urban population": 4,
                         "basic national hygiene": 5, "limited national hygiene": 6, "no facility national hygiene": 7,
                         "annual rate of basic change in national hygiene": 8, "basic rural hygiene": 9,
                         "limited rural hygiene": 10, "no facility rural hygiene": 11,
                         "annual rate of change in basic rural hygiene": 12, "basic urban hygiene": 13,
                         "limited urban hygiene": 14, "no facility urban hygiene": 15,
                         "annual rate of change in basic urban sanitation": 16, "SDG region": 17, "WHO region": 18,
                         "UNICEF programming region": 19, "UNICEF reporting region": 20
                         }

    read_data()


# reads all the necessary data from csv files
def read_data():
    global dfWater
    global dfSanitation
    global dfHygiene
    dfWater = pd.read_csv("Water_28_09_2021.csv", header=None)
    dfSanitation = pd.read_csv("Sanitation_28_09_2021.csv", header=None)
    dfHygiene = pd.read_csv("Hygiene_28_09_2021.csv", header=None)

# prints every country
def print_nations():
    print(dfSanitation.iloc[:, 0].unique().tolist())
    print("Just type any country that you want. Make sure it's spelled correctly.")

# prints every variable from every sheet
def print_variables():
    print("Variables from the sanitation sheet:")
    for key in variables_sanitation.keys():
        print(key)
    print("Variables from the water sheet:")
    for key in variables_water.keys():
        print(key)
    print("Variables from the hygiene sheet:")
    for key in variables_hygiene.keys():
        print(key)
    print("Just type any variable that you want. You don't have to specify the sheet it's from. Make sure it's spelled correctly.")

# responsible for the CLI so that the user can select all the variables for a diagram
def get_user_input(diag):
    print_nations()
    print_variables()
    type = ""
    while type != "scatterplot" and type != "barplot" and type != "lineplot" and type != "map":
        type = input("Select the type of diagram you want to create. Available are scatterplot, barplot, lineplot and map:").lower()
        if type != "scatterplot" and type != "barplot" and type != "lineplot" and type != "map":
            print("Error: Unrecognized type!")
    variables = []
    if type == "scatterplot":
        count = input("Please choose whether you want two or three variables. The third one would determine the size of each individual point:")
        variables.append(input("Please choose the first variable for the x axis:"))
        variables.append(input("Please choose the second variable for the y axis:"))
        if count == 3 or count == "3":
            variables.append(input("Please choose the third variable for the size:"))
    elif type == "barplot" or type == "lineplot":
        variables.append(input("Please choose the first variable for the x axis:"))
        variables.append(input("Please choose the second variable for the y axis:"))
    elif type == "map":
        variables.append(input("Please choose the variable:"))
        year = input("Please choose the year (2000-2020):")
        diag.create_plot(dgrm.Type.MAP, variable=variables[0], nations=[], year=year)
    nations = []
    if type != "map":
        while nations.__sizeof__() == 0 or nations[-1] != "finished":
            nations.append(str(input("Please select a country you want to add. Type 'finished' when you are finished:")))
        if type == "scatterplot":
            diag.create_plot(dgrm.Type.SCATTER, variables, nations)
        elif type == "barplot":
            diag.create_plot(dgrm.Type.BAR, variables, nations)
        elif type == "lineplot":
            diag.create_plot(dgrm.Type.LINE, variables, nations)



# creates csv files from excelfiles, shouldnt be needed ever again, didnt delete for completeness
def excel_to_csv():
    read_file = pd.read_excel('WHS_11_08_2021.xlsx', sheet_name='Sanitation')
    read_file.to_csv(r'C:\Users\schoe\PycharmProjects\testing\Sanitation_12_08_2021.csv', index=None, header=True)


# currently cleans water, shouldnt be needed ever again, didnt delete for completeness
def clean_data():
    global dfHygiene
    dfHygiene = dfHygiene.replace("<1", "0.1")
    dfHygiene = dfHygiene.replace(">99", "99.9")
    dfHygiene = dfHygiene.replace("-", "0")
    dfHygiene = dfHygiene.fillna(0)
    dfHygiene.to_csv("Hygiene_28_09_2021.csv")


# pretty much the main function, but havent googled yet on how to do it properly
def run_program():
    initialize_global_variables()
    diag = dgrm.Diagram(
        type=dgrm.Type.MAP,
        df_s=dfSanitation,
        df_w=dfWater,
        df_h=dfHygiene,
        var_s=variables_sanitation,
        var_w=variables_water,
        var_h=variables_hygiene
    )
    get_user_input(diag)
    #dgrm.Diagram.create_map(diag)

print('hello')
run_program()
