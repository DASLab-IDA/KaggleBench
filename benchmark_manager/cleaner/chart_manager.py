# extract charts with specified type(e.g., bar, line, scatter, pie)
import json
import os
import sys

sys.path.append(os.path.abspath('../..'))
os.chdir(os.path.abspath('.'))
from ..cleaner.column_manager import check_cols_chart, drop_unused_cols_single
from ..util.file_manager import list_datasets, remove_tmpdirs, get_dataset_by_name
from ..util.monitor import monitor
from ..evaluator.comparator import compare
import copy
import pandas as pd


def extract_charts(benchmark_path, chart_types, dataset, output_dir='extracted'):
    bench_root = benchmark_path + '/'
    with monitor('Extracting charts: ' + dataset['dataset']['name'], level=0):
        new_jsons = []
        jsons = dataset['charts']
        out_path = bench_root + dataset['root_dir'] + output_dir
        csv_path = dataset['dataset']['path']
        data = pd.read_csv(csv_path, nrows=1)
        columns = data.columns
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        for js in jsons:
            with monitor('Processing file: ' + js['name'], level=1):
                with open(js['path']) as file:
                    temp = json.load(file)
                    charts = temp['charts']
                    to_remove = []
                    print('Original number of charts: ', len(charts))
                    for chart in charts:
                        if chart['chart'] not in chart_types or check_cols_chart(chart, columns):
                            to_remove.append(chart)
                    for item in to_remove:
                        charts.remove(item)
                    print('Final number of charts', len(charts), '\nCharts removed: ', len(to_remove))
                    json.dump(temp, open(out_path + js['name'][:-5] + '_extracted' + '.json', 'w'), indent=4)
                    new_jsons.append({
                        'name': js['name'][:-5] + '_extracted' + '.json',
                        'path': out_path + js['name'][:-5] + '_extracted' + '.json'
                    })
        dataset['charts'] = new_jsons


def assign_id_rank(benchmark_path, output_dir, dataset):
    bench_root = benchmark_path + '/'
    with monitor('Assigning id and rank: ' + dataset['dataset']['name'], level=0):
        jsons = dataset['charts']
        new_jsons = []
        for js in jsons:
            with monitor('Processing file: ' + js['name'], level=1):
                with open(js['path']) as file:
                    temp = json.load(file)
                    charts = temp['charts']
                    for index, chart in enumerate(charts):
                        chart['id'] = js['name'] + '_id_' + str(index + 1)
                        chart['rank'] = index + 1
                        chart['type'] = chart['chart']
                        del chart['chart']
                        channels = {}
                        for key in list(chart.keys()):
                            if key != 'describe' and key != 'type' and key != 'id' and key != 'rank' and key != 'filter':
                                channels[key] = chart[key]
                                del chart[key]
                        chart['channels'] = channels
                    out_path = bench_root + dataset['root_dir'] + output_dir
                    if not os.path.exists(out_path):
                        os.mkdir(out_path)
                    json.dump(temp,
                              open(out_path + js['name'][:-5] + '_id' + '.json',
                                   'w'),
                              indent=4)
                    new_jsons.append({
                        'name': js['name'][:-5] + '_id' + '.json',
                        'path': out_path + js['name'][:-5] + '_id' + '.json'
                    })
        dataset['charts'] = new_jsons


