import json
import os
import pickle
import sys

sys.path.append(os.path.abspath('../..'))
from KaggleBench.benchmark_manager.util.monitor import monitor
from KaggleBench.benchmark_manager.evaluator.comparator import compare_bench
from KaggleBench.benchmark_manager.metrics.metric import metrics as Metrics
from KaggleBench.benchmark_manager.util.file_manager import list_datasets
from VizGRank.vizgrank.personalization import chart_personalization
from VizGRank.vizgrank.vizgrank import VizGRank
from VizGRank.vizgrank.node_relation import context_dissimilarity


def find_corresponding_item_single_dataset(dataset, charts_bench, charts_eva, input_json, bench_root='../../benchmark/',
                                           input_root='./output/'):
    count = 0
    match = []
    with open(input_root + dataset + '/' + input_json[:-5] + '.match', 'w') as out:
        for chart in charts_eva:
            same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
            if same_list:
                count += 1
                match.append(same_list[0])
            else:
                match.append('None')
            out.writelines(str(same_list) + '\n')
        out.writelines('The total number of charts covered is {}/{}'.format(count, len(charts_eva)))
    
    return match


def find_corresponding_item_single_dataset_reverse(dataset, charts_bench, charts_eva, input_json, bench_root='../../benchmark/',
                                                   input_root='./output/'):
    count = 0
    with open(input_root + dataset + '/' + input_json[:-5] + '_reverse.match', 'w') as out:
        for chart in charts_bench:
            same_list = list(filter(lambda x: compare_bench(chart, x), charts_eva))
            if same_list:
                count += 1
            out.writelines(str(same_list) + '\n')
        out.writelines('The total number of charts covered is {}/{}'.format(count, len(charts_bench)))


def evaluate_single_dataset(dataset_name, input_json, topk=None, bench_root='../../benchmark/', input_root='./output/'):
    bench_json = bench_root + dataset_name + '/' + dataset_name + '.json'
    to_evaluate_json = input_root + dataset_name + '/' + input_json
    
    with open(bench_json, 'r') as j_f, open(to_evaluate_json, 'r') as to_eva:
        base_json = json.load(j_f)
        eva_json = json.load(to_eva)
    
    charts_bench = base_json['charts']
    charts_eva = eva_json['charts']
    
    if topk:
        charts_eva = charts_eva[0:topk]
    
    metric_funcs = Metrics.values()
    metrics = []
    for func in metric_funcs:
        metric_result = func(charts_bench, charts_eva)
        metrics.append(metric_result)
    if not topk:
        find_corresponding_item_single_dataset(dataset_name, charts_bench, charts_eva, input_json, bench_root=bench_root)
        find_corresponding_item_single_dataset_reverse(dataset_name, charts_bench, charts_eva, input_json, bench_root=bench_root)
    return tuple(metrics)


def evaluate_single(dataset_name, eva_json, input_json, topk=None, bench_root='../../benchmark/', input_root='./output/'):
    bench_json = bench_root + dataset_name + '/' + dataset_name + '.json'
    
    with open(bench_json, 'r') as j_f:
        base_json = json.load(j_f)
    
    charts_bench = base_json['charts']
    charts_eva = eva_json['charts']
    
    metric_funcs = Metrics.values()
    metrics = []
    for func in metric_funcs:
        metric_result = func(charts_bench, charts_eva)
        metrics.append(metric_result)
    match = []
    if not topk:
        match = find_corresponding_item_single_dataset(dataset_name, charts_bench, charts_eva, input_json, bench_root=bench_root)
    
    return tuple(metrics), match, len(charts_bench)


def get_dataset(dataset_name, output_file='/deepeye_output.json', bench_root='../../benchmark/', output_dir='./output'):
    csv_file = bench_root + dataset_name + '/' + dataset_name + '_drop_unused_cols.csv'
    type_file = bench_root + dataset_name + '/type/types.json'
    output_file = output_dir + '/' + dataset_name + output_file
    
    return {"csv_file": csv_file, "type_file": type_file, "output_file": output_file}


def from_visrank(dataset_name, base_alg, relation_func, personalization_func, authority=0, decay=None, output_dir='./output',
                 bench_root='../../benchmark/', output_f='/visrank_output.json', generation=None, parallel=False, model_name=None):
    dataset = get_dataset(dataset_name, output_file=output_f, bench_root=bench_root, output_dir=output_dir)
    vr = VizGRank('aaa', base_alg=base_alg, relation_func=relation_func, personalization_func=personalization_func, authority=authority,
                  decay=decay, parallel=parallel)
    with open(dataset['type_file']) as f:
        types = json.load(f)
    file = dataset['csv_file']
    vr.dataset_name = dataset_name
    vr.model_name = model_name
    
    result = []
    if generation:
        vr.load_visualizations_from_file(dataset_name, types, input_dir=generation, input_json='generation_output.json')
        bench_l = vr.to_list_benchmark_a()
    else:
        vr.read_data(file, dtypes=types).generate_visualizations().rank_visualizations()
        result = vr.output_visualizations()
        bench_l = vr.to_list_benchmark()
    
    dirpath, filename = os.path.split(dataset['output_file'])
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(dataset['output_file'], 'w') as test:
        json.dump(bench_l, test, indent=4)
    return result, bench_l


def process_benchmark_visrank(base_alg, relation_func, personalization_func, authority=0, decay=None, bench_root='../../benchmark/',
                              output_f='/visrank_output.json', excluded=None, output_dir='./output', generation=None):
    datasets = list_datasets(bench_root, '/raw_json', data_file_ext='_drop_unused_cols.csv')
    for dataset in datasets:
        if dataset['dataset']['name'] in excluded:
            continue
        with monitor('Processing ' + dataset['dataset']['name'] + '.' * 40):
            from_visrank(dataset['dataset']['name'], base_alg, relation_func, personalization_func, authority=authority, decay=decay,
                         bench_root=bench_root, output_f=output_f, output_dir=output_dir, generation=generation)


def evaluate_benchmark(bench_root, output, input_json, topK=None, excluded=None):
    datasets = list_datasets(bench_root, '/raw_json', data_file_ext='_drop_unused_cols.csv')
    if topK:
        out = './evaluate_output/top' + str(topK) + '/' + output
    else:
        out = './evaluate_output/all/' + output
    dirpath, filename = os.path.split(out)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(out, 'w') as out_f:
        metric_names = list(Metrics.keys())
        out_f.writelines(
            '%s\t%s\t%s\t%s\t%s\t%s\n' % tuple(['name'] + metric_names))
        all_datasets = []
        for dataset in datasets:
            dataset_name = dataset['dataset']['name']
            if dataset_name in excluded:
                continue
            metrics_result = evaluate_single_dataset(dataset['dataset']['name'], input_json, bench_root=bench_root, topk=topK)
            with monitor('Evaluating ' + dataset['dataset']['name']):
                out_f.write('%s\t' % dataset_name)
                out_f.writelines('%s\t%s\t%s\t%s\t%s\n' % metrics_result)
            all_datasets.append([dataset_name, ] + list(metrics_result))
    
    return tuple(all_datasets)


if __name__ == '__main__':
    process_benchmark_visrank(base_alg='PageRank', relation_func=context_dissimilarity,
                              personalization_func=chart_personalization,
                              generation=None, output_f='/visrank_output.json',
                              excluded=['avito_demand', 'donorschoose', 'employee_attrition', 'google_play_store'])
    evaluate_single_dataset('airplane_crashes', 'visrank_output.json')
