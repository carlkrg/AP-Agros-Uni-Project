import pandas as pd
import requests
import numpy as np
import os
import seaborn as sns
from matplotlib import pyplot as plt


class Group01:
    """
    A class representing agricultural output of several countries.

    Attributes:
        name (str): The name of the object.
    """

    def __init__(self, name: str):
        """
        Initialize the object with the given name.

        Args:
           name (str): The name of the object.
        """
        self.name = name
        self.df = None

    def get_data(self):
        """
        This method downloads a CSV file containing agricultural total factor productivity data from
        this Github repository (https://github.com/owid/owid-datasets/tree/master/datasets) and
        saves it into a downloads/ directory in the root directory of the project (main project
        directory). If the data file already exists, the method does not download it again. The
        method also reads the dataset into a pandas DataFrame, which is stored as an attribute of
        the class. If the DataFrame already exists (i.e., has already been loaded), the method does
        not reload it.

        Returns:
            None

        Raises:
            Exception: If there is an error while downloading the data file

        Example usage:
            my_object = MyClass()
            my_object.get_data()
        """

        URL = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/Agricultural%20total%20factor%20productivity%20(USDA).csv"

        if os.path.exists("downloads"):  # check if the downloads directory exists
            print("downloads directory already exists")
        else:
            print("creating downloads directory...")
            os.mkdir("downloads")  # create a downloads directory

        if os.path.exists("downloads/data.csv"):  # check if the data file exists
            print("data file already exists")
        else:
            print("downloading data file...")
            try:
                response = requests.get(URL)  # get the data from url
            except Exception as e:
                print("Error: unable to download data file")
                print(e)
                return
                # exit the method

            print("saving data into file ... downloads/data.cs")
            open("downloads/data.csv", "w").write(
                response.text
            )  # write the data to a csv file

        if self.df is None:
            print("reading data file into pandas dataframe...")
            self.df = pd.read_csv(
                "downloads/data.csv"
            )  # read the data into a pandas dataframe

    def get_countries(self) -> list:
        """
        Returns a list of available countries in the dataset.

        If the dataframe is not available, the method will first call the `get_data` method to
        download and read the dataset into the `df` attribute. Then it returns a list of unique
        countries in the 'Entity' column.

        Returns:
            A list of available countries in the dataset.
        """
        if self.df is None:
            self.get_data()  # check if df is available
        return self.df["Entity"].unique().tolist()  # return all countries in a list

    def plot_quantity(self):
        """
        Plots a heatmap of the correlation between all the columns in the Pandas DataFrame that end with the string '_quantity'.

        If the DataFrame does not exist as an attribute of the class instance, the method calls the 'get_data()' method to obtain the data.

        The method creates an empty list called 'plotted_columns', and loops through each column in the DataFrame, checking if the column name ends with the string '_quantity'. If a column name ends with '_quantity', the name is appended to the 'plotted_columns' list.

        Finally, the method calls the 'heatmap()' function from the seaborn library on the 'plotted_columns' data in the DataFrame, and displays the heatmap plot using 'plt.show()'.
        """
        if self.df is None:
            self.get_data()

        plotted_columns = []

        for column in self.df.columns:
            if column.endswith("_quantity"):
                plotted_columns.append(column)

        sns.heatmap(self.df[plotted_columns].corr())
        plt.show()

    def plot_area_chart(self, country: str, normalize: bool) -> None:
        """
        Plots an area chart of the distinct "_output_" columns for the given country.

        If the dataframe is not available, the method will first call the `get_data` method to
        download and read the dataset into the `df` attribute.

        Raises:
            Exception: If one or less columns with the "_output_" suffix are available or if the
            given country does not exist

        Returns:
            An area chart of the distinct "_output_" columns for the given country.
        """

        if self.df is None:
            self.get_data()

        # Get all columns with "_quantity" suffix and check if there are enough columns
        column_names = self.df.columns.tolist()
        df_subset = [c for c in column_names if "_output_" in c]
        df_subset.append("Year")
        if len(df_subset) < 2:
            raise Exception("Not enough columns with '_output' suffix")

        # Plotting function
        def country_plot(df_temp):
            norm = ""
            if normalize:
                df_temp["Total"] = (df_temp.iloc[:, :-1]).sum(axis=1)
                df_temp.iloc[:, :-2] = (
                    df_temp.iloc[:, :-2].div(df_temp.Total, axis=0) * 100
                )
                norm = "% (Normalized)"
            for each in df_subset[:-1]:
                plt.fill_between(df_temp.Year, df_temp[each], alpha=0.4)
                plt.plot(df_temp.Year, df_temp[each], label=each, alpha=0.4)
            plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
            plt.tick_params(labelsize=12)
            plt.xlabel("Year", size=12)
            plt.ylabel(("Counsumption" + norm), size=12)
            plt.ylim(bottom=0)
            plt.show()

        # Plotting for all countries or a specific country
        if (country is None) | (country == "World"):
            df_temp = self.df[df_subset]
            country_plot(df_temp)
        elif country in self.get_countries():
            df_temp = self.df[self.df["Entity"] == country]
            df_temp = df_temp[df_subset]
            country_plot(df_temp)
        else:
            raise ValueError("Country does not exist")

    def plot_country_chart(self, args: list) -> None:
        """
        Plots the total of the _output_ values of each selected country on the same chart with the
        X-axis being the Year.

        Raises:
            Exception: If the input is not a string or a list of strings

        Returns:
            None.
        """
        title = "Plot of total _output_ values of "

        if self.df is None:
            self.get_data()  # check if df is available
        # Get all columns with "_output"
        column_names = self.df.columns.tolist()
        df_subset = [c for c in column_names if "_output_" in c]
        df_subset.append("Year")

        def country_plot(country):
            df_temp = self.df[self.df["Entity"] == country]
            df_temp = df_temp[df_subset]
            df_temp["Total"] = (df_temp[:-1]).sum(axis=1)
            plt.plot(df_temp["Year"], df_temp["Total"], label=country)
            plt.legend()

        if isinstance(args, str):  # pass a string
            if args in self.get_countries():
                country_plot(args)
                title += args
            else:
                raise ValueError("Country does not exist")
        elif all(isinstance(each, str) for each in args):  # list
            for each in args:
                if each in self.get_countries():
                    country_plot(each)
                    title += each + ", "
                else:
                    raise ValueError("Country does not exist")
        else:
            raise ValueError("Please pass a country string or countries list")

        plt.title(title)
        plt.show()

    def gapminder(self, year: int) -> None:
        """
        Visualize Gapminder data for a specific year.

        Parameters
        ----------
        year : int
            The year for which to visualize the data.

        Raises
        ------
        TypeError
            If the received argument is not an int or if it's negative.
        ValueError
            If the year is not present in the dataset.

        Returns
        -------
        None
        """
        if not isinstance(year, int) or year < 0:
            raise TypeError("Please pass a positive integer for year")

        if self.df is None:
            self.get_data()  # check if df is available

        if year not in self.df["Year"].unique():
            raise ValueError(f"{year} is not present in the dataset")

        # Increase the graph size
        plt.figure(dpi=150)

        # Filter data by year
        year_data = self.df[self.df["Year"] == year]

        # Store animal_output_quantity as a numpy array: np_pop
        # Exploratory analysis showed that animal_output_quantity is the most relevant variable
        # regarding their correlation with fertilizer_quantity and output_quantity
        np_pop = np.array(year_data["animal_output_quantity"])
        np_pop2 = np_pop * 2

        # Create a scatter plot
        sns.scatterplot(
            x="fertilizer_quantity",
            y="output_quantity",
            data=year_data,
            legend=False,
            size=np_pop2,
            sizes=(20, 400),
            alpha=0.5,
        )

        # Use seaborn scatterplot for better customization
        plt.grid(True)
        plt.xlabel("fertilizer_quantity", fontsize=14)
        plt.ylabel("output_quantity", fontsize=14)
        plt.title("Gapminder agriculture", fontsize=20)
        plt.show()
