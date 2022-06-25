import pandas as pd
import glob

def pull_data(path):

    filenames = glob.glob(path + "\*.csv")
    dfs = []
    for file in filenames:
        # reading csv files
        dfs.append(pd.read_csv(file, header=3, index_col=False))

    big_data = pd.concat(dfs, ignore_index=True)

    col_names = list(big_data)

    if 'Unnamed: 0' in col_names:
        dfs = []
        for file in filenames:
            # reading csv files
            dfs.append(pd.read_csv(file, header=4, index_col=False))

        big_data = pd.concat(dfs, ignore_index=True)

    #big_data = big_data.apply(pd.to_numeric)

    return big_data


def get_quantiles(path):

    filenames = glob.glob(path + "\*.csv")
    df = pd.read_csv(filenames[0], header = 2, on_bad_lines = 'skip')
    q = list(df)
    q = q[1:10]
    q = [float(i) for i in q]

    return q