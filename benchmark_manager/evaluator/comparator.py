class hashabledict(dict):
    def __init__(self, dic):
        super().__init__()
        for key in dic:
            self[key] = dic[key]
    
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def compare_bar_set(chart_one, chart_two):
    dic1 = set()
    for key in chart_one['channels']:
        dic1.add(hashabledict(chart_one['channels'][key]))
    
    dic2 = set()
    for key in chart_two['channels']:
        dic2.add(hashabledict(chart_two['channels'][key]))
    return dic1 == dic2


def compare_line_set(chart_one, chart_two):
    dic1 = set()
    for key in chart_one['channels']:
        dic1.add(hashabledict(chart_one['channels'][key]))
    
    dic2 = set()
    for key in chart_two['channels']:
        dic2.add(hashabledict(chart_two['channels'][key]))
    return dic1 == dic2


def compare_pie_set(chart_one, chart_two):
    dic1 = set()
    for key in chart_one['channels']:
        dic1.add(hashabledict(chart_one['channels'][key]))
    
    dic2 = set()
    for key in chart_two['channels']:
        dic2.add(hashabledict(chart_two['channels'][key]))
    return dic1 == dic2


def compare_scatter_set(chart_one, chart_two):
    dic1 = set()
    for key in chart_one['channels']:
        dic1.add(hashabledict(chart_one['channels'][key]))
    
    dic2 = set()
    for key in chart_two['channels']:
        dic2.add(hashabledict(chart_two['channels'][key]))
    return dic1 == dic2


def compare_bar(chart_one, chart_two):
    for key in chart_one['channels']:
        for seckey in chart_one['channels'][key].keys():
            if chart_one['channels'][key][seckey] != chart_two['channels'][key][seckey]:
                return False
    return True


def compare_line(chart_one, chart_two):
    for key in chart_one['channels']:
        for seckey in chart_one['channels'][key].keys():
            if chart_one['channels'][key][seckey] != chart_two['channels'][key][seckey]:
                return False
    return True


def compare_pie(chart_one, chart_two):
    for key in chart_one['channels']:
        for seckey in chart_one['channels'][key].keys():
            if chart_one['channels'][key][seckey] != chart_two['channels'][key][seckey]:
                return False
    return True


def compare_scatter(chart_one, chart_two):
    for key in chart_one['channels']:
        for seckey in chart_one['channels'][key].keys():
            if chart_one['channels'][key][seckey] != chart_two['channels'][key][seckey]:
                return False
    return True


def compare(chart_one, chart_two):
    if chart_one['type'] != chart_two['type']:
        return False
    
    if chart_one['id'] == chart_two['id']:
        return True
    
    if len(chart_one['channels']) != len(chart_two['channels']):
        return False
    
    for key in chart_one['channels']:
        if key not in chart_two['channels']:
            return False
        for seckey in chart_one['channels'][key]:
            if seckey not in chart_two['channels'][key]:
                return False
    
    if chart_one['type'] == 'bar':
        return compare_bar(chart_one, chart_two)
    elif chart_one['type'] == 'line':
        return compare_line(chart_one, chart_two)
    elif chart_one['type'] == 'pie':
        return compare_pie(chart_one, chart_two)
    elif chart_one['type'] == 'scatter':
        return compare_scatter(chart_one, chart_two)


def compare_bench(chart_one, chart_two):
    if chart_one['type'] != chart_two['type']:
        return False
    
    if len(chart_one['channels']) != len(chart_two['channels']):
        return False
    
    for key in chart_one['channels']:
        if key not in chart_two['channels']:
            return False
        for seckey in chart_one['channels'][key]:
            if seckey not in chart_two['channels'][key]:
                return False
    
    if chart_one['type'] == 'bar':
        return compare_bar(chart_one, chart_two)
    elif chart_one['type'] == 'line':
        return compare_line(chart_one, chart_two)
    elif chart_one['type'] == 'pie':
        return compare_pie(chart_one, chart_two)
    elif chart_one['type'] == 'scatter':
        return compare_scatter(chart_one, chart_two)
