# %%
import pandas as pd
import numpy as np

data = pd.read_table(
    "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/manuscript//radius_0.5_level_set_epsilon_0.011257.txt", sep=",", header=0, index_col=None)

print(data.head())

# %%
times = [0, 0.01, 0.1, 1, 10]
radii = [0.0900, 0.1200]
small_data = data.loc[(data.time.isin(times)) &
                      (data.R0.isin(radii))]
# %%
for time in times:
    print(time)
    r09 = small_data.loc[(small_data.time == time) & (
        small_data.R0 == 0.09), "radius"].values[0]
    r12 = small_data.loc[(small_data.time == time) & (
        small_data.R0 == 0.12), "radius"].values[0]
    print("R0 = 0.09: " + str(r09))
    print("R0 = 0.12: " + str(r12))
    print("Ratio: " + str(r09/r12))

# %%
