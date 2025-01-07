#!/usr/bin/env python

import os

import yaml
import argparse


def main():
    parser = argparse.ArgumentParser(description='Create a configuration file from a folder of configuration files')
    parser.add_argument('--config-folder', type=str, help='Folder containing the configuration files')
    parser.add_argument('--output-file', type=str, help='Output file to save the configuration')

    args = parser.parse_args()
    create_config(args.config_folder, args.output_file)

def create_config(config_folder, output_file):
    config_files = [f.path for f in os.scandir(config_folder) if f.path.endswith(".yaml")]

    config = {}
    for config_file in config_files:
        with open(config_file, 'r') as file:
            config.update(yaml.safe_load(file))

    with open(output_file, 'w') as file:
        yaml.dump(config, file)

    return config


if __name__ == "__main__":

    main()