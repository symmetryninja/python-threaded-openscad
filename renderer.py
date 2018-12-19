#!/usr/bin/env python3
import threading, queue, subprocess, os, sys, yaml
from datetime import datetime

startTime = datetime.now()

# import the params file if specified
config_file = "{}/render_config.yml".format(os.getcwd())

# some defaults
number_of_threads = 8
quality = 96
openscad_path = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'
filename = 'renderer.scad'

# read the yaml in
with open(config_file, 'r') as stream:
    try:
        render_config = yaml.load(stream)
        if 'quality' in render_config:
            quality = render_config['quality']
        if 'threads' in render_config:
            number_of_threads = render_config['threads']
        if 'openscad_path' in render_config:
            openscad_path = render_config["openscad_path"]
        if 'filename' in render_config:
            filename = render_config["filename"]
        if 'models' in render_config:
            models = render_config["models"]
        else:
            raise Exception("no models to render in yaml file?")
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit
    except Exception as exc:
        print(exc)
        sys.exit
    
# Rendering worker class
class Job:
    module_name = output_format = temp_file_name = output_file_name = start = ""

    def __init__ (self, q):
        threading.Thread.__init__(self)
        self.q = q

    def setup (self, module_name, output_format = "stl"):
        self.module_name = module_name
        self.output_format = output_format
        self.temp_file_name = "{}/tmp_renderer_{}.scad".format(os.getcwd(), self.module_name)
        self.output_file_name = "{}/outputs/{}.{}".format(os.getcwd(), self.module_name, self.output_format)
        self.write_file()

    def run (self):
        while not self.q.empty():
            current_item = self.q.get()
            q.task_done()
            if 'suffix' in current_item:
                self.setup(current_item['module'], current_item['suffix'])
            else:
                self.setup(current_item['module'])

            # print("{} rendering started".format(self.module_name))
            self.start = datetime.now()
            self.execute_render()

    def write_file (self):
        temp_file = open(self.temp_file_name, "w") 
        temp_file.write("include <{}> \n batch_rendering = true; \n $fn={}; \n {}();".format(filename, quality, self.module_name))
        temp_file.close()
    
    def execute_render (self):
        subprocess.call([
                openscad_path, 
                "-o",
                self.output_file_name,
                self.temp_file_name
            ])
        print("{} rendering finished ({})".format(self.module_name, datetime.now() - self.start))
        os.remove(self.temp_file_name)

# Thread wrapper
def create_thread(q):
    cur_job = Job(q)
    cur_job.run()

# Globals
q = queue.Queue()
worker_threads = []

# Load up the queues
[q.put( model ) for model in models]

# Set up the threads
for worker in range(number_of_threads):
    worker_threads.append(threading.Thread(target=create_thread, args=(q,)))

# Run threads
for worker in worker_threads:
        worker.setDaemon(True)
        worker.start()

# Tell python to wait for threads by "joining" them
[worker.join() for worker in worker_threads]

print( "rendering took: {}".format(datetime.now() - startTime) )