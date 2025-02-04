import time
import threading
from math import floor

class Timer:
    def __init__(self, seconds=3*60, increment=2):
        self.seconds = seconds
        self.increment = increment
        self._original_seconds = seconds  # Store the original time to reset later
        self._timer_thread = None
        self._start_time = None
        self._remaining_seconds = seconds
        self._remaining_hundredths = 0
        self._running = False
        self._stopped = False
        self.times_up = False
    
    def __str__(self):
        sec = self._remaining_seconds % 60
        hundredths = self._remaining_hundredths
        if sec < 10:
            sec = f"0{sec}"            
        if hundredths < 10:
            hundredths = f"0{hundredths}"
        return f"{self._remaining_seconds//60}:{str(sec)}.{str(hundredths)}"

    def start(self):
        if self._timer_thread is None or not self._timer_thread.is_alive() and not self._stopped:
            self._running = True
            self._start_time = time.time()
            self._timer_thread = threading.Thread(target=self._run)
            self._timer_thread.start()

    def _run(self):
        while self._running and (self._remaining_seconds > 0 or (self._remaining_seconds == 0 and self._remaining_hundredths > 0)):
            time.sleep(0.01)  # sleep for 10 milliseconds (hundredth of a second)
            elapsed_time = time.time() - self._start_time
            total_elapsed_time = elapsed_time * 100  # convert to hundredths of seconds

            self._remaining_seconds = floor(self.seconds - total_elapsed_time / 100)
            self._remaining_hundredths = 99 - int(total_elapsed_time % 100)

            if self._remaining_seconds < 0:
                self._remaining_seconds = 0
                self._remaining_hundredths = 0
                self._running = False
                self.timesup = True
        
        self.seconds = self._remaining_seconds

    def stop(self):
        self._running = False
        self._stopped = True
        if self._timer_thread is not None:
            self._timer_thread.join()

    def pause(self):
        if not self._stopped:
            self.seconds += self.increment
            self._running = False
        
    def resume(self):
        if not self._running and (self._remaining_seconds > 0 or self._remaining_hundredths > 0) and not self._stopped:
            self._running = True
            self._start_time = time.time()
            self._timer_thread = threading.Thread(target=self._run)
            self._timer_thread.start()

    def reset(self):
        self.stop()  # Ensure the timer stops completely
        self._remaining_seconds = self._original_seconds
        self.seconds = self._original_seconds
        self._remaining_hundredths = 0
        self.timesup = False
        self._stopped = False

    def get_remaining_time(self):
        return self._remaining_seconds, self._remaining_hundredths

if __name__ == "__main__":
    t = Timer(10)
    t.start()
    while t._running:
        if t.get_remaining_time()[0]==5:
            t.stop()
        if t.get_remaining_time()[1] == 0: 
            print(t)
    
    t.stop()
        