def merge_charts(benchmark_path, output_dir, dataset, compare_func=compare, only_channels=True):
    bench_root = benchmark_path + '/'
    with monitor('Merging charts: ' + dataset['dataset']['name'], level=0):
        json_files = dataset['charts']
        jsons = []
        votes = []
        names = []
        for js in json_files:
            with open(js['path']) as file:
                temp = json.load(file)
                jsons.append(temp)
                votes.append(temp['votes'])
                names.append(js['name'])
        
        weights = list(map(lambda x: x / sum(votes), votes))
        
        merged_jsons = []
        for index, js in enumerate(jsons):
            appended = copy.deepcopy(js)
            for idx, to_append in enumerate(jsons):
                if idx != index:
                    to_app = copy.deepcopy(to_append)
                    for pos, chart in enumerate(to_app['charts']):
                        same_list = list(filter(lambda x: compare_func(chart, x), appended['charts']))
                        if not same_list:
                            temp = copy.deepcopy(chart)
                            temp['rank'] = len(appended['charts']) + 1
                            appended['charts'].append(temp)
                        elif len(same_list) == 1:
                            dup = same_list[0]
                            dup['id'] += '-' + chart['id']
            merged_jsons.append(appended)
        
        for index, js in enumerate(merged_jsons):
            js = copy.deepcopy(js)
            for idx, to_append in enumerate(merged_jsons):
                if idx != index:
                    num = len(js['charts'])
                    for pos, chart in enumerate(js['charts']):
                        same_list = list(filter(lambda x: compare_func(chart, x), to_append['charts']))
                        ranks = chart.get('ranks',
                                          [
                                              (chart['rank'], num + 1 - chart['rank'], weights[index],
                                               (num + 1 - chart['rank']) * weights[index])
                                          ]
                                          )
                        rank_otherfile = (
                            same_list[0]['rank'],
                            num + 1 - same_list[0]['rank'], weights[idx],
                            (num + 1 - same_list[0]['rank']) * weights[idx])
                        ranks.append(rank_otherfile)
                        ranks.sort(key=lambda x: x[3], reverse=True)
                        chart['ranks'] = ranks
                        chart['score'] = chart.get('score', (num + 1 - chart['rank']) * weights[index]) + \
                                         rank_otherfile[3]
            js['charts'].sort(key=lambda x: x['score'], reverse=True)
            
            def assin_new_rank(x):
                x[1]['new_rank'] = x[0] + 1
                return x[1]
            
            js['charts'] = list(map(assin_new_rank, enumerate(js['charts'])))
            out_path = bench_root + dataset['root_dir'] + output_dir
            if not os.path.exists(out_path):
                os.mkdir(out_path)
            json.dump(js['charts'],
                      open(out_path + names[index][:-5] + '_merged' + '.json',
                           'w'),
                      indent=4)
            
            only_path = bench_root + dataset['root_dir'] + '/only/'
            only = list(map(type_channels, js['charts']))
            if not os.path.exists(only_path):
                os.mkdir(only_path)
            json.dump(only,
                      open(only_path + names[index][:-5] + '_only' + '.json',
                           'w'),
                      indent=4)
    
    if only_channels:
        channels = list(map(type_channels, merged_jsons[0]['charts']))
        json.dump({"charts": channels},
                  open(out_path + '../' + dataset['dataset']['name'] + '.json',
                       'w'),
                  indent=4)
    else:
        json.dump({"charts": merged_jsons[0]['charts']},
                  open(out_path + '../' + dataset['dataset']['name'] + '.json',
                       'w'),
                  indent=4)
    print('Number of charts remain: {0}'.format(len(merged_jsons[0]['charts'])))


def type_channels(x):
    tmp = dict()
    tmp['type'] = x['type']
    tmp['channels'] = x['channels']
    return tmp


def process_whole_benchmark(bench_root):
    # extract_charts(benchmark_path='../../benchmark', chart_types=['bar', 'line', 'pie', 'scatter'],
    #                json_path='/raw_json', output_dir='/extracted/')
    # assign_id_rank(benchmark_path='../../benchmark', output_dir='/reid/', json_path='/extracted')
    # merge_charts(benchmark_path='../../benchmark', output_dir='/merged/', json_path='/reid', only_channels=False)
    # remove_tmpdirs('../../benchmark/', 'extracted', 'reid', 'merged', 'only')
    datasets = list_datasets(bench_root, '/raw_json', data_file_ext='_raw.csv')
    for dataset in datasets:
        process_single_dataset(dataset)


def process_single_dataset(dataset, bench_root='../../benchmark/'):
    extract_charts(benchmark_path=bench_root, chart_types=['bar', 'line', 'pie', 'scatter'], dataset=dataset, output_dir='/extracted/')
    assign_id_rank(benchmark_path=bench_root, output_dir='/reid/', dataset=dataset)
    merge_charts(benchmark_path=bench_root, output_dir='/merged/', dataset=dataset, only_channels=False)
    remove_tmpdirs(bench_root, dataset, 'extracted', 'reid', 'merged', 'only')
    drop_unused_cols_single(dataset['dataset']['name'], '_drop_unused_cols', bench_root=bench_root)


if __name__ == '__main__':
    # process_whole_benchmark(bench_root='../../benchmark/')
    dataset_name = 'avito_demand'
    dataset = get_dataset_by_name(bench_root='../../benchmark/', dataset_name=dataset_name, data_file_ext='_raw.csv')
    process_single_dataset(dataset, bench_root='../../benchmark/')
