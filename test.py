import pandas as pd

p = ['gaea', 'gaea']
a = ['gra'] + p
print(a)

df = pd.DataFrame([['BR-vsen_imitation_WP_back', 'io', 'Bool', '%I21.5', '#no - [I21.5] czujnik BR-imitacja WP back', 'True', 'True', 'True', '', '', '']],
                  columns=['Name', 'Path', 'Data Type', 'Logical Address', 'Comment', 'Hmi Visible', 'Hmi Accessible', 'Hmi Writeable', 'Typeobject ID', 'Version ID', 'BelongsToUnit'])

print(df)
df.index.name = 'foo'
df.index += 1
df.to_excel("x:\pandas_to_excel.xlsx", sheet_name='PLC Tags', index=True)
