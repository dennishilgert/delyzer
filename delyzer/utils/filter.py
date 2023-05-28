import pandas as pd
import datetime
import logging

logger = logging.getLogger(__name__)

class Filter:

    def by_line(delay_df:pd.DataFrame, line, direction):
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

    def join_station_name(delay_df:pd.DataFrame):
        stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')

        delay_df = delay_df.set_index("station_id")

        delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

        return delay_df

    def delay_at_station(delay_df:pd.DataFrame):
        
        delay_df = delay_df.groupby(['station_id'], as_index=False).agg({'delay': 'mean'}).round(2)
        #delay_series = delay_series.sort_values('delay')


        if not delay_df.empty:

            delay_df = Filter.join_station_name(delay_df)
        
            delay_df = delay_df[['Name mit Ort', 'delay']]
        

            delay_df = delay_df.sort_values('delay', ascending=False)

        return delay_df
    
    def propability_at_station(delay_df:pd.DataFrame) -> pd.DataFrame:
        
        delay_series = delay_df.groupby(['station_id'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)

        delay_df = pd.DataFrame(delay_series)

        if not delay_df.empty:

            delay_df = Filter.join_station_name(delay_df)
        
            delay_df = delay_df[['Name mit Ort', 'delay']]
        

            delay_df = delay_df.sort_values('delay', ascending=False)

        return delay_df
        
    def propability_of_line(delay_df:pd.DataFrame):
        
        delay_series = delay_df.groupby(['line_number','direction'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)
        delay_df = pd.DataFrame(delay_series).sort_values('delay', ascending=False)


        return delay_df