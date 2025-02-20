from datetime import datetime
import pandas as pd 
import time

agesuitability = 'Age requirements.xlsx'
df = pd.read_excel(agesuitability, usecols="C, E")
df["Course code"] = df["Course code"].str.strip()
df_indexed = df.set_index("Course code")

course = "OC08LF1A013P"


age_requirement = df_indexed.loc[course, 'Age suitable']

print (age_requirement)