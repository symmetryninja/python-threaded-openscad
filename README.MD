# Threaded OpenSCAD rendering with Python3

While rendering several, highly complex modules in OpenSCAD, I found the limit of one CPU thread to be not enough.

I wrote something in bash that makes use of ```&``` and decided to take it further to do it with organised threading and queueing in Python.

This code __does not__ make single operations faster, it only parralellises single operations and runs them simultaneously. If you've got a single model being rendered, it __will not__ make anything faster. If you've got heaps of models being rendered at once, __it wont do that faster__ either.

If you render multiple models out of one or many OpenSCAD files and you're happy to change your code to have an entry point blocker, this may help you get things done faster.

## What it does

1. It uses a gateway scad file (renderer.scad) to include your code files
1. Then it uses a yaml file that has a list of names of modules and the desired output format
1. It then creates a temporary scad file that includes the gateway script and triggers the desired module
1. The script spins up as many threads as specified in the config to render the module - it does this with  subprocess to trigger OpenSCAD into the outputs directory
1. Then it deletes the temporary scad file
1. Finally the script reports the runtime.

## Using it in your projects

There are a few things you need to do to use this in your project:

1. In your current code files wrap working code areas in a module called ```render_working_code()``` that specifies the ```$fn``` value you prefer while your working (I usually have it at about 40)
1. create a `render_config.yaml` file (details below) in your repo
1. Include your primary code files into the `renderer.scad` file in your repo
1. Put the renderer.py into your `$PATH` or refer to it's full path

Because it queue's up the jobs in order, it would make sense to add your largest/slowest modules at the top.

__Note:__ The suffix value can be anything understandable by OpenSCAD.

Once you have all this above you just need to execute the renderer.py script while you're CWD is in your project dir. It will expect there to be a `render_config.yaml` and `renderer.scad` file in there and probably freak out without it.

## The `renderer.scad` file

```OpenSCAD
include <work_doc_1.scad>
batch_rendering = true;
```

## The `render_config.yml` file

Only the models list is necessary in here

```YAML
#openscad_path: "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD" # optional on mac/windows
#threads: 16 # defaults to all cores
#quality: 90 # default 90
models:
  - module: "easy_render_5_for_dxf" # name of the openscad function to run
    suffix: "dxf" # Suffix is needed if you don't want an STL
  - module: "easy_render_4" # had no suffix so defaults to STL
```

## Running examples

The base code tests how fast this can process using 4 threads, execute the code with no changes to see how well it works with 4 threads.

Change the ```number_of_threads``` variable in the `yaml` file to see how well it does with 1,8,16,42,200 threads and, provided your OS is happy to do so and doesn't run out of resources, it will render simultaneously and thus make use of all those CPU cores you're not using.

## Some benchmarks

Benchmarked on a Windows 11 machine with:

* Intel Core i7 10700KF (8 core/16 thread) (3.8 GHz base, 4.8ghz boost)
* 32GB Ram
* PCI SSD's
* Python 3.9.7
* RTX3080
* OpenSCAD version 2021.05.26
* Not much else going on

I've configured a pretty brutal test, possibly introducing a variation thats way too high because the ```$fn = 90``` increases the amount of operations dramatically, still why not test a boat with a storm?

In my default file, I've disabled rendering jobs for the really complex modules because they weren't demonstrating anything new, feel free to enable them.

Threaded stats here:

| Threads | Render time | Notes |
| ------- | ----------- | ------ |
| 1 | 4:54 | Comparable to the GUI - computer didn't notice |
| 2 | 2:35 | again Comparable to the GUI - computer didn't notice |
| 8 | 1:17 | the total time for all 16 models was 1 second longer than the longest build  |

As to be expected; my CPU does a better job at rendering 8 things at a time than it would trying to do 1 things at a time. 

If you manage to render more models at once than you have threads, the CPU will start scheduling hard, so more threads than you have means less productivity.

By default the script will use a thread per registered CPU - which is one per hyper-thread - up until it runs out of models to render. 

## Requirements

* Python 3.6+
* OpenSCAD
* Windows/MacOS/Linux environment

This was built with Python3.6 installed using pyenv, I'm no python master, this is not tricky.

## Credits

Dan Kirshner.

In the interests of making hard-to-render workloads I've used the thread module file from [openscad-threads](http://dkprojects.net/openscad-threads/) its fantastic!

I've modified it so it doesn't limit the ```$fn``` variable because while this is very useful in normal use, I don't want to reduce the load in this case.

## Licence

[See Licence.txt](Licence.txt)

Generally, do what you like with this code/project and say thanks if you want to - but if you save the world or break the universe or anything in between, you're on your own.