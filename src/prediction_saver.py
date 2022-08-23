import json
from typing import List, Tuple
from datetime import datetime
from events_data import events_in_groups, events


def _format_event_result(event: str, result: List[str], top: int) -> dict:
    prediction = {}
    prediction['date'] = datetime.now().date().strftime(r'%Y/%m/%d')
    prediction['prediction'] = {}

    if event in events_in_groups:
        for i in range(top):
            prediction['prediction'][f'{i+1}'] = {}
            prediction['prediction'][f'{i+1}']['country'] = result[i]
    else:   
        for i in range(top):
            prediction['prediction'][f'{i+1}'] = {}
            g_country, g_name = get_country_nd_name(result[i])
            prediction['prediction'][f'{i+1}']['country'] = g_country
            prediction['prediction'][f'{i+1}']['name'] = g_name

    return prediction


def get_country_nd_name(file_name: str) -> Tuple[str, str]:
    splitted_list = file_name.split('_')
    country = splitted_list[0]
    name = ' '.join(splitted_list[1:])
    return country, name


def load_json(file: str) -> dict:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: 
        return {}


def save_json(data: dict, file: str):
    with open(file, 'w+', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_prediction(results: dict, top: int, file: str = 'predictions.json'):
    predictions = load_json(file)

    for event in results:
        if not event in predictions:
            predictions[event] = {}
            predictions[event]['name'] = events[event]['name']
            predictions[event]['sex'] = {}

        for sex in results[event]:
            predictions[event]['sex'][sex] = _format_event_result(event, results[event][sex], top)

    save_json(predictions, file)