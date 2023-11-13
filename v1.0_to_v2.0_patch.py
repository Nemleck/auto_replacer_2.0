import json

def correct_key_syntax(key: dict):
    # accept_lower_and_upper_case fix
    new_key = key
    new_params = None
    if "params" in key.keys() and key["params"] is list:
        new_params = {}
        for param in key["params"]:
            if param == "accept_lower_and_upper_case":
                new_params["case_sensitive"] = False
            else:
                new_params[param] = True
    
    new_key["params"] = new_params

    return new_key

def global_correct(file_content):
    file_content["global_params"]["default_config_params"] = {
        "keep_text": False,
        "case_sensitive": True,
        "separator": None,
        "operation": None
    }

    file_content["special_keys"]["clear"] = "²clear"

    return file_content

all_keys = []

# Open main file
with open("keys.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

data = global_correct(data)
data["keys"] = [correct_key_syntax(key) for key in data["keys"]]

# Write in the file the corrected configs
with open("keys.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Open external files and change configs inside
for file in data["external_keys"]:
    with open(file, "r", encoding="utf-8") as f:
        external_data = json.loads(f.read())

    external_data = [correct_key_syntax(key) for key in external_data]

    with open(file, "w", encoding="utf-8") as f:
        json.dump(external_data, f, indent=4, ensure_ascii=False)
