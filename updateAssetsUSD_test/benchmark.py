import cProfile
import pstats
import os

class Profiler():
    
    def __init__(self):
        self.profiler = cProfile.Profile()

    def clear(self):
        self.profiler.clear()
        
    def profile_function(self, func):
        def inner(*args, **kwargs):
            self.profiler.enable()
            result = func(*args, **kwargs)
            self.profiler.disable()
            return result
        return inner

    def print(self, stats="cumtime"):
        stats = pstats.Stats(self.profiler)
        stats.strip_dirs().sort_stats("cumtime").print_stats(20)
