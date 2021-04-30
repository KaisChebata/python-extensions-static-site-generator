# 1- Load Extensions

## Imports
Project Overview

In this project, you will add two extensions to an existing command line static site generator.

The first two modules will build up an extension loading and event system. These modules have no output on the command line.

After module three, you will see the effects of the extension system by viewing any html file in the output directory `(dist)`.
First Task

In this module, we'll create several functions that dynamically load extensions from a directory. An extension is a single python file found in the `ssg/extensions` directory.

Open the `extensions.py` file in the ssg directory. Import `sys` and `importlib` so we can dynamically add files to the sys path. Adjusting the sys path allows Python to find our extensions.

Since we will work with paths throughout this module, import `Path` from `pathlib`.

## Load Module Dynamically
To load a single extension, create a function called `load_module` in `extensions.py`. The first argument to the function is the `directory` from which to load the extension, and the second argument is the `name` of the module.

In the `load_module` function body, use `sys.path.insert()` to add directory to the first position (`0`) of the sys path.

## Adjust Sys Path
To dynamically load the module, call the `import_module()` method of importlib in the `load_module` function. Pass in the `name` to load.

We now need to remove the dynamically added path from the sys path with `sys.path.pop()`. Pass in the first position (`0`).

## Load Extensions Directory
We now have a function that will load a single file as a module. We'll use this function to load an entire directory of extensions.

Below the existing code in `extensions.py`, create a function called `load_directory` that has one argument, the `directory` to load.

In the body of the function, create a `for` loop. Call the iterator of the loop `path`, and loop through `directory`, which will be a `Path`, finding only `.py` files with the `rglob()` method.

In the body of the `for` loop, call the `load_module()` function to load the correct directory (`directory.as_posix()`) and name (`path.stem`).

## Load Bundled Extensions
Now that we have the `load_directory` function we'll use it to load all bundled extensions.

Create a function called `load_bundled` below the other functions in `extensions.py`.

In the body of the function, create a variable called `directory`. Assign this variable the path of the current file's parent with `Path(__file__).parent` and add the `"extensions"` directory to this path with `/` [slash operator](https://docs.python.org/3/library/pathlib.html#operators).

On a new line in the `load_bundled` function, call `load_directory()` passing it `directory`.

## Configure Site to Load Extensions
Open the `ssg/site.py` file, and at the top import `extensions` from `ssg`.

Next, find the `build` method of the `Site` class, and as the first line call the `load_bundled()` method of `extensions`.

# 2- Event and Filter Hooks

## Store Callbacks
In this module, we'll build a basic event system. There will be two ways to fire an event: one that calls a callback and one that captures the result of a callback. We'll store these callbacks in a dictionary.

Open the `hooks.py` file in the `ssg` directory. At the top, create a variable called `_callbacks` and assign it an empty dictionary.

## Register Decorator
We will need a way to associate events with functions in our extensions. This will be done with a function decorator. Below the `_callback` dictionary in the the `hooks.py` file, create a function called `register`. This function will need to accept the name of the `hook` and an `order`, with a default value of `0`.

In the body of the `register` function, create a nested function called `register_callback` that accepts a `func` argument. This represents the decorated function. In the body of `register_callback`, return the `func`. **Hint: do not call `func()`**, **return `func` without parentheses**.

Finally, `return` the `register_callback` function from `register`. **Hint: no parentheses here either**.

## Configure Hooks Dictionary
The `register_callback` function is responsible for adding default key value pairs to the `_callbacks` dictionary.

In the `register_callback` function, above the `return` statement, call the `setdefault()` method on `_callbacks`. Pass in `hook`, and an empty dictionary `{}`.

Chain a second call to the `setdefault()` method on to the first, to this pass `order` and an empty list `[]`.

Finally, still working with the same expression, chain a call to `append()`, passing in `func`.

## Event Hook
There will be two ways to fire an event. We'll create the first now, which will simply call the registered callback for the named event.

Below the `register` function, create a function called `event`. The first argument to the function will contain the name of the event, called `hook`. Next, use the special syntax for a variable number of arguments `*args` as the second argument.

In the body of the function, create a `for` loop with an iterator called `order` that loops through the target `sorted(_callbacks.get(hook, {}))`. This loops through the dictionary of the named event.

Nest another `for` loop in the first loop that has an iterator of `func` and a target of `_callbacks[hook][order]`. This will be a list of functions for the named event. In the body of the second for loop call `func()` passing in `*args`.

## Filter Hook
The second way to fire an event will be with the `filter` function. It will capture the result of the callback.

Below the `event` function, create a function called `filter`. The first argument to the function will contain the name of the event, called `hook`. The second will eventually store the result of the callback, call it `value`. The final argument is `*args`.

In the body of the function, create a `for` loop with an iterator called `order` that loops through the target `sorted(_callbacks.get(hook, {}))`. This loops through the dictionary of the named event.

Nest another `for` loop in the first loop that has an iterator of `func` and a target of `_callbacks[hook][order]`. This will be a list of functions for the named event. In the body of the second for loop, call `func()` and pass in `value` and `*args`. Assign the result of this call to `value`.

Outside both `for` loops but still in the `filter` function, `return` `value`.

# 3- Menu Extension

## Menu Extension Imports
In this module, we will harness the event system to create an extension. The goal of the extension is to generate a site menu.

To use the event system we first have to import the components. Open the `menu.py` file in the `ssg/extensions` directory and at the top import `hooks` and `parsers` from `ssg`.

The core of any menu is a link to the resource, after the imports, create an empty list called `files`.

## Register Collect Files Event
Let's create a function that gathers all Markdown and ReStructuredText file names. These are found in the `content` directory and are the core files of our site, they will be converted to HTML. Call this function `collect_files` and add two arguments of `source` and `site_parsers`.

