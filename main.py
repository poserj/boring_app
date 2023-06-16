import json
import time
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
    args = ((tmp, api['base_url']) for tmp in (query * api['number_req']))
    net_results = set()
    with ThreadPoolExecutor(max_workers=app['number_threads']) as executor:
        # set позволяет удалить дубли
        net_results = set(executor.map(helpers.get_activity, args))
    net_results = helpers.filter(net_results)
    a = [p.price, p.type, p.accessibility, p.participants]
    args = (
        (
            a,
            [tmp['price'], tmp['type'], tmp['accessibility'], tmp['participants']],  # type: ignore
            tmp,
        )
        for tmp in net_results
    )
    with ProcessPoolExecutor(max_workers=app['number_process']) as executer:
        results = executer.map(helpers.get_similar, args)
    sorted_result = sorted(results, key=lambda x: x['matcher'], reverse=True)
    helpers.show_result(sorted_result)
