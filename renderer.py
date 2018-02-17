#!/usr/bin/env python3
import threading, queue, subprocess, os
from datetime import datetime

startTime = datetime.now()

# Input Vars
models = [
    # {"module": "difficult_render_5_for_dxf",    "suffix": "dxf"},
    # {"module": "difficult_render_1",            "suffix": "stl",},
    # {"module": "easy_render_4",                 "suffix": "stl",},
    # {"module": "easy_render_1",                 "suffix": "stl",},
    # {"module": "difficult_render_2",            "suffix": "stl",},
    # {"module": "easy_render_2",                 "suffix": "stl",},
    # {"module": "easy_render_5",                 "suffix": "stl",},
    # {"module": "difficult_render_3",            "suffix": "stl",},
    # {"module": "easy_render_6",                 "suffix": "stl",},
    # {"module": "easy_render_7",                 "suffix": "stl",},
    # {"module": "difficult_render_5",            "suffix": "stl",},
    # {"module": "easy_render_8",                 "suffix": "stl",},
    # {"module": "easy_render_9",                 "suffix": "stl",},
    # {"module": "difficult_render_4",            "suffix": "stl",},
    # {"module": "easy_render_10",                "suffix": "stl",},
    {"module": "easy_render_3",                 "suffix": "stl",},
]

number_of_threads = 4

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
                "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD", 
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