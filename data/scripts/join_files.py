"""Join csv files into only one with unique urls"""
import os
import pandas as pd


def list_csv_files(path):
    """List csv files in a path

    Args: path - path to the directory containing the csv files

    Returns: list of strings with filename
    """
    csv_list = []
    for filename in os.listdir(path):
        if filename.endswith("csv"):
            csv_list.append(filename)

    return csv_list


def concat_files(directory_list, unique_column="url"):
    """concatenate all CSV into one dataframe with unique values in one column

    Args: directory_list: list of directories containing csv files to be joined

    Returns: Pandas DataFrame object
    """

    data = None
    for directory in directory_list:
        print("Joining from {}".format(directory))
        csv_files = list_csv_files(directory)
        for filename in csv_files:
            filename_with_path = os.path.join(directory, filename)
            this_data = pd.read_csv(filename_with_path)
            this_data.columns = [c.strip() for c in this_data.columns]
            if data is None:
                data = this_data
            else:
                data = pd.concat([data, this_data])

    return data.drop_duplicates(unique_column)


if __name__ == '__main__':
    dataset = concat_files(["../GoogleNews", "../Webhose"])
    dataset.to_csv("news_articles_joined")
