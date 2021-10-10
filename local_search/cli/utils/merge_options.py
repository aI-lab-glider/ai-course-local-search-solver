import json
from local_search.cli.utils.console import console


def merge_options(config_file_path: str, cli_options):
    options = cli_options
    if config_file_path:
        with open(config_file_path, 'r') as config:
            config = json.load(config)
            options = {
                k: cli_options.setdefault(
                    k, None) or config.setdefault(k, None)
                for k in set([*cli_options.keys(), *config.keys()])}
    console.log("Initialized with options: ", options)
    return options
