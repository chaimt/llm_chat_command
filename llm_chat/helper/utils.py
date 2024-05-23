import json
import os
import random
from datetime import datetime, timedelta


def generate_random_value(value_type):
    if value_type == int:
        return random.randint(0, 100)
    elif value_type == float:
        return random.uniform(0.0, 100.0)
    elif value_type == str:
        return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=10))
    elif value_type == bool:
        return random.choice([True, False])
    elif value_type == datetime:
        start_date = datetime(1970, 1, 1)
        end_date = datetime.today()
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        return random_date
    else:
        raise ValueError("Unsupported type")


def add_suffix_to_filename(file_path: str, suffix: str):
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{suffix}{ext}"
    new_file_path = os.path.join(directory, new_filename)
    return new_file_path


def load_json_file(json_file):
    with open(json_file, "r") as file:
        return json.load(file)


def save_json_file(obj, json_file):
    with open(json_file, "w") as file:
        return json.dump(obj, indent=4, fp=file)


def subfolder_exists(folder_path, subfolder_name):
    subfolder_path = os.path.join(folder_path, subfolder_name)
    return os.path.exists(subfolder_path) and os.path.isdir(subfolder_path)


def remove_keys_recursively(dict_obj, keys_to_remove):
    """Removes multiple keys from a nested dictionary, no matter how deeply nested."""
    if isinstance(dict_obj, dict):
        for k in list(dict_obj.keys()):
            if k in keys_to_remove:
                del dict_obj[k]
            else:
                remove_keys_recursively(dict_obj[k], keys_to_remove)
    elif isinstance(dict_obj, list):
        for i in range(len(dict_obj)):
            remove_keys_recursively(dict_obj[i], keys_to_remove)
    return dict_obj


def clean_llm_json(text: str) -> str:
    return text.replace("```{", "{").replace("```json", "").replace("```", "").replace("\n\t", "").replace("\n", "")


def add_slash_if_missing(input_string: str) -> str:
    if not input_string.endswith("/"):
        input_string += "/"
    return input_string


def list_normalized(data: dict):
    attributes = []
    for attr in data.keys():
        if attr.endswith("_normalized"):
            attributes.append(attr)
    return attributes


def list_null_keys(data: dict):
    attributes = []
    for attr in data.keys():
        if not data[attr]:
            attributes.append(attr)
    return attributes


def clean_dict(data: dict, attributes):
    for attr in attributes:
        if attr in attributes:
            data.pop(attr, None)

    return data


def remove_duplicates(dict_list):
    seen = set()
    unique_list = []

    for d in dict_list:
        if isinstance(d, list):
            sub_unique_list = remove_duplicates(d)
            for item in sub_unique_list:
                items = frozenset(item.items())
                if items not in seen:
                    seen.add(items)
                    unique_list.append(item)

        else:
            # Convert dictionary to frozenset of items
            items = frozenset(d.items())
            if items not in seen:
                seen.add(items)
                unique_list.append(d)

    return unique_list
