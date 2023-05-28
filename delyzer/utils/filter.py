import pandas as pd


class Filter:

    def by_line(delay_df, line, direction):
        delay_df = pd.DataFrame(delay_df.loc[delay_df['line_number'] == line])
        delay_df = pd.DataFrame(delay_df.loc[delay_df['direction'] == direction])

        return delay_df

    def by_time(delay_df:pd.DataFrame):
        
        delay_df['planned_departure_time'] = delay_df['planned_departure_time'].apply(lambda x: datetime.datetime.combine(datetime.datetime.today(), x))
        delay_df.set_index('planned_departure_time', inplace=True)

        delay_df = delay_df['delay'].resample('30min').mean().round(2).reset_index().ffill()
        
        delay_df.rename(columns={'planned_departure_time':'timeslot_start'}, inplace=True)

        return delay_df
        
    def by_delay(delay_df:pd.DataFrame):
        
        delay_df = delay_df.groupby(['line_number','direction'], as_index=False).agg({'delay': 'mean'}).round(2)
        delay_df = delay_df.sort_values('delay', ascending=False)

        return delay_df

    def join_station_name(delay_series:pd.Series):
        stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')

        delay_df = pd.DataFrame(delay_series)

        delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

        delay_series = pd.Series(delay_df)

        return delay_series

    def delay_at_station(self, delay_df:pd.DataFrame):
        
        delay_df = delay_df.groupby(['station_id'], as_index=False).agg({'delay': 'mean'}).round(2)
        delay_df = delay_df.sort_values('delay', ascending=False)

        delay_series = self.join_station_name(delay_series)

        delay_series = delay_series[['Name mit Ort', 'delay']]
        delay_df = pd.DataFrame(delay_series)

        return delay_df
    
    def propability_at_station(self, delay_df:pd.DataFrame):
        
        delay_series = delay_df.groupby(['station_id'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)
        delay_series = delay_series.sort_values('delay', ascending=False)

        delay_series = self.join_station_name(delay_series)

        delay_series = delay_series[['Name mit Ort', 'delay']]
        
        delay_df = pd.DataFrame(delay_series)

        return delay_df
        
    def propability_of_line(delay_df:pd.DataFrame):
        
        delay_series = delay_df.groupby(['line_number','direction'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)
        delay_series = delay_series.sort_values('delay', ascending=False)

        delay_df = pd.DataFrame(delay_series)

        return delay_df