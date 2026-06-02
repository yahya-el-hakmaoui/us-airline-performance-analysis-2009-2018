# Author: TAHA 
#lire CSV

import pandas as pd

df = pd.read_csv("data/raw/2015.csv")

# checking the dataset:lignes,colonnes,types

print(df.shape)
print(df.info())
print(df.head())

# profiling

# FIX: nouveau import compatible
from data_profiling import ProfileReport

profile = ProfileReport(
    df,
    minimal=False
)

# export
profile.to_file(
    "reports/profiling/profiling_2015.html"
)

# Analyse manuelle demandée par le CDC:
#Nulls des causes
cause_cols = [
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

for c in cause_cols:
    print(c, df[c].isna().mean()*100)

#Distribution ARR_DELAY

df["ARR_DELAY"].describe()

# FIX: création de la colonne manquante ARR_DEL15
df["ARR_DEL15"] = (df["ARR_DELAY"] > 15).astype(int)

#Vérification ARR_DEL15

errors = df[
    (
        (df["ARR_DELAY"] > 15)
        &
        (df["ARR_DEL15"] != 1)
    )
]

print(errors.shape)