from VizGRank.vizgrank.node_relation import *
from VizGRank.vizgrank.personalization import *
from VizGRank.dp_pack.instance import Instance


class Schemes:
    excluded = []
    schemes = [
        'baseline',
        'DeepEye',
        'VizGRank-Sim',
        'VizGRank-Devi'
    ]
    params = {
        "baseline":
            {'input_json': 'baseline_output.json', 'output_result': ''},
        "DeepEye":
            {'input_json': 'deepeye_output.json', 'output_result': ''},
        "VizGRank-Devi":
            {'input_json': 'vizgrank_sim_output.json', 'output_result': '',
             'r_func': context_dissimilarity, 'p_func': None, 'decay': False},
        "VizGRank-Sim":
            {'input_json': 'vizgrank_devi_output.json', 'output_result': '',
             'r_func': context_similarity, 'p_func': None, 'decay': False},
    }


if __name__ == '__main__':
    print(len(Schemes.schemes), len(Schemes.params))
    for key in Schemes.schemes:
        print(Schemes.params[key])
