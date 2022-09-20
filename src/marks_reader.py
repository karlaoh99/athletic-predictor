import os
import pandas as pd
from datetime import datetime
from typing import List


_month_numbers = {
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


def _convert_date(date: str) -> datetime:
    if isinstance(date, int):
        return datetime(year=date, month=1, day=1)
    
    day, month, year = date.split()
    return datetime(year=int(year), month=_month_numbers[month], day=int(day))


def _clean_marks(df: pd.DataFrame, limit_date: datetime = None) -> None:
    df.dropna(inplace=True)
    df.Date = df.Date.map(_convert_date)
    
    if limit_date is not None:
        indexs = []
        for index, row in df.iterrows():
            if row.Date.to_pydatetime() >= limit_date:
                indexs.append(index)
        df.drop(indexs, inplace=True)


def read_marks(folder_path: str, only: List[str] = None, limit_date: datetime = None) -> dict:
    """Reads the athletes marks.

    Only the events that are inside the `folder_path` folder and the 
    genders inside them will be read. It is important to only have 
    valid folders and files, because otherwise unexpected errors 
    could occur. The valid structure inside of the folder must be:
    ├── event1/
    │   ├── sex1/
    │   │   ├── athlete1_marks.csv
    │   │   │   ...
    │   │   └── 
    │   │   ...
    │   └──
    │   ...
    └──
    
    Parameters
    ----------
    folder_path : str
        Folder path that contains the folder of each event
    only : List[str], optional
        List of events to be read only
    limit_date : datetime, optional
        Limit date for marks

    Returns
    -------
    dict
        Athletes marks for each event and genders
        
        Example dict:
            {
                'event_name_1' : {
                    'male' : {
                        'athlete-name-1' : athlete1_marks_df,
                        'athlete-name-2' : athlete2_marks_df,
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
        
        if only is not None and event not in only:
            continue
        
        events_data[event] = {}
        
        for sex_entry in os.scandir(event_entry.path):
            sex = sex_entry.name

            marks = {}
            for athlete_entry in os.scandir(sex_entry.path):
                athlete = athlete_entry.name.split('.')[0]
                athlete_marks = pd.read_csv(athlete_entry.path, encoding='utf-8')
              
                _clean_marks(athlete_marks, limit_date)
                marks[athlete] = athlete_marks
            
            events_data[event][sex] = marks
            
    return events_data


__all__ = [
    "read_marks",
]