import json
import typer
from json import JSONDecodeError
from typing import Any, List, Dict

def is_valid_json(json_path: str) -> Dict:
    try:
        with open(json_path) as f:
            data = json.load(f)
            return {'data' : data, 'is_valid' : True, 'error_msg' : None}
    except JSONDecodeError as e:
        return {'data' : {}, 'is_valid' : False, 'error_msg' : e}

def extract_keys(data: Any, keys: List) -> List[str]:
    if isinstance(data, dict):
        for key ,value in data.items():
            if key not in keys:
                keys.append(key)
            extract_keys(value, keys)
    elif isinstance(data, list):
        for dict_obj in data:
            if isinstance(dict_obj, dict):
                extract_keys(dict_obj, keys)
    return keys

def get_query(json_path: str) -> Dict:
    json_data = is_valid_json(json_path)
    if json_data['is_valid']:
        return json_data['data']
    else:
        error_msg = json_data['error_msg']
        raise ValueError(f'Error Parsing Json:  {error_msg}')

def get_keys(json_path: str) -> Any:
    json_obj = is_valid_json(json_path)
    if json_obj['is_valid']:
        json_data = json_obj['data']
        if isinstance(json_data, dict):
            return ', '.join(extract_keys(json_data, []))
    else:
        error_msg = json_obj['error_msg']
        raise ValueError(f'Error Parsing Json:  {error_msg}')

def run():
    print(get_keys('data/query.json'))

if __name__ == "__main__":
    typer.run(run)
