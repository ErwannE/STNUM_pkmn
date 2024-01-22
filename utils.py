import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

def get_attributes_by_names(list_names, attributes=["Attack", "Defense", "Sp. Atk", "Sp. Def", "HP", "Speed", "Total"]): # list_names is a list of strings
    conn = sqlite3.connect('STNUM_pokemon.db')
    names = ', '.join([f'"{name}"' for name in list_names])
    str_attributes = ', '.join([f'"{attribute}"' for attribute in attributes])
    request = f'SELECT {str_attributes} FROM Pokemon WHERE Name IN ({names})'
    print(request)
    result = pd.read_sql(request, conn)
    return result


def plot_average_attributes(list_names, attributes=["Attack", "Defense", "Sp. Atk", "Sp. Def", "HP", "Speed", "Total"]):
    # Assuming you have already connected to the database and retrieved the Pokemon table as a pandas DataFrame
    pokemon_df = get_attributes_by_names(list_names, attributes)

    # Calculate the average of the attributes
    average_attributes = pokemon_df[attributes].mean()

    # Divide all values in the ""Total" column by 6
    average_attributes["Total"] /= 6

    # Change the index "Total" to "Mean"
    average_attributes.rename(index={"Total": "Mean"}, inplace=True)

    # Plot the average attributes using a bar chart
    plt.bar(average_attributes.index, average_attributes.values)
    plt.xlabel("Attributes")
    plt.ylabel("Average Value")
    plt.title("Average Attributes of Pokemon")
    plt.show()


# Call the function to display the plot
plot_average_attributes(["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Charizard", "Blastoise", "Venusaur"])
