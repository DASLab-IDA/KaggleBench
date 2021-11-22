# dropping all unused columns in each dataset
import pandas as pd
import json

from ..util.file_manager import list_datasets, get_dataset_by_name
from ..util.monitor import monitor


# check unknown columns in chart files of a given dataset using collected raw json files.
def check_unknown_cols_single_raw(dataset_name, json_path='/raw_json', bench_root='../../benchmark/'):
    dataset = get_dataset_by_name(bench_root, dataset_name, json_dir=json_path, data_file_ext='_raw.csv', chart_file_ext='.json')
    with monitor('Checking unknown columns: ' + dataset['dataset']['name'], level=0):
        jsons = dataset['charts']
        csv_path = dataset['dataset']['path']
        data = pd.read_csv(csv_path, nrows=1)
        columns = data.columns
        for js in jsons:
            with monitor('Processing file: ' + js['name'], level=1):
                with open(js['path']) as file:
                    temp = json.load(file)
                    charts = temp['charts']
                    unknown = unknown_cols(charts, columns)
                    print(unknown)


# check unknown columns in chart files of each dataset using collected raw json files.
def check_unknown_cols_raw(benchmark_path, json_path):
    bench_root = benchmark_path + '/'
    datasets = list_datasets(bench_root, json_path, data_file_ext='_raw.csv')
    for dataset in datasets:
        check_unknown_cols_single_raw(dataset['dataset']['name'], json_path)


# check unknown columns in chart files given a dataset using merged json file.
def check_unknown_cols_single_merged(dataset_name, bench_root='../../benchmark/', json_path=''):
    dataset = get_dataset_by_name(bench_root, dataset_name, json_dir=json_path, data_file_ext='_raw.csv', chart_file_ext='.json')
    with monitor('Checking unknown columns: ' + dataset['dataset']['name'], level=0):
        jsons = dataset['charts']
        csv_path = dataset['dataset']['path']
        data = pd.read_csv(csv_path, nrows=1)
        columns = data.columns
        for js in jsons:
            with monitor('Processing file: ' + js['name'], level=1):
                with open(js['path']) as file:
                    temp = json.load(file)
                    charts = list(map(lambda x: x['channels'], temp['charts']))
                    unknown = unknown_cols(charts, columns)
                    print(unknown)


# check unknown columns in chart files of each dataset using merged json file.
def check_unknown_cols_merged(benchmark_path, json_path=''):
    bench_root = benchmark_path + '/'
    datasets = list_datasets(bench_root, json_path, data_file_ext='_raw.csv')
    for dataset in datasets:
        check_unknown_cols_single_merged(dataset['dataset']['name'], bench_root='../../benchmark/', json_path=json_path)


def unknown_cols(charts, columns):
    cols = set()
    for chart in charts:
        for key in list(chart.keys()):
            if key not in ['describe', 'chart', 'id', 'rank', 'filter']:
                if isinstance((chart[key]), dict):
                    if chart[key]['attr'] not in columns:
                        cols.add(chart[key]['attr'])
                elif isinstance(chart[key], list):
                    for item in chart[key]:
                        if item['attr'] not in columns:
                            cols.add(item['attr'])
                else:
                    print(chart[key])
    return cols


def check_cols_chart(chart, columns):
    for key in list(chart.keys()):
        if key == 'filter':
            return True
        if key not in ['describe', 'chart', 'id', 'rank', 'filter']:
            if chart[key]['attr'] not in columns:
                return True
    return False


def drop_unused_cols(benchmark_path, json_path, postfix=''):
    bench_root = benchmark_path + '/'
    datasets = list_datasets(bench_root, json_path, data_file_ext='_raw.csv')
    
    # filtering out unused columns
    for dataset in datasets:
        csv_path = dataset['dataset']['path']
        jsons = dataset['charts']
        with monitor('Checking ununsed columns: ' + csv_path, level=0):
            data = pd.read_csv(csv_path)
            colomns = data.columns
            columns_used = set()
            for item in jsons:
                with monitor('Processing file: ' + item['name'], level=1):
                    with open(item['path']) as file:
                        temp = json.load(file)
                        charts = temp['charts']
                        for chart in charts:
                            for k, v in chart.items():
                                if type(v) is dict:
                                    columns_used.add(v['attr'])
                    columns_unused = set(colomns) - columns_used & set(colomns)
                    print(columns_unused)
            data.drop(columns=columns_unused, axis=1, inplace=True)
            data.to_csv(bench_root + dataset['root_dir'] + dataset['dataset']['name'] + postfix + '.csv', index=None)


