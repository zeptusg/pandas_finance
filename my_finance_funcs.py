import pandas as pd
import plotly.express as px
import sys


def get_dataframe_time_indexed(path) -> pd.DataFrame:
    """
    Helper function to turn a 'path to csv file' - to a DataFrame with 'TIMESTAMP' as 1. its index  2. a datetime type
    :param path: path to csv file
    :return: a DataFrame indexed by 'TIMESTAMP' - a datetime value
    """
    return pd.read_csv(path, parse_dates=["TIMESTAMP"], index_col="TIMESTAMP")


def get_daily_average(df: pd.DataFrame) -> pd.Series:
    """
    :param df: DataFrame indexed by 'TIMESTAMP' - a datetime value
    :return: A series of daily averages
    """
    return df["close"].resample("1D").mean()


def get_daily_high_low(df: pd.DataFrame) -> pd.DataFrame:
    """
    :param df: Path to csv file
    :return: A DataFrame with highest and lowest price of each day
    """
    return df[["high", "low"]].resample("1D").agg({"high": "max", "low": "min"})


def get_graph_by_date(df: pd.DataFrame, date: str):
    """
    Opens a window to a graph describing price change at a given date.
    -May issue a warning because given date is not in a specific format, pandas infers the format.
    :param df: DataFrame indexed by 'TIMESTAMP' - a datetime value
    :param date: Date we want to graph
    """
    df_date_specific = df.loc[date]
    px.line(data_frame=df_date_specific, x=df_date_specific.index, y=["close"]).show()


def main():
    # If given path has no data within certain day, after downsampling to frequency of 1 day, this day will be 'NaN'.
    # Depends on the need, we can drop the 'Nan' values or fill them by a desired pattern.

    path = "gbpusd_sample.csv" if len(sys.argv) == 1 else sys.argv[1]

    df = get_dataframe_time_indexed(path)
    daily_average_series = get_daily_average(df)
    daily_high_and_low_df = get_daily_high_low(df)

    # 1. print series of daily average prices.
    print("Daily average prices -")
    print(daily_average_series)
    # 2. print DateFrame of daily highest and lowest price.
    print("Daily highest and lowset price -")
    print(daily_high_and_low_df)

    # 3. draw a graph for 26/02/2018 price change.
    get_graph_by_date(df, r"26/02/2018")

    input("Press Enter to continue")


if __name__ == "__main__":
    main()
