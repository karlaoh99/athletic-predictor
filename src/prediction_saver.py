from typing import List, Tuple
from datetime import datetime
from src.competition_data import CompetitionData
from src.utils import load_json, save_json, get_country_and_name


def _format_event_result(result: List[str], is_group: bool, top: int) -> dict:
    prediction = {}
    prediction['date'] = datetime.now().date().strftime(r'%Y/%m/%d')
    prediction['prediction'] = {}

    if is_group:
        for i in range(top):
            prediction['prediction'][f'{i+1}'] = {}
            prediction['prediction'][f'{i+1}']['country'] = result[i]
    else:   
        for i in range(top):
            prediction['prediction'][f'{i+1}'] = {}
            g_country, g_name = get_country_and_name(result[i])
            prediction['prediction'][f'{i+1}']['country'] = g_country
            prediction['prediction'][f'{i+1}']['name'] = g_name

    return prediction


def save_prediction(results: dict, competition: CompetitionData, top: int = 3, file: str = 'predictions.json') -> None:
    """Saves the resulting predictions in a file.
    
    Parameters
    ----------
    results : dict
        Resulting prediction for each event and gender
    competition : CompetitionData
        The data of the events in a competition
    top : int, optional
        Number of positions to save
    file : str, optional
        File path where to save the predictions
    """

    predictions = load_json(file)

    for event in results:
        if not event in predictions:
            predictions[event] = {}
            predictions[event]['sex'] = {}
            predictions[event]['name'] = competition.get_event_data(event, 'name')

        for sex in results[event]:
            predictions[event]['sex'][sex] = _format_event_result(results[event][sex], competition.is_event_in_group(event), top)

    save_json(predictions, file)


__all__ = [
    "save_prediction",
]