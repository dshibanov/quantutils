import json
import sys
sys.path.append('../')
sys.path.append('./')
import dictdiffer
from pprint import pprint
import copy
import inspect

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

def test_set_value_to():

    config = {'symbols':[
                            {'name': 'BTCUSDT',
                             'params': [{'name': 'from', 'value': 'ff'},
                                        {'name': 'to', 'value': 'ss'},
                                        {'name': 'cac', 'value': 121}]},

                            {'name': 'ETHUSDT',
                             'params': [{'name': 'from', 'value': 'ff'},
                                        {'name': 'to', 'value': 'ss'},
                                        {'name': 'cac', 'value': 121}]}]
             }

    before = copy.deepcopy(config)
    pprint(config)
    set_value_to(config, ['symbols', '0', 'params', '2'], 666)
    after = config
    pprint(config)

    diffs = list(dictdiffer.diff(before, after))
    pprint(diffs)

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

def test_extract_params_simple():

    # small test
    # config = {'symbols':[{'name': 'BTCUSDT', 'from': '', 'to': '', 'params': [{'name': 'cac', 'value': 121}]},
    #                               {'name': 'ETHUSDT', 'from': '', 'to': ''}]
    #          }


    # config = {'symbols':[
    #                         {'BTCUSDT': {'params': [{'name': 'from', 'value': 'ff'},
    #                                              {'name': 'to', 'value': 'ss'},
    #                                              {'name': 'cac', 'value': 121}]}},

    #                         {'ETHUSDT': {'params': [{'name': 'from', 'value': 'ff'},
    #                                              {'name': 'to', 'value': 'ss'},
    #                                              {'name': 'cac', 'value': 121}]}}]
    #          }



    config = {'symbols':[
                            {'name': 'BTCUSDT', 'params': [{'name': 'from', 'value': 'ff'},
                                                 {'name': 'to', 'value': 'ss'},
                                                 {'name': 'cac', 'value': 121}]},

                            {'name': 'ETHUSDT', 'params': [{'name': 'from', 'value': 'ff'},
                                                 {'name': 'to', 'value': 'ss'},
                                                 {'name': 'cac', 'value': 121}]}]
             }



    params = extract_params(config)
    # print(params)

    print(json.dumps(params, sort_keys=True, indent=4))


    assert len(params) == 6
    assert params[0]['name'] == 'symbols.0.params.0.from'
    assert params[1]['name'] == 'symbols.0.params.1.to'
    assert params[2]['name'] == 'symbols.0.params.2.cac'
    assert params[3]['name'] == 'symbols.1.params.0.from'
    assert params[4]['name'] == 'symbols.1.params.1.to'
    assert params[5]['name'] == 'symbols.1.params.2.cac'

def test_extract_params_complex():

    # full test
    config = {'data': {'symbols':[{'name': 'BTCUSDT', 'from': '', 'to': '', 'params': [{'name': 'cac', 'value': 121}]},
                                  {'name': 'ETHUSDT', 'from': '', 'to': ''}],

                       'params': [{'name': 'a', 'value': 4},
                                    {'name': 'b', 'value': 14},
                                    {'name': 'c', 'value': 54},
                                    {'name': 'd', 'value': 0.2334}
                                 ]
                      }
            }


    params = extract_params(config)
    print(params)


def test_inject_params_simple():
    params = [
    {
        "name": "symbols.0.params.0.from",
        "value": "666"
    },
    {
        "name": "symbols.0.params.1.to",
        "value": "ss"
    },
    {
        "name": "symbols.0.params.2.cac",
        "value": 121
    },
    {
        "name": "symbols.1.params.0.from",
        "value": "fffg"
    },
    {
        "name": "symbols.1.params.1.to",
        "value": "ss"
    },
    {
        "name": "symbols.1.params.2.cac",
        "value": 9000
    }
    ]


    config = {'symbols':[
                            {'name': 'BTCUSDT',
                             'params': [{'name': 'from', 'value': 'ff'},
                                        {'name': 'to', 'value': 'ss'},
                                        {'name': 'cac', 'value': 121}]},

                            {'name': 'ETHUSDT',
                             'params': [{'name': 'from', 'value': 'ff'},
                                        {'name': 'to', 'value': 'ss'},
                                        {'name': 'cac', 'value': 121}]}]
             }


    new_config = inject_params(copy.deepcopy(config), params)

    diffs = list(dictdiffer.diff(config, new_config))
    for d in diffs:
        print(d)


    assert diffs[0][0] == 'change'
    assert diffs[1][0] == 'change'
    assert diffs[2][0] == 'change'





def test_dictdiffer():
    a_dict = {
      'a': 'foo',
      'b': 'bar',
      'd': 'barfoo'
    }

    b_dict = {
      'a': 'foo',
      'b': 'BAR',
      'c': 'foobar'
    }


    diffs = list(dictdiffer.diff(a_dict, b_dict))

    assert diffs[0][0] == 'change'
    assert diffs[1][0] == 'add'
    assert diffs[2][0] == 'remove'

    # for diff in diffs:
    #     print(diff)


def get_param(params, name, default_value=None):
    for p in params:
        if p['name'] == name:
            return p
    raise Exception(f'Parameter {name} not found')
    return default_value

