import time

class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()
        print("Timer started at:", self.start_time)


    def elapsed_time(self):
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time
        print("Elapsed time:", elapsed)
        return elapsed
    

    def reset(self):
        self.start_time = time.perf_counter()
        print("Timer reset at:", self.start_time)

    @staticmethod
    def sleep(seconds: float):
        time.sleep(seconds)
        print(f"Slept for {seconds} seconds")