import pandas as pd
import sqlite3

df = pd.read_csv('Apr2.csv').head(1)
df_tr = df.transpose()
print(df_tr)

df_tr = df_tr.str.contains("twitter.com") == False
print(df_tr)

#conn = sqlite3.connect('UnprocessedLinks')
#c = conn.cursor()

#df_tr.to_sql(name='UnprocessedLinks', con=conn)