import sys

sys.path.append('../..')

from KaggleBench.benchmark_manager.plot import Plot
from KaggleBench.benchmark_manager.schemes.scheme import Schemes
from KaggleBench.benchmark_manager.metrics.metric import metrics as Metrics
from KaggleBench.benchmark_manager.evaluator.evaluator import process_benchmark_visrank, evaluate_benchmark

bench_root = '../benchmark/'


def topk_evaluator(topks=None, excluded=None, schemes=Schemes.schemes):
    metric_names = list(Metrics.keys())
    if not topks:
        topks = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    
    average_among_datasets = []
    for topk in topks:
        all_datasets = evaluate_benchmark_all(topk, excluded, schemes=schemes)
        
        # Plot.plot_bars(schemes, all_datasets, metric_names, output_dir='./plot_output_all' + '/top' + str(topk))
        
        average_results = []
        for j in range(len(schemes)):
            one_scheme = []
            for i in range(len(metric_names)):
                temp = list(map(lambda x: x[i + 1], all_datasets[j]))
                one_scheme.append(sum(temp) / len(temp))
            average_results.append(one_scheme)
        
        average_among_datasets.append(average_results)
    
    Plot.plot_lines(schemes, average_among_datasets, metric_names, topks, output_dir='./plot_output_all')


def process_benchmark_all(excluded=None, schemes=Schemes.schemes, params=Schemes.params):
    for i in range(len(schemes)):
        param = params[schemes[i]]
        if schemes[i].startswith('baseline'):
            continue
        elif schemes[i] == 'DeepEye':
            continue
        else:
            process_benchmark_visrank(base_alg='PageRank',
                                      relation_func=param['r_func'], personalization_func=param['p_func'], decay=param['decay'],
                                      bench_root=bench_root, output_f='/' + param['input_json'], excluded=excluded)


def evaluate_benchmark_all(topk=None, excluded=None, schemes=Schemes.schemes, params=Schemes.params):
    result = []
    for i in range(len(schemes)):
        result.append(evaluate_benchmark(bench_root, output=schemes[i] + '.result', input_json=params[schemes[i]]['input_json'], topK=topk,
                                         excluded=excluded))
    
    return result


if __name__ == '__main__':
    to_run = ['VizGRank-Sim', 'VizGRank-Devi']
    ### process all dataset
    process_benchmark_all(schemes=to_run, excluded=Schemes.excluded)
    evaluate_benchmark_all(schemes=to_run, excluded=Schemes.excluded)
    
    ### process all dataset with topk constraint
    topk_evaluator(schemes=to_run, excluded=Schemes.excluded)
    Plot.plot_lines_from_file(
        scheme=['baseline_shuffle', 'DeepEye', 'VizGRank-Sim', 'VizGRank-Devi'],
        schemes_name=['baseline', 'DeepEye', 'VizGRank-Sim', 'VizGRank-Devi'],
        input_dir='./evaluate_output',
        output_dir='./plot_output'
    )
