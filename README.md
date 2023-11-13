# Auto Replacer

- This program will **help you writing texts**, **do maths**, **search on wiki**, etc...
- To make this work, you'll just have to **start the `start.bat` file**.
- You can also create your own configurations. To make this, you may want to **edit the `keys.json` file**.

# Update from v1.0 to v2.0

You have to put the "v1.0_to_v2.0_patch.py" file in the same folder than your old version of auto_replacer.
Launch it (in a command prompt), and your key files will be updated.
Then, download the new version on GitHub (this one), and put the corrected keys.json and others files in your new folder, and that's it !

# Configuration of `keys.json`

## First steps

The most basic utilisation of this program is like as follows :

`part of keys.json`
```json
{
    "input": "²sent1",
    "output": "This is an example of registered sentences !"
}
```

Here, when starting the program, writing *"²sent1"* will replace that with *"This is an example of registered sentences !"*

## Add configs

To make others configs, you'll just have to add a new dict to the `keys.json` file, like this :

`part of keys.json`
```json
"keys": [
    {
        "input": "²sent1",
        "output": "This is an example of registered sentences !"
    },
    {
        "input": "²sent2",
        "output": "Another sentence !"
    }
]
```

Don't forget the "," after your first configuration.

## React on key combinaison or output it

### In the output

The input isn't only limited to a text, it's possible to make keyboard shortcuts by using a list :

`part of keys.json`
```json
{
    "input": "²select_all",
    "output": ["ctrl", "a", "c"]
}
```

This configuration will select all the text and copy it when "*²select_all*" is written.
As always, don't forget the "," between all keys.

### In the input

`part of keys.json`
```json
{
    "input": ["esc"],
    "output": "echapped !"
}
```

This will write "*echapped !*" when you press escape.

### Keys name

Here are the names of some keys to help you configure :
`backspace`, `space`, `esc`, `ctrl`

Be sure of using these exact names, or it won't work.

## Configure basic Parameters

### Case Sensitive

You can also add parameters to your configuration.

`part of keys.json`
```json
{
    "input": "LoWeR",
    "output": "It still works with lower case !",
    "params": {
        "case_sensitive": false
    }
}
```

By default, the "*case_sensitive*" parameters is set to true. *(To change the default values of configs, please follow the "**Extra configurations**" section)*

Here, we change that parameter to false to make the programm accept lower and upper cases.

### Keep Text

You may sometimes want to **keep the text you just wrote** when using this program. You could just write the input in the output to make this work, but there's a better solution.

`part of keys.json`
```json
{
    "input": "Example of",
    "output": " auto completion",
    "params": {
        "keep_text": true
    }
}
```

By adding this on the parameters, the program will no longer delete the input when written.

### Put several parameters

Of course, it's possible to do that :

`part of keys.json`
```json
{
    "input": "Example of",
    "output": " auto completion",
    "params": {
        "keep_text": true,
        "case_sensitive": false
    }
}
```

Just be carefull to add the "," **between** elements, and not after the last.

## Advanced parameters

### Basic utilisation

Thanks to the 2.0, it's now possible to add inputs with arguments. It works as follows :

`part of keys.json`
```json
{
    "input": "²like{food}",
    "output": "It seems that you like {food}",
    "params": {
        "separator": "{}"
    }
}
```

This config accepts now everything replacing "food", and this food will be in the replaced text.

For Example, writing "*²like{Tomato}*" will write "*It seems that you like Tomato*"

To do that, it's important to set the "separator" parameter. This sets the characters that contain the arguments. Putting "[]" as separator will make you set the arguments as follows:

`part of keys.json`
```json
{
    "input": "²like[food]",
    "output": "It seems that you like [food]",
    "params": {
        "separator": "[]"
    }
}
```

... and so on. Just do not set the separator with the same character twice. It won't work.

### Operations

It's also possible to perform math operations. Please consider this example :

`part of keys.json`
```json
{
    "input": "²calc(op)",
    "output": "(op) = (result)",
    "params": {
        "separator": "()",
        "operation": {
            "result": "(op)"
        }
    }
}
```

We added a new parameter : "operation". All the keys in it are new arguments that are set for the output.

In this example, the parameter "result" will be set to the calculation's result. After that, the output take this value to write this result. Writing `²calc(3*3)` would write `3*3 = 9`.

## Extra configurations

### Special keys

`part of keys.json`
```json
"special_keys": {
    "end": "²end",
    "reload": "²r",
    "on": "²on",
    "off": "²off",
    "clear": "²clear"
}
```

This is the list of special keys :
- "end" ends the program.
- "reload" reloads the keys.json file. You can use it when you edit it while using the program.
- "on"/"off" enables or disables the program but do not end it.
- "clear" is a debug key. If the program doesn't work, you can try to clear the registered keys.

To use these keys, it's simply as writing "²" + the option. However, you can change it if you want.

### Extra files

If you have too much configurations in your file (at first maybe the program would start lagging), you can add external files only with keys.

`part of keys.json`
```json
"external_keys": [
    "external_file.json"
]
```

This property of `keys.json` is a simple list with the names of all the external files. Putting a file in an other folder is also possible : Just write `folder/file.json`.

The content of this new file would be :

`external_file.json`
```json
[
    {
        "input": "²external_command",
        "output": "Wow, that seems much more organized now"
    }
]
```

### Global Parameters

`part of keys.json`
```json
"global_params": {
    "max_keys": 50,
    "default_config_params": {
        "keep_text": false,
        "case_sensitive": true,
        "separator": null,
        "operation": null
    }
}
```

This is on the top of your `keys.json` file.

- "max_keys" is the max size of registered text. In other words, it accepts 50 letters maximum. Doing inputs with more than 50 won't work. You can extend this limit, but it may more lag a bit.

- "default_config_params" is the default value for all the parameters of configurations. You can change it if you want, to make all configurations accept lower case, to keep all the text written, etc...