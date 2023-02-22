import pandas as pd
import requests
import os
import matplotlib.pyplot as plt
import seaborn as sns



class Group01:
    def __init__(self, name: str):
        self.name = name
        self.df = None

    def get_data(self):
        """
        This method downloads a CSV file containing agricultural total factor productivity data from this Github repository
        (https://github.com/owid/owid-datasets/tree/master/datasets) and saves it into a downloads/ directory in the root directory of the project (main project directory).
         If the data file already exists, the method does not download it again. The method also reads the dataset into a pandas DataFrame, which is stored as an attribute of the class.
         If the DataFrame already exists (i.e., has already been loaded), the method does not reload it.

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

    """
    Develop a second method that outputs a list of the available countries in the data set.
    """

    def get_countries(self) -> list:
        """
        Returns a list of available countries in the dataset.

        If the dataframe is not available, the method will first call the `get_data` method to download and
        read the dataset into the `df` attribute. Then it returns a list of unique countries in the 'Entity' column.

        Returns:
            A list of available countries in the dataset.
        """
        if self.df is None:
            self.get_data()  # check if df is available
        return self.df["Entity"].unique().tolist()  # return all countries in a list

    """
    Develop a third method that plots a way to correlate the "_quantity" columns.
    """

    def quantity_corr(self) -> None:
        """
        Returns a correlation list of the "_quantity" columns in the given dataframe and plots a correlation plot.

        If the dataframe is not available, the method will first call the `get_data` method to download and
        read the dataset into the `df` attribute. Then it returns a correlation list of the "_quantity" columns.

        Raises:
            Exception: If one or less columns with the "_quantity" suffix are available

        Returns:
            A correlation list of the "_quantity" columns.
        """
        
        if self.df is None:
            self.get_data()  # check if df is available
        # Get all columns with "_quantity" suffix
        columnNames = self.df.columns.tolist()
        dfSubset = [c for c in columnNames if "_quantity" in c]

        if len(dfSubset) <= 1:
            raise Exception("Not enough columns with '_quantity' suffix")
        else:
            # Subset the dataframe into only those columns with the "_quantity" suffix
            dfTemp = self.df[dfSubset]
            sns.heatmap(dfTemp.corr())
            plt.show()
        #dfTemp.corr().style.background_gradient(cmap='coolwarm').set_precision(2)


    """
    Develop a fourth method that plots an area chart of the distinct "_output_" columns. 
    This method should have two arguments: a country argument and a normalize argument. 
    The former, when receiving NONE or 'World' should plot the sum for all distinct countries. 
    The latter, if True, normalizes the consumption in relative terms: each year, consumption should always be 100%. The X-axis should be the Year. 
    The method should return a ValueError when the chosen country does not exist.
    """

    def plot_area_chart(self, country: str, normalize: bool) -> None:
        
        if self.df is None:
            self.get_data()  # check if df is available
        # Get all columns with "_quantity" suffix
        columnNames = self.df.columns.tolist()
        dfSubset = [c for c in columnNames if "_output_" in c]
        dfSubset.append("Year")

        if (country == None) | (country == "World"):
            dfTemp = self.df[dfSubset]
            #dfTemp = dfTemp.sum(axis=1)
            for each in dfSubset[:-1]:
                if normalize: 
                    dfTemp[each] = dfTemp[each]/dfTemp.groupby("Year")[each].transform(sum)
                dfTemp.plot(kind='area', x='Year', y=each)
                plt.show()
        elif country in self.get_countries():
            dfTemp = self.df[self.df["Entity"] == country]
            dfTemp = dfTemp[dfSubset]
            #dfTemp = dfTemp.sum(axis=1)
            for each in dfSubset[:-1]:
                if normalize: 
                    dfTemp[each] = dfTemp[each]/dfTemp.groupby("Year")[each].transform(sum)
                dfTemp.plot(kind='area', x='Year', y=each)
                plt.show()
        else:
            raise ValueError("Country does not exist")


        

    """
    Develop a fifth method that may receive a string with a country or a list of country strings. 
    This method should compare the total of the "_output_" columns for each of the chosen countries and plot it, so a comparison can be made. 
    The X-axis should be the Year.
    """

    def plot_country_area_chart(self, country: str = None, countries: list = None) -> None:
        if country & countries:  # if both are passed raise an error
            raise ValueError("Please pass a country or countries")
        elif country:  # pass a string
            pass
        elif countries:  # pass a list
            pass
        else:
            raise ValueError("Please pass a country or countries")

    """
    Develop a sixth method that must be called gapminder. This is a reference to the famous gapminder tools. 
    This method should receive an argument year which must be an int. If the received argument is not an int, the method should raise a TypeError. 
    This method should plot a scatter plot where x is fertilizer_quantity, y is output_quantity, 
    and the area of each dot should be a third relevant variable you find with exploration of the data.
    """

    def gapminder(self, year: int, df: pd.DataFrame) -> None:
        if isinstance(year, int):
            pass
        else:
            raise ValueError("Please pass an integer")
