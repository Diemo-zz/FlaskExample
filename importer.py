import pandas as pd

input = read_csv("Adressen__Berlin.csv")

columns_to_keep = [s for s in input.columns if len(input[s].unique())>1] #  Assumption that columns with only a single entry or with no entries don't contain any useful information

df_to_store = input[columns_to_keep]

