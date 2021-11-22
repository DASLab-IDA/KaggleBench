import json
import os

import pandas


def diversity(dataset, bench_root='../../benchmark/'):
    bench_json = bench_root + dataset + '/' + dataset + '.json'
    
    with open(bench_json, 'r') as j_f:
        base_json = json.load(j_f)
    
    base_json = base_json['charts']
    s = 0
    n = len(base_json)
    for i in range(n):
        for j in range(i + 1, n):
            a = context_distance(base_json[i], base_json[j])
            s += a
    
    return s / (n * (n - 1))


def diversity_json(base_json):
    s = 0
    n = len(base_json)
    for i in range(n):
        for j in range(i + 1, n):
            a = context_distance(base_json[i], base_json[j])
            s += a
    
    return s / (n * (n - 1))


def similarity(dataset, bench_root='../../benchmark/'):
    bench_json = bench_root + dataset + '/' + dataset + '.json'
    
    with open(bench_json, 'r') as j_f:
        base_json = json.load(j_f)
    
    base_json = base_json['charts']
    s = 0
    n = len(base_json)
    for i in range(n):
        for j in range(i + 1, n):
            a = context_similarity(base_json[i], base_json[j])
            s += a
    
    return s / (n * (n - 1))


def similarity_json(base_json):
    s = 0
    n = len(base_json)
    for i in range(n):
        for j in range(i + 1, n):
            a = context_similarity(base_json[i], base_json[j])
            s += a
    
    return s / (n * (n - 1))


def context_similarity(view_i, view_j):
    viz_a = []
    viz_b = []
    
    # get all columns
    columns_a = []
    
    cha_a = view_i['channels']
    for key in cha_a:
        columns_a.append((cha_a[key]['attr'], cha_a[key]['trans']))
    
    columns_b = []
    cha_b = view_j['channels']
    for key in cha_b:
        columns_b.append((cha_b[key]['attr'], cha_b[key]['trans']))
    
    viz_a.extend(columns_a)
    viz_b.extend(columns_b)
    
    # get chart type
    viz_a.append(view_i['type'])
    viz_b.append(view_j['type'])
    
    set1, set2 = set(viz_a), set(viz_b)
    similarity = len(set1 & set2) / float(len(set1 | set2))
    
    return similarity


def context_distance(view_i, view_j):
    viz_a = []
    viz_b = []
    
    # get all columns
    columns_a = []
    
    cha_a = view_i['channels']
    for key in cha_a:
        columns_a.append((cha_a[key]['attr'], cha_a[key]['trans']))
    
    columns_b = []
    cha_b = view_j['channels']
    for key in cha_b:
        columns_b.append((cha_b[key]['attr'], cha_b[key]['trans']))
    
    viz_a.extend(columns_a)
    viz_b.extend(columns_b)
    
    # get chart type
    viz_a.append(view_i['type'])
    viz_b.append(view_j['type'])
    
    set1, set2 = set(viz_a), set(viz_b)
    similarity = len(set1 & set2) / float(len(set1 | set2))
    
    return 1 - similarity


if __name__ == '__main__':
    bench_root = '../../benchmark/'
    datasets = os.listdir(bench_root)
    
    with open('describe', 'w') as f:
        f.writelines('|Name| #-Row| #-Attr | #-Attr-used|#-Viz|\n')
        f.writelines('| ------ | ------ | ------ |------ | ------ | \n')
        for dataset in datasets:
            csv = bench_root + '/' + dataset + '/' + dataset + '_drop_unused_cols.csv'
            csv1 = bench_root + '/' + dataset + '/' + dataset + '_raw.csv'
            jsonfile = bench_root + '/' + dataset + '/' + dataset + '.json'
            df = pandas.read_csv(csv)
            df1 = pandas.read_csv(csv1)
            with open(jsonfile) as f1:
                js = json.load(f1)
            f.writelines('|{}|{}|{}|{}|{}|\n'.format(dataset, len(df1), len(df1.columns), len(df.columns), len(js['charts'])))
