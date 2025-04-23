import time

class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()
 

    def elapsed_time(self):
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time

        return elapsed   

    def reset(self):
        self.start_time = time.perf_counter()

    @staticmethod
    def sleep(seconds: float):
        time.sleep(seconds)