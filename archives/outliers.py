#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data/datasetv1.csv')
df.set_index('id', inplace=True)
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)

IQR = Q3 - Q1

print(IQR)

df_out = df.drop(df[df.commits < 30].index)

print(df_out.shape)
df_out.drop_duplicates(subset="link",
                     keep='first', inplace=True)
df_out.reset_index(drop = True, inplace=True)
df_out.to_csv('data/datasetv2.csv')
print(df_out.shape)

