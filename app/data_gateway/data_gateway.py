from threading import Thread
import queue
import asyncio
from random import randint
from serial.tools.list_ports import comports as getComPorts
import serial

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
    port = None
    _loop = None
    _thread = None
    _serial_stream = None
    
    @classmethod
    def setup(cls):

        def get_random_color():
            color_max_i = len(Colors.Favorites.get_list()) - 1
            color_list = Colors.Favorites.get_list()
            return color_list[randint(0, color_max_i)]
        cls.ts_info = {
            1: {'lb': 'Time Series 1', 'color': get_random_color()},
            2: {'lb': 'Time Series 2', 'color': get_random_color()},
        }
        cls.ts_data = {
            1: {'time': [], 'values': []},
            2: {'time': [], 'values': []}
        }

        ports = getComPorts()
        if len(ports) > 1:
            raise ValueError("There are more then one com port available!")
        elif len(ports) < 1:
            raise ValueError("There are not ports available!")
        port_name = ports[0].device
        baud_rate = 1000000
        stop_bits = serial.STOPBITS_TWO
        cls.port = serial.Serial(port=port_name, baudrate=baud_rate, stopbits=stop_bits)

        cls._loop = asyncio.new_event_loop()
        cls._out_queue = queue.Queue()
        cls._in_ts_queue = asyncio.Queue(loop=cls._loop)
        cls._in_flag_queue = asyncio.Queue(loop=cls._loop)
        cls._thread = Thread(target=cls._run_background_loop, args=[cls, cls._loop])
        cls._thread.daemon = True
        cls._thread.start()

    @staticmethod
    def _run_background_loop(cls, loop: asyncio.AbstractEventLoop):
        loop.run_until_complete(cls._start_streaming(cls))

    @staticmethod
    async def _start_streaming(cls):
        cls._serial_stream = SerialStream(cls.port, cls._out_queue, cls._in_ts_queue,
                                          cls._in_flag_queue)
        await cls._run_data_handler(cls)

    @staticmethod
    async def _run_data_handler(cls):
        while True:
            # Gets a pack of generated samples from SerialStream and appends it to ts_data.
            id, time, values = await cls._in_ts_queue.get()
            cls.ts_data[id]['time'].extend(time)
            cls.ts_data[id]['values'].extend(values)

    @classmethod
    def stop(cls):
        cls._serial_stream.stop()
