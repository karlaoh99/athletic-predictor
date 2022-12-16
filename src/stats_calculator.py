from src.utils import save_json, load_json


def convert_pred(prediction):
    final = {}

    for event in prediction:
        final[event] = {}
        for sex in prediction[event]['sex']:
            final[event][sex] = {}
            p = prediction[event]['sex'][sex]['prediction']
            for i in p:
                name = '_'.join(p[i]['name'].split(' ')).lower()
                final[event][sex][i] = f"{p[i]['country']}_{name}"

    return final


def calculate_stats(real, pred):
    ranking_pos = 0
    ranking_exact_pos = 0
    podium_pos = 0
    podium_exact_pos = 0
    champion = 0

    for r_index, name in enumerate(real):
        try:
            p_index = pred.index(name)
            
            if r_index == p_index:
                ranking_exact_pos += 1
                if r_index == 0:
                    champion += 1
                if r_index < 3:
                    podium_exact_pos += 1
                    
            ranking_pos += 1
            if r_index < 3 and p_index < 3:
                podium_pos += 1

        except:
            continue
    
    return ranking_pos, ranking_exact_pos, podium_pos, podium_exact_pos, champion


def calculate_all_stats(results_file, pred_file, stats_file):
    results = load_json(results_file)
    predictions = load_json(pred_file)
    predictions = convert_pred(predictions)
    
    total_ranking_pos = 0
    total_ranking_exact_pos = 0
    total_podium_pos = 0
    total_podium_exact_pos = 0
    total_champion = 0

    total_ranking_pos_gender = {'female': 0, 'male': 0}
    total_ranking_exact_pos_gender = {'female': 0, 'male': 0}
    total_podium_pos_gender = {'female': 0, 'male': 0}
    total_podium_exact_pos_gender = {'female': 0, 'male': 0}
    total_champion_gender = {'female': 0, 'male': 0}

    stats = {}

    for event in results:
        if event not in predictions:
            continue
        
        stats[event] = {}
        for sex in results[event]:
            stats[event][sex] = {}

            res = list(results[event][sex].values())
            pred = list(predictions[event][sex].values())

            ranking_pos, ranking_exact_pos, podium_pos, podium_exact_pos, champion = calculate_stats(res, pred)
            total_ranking_pos += ranking_pos
            total_ranking_exact_pos += ranking_exact_pos
            total_podium_pos += podium_pos
            total_podium_exact_pos += podium_exact_pos
            total_champion += champion

            total_ranking_pos_gender[sex] += ranking_pos
            total_ranking_exact_pos_gender[sex] += ranking_exact_pos
            total_podium_pos_gender[sex] += podium_pos
            total_podium_exact_pos_gender[sex] += podium_exact_pos
            total_champion_gender[sex] += champion

            stats[event][sex]['ranking_pos'] = ranking_pos
            stats[event][sex]['ranking_exact_pos'] = ranking_exact_pos
            stats[event][sex]['podium_pos'] = podium_pos
            stats[event][sex]['podium_exact_pos'] = podium_exact_pos
            stats[event][sex]['champion'] = champion

    stats['total_ranking_pos'] = total_ranking_pos
    stats['total_ranking_exact_pos'] = total_ranking_exact_pos
    stats['total_podium_pos'] = total_podium_pos
    stats['total_podium_exact_pos'] = total_podium_exact_pos
    stats['total_champion'] = total_champion

    stats['total_ranking_pos_gender'] = total_ranking_pos_gender
    stats['total_ranking_exact_pos_gender'] = total_ranking_exact_pos_gender
    stats['total_podium_pos_gender'] = total_podium_pos_gender
    stats['total_podium_exact_pos_gender'] = total_podium_exact_pos_gender
    stats['total_champion_gender'] = total_champion_gender

    save_json(stats, stats_file)


__all__ = [
    "calculate_stats",
    "calculate_all_stats",
]