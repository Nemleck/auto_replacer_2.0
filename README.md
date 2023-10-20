# Auto Replacer

- This program will **help you writing texts**, **do maths**, **search on wiki**, etc...
- To make this work, you'll just have to **start the `start.bat` file**.
- You can also create your own configurations. To make this, you may want to **edit the `keys.json` file**.
*(If there's no `keys.json` file, just launch the script once)*

# Configuration of `keys.json`

## First steps

The most basic utilisation of this program is like as follows :

`part of keys.json`
```json
{
    "input": "²sent1",
    "output": "This is an example of registered sentences !",
    "params": {
        "case_sensitive": false
    }
}
```

Here, when starting the programm, writing *"²sent1"* will replace that with *"This is an example of registered sentences !"*

## Add configs

To make another configs, you'll just have to add a new dict to the `keys.json` file, like this :

`part of keys.json`
```json
"keys": [
    {
        "input": "²sent1",
        "output": "This is an example of registered sentences !",
    },
    {
        "input": "²sent2",
        "output": "Another sentence !",
    }
]
```

Don't forget the "," after your first configuration.

## React on key combinaison or output it

The input isn't only limited to a text, it's possible to make keyboard shortcuts by using a list :

`part of keys.json`
```json
{
    "input": "²select_all",
    "output": ["ctrl", "a", "c"]
}
```

This configuration will select all the text and copy it when "²select_all" is written.
As always, don't forget the "," between all keys.

Here are the names of some keys to help you configure :
`backspace`, `space`, `esc`

## Configure basic Parameters

### Case Sensitive

You can also add parameters to your configuration.

`part of keys.json`
```json
{
    "input": "LoWeR",
    "output": "It still work with lower case !",
    "params": {
        "case_sensitive": false
    }
}
```

By default, the "case_sensitive" parameters is set to true. *(To change the default values of configs, please follow the "**Extra configurations**" section)*

Here, we change that parameter to false to make the programm accept lower and upper cases.

### Keep Text

You may sometimes want to **keep the text you just wrote** when using this program. You could just write the input in the output to make this work, but I have a better solution.

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

This config accept now everything replacing "food", and this food will be in the replaced text.

For Example, writing "²like{Tomato}" will write "It seems that you like Tomato"

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

... and so on. Just do not set the separator the the same character twice. It won't work.

### Operations

It's also possible to perform math operations. Please consider this example :

`part of keys.json`
```json

```