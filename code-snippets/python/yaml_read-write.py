#!/usr/bin/env python
"""
Author : Veerendra K
Description : Simple yaml file reader and writer
"""
import os
import yaml
import io


def read_yaml(file_name):
    if not os.path.exists(file_name):
        print "{} not found! Please check.".format(file_name)
        exit(1)
    with open(file_name) as f:
        data = yaml.load(f)
    return data


def write_yaml(data, yaml_file):
    with io.open(yaml_file, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)