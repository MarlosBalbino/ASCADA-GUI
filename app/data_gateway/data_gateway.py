from threading import Thread
import asyncio
from random import randint

from app.helpers import logDebug
from app.ts_chart import Colors
from .serial_stream import SerialStream


class DataGateway:
    """
    Implements a data gateway, througth witch all data from and to serial port is handled.
    It implements a thread safe comunication and data shering over all application.

    :param ts_data: A dictionary on format:
    {
        ts_id_1: { 'time': time_samples_list, 'values': values_samples_list },
        ts_id_2: { 'time': time_samples_list, 'values': values_samples_list }
        ...
    }
    ts_data is a data source of samples from real time waves, its time waves are TimeSeries (ts(s))
    data. All consumers can read data from it, but never can edit then.
    :param ts_info: A dictionary on format:
    {
        ts_id_1: {'lb': Time_Series_1_label, 'color': color},
        ts_id_2: {'lb': Time_Series_2_label, 'color': color},
        ...
    }
    """

    ts_data = {}
    ts_info = {}

    def __init__(self):

        def get_random_color():
            color_max_i = len(Colors.Favorites.get_list()) - 1
            color_list = Colors.Favorites.get_list()
            return color_list[randint(0, color_max_i)]
        DataGateway.ts_info = {
            1: {'lb': 'Time Series 1', 'color': get_random_color()},
            2: {'lb': 'Time Series 2', 'color': get_random_color()},
        }
        DataGateway.ts_data = {
            1: {'time': [], 'values': []},
            2: {'time': [], 'values': []}
        }

        self._waves_sources = {}

        self.loop = asyncio.new_event_loop()
        self._queue = asyncio.Queue(loop=self.loop)
        self._thread = Thread(target=self._run_background_loop, args=[self.loop])
        self._thread.daemon = True
        self._thread.start()

    def _run_background_loop(self, loop: asyncio.AbstractEventLoop):
        loop.run_until_complete(self._start_streaming())

    async def _start_streaming(self):
        sampling_rate = 256
        frame_rate = 60
        self._waves_sources = {
            1: SerialStream(self._queue, wave_id=1, sampling_rate=sampling_rate,
                            frame_rate=frame_rate, offset=1.5, wave_frequency_hz=1,
                            delay_rate=0.075),
            2: SerialStream(self._queue, wave_id=2, sampling_rate=sampling_rate,
                            frame_rate=frame_rate, offset=3.5, wave_frequency_hz=1.5)
        }
        await self._run_data_handler()

    async def _run_data_handler(self):
        while True:
            # Gets a pack of generated samples from SerialStream and appends it to ts_data.
            id, time, values = await self._queue.get()
            self.ts_data[id]['time'].extend(time)
            self.ts_data[id]['values'].extend(values)
