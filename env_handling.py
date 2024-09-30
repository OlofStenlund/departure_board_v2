import os
from dotenv import load_dotenv


def read_env_vars(env_path: str):
    with open(env_path, 'r') as file:
        lines = file.readlines()
    env_vars = {}
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            env_vars[key] = value
    return env_vars


def set_new_token_var(vars: list, new_token: str):
    """
    If token has expired do this. Otherwise, pass.
    if get_token_expiry (to be build) returns <3 (less than 3 seconds left),
    then a new token is needed, so continue. 
    Suggestion:
    if get_token_expiry(TOKEN) > 3:
        pass
    else:
        vars["TOKEN"] = f"{new_token}\n"
        return vars
        update_token_var(env_path, updated_vars)
    """

    vars["TOKEN"] = f"{new_token}"
    return vars


def update_token_var(env_path: str, env_vars: dict):
    with open(env_path, 'w') as file:
        for key, value in env_vars.items():
            file.write(f"{key}={value}\n")




def reload_env(env_path: str):
    # Clear current environment variables loaded from .env
    for key in read_env_vars(env_path).keys():
        os.environ.pop(key, None)
    # Load the environment variables from the .env file
    load_dotenv(env_path)
