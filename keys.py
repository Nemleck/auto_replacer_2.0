import keyboard
import time, json
from copy import deepcopy

# Allow more math operations in configs
from operations import *

from req import get_wiki_info

keyboard.on_press_key

class Keys:
    def __init__(self):
        c.out("info", "Program just started !")

        self.last_keys = []
        self.last_text = ""

        self.limit = 50

        self.on = True
        # self.input_content = None

        self.parameters = {}
        self.configs = []
        self.debug = False

        self.load_configs()

        if self.limit > 100:
            c.out("warning", "Limit bigger than 100 may cause lag.")
    
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

            # Condition default params
            if key["params"]["condition"] != None: # We assume that condition is on bc it was set just before
                if not "default_condition_params" in data["global_params"]:
                    c.out("warning", "Conditions won't be available due to your version.")
                    continue
                
                default_cond_params = data["global_params"]["default_condition_params"]
                for cond in key["params"]["condition"]:
                    for param in default_cond_params:
                        if not param in cond.keys():
                            cond[param] = default_cond_params[param]

        self.configs = all_keys
        self.parameters = data

        try:
            self.limit = data["global_params"]["max_keys"]
        except:
            c.out("error", "Main configuration file should have set the keys limit 'max_keys' in 'global_params'.", "Config Error")
        
        try:
            self.debug = data["global_params"]["debug"]
        except:
            c.out("error", "Main configuration file should have 'debug' in 'global_params'.", "Config Error")
    
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
    
    def operation_vars(self, common_params, op, config):
        error_params = []

        for var in op.keys():
            text_to_eval = self.get_replaced_text(op[var], config, common_params)
            
            try:
                common_params[var] = str(eval(text_to_eval))
                
                if self.debug:
                    c.out("debug", f"Assigned '{common_params[var]}' to name '{var}'")
            except Exception as e:
                c.out("error", f"Couldn't make any result of '{text_to_eval}'", "Config Error")
                common_params[var] = "error"
                error_params.append(var)

        return common_params, error_params
    
    def is_in_config(self):
        # Test all configs

        for config in self.configs:
            input_params = config["params"]
            input_text, input_args = self.get_text_and_params(self.last_text, config["params"]["separator"])

            is_there_input, common_params = self.endswith(config["input"], input_text, input_args, config["params"])
            
            if is_there_input:
                output_text = config["output"]

                if self.debug:
                    c.out("debug", f"Began '{output_text}' treatment with input '{input_text}'.")

                # Perform operations
                op = config["params"]["operation"]
                if op != None:
                    common_params, error_params = self.operation_vars(common_params, op, config)
                
                # Delete text if not keep_text param enabled
                if type(config["input"]) is str and config["params"]["keep_text"] == False:
                    to_remove = len(self.get_replaced_text(config["input"], config, common_params, True))

                    # Avoid backspaces ignored because of already doing key_press
                    time.sleep(0.2)
                    self.remove(to_remove)
                
                # Conditions
                conditions = config["params"]["condition"]
                if conditions:
                    test = True
                    for cond in conditions:
                        # Has previous test been ... ?
                        if cond["test_if_previous_test_was"] == (not test) :
                            continue

                        # Reset the test value to True
                        test = None

                        last_element = None
                        curr_element = None
                        for i in range(len(cond["elements"])):
                            last_element = curr_element
                            curr_element = self.get_replaced_text(cond["elements"][i], config, common_params)

                            if i-1 >= 0:
                                # Has an element before
                                if     (cond["mode"] == "=" and curr_element != last_element) \
                                    or (cond["mode"] == "~=" and not (last_element in curr_element)) \
                                    or (cond["mode"] == "=~" and not (curr_element in last_element)) \
                                    or (cond["mode"] == ">" and last_element <= curr_element) \
                                    or (cond["mode"] == "<" and last_element >= curr_element) \
                                    or (cond["mode"] == ">=" and last_element < curr_element) \
                                    or (cond["mode"] == "<=" and last_element > curr_element):
                                    # Condition false
                                    test = False
                                else:
                                    test = True
                                
                                if test == None:
                                    c.out("warning", f"'{cond['mode']}' is not a valid condition mode.")
                            
                                if self.debug:
                                    c.out("debug", f"   Got result '{test}' while comparing '{last_element}' and '{curr_element}' on mode '{cond['mode']}'")

                        if self.debug:
                            c.out("debug", f"   Got global result '{test}' on condition.")

                        if test and cond["success_text"] != None:
                            success = self.get_replaced_text(cond["success_text"], config, common_params)

                            if cond["operation_result_name"] != None:
                                # Put success text in var
                                common_params[cond["operation_result_name"]] = success
                                
                                if self.debug:
                                    c.out("debug", f"Assigned success text '{success}' to name '{cond['operation_result_name']}'.")
                            else:
                                # Write success text
                                self.write(success)

                        elif not test and cond["failure_text"] != None:
                            failure = self.get_replaced_text(cond["failure_text"], config, common_params)

                            if cond["operation_result_name"] != None:
                                # Put failure text in var
                                common_params[cond["operation_result_name"]] = failure

                                if self.debug:
                                    c.out("debug", f"Assigned failure text '{failure}' to name '{cond['operation_result_name']}'.")
                            else:
                                # Write failure text
                                self.write(failure)
                
                op = config["params"]["operation"]
                if op != None and len(error_params) > 0:
                    for param in error_params:
                        common_params, _ = self.operation_vars(common_params, 
                                            {param: op[param]}, config)
                            
                # Replace str params with actual content
                output_text = self.get_replaced_text(output_text, config, common_params)
                
                if self.debug:
                    c.out("debug", f"Found '{output_text}' as output. Output will be repeated {input_params['repeat_output']} time(s).")

                for n in range(input_params["repeat_output"]):
                    self.write(output_text)

                self.last_text = ""
                self.last_keys = []
    
    def get_replaced_text(self, text:str, config:dict, common_params:dict, keep_separator=False):
        input_args, output_args = list(common_params.keys()), list(common_params.values())
        separator = config["params"]["separator"]

        if input_args:
            for i in range(len(input_args)):
                if not keep_separator:
                    text = text.replace(separator[0] + input_args[i] + separator[1], output_args[i])
                else:
                    text = text.replace(separator[0] + input_args[i] + separator[1], separator[0] + output_args[i] + separator[1])
        
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
            keyboard.write(text, 0.02)
        
        else:
            for key in text:
                keyboard.press(key)
            
            for key in text:
                keyboard.release(key)

    def remove(self, num):
        for i in range(num):
            keyboard.press_and_release("backspace")
            time.sleep(0.02)

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
                
                c.out("info", f"Used event {event} !")

                self.remove(len(spec_keys[event]))
                self.write(msg)

                time.sleep(0.5)
                self.remove(len(msg))

                if event == "end":
                    exit() # Doesn't work on main.py

                del self.last_keys[-1 * len(spec_keys[event])]
                self.last_text = self.last_text[0:-len(spec_keys[event])]