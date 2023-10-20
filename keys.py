import keyboard
import time, json
from copy import deepcopy

# Allow more math operations in configs
from operations import *

from req import get_wiki_info

keyboard.on_press_key

class Keys:
    def __init__(self):
        self.last_keys = []
        self.last_text = ""

        self.limit = 50

        self.on = True
        # self.input_content = None

        self.parameters = {}
        self.configs = []

        self.load_configs()
    
    def load_configs(self):
        all_keys = []

        # Open main file
        with open("keys.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        
        all_keys += data["keys"]
        
        # Open external files and read configs inside
        for file in data["external_keys"]:
            with open(file, "r", encoding="utf-8") as f:
                external_data = json.loads(f.read())
                all_keys += external_data

        # Avoid "params" missing error
        for key in all_keys:
            if not "params" in key:
                key["params"] = {}

            # Put default values if there isn't
            default_params = data["global_params"]["default_config_params"]
            for param in default_params:
                if not param in key["params"].keys():
                    key["params"][param] = default_params[param]

        self.configs = all_keys
        self.parameters = data
    
    def add_key(self, event):
        if (event.event_type == keyboard.KEY_UP):
            return
        
        name = event.name.replace("space", " ")
        
        # if not self.input_content:
        #     if event.name == "enter":
        #         self.input_content = None
        #     elif len(name) == 1:
        #         self.input_content += name

        #     return

        self.last_keys.append(event.name)

        # If the list is "full", delete the first element
        if len(self.last_keys) > self.limit:
            if len(self.last_keys[0]) == 1:
                self.last_text = self.last_text[1:]

            del self.last_keys[0]
        
        # Delete letters
        if event.name == "backspace":
            del self.last_keys[-1]
            self.last_text = self.last_text[0:-1]
        
        # "Normal" key
        if len(name) == 1:
            self.last_text += name

            self.is_there_special_event()

        # Test the key if on
        if self.on:
            self.is_in_config()
    
    def is_in_config(self):
        # Test all configs

        for config in self.configs:
            input_params = config["params"]
            input_text, input_args = self.get_text_and_params(self.last_text, config["params"]["separator"])

            is_there_input, common_params = self.endswith(config["input"], input_text, input_args, config["params"])
            
            if is_there_input:
                output_text = config["output"]

                # Perform operations
                op = config["params"]["operation"]
                if op != None:
                    for var in op.keys():
                        text_to_eval = self.get_replaced_text(op[var], config, common_params)
                        
                        try:
                            common_params[var] = str(eval(text_to_eval))
                        except Exception as e:
                            print(e.args)
                            common_params[var] = "error"

                # Replace str params with actual content
                output_text = self.get_replaced_text(output_text, config, common_params)

                # Delete text if not keep_text param enabled
                if type(config["input"]) is str and config["params"]["keep_text"] == False:
                    to_remove = len(self.get_replaced_text(config["input"], config, common_params)) + (len(common_params))

                    self.remove(to_remove)
                    pass
                
                self.write(output_text)

                self.last_text = ""
                self.last_keys = []
    
    def get_replaced_text(self, text:str, config:dict, common_params:dict):
        input_args, output_args = list(common_params.keys()), list(common_params.values())
        separator = config["params"]["separator"]

        if input_args:
            for i in range(len(input_args)):
                text = text.replace(separator[0] + input_args[i] + separator[1], output_args[i])
        
        return text

    def endswith(self, text: str|list[str], input_text, input_args, params=None):
        if params == None:
            params = self.parameters["global_params"]["default_config_params"]

        if type(text) is str:
            # Get params
            separator = params["separator"]
            case_sensitive = params["case_sensitive"]

            # Lower the text if lower enabled
            last_text = self.last_text
            if not case_sensitive:
                last_text = last_text.lower()
                text = text.lower()

            # No options ?
            if separator == None:
                return last_text.endswith(text), {}
            
            # Options ?
            else:
                # Get text without params, and params
                to_test_text, to_test_params = self.get_text_and_params(text, separator)

                # Make the two params lists have the same len, taking the last elements
                excess_values = len(input_args) - len(to_test_params)

                # Too much or just enough parameters in user input
                if excess_values >= 0:
                    input_args = input_args[excess_values:]

                    print(input_args, to_test_params)

                    # Link the config input param to the user input param in one dict
                    common_params = {}
                    for i in range(len(to_test_params)):
                        common_params[to_test_params[i]] = input_args[i]

                    return input_text.endswith(to_test_text), common_params
                
                else: # No parameters in user input
                    return False, {}
        else:
            # Input is list ?
            check = True
            for key in text:
                if not key in self.last_keys:
                    check = False
                    break
            
            return check, {}

    def get_text_and_params(self, text, separator):
        # No separator configured
        if not separator:
            return text, None
        
        final_text = ""
        params = []
        param_text = ""

        oppened = False
        for ch in text:
            if ch == separator[0]:
                if not oppened:
                    oppened = True
                else:
                    final_text += param_text
                    param_text = ""

                final_text += separator[0]

                continue
            elif ch == separator[1]:
                final_text += separator[1]

                oppened = False

                params.append(param_text)
                param_text = ""

                continue

            if oppened:
                param_text += ch
            else:
                final_text += ch

        print(text, "->", final_text, params)
        return final_text, params
    
    def get_stringed_configs(self):
        final_text = ""
        for config in self.configs:
            output = config["output"].replace("\n","")
            input = config["input"].replace("\n","")

            final_text += f'{input} => {output}\n'
        
        return final_text

    def write(self, text: list[str] | str):
        if type(text) is str:
            keyboard.write(text, 0.01)

            # .replace("{","bo").replace("}","bf").replace("[","co").replace("]","cf")
        
        else:
            for key in text:
                keyboard.press(key)
            
            for key in text:
                keyboard.release(key)

    def remove(self, num):
        for i in range(num):
            keyboard.press_and_release("backspace")
            time.sleep(0.01)

    def is_there_special_event(self):
        spec_keys = self.parameters["special_keys"]
        
        for event in spec_keys.keys():
            is_inputed = self.last_text.endswith(spec_keys[event])

            if is_inputed:
                if event == "end":
                    msg = "Programm ending !"

                elif event == "reload":
                    self.load_configs()
                    msg = "Reloaded !"
                
                elif event == "on":
                    if self.on:
                        msg = "I'm already activated !"
                    else:
                        self.on = True
                        msg = "Activating !"

                elif event == "off":
                    if not self.on:
                        msg = "Already off !"
                    else:
                        self.on = False
                        msg = "Goodbye !"
                
                elif event == "clear":
                    self.last_keys = []
                    self.last_text = ""
                    msg = "Cleared !"
                
                else:
                    msg = "What is supposed to be this event ?"

                self.remove(len(spec_keys[event]))
                self.write(msg)

                time.sleep(0.5)
                self.remove(len(msg))

                del self.last_keys[-1 * len(spec_keys[event])]
                self.last_text = self.last_text[0:-len(spec_keys[event])]