def test_inject():

    import env.env_config as fd
    from api.search import get_agent
    import api.datamart.datamart as dm

    timeframes = ['15m', '1h']
    config = {'env':{
                    'data': {
                              'timeframes': timeframes,
                              'from': '2020-1-1',
                              'to': '2020-1-2',
                              'symbols': [
                                            {
                                             'name': 'AST0',
                                             'from': '2020-1-1',
                                             'to': '2020-1-2',
                                             'synthetic': True,
                                             'ohlcv': True,
                                             'code': 0
                                            },

                                           {
                                            'name': 'AST1',
                                            'from': '2020-1-1',
                                            'to': '2020-1-2',
                                            'synthetic': True,
                                            'ohlcv': True,
                                            'num_of_samples': 1050,
                                            'code': 1
                                           }],
                              # 'num_folds': 3,
                              'max_episode_length': 40,
                              'min_episode_length': 15
                            },

                    'action_scheme': {'name': 'tensortrade.env.default.actions.MultySymbolBSH',
                                      'params': []},
                    'reward_scheme': {'name': 'tensortrade.env.default.rewards.SimpleProfit',
                                      'params': [{'name': 'window_size', 'value': 2}]},

                    # in this section general params
                    'params':[{'name': "feed_calc_mode", 'value': fd.FEED_MODE_NORMAL},
                            {'name': "make_folds", 'value': False},
                            {'name': "multy_symbol_env", 'value': True},
                            {'name': "use_force_sell", 'value': True},
                            {'name': "add_features_to_row", 'value': True},
                            {'name': "max_allowed_loss", 'value': 100},
                            {'name': "test", 'value': False},
                            {'name': "reward_window_size", 'value': 7},
                            {'name': "window_size", 'value': 1},
                            {'name': "num_service_cols", 'value': 2},
                            # {'name': "load_feed_from", 'value': 'feed.csv'},
                              {'name': "load_feed_from", 'value': ''},

                            ## save_feed, save calculated feed 
                            ## WARNING: this works if num of your agent is 1,
                            ## Otherwise it will work not correctly
                            {'name': "save_feed", 'value': False}]
                },

              'agents': [{'name': 'agents.sma_cross_rl.SMACross_TwoScreens',
                         'params': [{'name': 'n_actions', 'value': 2},
                                    {'name': 'observation_space_shape', 'value': (10,1)},
                                    {'name': 'upper_screen_fast_ma', 'value': 3, 'optimize': True, 'lower': 2,
                                     'upper': 5},
                                    {'name': 'upper_screen_slow_ma', 'value': 5, 'optimize': True, 'lower': 5,
                                     'upper': 11},
                                    {'name': 'lower_screen_fast_ma', 'value': 2, 'optimize': True, 'lower': 2,
                                     'upper': 5},
                                    {'name': 'lower_screen_slow_ma', 'value': 13, 'optimize': True, 'lower': 11,
                                     'upper': 17},
                                    {'name': 'timeframes', 'value': timeframes}]},
                         {'name': 'agents.sma_cross_rl.SMACross_TwoScreens',
                          'params': [{'name': 'n_actions', 'value': 2},
                                     {'name': 'observation_space_shape', 'value': (10, 1)},
                                     {'name': 'upper_screen_fast_ma', 'value': 2},
                                     {'name': 'upper_screen_slow_ma', 'value': 11},
                                     {'name': 'lower_screen_fast_ma', 'value': 5},
                                     {'name': 'lower_screen_slow_ma', 'value': 23},
                                     {'name': 'timeframes', 'value': timeframes}]}
                         ],
               'datamart': dm.DataMart(),
               'params': [{'name': 'add_features_to_row', 'value': True},
                            {'name':'check_track', 'value':True}],
              # "evaluate": 'nothing',
              "algo": {},
              "max_episode_length": 15, # smaller is ok
              "min_episode_length": 5, # bigger is ok, smaller is not
              "make_folds":True,
              "num_folds": 5,
              # "symbols": make_symbols(5, 410),
              # "symbols": make_symbols(2, 160),
              "cv_mode": 'proportional',
              "test_fold_index": 3,
              "reward_window_size": 1,
              "window_size": 2,
              "max_allowed_loss": 0.9,
              "use_force_sell": True,
              "multy_symbol_env": True,
              "test": False
    }

    agent = get_agent(config['agents'][0])
    config['env']['data']['features'] = agent.get_features()

    from api.search import get_search_space
    sspace = get_search_space(extract_params(copy.deepcopy(config)))
    for s in sspace:
        print(sspace[s].sample())
        sspace[s] = sspace[s].sample()

    config['optimize_params'] = {}
    for k in sspace:
        config['optimize_params'][k] = sspace[k]

    inject_params(config, config['optimize_params'])


def test_split():
    sep = '.'

    params = [{'name':'agents.0.params.2.fast_ma', 'value': 32}]
    for p in params:
        # fgf = 'agent.0.params.2.faat_ma'
        keys = p['name'].split(sep)[:-1]
        print(keys)
        # keys = p['name'].split(sep)[:-1]
        pipk = {'agents':[{'params': [{'sdsdsd'}, {'ssss'}, {'name': 'fast_ma', 'value': 12}]}]}
        set_value_to(pipk, keys, p['value'])



if __name__ == "__main__":
    # test_extract_params_simple()
    test_inject()
    # test_split()
    # test_inject_params_simple()
    # test_dictdiffer()
    # test_pointer()
    # test_set_value_to()



