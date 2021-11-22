import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from .metrics.metric import metrics as Metrics
from .schemes.scheme import Schemes
import json


class Plot:
    color = ["#c1232b", "#27727b", "#fcce10", "#e87c25", "#b5c334", "#fe8463", "#9bca63", "#fad860", "#f3a43b",
             "#60c0dd", "#d7504b", "#c6e579", "#f4e001", "#f0805a", "#26c0c0"]
    marker = ['*', '+', 'x', 'o', '.', '|', 'v', ',', '^', '<', '>', 's', 'p', 'h', 'H', 'D', 'd', '_', '1', '2', '3', '4']
    hatch = ['/', '+', 'x', 'o', 'O', '.', '*', '\\', '|', '-']
    
    @staticmethod
    def plot_lines_from_file(input_dir='./evaluate_output', scheme=Schemes.schemes, output_dir='./plot_line_output', schemes_name=None):
        if not schemes_name:
            schemes_name = scheme
        if os.path.isdir(input_dir):
            lists = os.listdir(input_dir)
            topk_result = []
            metric_names = []
            filenames = []
            for item in lists:
                path = input_dir + '/' + item
                filenames = []
                if os.path.isdir(path) and item != 'all':
                    all_schemes = []
                    for sche in scheme:
                        filenames.append(sche)
                        filepath = path + '/' + sche + '.result'
                        one_scheme = pd.read_csv(filepath, '\t', index_col=0)
                        metric_names = one_scheme.columns.tolist()
                        all_schemes.append(one_scheme.mean().values.tolist())
                    topk_result.append((int(item[3:]), all_schemes))
                topk_result.sort(key=lambda x: x[0])
            Plot.plot_lines(filenames, list(map(lambda x: x[1], topk_result)), metric_names,
                            list(map(lambda x: x[0], topk_result)),
                            output_dir=output_dir, schemes_name=schemes_name)
    
    @staticmethod
    def plot_bars_from_file(input_dir='./evaluate_output/top5', scheme=Schemes.schemes, output_dir='./plot_output/top5', scheme_name=None,
                            baseline=None, datasets=[]):
        if os.path.isdir(input_dir):
            lists = os.listdir(input_dir)
            all_dataset = []
            filenames = []
            if baseline:
                base = pd.read_csv(baseline, '\t').values.tolist()
                tmp = []
                for i in base:
                    if i[0] in datasets:
                        tmp.append(i)
                all_dataset.append(tmp)
                scheme_name.insert(0, 'baseline')
                filenames.insert(0, 'baseline')
            for item in lists:
                if item.endswith('.result'):
                    if item[:-7] in scheme:
                        filenames.append(item[:-7])
                        filepath = input_dir + '/' + item
                        one_scheme = pd.read_csv(filepath, '\t')
                        all_dataset.append(one_scheme.values.tolist())
            
            Plot.plot_bars(filenames, all_dataset, list(Metrics.keys()), output_dir=output_dir, scheme_name=scheme_name)
            Plot.plot_boxes(filenames, all_dataset, list(Metrics.keys()), output_dir=output_dir, scheme_name=scheme_name)
    
    @staticmethod
    def plot_bars(schemes, all_datasets, metric_names, output_dir='./evaluate_output', scheme_name=None):
        if not scheme_name:
            scheme_name = schemes
        x_axis = [x for x in list(map(lambda x: x[0], all_datasets[0]))]
        bar_width = 0.6
        margin = 0.3
        scale = 1 / (bar_width * len(schemes) + margin * 2)
        loc = np.arange(len(x_axis))
        for i in range(len(metric_names)):
            for j in range(len(schemes)):
                y_axis = list(map(lambda x: x[i + 1], all_datasets[j]))
                plt.bar(loc / scale + bar_width * j, y_axis, bar_width, align='center',
                        color='#08BAE7' if scheme_name[j] == 'baseline' else Plot.color[j % len(Plot.color)],
                        label=scheme_name[j])
            
            # plt.xlim(min(loc) - bar_width, max(loc) + bar_width * len(x_axis))
            fontsize = 12
            plt.xlabel("Dataset", fontsize=fontsize)
            plt.ylabel(metric_names[i], fontsize=fontsize)
            plt.xticks(loc / scale + bar_width * len(schemes) / 2, x_axis, size='small', rotation=60)
            plt.legend(loc='center left', fontsize=fontsize, bbox_to_anchor=(1, 0.5))
            out = output_dir + '/' + metric_names[i] + '.pdf'
            dirpath, filename = os.path.split(out)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            plt.savefig(fname=out, format='pdf', bbox_inches='tight')
            plt.clf()
    
    @staticmethod
    def plot_lines(schemes, results, metric_names, topks, output_dir='./top5-100', schemes_name=None):
        if not schemes_name:
            schemes_name = schemes
        for i in range(len(metric_names)):
            x_axis = topks
            plt.figure(figsize=(10, 8))
            for j in range(len(schemes)):
                y_axis = list(map(lambda x: x[j][i], results))
                plt.plot(x_axis, y_axis, color=Plot.color[j % len(Plot.color)], label=schemes_name[j],
                         marker=Plot.marker[j % len(Plot.marker)], ms=12, linewidth=2)
            fontsize = 24
            plt.xlabel("Top K recommended visualizations", fontsize=fontsize)
            plt.ylabel(metric_names[i], fontsize=fontsize)
            plt.legend(loc='lower right', fontsize=fontsize)
            plt.xticks(fontsize=fontsize)
            plt.yticks(fontsize=fontsize)
            out = output_dir + '/' + metric_names[i].replace(' ', '') + '.pdf'
            dirpath, filename = os.path.split(out)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            plt.savefig(fname=out, format='pdf', bbox_inches='tight')
            plt.show()
    
    @staticmethod
    def plot_all_topk(input_dir='./evaluate_output', scheme=Schemes.schemes, output_dir='./plot_output', scheme_name=None, baseline=None,
                      datasets=None):
        if os.path.isdir(input_dir):
            lists = os.listdir(input_dir)
            for item in lists:
                path = input_dir + '/' + item
                outpath = output_dir + '/' + item
                if os.path.isdir(path):
                    Plot.plot_bars_from_file(input_dir=path, scheme=scheme, output_dir=outpath, scheme_name=scheme_name, baseline=baseline,
                                             datasets=datasets)
    
    @staticmethod
    def plot_boxes(schemes, all_datasets, metric_names, output_dir='./evaluate_output', scheme_name=None):
        if not scheme_name:
            scheme_name = schemes
        for i in range(len(metric_names)):
            box = []
            for j in range(len(schemes)):
                y_axis = list(map(lambda x: x[i + 1], all_datasets[j]))
                box.append(y_axis)
            
            boxes = plt.boxplot(box, patch_artist=True, labels=scheme_name, showmeans=True)
            
            for patch, color in zip(boxes['boxes'], Plot.color):
                patch.set_facecolor(color)
            
            # plt.xlim(min(loc) - bar_width, max(loc) + bar_width * len(x_axis))
            plt.figure(figsize=(10, 10))
            fontsize = 24
            plt.xlabel("Method", fontsize=fontsize)
            plt.ylabel(metric_names[i], fontsize=fontsize)
            plt.xticks(size='small')
            # plt.legend(boxes['boxes'], scheme_name, loc='upper right', fontsize=fontsize)
            out = output_dir + '/' + metric_names[i] + '_box.pdf'
            dirpath, filename = os.path.split(out)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            plt.savefig(fname=out, format='pdf', bbox_inches='tight')
            plt.clf()


