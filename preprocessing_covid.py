import pandas as pd
import numpy as np
import datetime as dt

def general_clean(df):
    """
    Function for a basic cleaning of the raw dataframe
    """

    g1columns = ['iso_code', 'continent', 'location', 'date',
             'new_cases', 'new_deaths', 'new_cases_per_million', 'new_deaths_per_million',
             'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million',
             'total_vaccinations', 'new_vaccinations', 'people_vaccinated_per_hundred',
             'population','gdp_per_capita', 'human_development_index']

    df = df[g1columns]

    # Cleaning date
    df['date'] = df.date.apply(pd.to_datetime)

    # Cleaning rows
    row_cleaner = [ 'Africa', 'Asia', 'Central African Republic', 
                    'World', 'Europe', 'Oceania', 'South America', 
                    'European Union', 'Anguilla', 'Bosnia and Herzegovina',
                    'Brunei', 'Chad', 'Comoros', 'Djibouti', 'Equatorial Guinea',
                    'Eritrea', 'Eswatini','Gabon', 'Greenland', 'Grenada',
                    'Lesotho', 'Malawi', 'Micronesia (country)', 'Saint Helena', 
                    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
                    'Seychelles', 'Turks and Caicos Islands' ]

    return df[ ~df.location.isin(row_cleaner) ]

def europe_cleaning(df, pop = 5000000):
    """
    Function for a cleaning in the european countries 
    """

    # Doing Basic cleaning:
    df = general_clean(df)

    # Filtering: 
    df = df[ df.continent == 'Europe']

    # Keeping values with no NaN values in gdp:
    df = df[ ~df.gdp_per_capita.isna() ]

    # Keeping population over 5Mill
    df = df[df.population >= pop]

    # Cleaning negative values
    df = df[df.new_cases >= 0]
    df = df[df.new_deaths >= 0]

    # --- Preparing exports ---

    # Cases historical
    dfc = df[['iso_code', 'location', 'date','new_cases', 'new_deaths', 'new_cases_per_million', 'new_deaths_per_million', 
            'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million', 
            'population','gdp_per_capita', 'human_development_index']]

    dfc = dfc.sort_values(by=['location', 'date'])

    # Vaccination:
    dfvac = df[~df.total_vaccinations.isna()]

    dfvac = dfvac[['iso_code', 'location', 'date', 'total_vaccinations', 'new_vaccinations', 
                'people_vaccinated_per_hundred', 'population','gdp_per_capita', 'human_development_index']]

    dfvac = dfvac.sort_values(by=['location', 'date'])

    # Exporting:
    #dfc.to_csv('Data/preprocessed_cases_country.csv', index = False)
    #dfvac.to_csv('Data/preprocessed_vaccination_country.csv', index = False)

    return dfc, dfvac

def continent_cleaning(df):

    continents = ['Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania']

    dfcont = df[ df.location.isin(continents) ]

    # Cases Historical
    dfhist = dfcont[['location', 'date','new_cases', 'new_deaths', 'new_cases_per_million', 'new_deaths_per_million', 
                    'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million']]

    dfhist = dfhist.sort_values(by=['location', 'date'])

    dfhist.to_csv('Data/preprocessed_cases_continents.csv', index = False)

    # Vaccination:
    dfvaccont = dfcont[~dfcont.total_vaccinations.isna()]

    dfvaccont = dfvaccont[['location', 'date', 'total_vaccinations', 'new_vaccinations', 'people_vaccinated_per_hundred']]

    dfvaccont = dfvaccont.sort_values(by=['location', 'date'])

    dfvaccont.to_csv('Data/preprocessed_vaccination_continents.csv', index = False)


# Importing Data
df = pd.read_csv('Data/owid-covid-data.csv')

"""
Running Cleaning:
"""
europe_cleaning(df)
continent_cleaning(df)





