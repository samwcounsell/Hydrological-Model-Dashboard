import pandas as pd
import glob

def pull_data():
    path = 'data'
    #path = r'C:\Users\samwc\Desktop\New'
    filenames = glob.glob(path + "\*.csv")
    dfs = []
    for file in filenames:
        # reading csv files
        dfs.append(pd.read_csv(file, header=3, index_col=False))

    big_data = pd.concat(dfs, ignore_index=True)

    return big_data