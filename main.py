import json
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import helpers

if __name__ == '__main__':

    data = helpers.app_init()
    api = data['API']
    app = data['APP']
    p = helpers.input_parametr(
        app['base_accessibility'],
        app["base_type"],
        app["base_participants"],
        app["base_price"],
    )
    query = helpers.form_query(p)
    tmp_res = []
    args = ((tmp, api['base_url']) for tmp in (query * 10))
    net_results = set()
    with ThreadPoolExecutor() as executor:
        net_results = set(executor.map(helpers.get_activity, args))
    for r in net_results:
        tmp: dict = json.loads(r)
        if tmp.get('error'):
            continue
        else:
            tmp_res.append(tmp)
    # prepare args for model
    a = [p.price, p.type, p.accessibility, p.participants]
    args = (
        (
            a,
            [tmp['price'], tmp['type'], tmp['accessibility'], tmp['participants']],  # type: ignore
            tmp,
        )
        for tmp in tmp_res
    )
    with ProcessPoolExecutor() as executer:
        results = executer.map(helpers.get_similar, args)
    del tmp_res
    r = sorted(results, key=lambda x: x[0], reverse=True)
    helpers.show_result(r)
