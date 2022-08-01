import pandas as pd
from typing import Dict
from events_data import get_event_param, maximize_events


def ponderate_recent_events(events_data: Dict, years_weight: Dict, alpha: int = 1.3) -> Dict:
    pond_data = {}
    for event in events_data:
        pond_data[event] = {}

        if event in maximize_events:
            alpha = -abs(alpha)
        else:
            alpha = abs(alpha)
            
        for sex in events_data[event]:
            pond_data[event][sex] = {}
            
            for athlete, df in events_data[event][sex].items():
                ponderated_results = []

                # Extending DataFrame, prioritizing the recent marks
                for i in range(len(df)):
                    row = df.iloc[i]
                    date = row[0]
                    
                    if date.year not in years_weight.keys():
                        continue
                    
                    times = years_weight[date.year]
                    ponderated_results.extend([row] * times)
                
                if ponderated_results:
                    results = pd.DataFrame(ponderated_results)
                    
                    if get_event_param(event, sex, 'alpha_excp', False):
                        marks_count = len(ponderated_results)
                        pond_val = 1 + alpha / marks_count
                        results.Result *= pond_val
                    
                    pond_data[event][sex][athlete] = results

    return pond_data