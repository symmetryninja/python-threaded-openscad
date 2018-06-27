#!/usr/bin/env python3
import threading, queue, subprocess, os, yaml
from datetime import datetime

startTime = datetime.now()

#get the config stuff!
stream = open('render_config.yaml', 'r')
render_config = yaml.load(stream)


# Input Vars
openscad_path = render_config["openscad_path"]
models = render_config["models"]
number_of_threads = render_config['number_of_threads']

# Rendering worker class
class Job:
    module_name = output_format = temp_file_name = output_file_name = ""

    def __init__ (self, q):
        threading.Thread.__init__(self)
        self.q = q

    def setup (self, module_name, output_format):
        self.module_name = module_name
        self.output_format = output_format
        self.temp_file_name = "tmp_renderer_{}.scad".format(self.module_name)
        self.output_file_name = "outputs/{}.{}".format(self.module_name,self.output_format)
        self.write_file()

    def run (self):
        while not self.q.empty():
            current_item = self.q.get()
            q.task_done()
            self.setup(current_item['module'], current_item['suffix'])
            print("{} rendering started".format(self.module_name))
            self.execute_render()

    def write_file (self):
        temp_file = open(self.temp_file_name, "w") 
        temp_file.write("include <renderer.scad> \n {}();".format(self.module_name))
        temp_file.close()
    
    def execute_render (self):
        subprocess.call([
                openscad_path, 
                "-o",
                self.output_file_name,
                self.temp_file_name
            ])
        print("{} rendering finished".format(self.module_name))
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