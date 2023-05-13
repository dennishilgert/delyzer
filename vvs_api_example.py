import pandas as pd

stations_df = pd.read_csv('vvs_data.csv')
stations_result = stations_df.loc[stations_df['Name mit Ort'].str.contains('Stadtmitte')]

stations_info_df = pd.read_csv('vvs_haltestellen.csv', sep=';', encoding='cp1252')
stations_info_result = stations_info_df.loc[stations_info_df['Linien (EFA)'].str.contains('S1')]
stations_info_result['Nummer'] = stations_info_result['Nummer'].apply(lambda nummer: 5000000 + nummer)

print(stations_info_result)

