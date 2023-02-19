import pandas as pd


class Group01:
    def __init__(self, name: str):
        self.name = name
        self.df = None

    """
    This method will download the data file into a downloads/ directory in the root directory of the project (main project directory). If the data file already exists, the method will not download it again.
    This method must also read the dataset into a pandas dataframe which is an attribute of your class.
    """

    def get_data(self):
        pass

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
            self.get_data() #check if df is available
        return self.df["Entity"].unique().tolist() #return all countries in a list

    """
    Develop a third method that plots a way to correlate the "_quantity" columns.
    """

    def quantity_corr(self, df: pd.DataFrame) -> None:
        pass

    """
    Develop a fourth method that plots an area chart of the distinct "_output_" columns.
    This method should have two arguments: a country argument and a normalize argument.
    The former, when receiving NONE or 'World' should plot the sum for all distinct countries.
    The latter, if True, normalizes the consumption in relative terms: each year, consumption should always be 100%. The X-axis should be the Year.
    The method should return a ValueError when the chosen country does not exist.
    """

    def plot_area_chart(self, country: str, normalize: bool) -> None:
        pass

    """
    Develop a fifth method that may receive a string with a country or a list of country strings.
    This method should compare the total of the "_output_" columns for each of the chosen countries and plot it, so a comparison can be made.
    The X-axis should be the Year.
    """

    def plot_area_chart(self, country: str = None, countries: list = None) -> None:

        if country & countries:  # pass a string
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
