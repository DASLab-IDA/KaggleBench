import sys
import os
sys.path.append(os.path.abspath('..'))
from KaggleBench.benchmark_manager.cleaner.chart_manager import process_single_dataset
from KaggleBench.benchmark_manager.cleaner.column_manager import drop_unused_cols_single
from KaggleBench.benchmark_manager.util.file_manager import get_dataset_by_name

if __name__ == '__main__':
    # process_whole_benchmark(bench_root='../../benchmark/')
    dataset_name = 'zomato'
    dataset = get_dataset_by_name(bench_root='../benchmark/', dataset_name=dataset_name, data_file_ext='_raw.csv')
    process_single_dataset(dataset, bench_root='../benchmark/')
    drop_unused_cols_single(dataset_name, '_drop_unused_cols', bench_root='../benchmark/')
