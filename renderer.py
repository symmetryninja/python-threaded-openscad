##!/usr/bin/env python3
import threading, queue, subprocess, os, sys, yaml, platform, multiprocessing, getopt
# from datetime.datetime 
from datetime import datetime

startTime = datetime.now()

# import the params file
current_dir = os.getcwd()
config_file = "render_config.yml"
scad_file = "project.scad"

help_text = """
OpenSCAD threaded renderer
--------------------------
usage: renderer.py -f <scadfile> -c <configfile>
Params:
    * -f (optional) : base scad file - defaults to project.scad, can be overridden by config file
    * -c (optional) : config file - defaults to render_config.yaml
"""

# parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"hf:c:",["scadfile=","configfile="])
except getopt.GetoptError:
    print (help_text)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print (help_text)
        sys.exit()
    elif opt in ("-f", "--scadfile"):
        scad_file = arg
    elif opt in ("-c", "--configfile"):
        config_file = arg

# some defaults
number_of_threads = multiprocessing.cpu_count()
quality = 95
if platform.system() == "Windows":
  openscad_path = 'c:/Program Files/OpenSCAD/openscad.exe'
if platform.system() == "Darwin":
  openscad_path = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'

# read the yaml in
with open("{}/{}".format(current_dir, config_file), 'r') as stream:
    try:
        render_config = yaml.load(stream, Loader=yaml.FullLoader)
        if 'scad_file' in render_config:
            scad_file = render_config['scad_file']
        if 'quality' in render_config:
            quality = render_config['quality']
        if 'threads' in render_config:
            number_of_threads = render_config['threads']
        if 'openscad_path' in render_config:
            openscad_path = render_config["openscad_path"]
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
        self.temp_file_name = "{}/tmp_renderer_{}.scad".format(current_dir, self.module_name)
        self.output_file_name = "{}/outputs/{}.{}".format(current_dir, self.module_name, self.output_format)
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
        temp_file.write("batch_rendering = true; \n include <{}> \n $fn={}; \n {}();".format(scad_file,quality,self.module_name))
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