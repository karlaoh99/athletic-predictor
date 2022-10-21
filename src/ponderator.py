import pandas as pd
from src.competition_data import CompetitionData


def ponderate_all_events(data: dict, competition: CompetitionData, years_weight: dict, alpha: int = 0, logs: bool = False) -> dict:
    """Transforms data according to parameters years_weight and alpha.

    Parameters
    ----------
    data : dict
        Athletes marks for each event and gender
    competition : CompetitionData
        Contains the data of the competition
    years_weight : dict
        A dictionary with the years to be taken and its weight
    alpha : int, optional
        Alpha default value involved in the experience of athletes
    logs : bool, optional
        True if logs want to be shown

    Returns
    -------
    dict
        A dictionary with the data transformed
        
        Example dict:
            {
                'event_name_1' : {
                    'male' : {
                        'athlete-name-1': athlete1_marks_df,
                        'athlete-name-2': athlete2_marks_df,
                        ...
                    },
                    ...
                },
                ...
            }
    """

    pond_data = {}
    for event in data:
        pond_data[event] = {}
        maximize = competition.is_maximize_event(event)

        for sex in data[event]:
            alpha = competition.get_event_param(event, sex, 'alpha', alpha)
            pond_data[event][sex] = ponderate_event(data[event][sex], maximize, years_weight, alpha, logs)
        
    return pond_data


def ponderate_event(data: dict, maximize: bool, years_weight: dict, alpha: int, logs: bool = False) -> dict:
    """Transforms an event data according to parameters years_weight and alpha.

    Parameters
    ----------
    data : dict
        Athletes marks of an event and gender
    maximize : bool
        True if the goal of the event is to maximize the result
    years_weight : dict
        A dictionary with the years to be taken and its weight
    alpha : int
        Alpha value involved in the experience of athletes
    logs : bool, optional
        True if logs want to be shown

    Returns
    -------
    dict
        A dictionary with the data transformed for each athlete
    """

    pond_data = {}
    
    for athlete, df in data.items():
        pond_marks = ponderate_marks(df, maximize, years_weight, alpha)
        if pond_marks is not None:
            pond_data[athlete] = pond_marks
        elif logs:
            print(f"WARNING: Athlete {athlete} does not have any valid mark")
        
    return pond_data


def ponderate_marks(marks: pd.DataFrame, maximize: bool, years_weight: dict, alpha: int) -> pd.DataFrame:
    """Transforms marks according to parameters years_weight and alpha.

    Parameters
    ----------
    marks : pd.DataFrame
        Athlete's marks
    maximize : bool
        True if the goal of the event is to maximize the result
    years_weight : dict
        A dictionary with the years to be taken and its weight
    alpha : int
        Alpha value involved in the experience of athletes

    Returns
    -------
    pd.DataFrame
        DataFrame with the athlete's marks transformed
    """

    if maximize:
        alpha = -abs(alpha)
    else:
        alpha = abs(alpha)

    pond_marks = []

    # Extending DataFrame, prioritizing the recent marks
    for i in range(len(marks)):
        row = marks.iloc[i]
        date = row[0]
        
        # Select only the marks obtained recently
        if date.year not in years_weight.keys():
            continue
        
        times = years_weight[date.year]
        pond_marks.extend([row] * times)

    if pond_marks:
        df_marks = pd.DataFrame(pond_marks)
        pond_val = 1 + alpha / len(pond_marks)
        df_marks.Result *= pond_val
        
        return df_marks

    return None


__all__ = [
    ponderate_all_events,
    ponderate_event,
    ponderate_marks,
]