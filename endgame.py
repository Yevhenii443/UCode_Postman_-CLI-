import requests
import json
import argparse
import logging
from check_url import check_url
from parameter_parse import parameter_parse
import yaml
import time
from create_db import create_db, insert, show_db, clear_db, show_raw
from gui import start


def gui_start():
    start()


def method_to_create(site_url):
    start = time.time()
    try:
        res = requests.request(method=arguments.method, url=site_url,
                               params=parameter_parse(arguments.params),
                               headers=parameter_parse(arguments.headers),
                               data=parameter_parse(arguments.body))
    except Exception:
        return 'INVALID METHOD / INVALID URL: Method does not match in address'

    end = time.time()
    time_elapsed = end - start

    # SQL INSERTION
    method_sql = str(arguments.method)
    url_sql = str(arguments.endpoint)
    params_sql = str(parameter_parse(arguments.params))
    body_param_sql = str(arguments.body)
    requests_status_sql = str(res.status_code)
    headers_sql = str(arguments.headers)
    ####

    print(f'---Got response {res.status_code} OK in {round(time_elapsed, 2)} seconds---')
    print('---Response body---')
    if arguments.yaml:
        yaml_obj = yaml.safe_load(res.text)
        yaml_res = yaml.dump(yaml_obj)
        try:
            insert(method_sql, url_sql, params_sql, body_param_sql, headers_sql, requests_status_sql, yaml_res)
        except Exception:
            return 'Invalid parameter entered for the method.'

        print(yaml_res)
    else:
        json_obj = json.loads(res.text)
        json_res = json.dumps(json_obj, indent=4)
        try:
            insert(method_sql, url_sql, params_sql, body_param_sql, headers_sql, requests_status_sql, json_res)
        except Exception:
            return 'Invalid parameter entered for the method.'

        print(json_res)


# ARGPARSE OBJECT
parser = argparse.ArgumentParser()
parser.add_argument('--method', default='GET', choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
parser.add_argument('--gui', action='store_true')
parser.add_argument('--history', choices=['clear', 'show'])
parser.add_argument('--yaml', action='store_true')
parser.add_argument('--endpoint')
parser.add_argument('--show', choices=['raw', 'table', 'json', 'yaml'])
# PANDAS OUTPUT


#####

# POST, PUT REQUESTS
parser.add_argument('--body', nargs='*')
#####

# GET REQUEST
parser.add_argument('--params', nargs='*')
parser.add_argument('--headers', nargs='*')
#####

arguments = parser.parse_args()
#####


if __name__ == '__main__':
    create_db()
    if arguments.gui:
        gui_start()
    else:
        if arguments.history == 'clear':
            print(clear_db())
        elif arguments.history == 'show':
            show_db()
        elif arguments.show == 'raw':
            show_raw()
        else:
            method_to_create(check_url(arguments.endpoint))
