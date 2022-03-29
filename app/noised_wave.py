import time
import numpy as np
from PySide6.QtCore import Signal, QObject
from threading import Thread


class NoisedWave:

    def __init__(self,
                 queue,
                 wave_id=0,
                 sampling_rate=300,
                 frame_rate=30,
                 offset=0,
                 window_len=5,
                 f=4,
                 delay_rate=0):
        super().__init__()
        self.queue = queue
        self.wave_id = wave_id
        self.fs = sampling_rate
        self.fr = frame_rate
        self.window_len = window_len
        self.delay_rate = delay_rate
        self.f_rad = 2*np.pi*f

        self.t0 = 0
        self.points_per_frame = round(self.fs/self.fr)
        self.frame_time_interval = 1/self.fr
        self.offset = offset
        self.x = []
        self.y = []
        self.window_points_count = round(self.fs * self.window_len)
        self.keep_running = False
        self.thread = Thread(target=self._run)
        self.run()

    def get_id(self):
        return self.wave_id

    def stop(self):
        self.keep_running = False

    def run(self):
        self.keep_running = True
        self.thread.start()

    def _run(self):
        while self.keep_running:
            # Make new points
            t0_old, self.t0 = self.t0, self.t0+self.frame_time_interval*(1-self.delay_rate)
            x = np.linspace(t0_old, self.t0, self.points_per_frame)
            # noise = np.random.uniform(-.2, .2, self.points_per_frame)
            y = np.sin(self.f_rad*x) + self.offset
            # Emit data
            self.queue.put((x, y, self.wave_id))
            # Waits for new frame time
            time.sleep(self.frame_time_interval)
