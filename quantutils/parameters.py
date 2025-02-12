import json
import sys
sys.path.append('../')
sys.path.append('./')
import dictdiffer
from pprint import pprint
import copy
import inspect


def get_distribution(config):
    # func_name = config.get('distribution', 'uniform')
    func_name = config.get('distribution', 'randint')
    module_path = 'ray.tune'
    module = ilib.import_module(module_path)
    f_name = getattr(module, func_name)
    keys_to_remove = {'name', 'distribution', 'optimize', 'value'}
    params = {k: v for k, v in config.items() if k not in keys_to_remove}
    return f_name(**params)
def get_search_space(params):
    search_space = {}
    for p in params:
        if p.get('optimize', False) == True:
            search_space[p['name']] = get_distribution(p)
    return search_space
def get_agent(config):
    agent_name = config["name"]
    agent_params = config["params"]
    class_name = agent_name.rpartition('.')[-1]
    module_path, class_name = agent_name.rsplit('.', 1)
    module = ilib.import_module(module_path)
    class_name = getattr(module, class_name)
    return class_name(agent_params)

def set_value_to(config, keys, value):
    d = config
    for k in keys:
        if type(d) == list:
            d = d[int(k)]
        elif type(d) == dict:
            d = d.get(k)
        # else:
        #     print('Unexpected type:', type(d))

    d['value'] = value


def inject_params(params, config, sep='.'):

    for p in params:
        # get keys
        # ss = p['name'].split(sep)
        ss = p.split(sep)
        # keys = p['name'].split(sep)[:-1]
        keys = p.split(sep)[:-1]
        # set_value_to(config, keys, p['value'])
        set_value_to(config, keys, params[p])
        # print(keys)
        # return
        #
    return config





def extract_params(config, pref='', sep='.'):
    # print('func: ', inspect.currentframe().f_code.co_name)
    params = []

    if type(config) == dict:
        for k in config:
            if k == 'params':
                for i,p in enumerate(config[k],0):
                    # p = copy.deepcopy(v)
                    params.append(p)
                    params[-1]['name'] = f'params.{i}.{params[-1]["name"]}'
            else:
                extracted = extract_params(config[k], f'{k}', sep)
                for p in extracted:
                    params.append(p)

    elif type(config) == list:
        for i,k in enumerate(config,0):
            extracted = extract_params(k, f'{i}', sep)
            for p in extracted:
                params.append(p)
    else:
        # print('Unexpected type:', type(config))
        return []

    for p in params:
        p['name'] = f'{p["name"]}' if pref == '' else f'{pref}{sep}{p["name"]}'

    return params



def get_param(params, name, default_value=None):
    for p in params:
        if p['name'] == name:
            return p
    raise Exception(f'Parameter {name} not found')
    return default_value




if __name__ == "__main__":
    # test_extract_params_simple()
    test_inject()
    # test_split()
    # test_inject_params_simple()
    # test_dictdiffer()
    # test_pointer()
    # test_set_value_to()



