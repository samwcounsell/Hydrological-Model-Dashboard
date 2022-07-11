import pandas as pd
import glob

# Function to pull all data from user inputted file path
def pull_data(path):

    filenames = glob.glob(path + "\*.csv")
    dfs = []
    for file in filenames:
        # reading csv files
        dfs.append(pd.read_csv(file, header=3, index_col=False))

    big_data = pd.concat(dfs, ignore_index=True)

    col_names = list(big_data)

    # Allows for row below meta-data to not be empty (,,,,,,,,) and still read data correctly
    if 'Unnamed: 0' in col_names:
        dfs = []
        for file in filenames:
            # reading csv files
            dfs.append(pd.read_csv(file, header=4, index_col=False))

        big_data = pd.concat(dfs, ignore_index=True)


    return big_data

# Pull quantiles from meta-data (1, 5, 10, 30, 50, 70, 90, 95, 99)
def get_quantiles(path):

    filenames = glob.glob(path + "\*.csv")
    df = pd.read_csv(filenames[0], header=2, on_bad_lines='skip')
    q = list(df)
    q = q[1:10]
    q = [float(i) for i in q]

    return q