if __name__ == '__main__':
    # Plot.plot_all_topk(input_dir='./evaluator/evaluate_output', output_dir='./evaluator/evaluate_output',
    #                    baseline='./evaluate_output/all/VisRank-rsim-corr.result',
    #                    datasets=['airplane_crashes',
    #                              'avocados_price',
    #                              'flight_delay',
    #                              'google_play_store',
    #                              'gun_violence',
    #                              'h1b_visa',
    #                              'kickstarter',
    #                              'patient_charge',
    #                              # 'student_performance',
    #                              'suicide_rates',
    #                              'titan',
    #                              'videogame',
    #                              'zomato'],
    #                    scheme=['dt_model', 'etr_model', 'mlp_model',
    #                            'lgbm_model', 'xgb_model', 'gbdt_model'],
    #                    scheme_name=['DT', 'ETR', 'MLP',
    #                                 'LGBM', 'XGB', 'GBDT'])
    
    comparionofrelations = [
        'baseline_shuffle',
        'VisRank-sim_withviz',
        'VisRank-rsim_withviz',
        'VisRank-session_aware_withviz',
        # 'VisRank-sim_withoutviz',
        # 'VisRank-rsim_withoutviz',
        # 'VisRank-session_aware_withoutviz',
    ]
    
    thresholds = [
        'baseline_shuffle',
        # 'VisRank-session_aware_withviz',
        # 'VisRank-session_aware_withoutviz',
        # "VisRank-session_aware_withoutviz-0.0",
        "VisRank-session_aware_withoutviz-0.05",
        # "VisRank-session_aware_withviz-0.1",
        # "VisRank-session_aware_withoutviz-0.15",
        # "VisRank-session_aware_withoutviz-0.2",
        "VisRank-session_aware_withoutviz-0.25",
        # "VisRank-session_aware_withoutviz-0.3",
        "VisRank-session_aware_withoutviz-0.35",
        # "VisRank-session_aware_withoutviz-0.4",
        "VisRank-session_aware_withoutviz-0.45",
        # "VisRank-session_aware_withoutviz-0.5",
        # "VisRank-session_aware_withoutviz-0.6",
        # "VisRank-session_aware_withoutviz-0.7",
    ]
    
    comparisonofdeepeye = [
        'baseline_shuffle',
        'VisRank-sim_withviz',
        'VisRank-rsim_withviz',
        'VisRank-session_aware_withviz',
        'DeepEye',
        "Similarity-DeepEye",
        "Distance-DeepEye",
        "Hybrid-DeepEeye",
        # "Similarity-DeepEye-withoutviz",
        # "Distance-DeepEye-withoutviz",
        # "Hybrid-DeepEeye-withoutviz",
    ]
    
    scheme = [
        'baseline',
        'baseline_corr',
        'baseline_shuffle_table',
        'baseline_shuffle',
        'baseline_matching_quality',
        'DeepEye',
        'VisRank-sim_withviz',
        'VisRank-sim_withviz-corr',
        'VisRank-sim_withviz-match',
        'VisRank-rsim_withviz',
        'VisRank-rsim_withviz-corr',
        'VisRank-rsim_withviz-match',
        'VisRank-session_aware_withviz',
        'VisRank-session_aware_withviz-corr',
        'VisRank-session_aware_withviz-match',
        'VisRank-sim_withoutviz',
        'VisRank-sim_withoutviz-corr',
        'VisRank-sim_withoutviz-match',
        'VisRank-rsim_withoutviz',
        'VisRank-rsim_withoutviz-corr',
        'VisRank-rsim_withoutviz-match',
        'VisRank-session_aware_withoutviz',
        'VisRank-session_aware_withoutviz-corr',
        'VisRank-session_aware_withoutviz-match',
        "VisRank-session_aware_withoutviz-0.0",
        "VisRank-session_aware_withoutviz-0.05",
        "VisRank-session_aware_withoutviz-0.1",
        "VisRank-session_aware_withoutviz-0.15",
        "VisRank-session_aware_withoutviz-0.2",
        "VisRank-session_aware_withoutviz-0.25",
        "VisRank-session_aware_withoutviz-0.3",
        "VisRank-session_aware_withoutviz-0.35",
        "VisRank-session_aware_withoutviz-0.4",
        "VisRank-session_aware_withoutviz-0.45",
        "VisRank-session_aware_withoutviz-0.5",
        "VisRank-session_aware_withoutviz-0.6",
        "VisRank-session_aware_withoutviz-0.7",
        "Similarity-DeepEye",
        "Distance-DeepEye",
        "Hybrid-DeepEeye"
    ]
    
    vsdp_ide = [
        'baseline_shuffle_ide',
        # 'VisRank-sim_withviz',
        # 'VisRank-rsim_withoutviz',
        'VisRank-session_aware_withviz-0.45',
        'DeepEye',
        # "Similarity-DeepEye",
        # "Distance-DeepEye",
        # "Hybrid-DeepEeye",
    ]
    
    with open('scheme2name.json') as f:
        dic = json.load(f)
    to_plot = thresholds
    scheme_name = []
    for schem in to_plot:
        scheme_name.append(dic[schem])
    
    Plot.plot_lines_from_file(
        scheme=to_plot,
        schemes_name=scheme_name,
        input_dir='./evaluate_output',
        output_dir='./thresholds'
    )
    # Plot.plot_all_topk(
    #     scheme=dic['scheme'],
    #     scheme_name=dic['schemes_name'],
    # )
