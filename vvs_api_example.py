from vvspy import get_departures
import pandas as pd

stations_df = pd.read_csv('vvs_data.csv')
stations_result = stations_df.loc[stations_df['Name mit Ort'].str.contains('Stadtmitte')]
#print(stations_result)