def drop_unused_cols_filter(benchmark_path, json_path, postfix=''):
    bench_root = benchmark_path + '/'
    datasets = list_datasets(bench_root, json_path, data_file_ext='_raw.csv')
    
    # filtering out unused columns
    for dataset in datasets:
        csv_path = dataset['dataset']['path']
        jsons = dataset['charts']
        with monitor('Checking ununsed columns: ' + csv_path, level=0):
            data = pd.read_csv(csv_path)
            colomns = data.columns
            columns_used = set()
            for item in jsons:
                with monitor('Processing file: ' + item['name'], level=1):
                    with open(item['path']) as file:
                        temp = json.load(file)
                        charts = list(map(lambda x: x['channels'], temp['charts']))
                        for chart in charts:
                            for k, v in chart.items():
                                if type(v) is dict:
                                    columns_used.add(v['attr'])
                    columns_unused = set(colomns) - columns_used & set(colomns)
                    print(columns_unused)
            data.drop(columns=columns_unused, axis=1, inplace=True)
            data.to_csv(bench_root + dataset['root_dir'] + dataset['dataset']['name'] + postfix + '.csv', index=None)


# check unused columns in raw csv of a single dataset given the name of the dataset
def check_unused_cols_single_merged(dataset_name, bench_root='../../benchmark/'):
    dataset_root = bench_root + dataset_name
    csv_raw = dataset_root + '/' + dataset_name + '_raw.csv'
    csv_cleaned = dataset_root + '/' + dataset_name + '_drop_unused_cols.csv'
    json_file = dataset_root + '/' + dataset_name + '.json'
    
    # filtering out unused columns
    columns_unuse = set()
    with monitor('Checking ununsed columns: ' + csv_raw, level=0):
        data = pd.read_csv(csv_raw, nrows=1)
        cled = pd.read_csv(csv_cleaned, nrows=1)
        colomns = data.columns
        cled_colomns = cled.columns
        columns_used = set()
        with open(json_file) as file:
            temp = json.load(file)
            charts = list(map(lambda x: x['channels'], temp['charts']))
            for chart in charts:
                for k, v in chart.items():
                    if type(v) is dict:
                        columns_used.add(v['attr'])
        columns_unused = set(colomns) - columns_used & set(colomns)
        columns_unuse |= columns_unused
        print(columns_unuse)
        print(set(data.columns) - set(cled_colomns))


# check unused columns of each dataset in the benchmark
def check_unused_cols_merged(benchmark_path, json_path=''):
    bench_root = benchmark_path + '/'
    datasets = list_datasets(bench_root, json_path, data_file_ext='_raw.csv')
    # filtering out unused columns
    for dataset in datasets:
        check_unused_cols_single_merged(dataset['dataset']['name'])


def drop_unused_cols_single(dataset, output_postfix, bench_root='../../benchmark/'):
    csv_path = bench_root + dataset + '/' + dataset + '_raw.csv'
    json_file = bench_root + dataset + '/' + dataset + '.json'
    
    with monitor('Checking ununsed columns: ' + csv_path, level=0):
        data = pd.read_csv(csv_path)
        colomns = data.columns
        columns_used = set()
        with monitor('Processing file: ' + csv_path, level=1):
            with open(json_file) as file:
                temp = json.load(file)
                charts = list(map(lambda x: x['channels'], temp['charts']))
                for chart in charts:
                    for k, v in chart.items():
                        if type(v) is dict:
                            columns_used.add(v['attr'])
            columns_unused = set(colomns) - columns_used & set(colomns)
            print(columns_unused)
        data.drop(columns=columns_unused, axis=1, inplace=True)
        data.to_csv(bench_root + dataset + '/' + dataset + output_postfix + '.csv', index=None)


if __name__ == '__main__':
    # check_unknown_cols_merged('../../benchmark')
    # drop_unused_cols_filter('../../benchmark', '', '_drop_unused_cols')
    # check_unused_cols_merged('../../benchmark/')
    # drop_unused_cols_single('flight_delay', '_drop_unused_cols')
    check_unknown_cols_single_raw('fifa_world_cup', bench_root='../../benchmark_to_append/')
    # check_cols_all('../../benchmark', '/raw_json')
