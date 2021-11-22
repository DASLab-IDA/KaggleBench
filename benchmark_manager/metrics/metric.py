import math

from KaggleBench.benchmark_manager.evaluator.comparator import compare_bench


def calculate_P(charts_bench, charts_eva):
    # extract relevant items
    matches = []
    for chart in charts_eva:
        same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
        if same_list:
            matches.append(same_list)
    # calculate precision, recall and f1 score
    p = len(matches) / len(charts_eva)
    return 0 if len(matches) == 0 else p


def calculate_R(charts_bench, charts_eva):
    # extract relevant items
    matches = []
    for chart in charts_eva:
        same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
        if same_list:
            matches.append(same_list)
    # calculate precision, recall and f1 score
    r = len(matches) / len(charts_bench)
    return 0 if len(matches) == 0 else r


def calculate_P_R(charts_bench, charts_eva):
    # extract relevant items
    matches = []
    for chart in charts_eva:
        same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
        if same_list:
            matches.append(same_list)
    # calculate precision, recall and f1 score
    p = len(matches) / len(charts_eva)
    r = len(matches) / len(charts_bench)
    if (p + r) == 0:
        return 0
    f = 2 * p * r / (p + r)
    return f


def calculate_AP(charts_bench, charts_eva):
    # extract relevant items
    matches = []
    for index, chart in enumerate(charts_eva):
        same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
        if same_list:
            matches.append((index, same_list))
    # calculate average precision
    sum_p = 0
    for index, match in enumerate(matches):
        sum_p += (index + 1) / (match[0] + 1)
    norm = min(len(matches), len(charts_eva))
    if norm == 0:
        return 0
    ap = sum_p / norm
    return ap


def calculate_NDCG(charts_bench, charts_eva):
    # extract relevant items
    matches = []
    for index, chart in enumerate(charts_eva):
        same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
        if same_list:
            matches.append((index + 1, same_list[0]))
    # calculate discounted cumulative gain of relevant items
    dcg = 0
    for match in matches:
        dcg += (len(charts_bench) - match[1]['rank'] + 1) / math.log(match[0] + 1, 2)
    
    # calculate ideal discounted cumulative gain of relevant items
    matches_sorted = sorted(matches, key=lambda x: x[1]['rank'])
    idcg = 0
    for index, match in enumerate(matches_sorted):
        idcg += (len(charts_bench) - match[1]['rank'] + 1) / math.log((index + 1) + 1, 2)
    
    # normalized discounted cumulative gain
    if idcg == 0:
        return 0
    ndcg = dcg / idcg
    return ndcg


metrics = {
    'Precision': calculate_P,
    'Recall': calculate_R,
    'F1-score': calculate_P_R,
    'Average Precision': calculate_AP,
    'Normalized DCG': calculate_NDCG
}
