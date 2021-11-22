import os
import shutil


def remove_tmpdirs(bench_root, dataset, *dires):
    dir_names = os.listdir(bench_root + '/' + dataset['dataset']['name'])
    dir_paths = list(map(lambda x: bench_root + '/' + dataset['dataset']['name'] + '/' + x, dir_names))
    dirs = map(lambda x: {'name': x[0], 'path': x[1]}, zip(dir_names, dir_paths))
    for dire in dirs:
        if os.path.isdir(dire['path']):
            if dire['name'] in dires:
                shutil.rmtree(dire['path'])


def get_dataset_by_name(bench_root, dataset_name, json_dir='/raw_json', data_file_ext='.csv', chart_file_ext='.json'):
    dir_name = dataset_name
    dir_path = bench_root + dataset_name
    dire = {'name': dir_name, 'path': dir_path}
    # listing all dataset (one csv file) and chart files (several json files)
    dataset = {}
    
    dir_path = dire['path'] + json_dir + '/'
    if os.path.isdir(dir_path):
        dataset_file = {'name': dire['name'], 'path': dire['path'] + '/' + dire['name'] + data_file_ext}
        chart_files = []
        lists = os.listdir(dir_path)
        lists.sort(key=lambda x: int("".join(list(filter(str.isdigit, x)))))
        for item in lists:
            item_path = dir_path + item
            if os.path.isfile(item_path):
                if item.endswith(chart_file_ext):
                    chart_files.append({'name': item, 'path': item_path})
        
        if os.path.exists(dataset_file['path']):
            dataset = {
                'root_dir': dire['name'] + '/',
                'dataset': dataset_file,
                'charts': chart_files
            }
    return dataset


def list_datasets(bench_root, json_dir='/raw_json', data_file_ext='.csv', chart_file_ext='.json'):
    dir_names = os.listdir(bench_root)
    dir_paths = list(map(lambda x: bench_root + x, dir_names))
    dirs = map(lambda x: {'name': x[0], 'path': x[1]}, zip(dir_names, dir_paths))
    # listing all dataset (one csv file) and chart files (several json files)
    datasets = []
    for dire in dirs:
        dir_path = dire['path'] + json_dir + '/'
        if os.path.isdir(dir_path):
            dataset_file = {'name': dire['name'], 'path': dire['path'] + '/' + dire['name'] + data_file_ext}
            chart_files = []
            lists = os.listdir(dir_path)
            for item in lists:
                item_path = dir_path + item
                if os.path.isfile(item_path):
                    if item.endswith(chart_file_ext):
                        chart_files.append({'name': item, 'path': item_path})
            
            if os.path.exists(dataset_file['path']):
                datasets.append(
                    {
                        'root_dir': dire['name'] + '/',
                        'dataset': dataset_file,
                        'charts': chart_files
                    })
    return datasets
