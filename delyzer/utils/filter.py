import pandas as pd
import datetime
import logging

logger = logging.getLogger(__name__)

class Filter:
    """Class Filter
    description:
        * Helper class to filter the delay data.
        * Contains independet functions that return the modified object
    """

    def by_line(delay_df:pd.DataFrame, line:str, direction:str) -> pd.DataFrame:
        """by_line
        description:
            * Filters delay_df by line and direction

        Returns:
            DataFrame: Delay data grouped and ordered by line and direction

        Args:
            delay_df (pd.DataFrame): Delay data
            line (string): Line name
            direction (string): Direction name  
            
        tests:
            * Test if filter by line works
            * test if filter by direction works
            * test if return type is a dataframe
        """
        
        delay_df = pd.DataFrame(delay_df.loc[delay_df['line_number'] == line])
        delay_df = pd.DataFrame(delay_df.loc[delay_df['direction'] == direction])

        return delay_df

    def by_time(delay_df:pd.DataFrame) -> pd.DataFrame:
        """by_time
        description:
            * Filters delay_df by time
            * Returns a DataFrame with 30 min timeslots and the delay
            * Timeslots are are always for the whole day

        Returns:
            DataFrame: Delay data grouped and ordered by time

        Args:
            delay_df (pd.DataFrame): Delay data
            
        tests:
            * Test if filter by time results in 30 min timeslots
            * Test if the 30 min timeslots have relating delays
            * Test if return type is a dataframe
        """
    
        
        delay_df['planned_departure_time'] = delay_df['planned_departure_time'].apply(lambda x: datetime.datetime.combine(datetime.datetime.today(), x))
        delay_df.set_index('planned_departure_time', inplace=True)

        delay_df = delay_df['delay'].resample('30min').mean().round(2).reset_index().ffill()
        
        delay_df.rename(columns={'planned_departure_time':'timeslot_start'}, inplace=True)

        return delay_df
        
    def by_delay(delay_df:pd.DataFrame):
        """by_delay
        description:
            * Filters delay_df by the delay
            * Returns a Dataframe with the average delays of all lines
            * Ordered by delays

        Returns:
            DataFrame: Delay data grouped and ordered by delay

        Args:
            delay_df (pd.DataFrame): Delay data
            
        tests:
            * Test if filter by delay returns the right order by delays
            * Test if every line is just once in the return value
            * Test if return type is a dataframe
        """

        delay_df = delay_df.groupby(['line_number','direction'], as_index=False).agg({'delay': 'mean'}).round(2)
        delay_df = delay_df.sort_values('delay', ascending=False)

        return delay_df

    def join_station_name(delay_df:pd.DataFrame) -> pd.DataFrame:
        """join_station_name
        description:
            * Loads vvs_data.csv
            * Joins station name to delay_df by station_id/Nummer
            * Returns a Dataframe with the joined names at every entry in the DataFrame

        Returns:
            DataFrame: Delay data including the joined names

        Args:
            delay_df (pd.DataFrame): Delay data
            
        tests:
            * Test if join station name returns the same amount of entries as before
            * Test if every entrie of the return value has the column 'Name mit Ort'
            * Test if return type is a DataFrame
        """
        try:
            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            stations_info_df = stations_info_df[['Nummer', "Name mit Ort"]]

        except Exception as e:
            raise e
        
        delay_df = delay_df.set_index("station_id")

        delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

        return delay_df

    def delay_at_station(delay_df:pd.DataFrame) -> pd.DataFrame:
        """delay_at_station
        description:
            * Filters delay_df by the delay and orders by station
            * returns DataFrame including the joined station Name

        Returns:
            DataFrame: Delay data grouped by stations and ordered by delay

        Args:
            delay_df (pd.DataFrame): Delay data
            
        tests:
            * Test if delay_at_station groups the stations right
            * Test if the average delay value is correct
            * Test if every entrie of the return value has the column 'Name mit Ort'
            (* Test if return type is a DataFrame)
        """
        delay_df = delay_df.groupby(['station_id'], as_index=False).agg({'delay': 'mean'}).round(2)
        #delay_series = delay_series.sort_values('delay')


        if not delay_df.empty:

            delay_df = Filter.join_station_name(delay_df)
        
            try:
                delay_df = delay_df[['Name mit Ort', 'delay']]
            except Exception as e:
                raise e
            delay_df = delay_df.sort_values('delay', ascending=False)

        return delay_df
    
    def propability_at_station(delay_df:pd.DataFrame) -> pd.DataFrame:
        """propability_at_station
        description:
            * Filters delay_df by the delay propability in % and groups by stations
            * Returns DataFrame including the joined station Name

        Returns:
            DataFrame: Delay data grouped by stations and ordered by propability

        Args:
            delay_df (pd.DataFrame): Delay data
            
        tests:
            * Test if delay_at_station groups the stations right
            * Test if the propability value is between 0 and 100
            * Test if every entrie of the return value has the column 'Name mit Ort'
            (* Test if return type is a DataFrame)
        """
        delay_series = delay_df.groupby(['station_id'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)

        delay_df = pd.DataFrame(delay_series)

        if not delay_df.empty:

            delay_df = Filter.join_station_name(delay_df)
        
            delay_df = delay_df[['Name mit Ort', 'delay']]
        

            delay_df = delay_df.sort_values('delay', ascending=False)

        return delay_df
        
    def propability_of_line(delay_df:pd.DataFrame):
        """propability_of_line
        description:
            * Filters delay_df by the delay propability in % and groups by trains
            * Returns DataFrame ordered by propability

        Returns:
            DataFrame: Delay data grouped by lines and ordered by propability

        Args:
            delay_df (pd.DataFrame): Delay data
            
        tests:
            * Test if delay_at_station groups the lines right
            * Test if the propability value is between 0 and 100
            * Test if the propability value is calculated right
            (* Test if return type is a DataFrame)
        """
        delay_series = delay_df.groupby(['line_number','direction'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)
        delay_df = pd.DataFrame(delay_series).sort_values('delay', ascending=False)


        return delay_df