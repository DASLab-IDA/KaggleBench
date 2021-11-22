from KaggleBench.benchmark_manager.evaluator.comparator import compare_bench


def output(charts_eva, charts_bench, output_f='./output.match'):
    count = 0
    with open(output_f, 'w') as out:
        for chart in charts_eva:
            same_list = list(filter(lambda x: compare_bench(chart, x), charts_bench))
            if same_list:
                count += 1
            out.writelines(str(same_list) + '\n')
        out.writelines('The total number of charts covered is {}/{}'.format(count, len(charts_eva)))


def output_reverse(charts_eva, charts_bench, output_f='./output.match'):
    count = 0
    with open(output_f, 'w') as out:
        for chart in charts_bench:
            same_list = list(filter(lambda x: compare_bench(chart, x), charts_eva))
            if same_list:
                count += 1
            out.writelines(str(same_list) + '\n')
        out.writelines('The total number of charts covered is {}/{}'.format(count, len(charts_bench)))