This function needs to be registered with the event system. Decorator it with `hooks.register()`. Pass in the event name `"collect_files"` to the decorator.

In the body, create a variable named `valid`. Assign the `valid` variable a `lambda` with an argument of `p`. In the body of the lambda call `isinstance()` to see if `p` is an instance of `parsers.ResourceParser`. Flip the returned boolean value with `not`.

## Collect Valid Files
After the valid variable, create a `for` loop that has an iterator called `path` and loops through `source.rglob("*")`.

Nest a `for` loop that has an iterator of `parser` and loops through a filtered `site_parsers` list using `valid` as the filter function. **Hint: filter() returns a generator so it has to be converted to a list with** `list()`. **The whole expression will look something like** `list(filter(filter_function, original_list))`.

In the body of the nested loop, test `if` `path.suffix` has a valid file extension with the `parser.valid_file_ext()` method. If it does, `append()` the `path` to `files`.

## Register Generate Menu Filter
Once we have the file names to create to the links, we can generate a menu. Create a new function called `generate_menu`. It should accept two arguments `html`, and `ext`.

Like previous functions, this function needs to be registered with the event system. So, decorate it with the `hooks.register()` decorator and pass in the event name `"generate_menu"`.

In the body, create a variable named `template`. Assign the `template` variable a string of HTML with a few placeholders, `'<li><a href="{}{}">{}</a></li>'.`

## Menu Items Template
Below the template variable, create a `lambda` named `menu_item`.

The `lambda` should accept a `name` and an `ext`.

In the body of the `lambda`, call the `format()` method on `template`. Pass in the `name`, extension (`ext`), and the `name` with title case.

## Construct Menu
To construct a string of all menu items, create a variable called `menu` assigned to a list comprehension.

The left side of the comprehension should be a call to `menu_item()`. Pass it `path.stem` and `ext`.

The `for` loop of the comprehension should loop through `files` and the iterator should be called `path`.

Finally, in order to separate each menu item with a new line, wrap a call to `"\n".join()` around that entire list comprehension.

## Return Constructed Menu
The `generate_menu` event will eventually be fired by the `hooks.filter()` which requires that something be returned. We will return the constructed menu plus the HTML that was originally passed to the function.

At the end of the `generate_menu` function, return the string `"<ul>\n{}<ul>\n{}"`, append a call to `format` and pass in the `menu` and the `html`.

## Fire Collect Files Event
Open the `site.py` file and at the top add `hooks` to the existing `from ssg` import.

Now, find the `build` method of the `Site` class. Below the call to the `load_bundled()` function, call `hooks.event()`.

The event we want to fire is `"collect_files"`, and it requires `self.source` and `self.parsers`.

## Add Generated Menu to Markdown Parser
Open the `ssg/parsers.py` file, and import `hooks` from `ssg`.

Next, find the `parse` method of the `MarkdownParser` class. Below the `html` variable, create a new line.

Assign a variable named `filtered` a call to `hooks.filter()`. The event we want to fire is the `"generate_menu"` event. This event requires that the `html` and extension (`self.base_ext`) are passed.

In the `self.write()` call, change `html` to `filtered`

## Add Generated Menu to ReStructuredText Parser
Still in the `parsers.py` file, find the `parse` method of the `ReStructuredTextParser` class.

Below the `html` variable, create a new line. Assign a variable named `filtered` a call to `hooks.filter()`. The event we want to fire is the `"generate_menu"` event. This event requires that the html (`html["html_body"]`) and extension (`self.base_ext`) are passed.

In the `self.write()` call, change `html["html_body"]` to `filtered`.

# 4- Stats Extension

## Stats Extension Import
In this module, we will build a Stats extension that will calculate the average page conversion time, and the number of pages written to the file system. As with all extensions, we need access to the event system.

Open the `stats.py` file in the `extensions` folder, and import `hooks` from `ssg`.

To calculate times import `time`.

We'll keep track of things with a few global variables. Create two variables below the imports, `start_time` set to `None` and `total_written` set to `0`.

## Register Start Build Event
The first event will capture the start time. Create a function called `start_build`, register this function with the event system as `"start_build"` using the proper decorator.

In the body, use the `global` keyword to bring the `start_time` variable into scope. Next, set `start_time` to the current time.

## Register Written Event
The second event will capture how many pages are written to the file system. Create a function called `written`, register this function with the event system as `"written"` using the proper decorator.

In the body, use the `global` keyword to bring the `total_written` variable into scope. Next, add one to `total_written` and then assign it back to `total_written`.

## Register Stats Event
The final event will calculate everything, and construct a report. Create a function called `stats`, register this function with the event system as `"stats"` using the proper decorator.

In the body, create a variable called `final_time` that is assigned the result of subtracting `start_time` from the current time.

## Calculate Average Time
Below `final_time`, create another variable called `average` that is the result of `final_time` divide by `total_written`. To prevent a divide by zero error use a ternary `if`.

## Construct Report Template
The final variable we need is `report`. Assign it the string `"Converted: {} · Time: {:.2f} sec · Avg: {:.4f} sec/file"`.

## Output the Report
Print the `report`, `format()` it with `total_written`, `final_time`, and `average`.

## Fire Start Build & Stats Events
Open the `ssg/site.py` file and find the `build` method of the `Site` class.

Below the call to `hooks.event()`, fire the `"start_build"` event. As the last line of the `build` function, fire the `"stats"` events.

## Fire Written Events
Open the `ssg/parsers.py`, at the end of the `parse` method of both the `MarkdownParser` and `ReStructuredTextParser` classes, fire the `"written"` event.