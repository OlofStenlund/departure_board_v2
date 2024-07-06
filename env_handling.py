def read_env_vars(env_path):
    with open(env_path, 'r') as file:
        lines = file.readlines()
    env_vars = {}
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            env_vars[key] = value
    return env_vars

def add_token_to_env(env_path, key, value):
    with open(env_path, 'a') as file:
        file.write(f"{key} = {value}\n")

def set_new_token_var(vars, new_token):
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


def update_token_var(env_path, env_vars):
    with open(env_path, 'w') as file:
        for key, value in env_vars.items():
            file.write(f"{key}={value}\n")



