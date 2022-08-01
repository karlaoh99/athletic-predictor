import os
import pandas as pd
from datetime import datetime
from typing import List, Dict


month_numbers = {
    'JAN': 1,
    'FEB': 2,
    'MAR': 3,
    'APR': 4,
    'MAY': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12,
}


def convert_date(date: str) -> datetime:
    if isinstance(date, int):
        return datetime(year=date, month=1, day=1)
    
    day, month, year = date.split()
    return datetime(year=int(year), month=month_numbers[month], day=int(day))


def clean_results(df: pd.DataFrame) -> None:
    df.dropna(inplace=True)
    df['Date'] = df.Date.map(convert_date)


def read_results(folder_path: str, only: List[str] = None) -> Dict:
    """
    Read the athletes results from each folder.

    Parameters
    ----------
    folder_path: str
        Folder path that contains the folder of each event.
    only: List[str]
        List of events that will be readed.

    Returns
    -------
    Dict
        Athletes results for each event.
        
        Example dict:

            {
                'event_name_1' : {
                    'male' : {
                        'athlete-name-1': athlete1_result_df,
                        'athlete-name-2': athlete2_result_df,
                        ...
                    },
                    ...
                },
                ...
            }
    """

    events_data = {}

    for event_entry in os.scandir(folder_path):
        event = event_entry.name
        events_data[event] = {}

        if only is not None and event not in only:
            continue
        
        for sex_entry in os.scandir(event_entry.path):
            sex = sex_entry.name

            results = {}
            for athlete_entry in os.scandir(sex_entry.path):
                athlete = athlete_entry.name.split('.')[0]
                athlete_results = pd.read_csv(athlete_entry.path, encoding='utf-8')
                
                # TODO: Classified data reader is not working well
                if athlete == 'classified':
                    #results = {k:v for k, v in results.items() if k in classified.Country.to_numpy()}
                    continue
                else:
                    clean_results(athlete_results)
                    results[athlete] = athlete_results
            
            events_data[event][sex] = results
            
    return events_data