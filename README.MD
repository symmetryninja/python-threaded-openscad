# Threaded OpenSCAD rendering with Python3

While rendering several, highly complex modules in OpenSCAD, i found the limit of one CPU thread to be not enough.

I wrote something in bash that makes use of ```&``` and decided to take it further to do it with organised threading and queueing in Python.

This code __does not__ make single operations faster, it only parralellises single operations and runs them simultaneously. If you've got a single model being rendered, it __will not__ make anything faster. If you've got heaps of models being rendered at once, __it wont do that faster__ either.

If you render multiple models out of one or many OpenSCAD files and you're happy to change your code to have an entry point blocker, this may help you get things done faster.

## Requirements

* Python 3.5+
* OpenSCAD
* MacOS/Linux environment - unless you mod it for windows

This was built with Python3.5.7 installed using pyenv, I'm no python master, this is not tricky.

## Credits

__Dan Kirshner__

In the interests of making hard-to-render workloads I've used the thread module file from http://dkprojects.net/openscad-threads/ its fantastic!

I've modified it so it doesn't limit the ```$fn``` variable because I don't want to reduce the load in this case.

## What it does

The script uses a gateway scad file (renderer.scad) to include your code files, force rendering and set the quality - you'll need to change this to bring in your code or specify the quality.

Then the script uses an array of dictionaries including the names of modules and the desired output, previously the code didn't allow for dxf rendering but I needed it for some of my frames to be cut out of aluminium.

The script then creates a temporary scad file that includes the gateway script and triggers the desired module.

The script then spins up as many threads as specified to render the module using subprocess to trigger OpenSCAD into the outputs directory and deletes the temporary scad file.

Finally the script reports the runtime.

## Running examples

The base code tests how fast this can process using 4 threads, execute the code with no changes to see how well it works with 4 threads.

Change the ```number_of_threads``` variable to see how well it does with 1,8,16,42,200 threads and, provided your OS is happy to do so and doesn't run out of resources, it will render simultaneously and thus make use of all those CPU cores you're not using.

## Some benchmarks

Benchmarked on a mac with:

* 3.31 GHz Intel Core i5 (4 core)
* 32GB Ram
* PCI SSD's
* Python 3.5.4
* Fairly powerful graphics card
* OpenSCAD version 2017.02.08 (git 2ef5333)
* Not much else going on

I've configured a pretty brutal test, possibly introducing a variation thats way too high because the ```$fn = 80``` increases the amount of operations dramatically, still why not test a boat with a storm?

In my default file, I've disabled rendering jobs for the really complex modules because they weren't demonstrating anything new, feel free to enable them.

Threaded stats here:

| Threads | Render time | Load notes |
| ------- | ----------- | ------ |
| 1 | ? mins | computer useable
| 2 | ? mins | computer useable
| 4 | ? mins | computer useable
| 8 | 0:03:38 | computer less useable

## Using it in your projects

There are 4 things you need to do to use this in your project:

1. Move the base files into your project folder (or refer to them from here)
1. Wrap working code areas in a module called ```render_working_code()``` that specifies the ```$fn``` value you prefer
1. Include your primary code files into the renderer.scad file
1. Put the module names into the ```models``` list with respective ```module``` and ```suffix```

Because it queue's up the jobs in order, it would make sense to add your largest/slowest modules at the top.

__Note:__ The suffix value has to be understandable by OpenSCAD.

## Licence

[See Licence.txt](Licence.txt)

Generally, do what you like with this code/project and say thanks if you want to - but if you safe the world or break the universe or anything in between, you're on your own.