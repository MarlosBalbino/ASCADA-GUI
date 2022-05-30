# https://docs.python.org/3/library/asyncio.html

from threading import Thread
import queue
import asyncio
from random import randint
from serial.tools.list_ports import comports as getComPorts
import serial

from app import logDebug
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
    in_flag = {}
    port = None
    _loop = None
    _thread = None
    _serial_stream = None
    _port = None
    _out_queue = None
    _in_ts_queue = None
    _in_flag_queue = None
    
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
        cls._in_ts_queue = asyncio.Queue(loop=cls._loop)
        cls._in_flag_queue = asyncio.Queue(loop=cls._loop)
        cls._out_queue = queue.Queue()
        cls._serial_stream = SerialStream(cls.port, cls._out_queue, cls._in_ts_queue,
                                          cls._in_flag_queue)

        cls._thread = Thread(target=cls._run_background_loop)
        cls._thread.daemon = True
        cls._thread.start()

    @classmethod
    def _run_background_loop(cls):
        cls._loop.run_until_complete(cls._start_streaming())

    @classmethod
    async def _start_streaming(cls):
        await asyncio.gather(cls._serial_stream.run(), cls._run_in_ts_handler(),
                             cls._run_in_flag_handler())

    @classmethod
    async def _run_in_ts_handler(cls):
        """
        Gets data from _in_ts_queue and puts it in ts_data. The data in _in_ts_queue is arrived
        throught serial.
        """
        while True:
            # Gets a pack of generated samples from SerialStream and appends it to ts_data.
            id, time, values = await cls._in_ts_queue.get()
            cls.ts_data[id]['time'].extend(time)
            cls.ts_data[id]['values'].extend(values)

    @classmethod
    async def _run_in_flag_handler(cls):
        """
        Gets data from _in_flag_queue and puts it in _xxx_. The data in _in_flag_queue is arrived
        throught serial.
        """
        id, value = await cls._in_flag_queue.get()
        cls.in_flag[id] = value
        logDebug(f"Flag received. id: {id}    value: {value}")

    @classmethod
    def send_flag(cls, id, type_str, value):
        """
        Puts data from user input to _out_queue, to be sent throught serial.

        :param type_str: Attribute of DataTypes (str).
        """
        cls._out_queue.put(id, type_str, value)
        logDebug(f"Flag sent. id: {id}    type: {type_str}    value: {value}")

    @classmethod
    def stop(cls):
        cls._serial_stream.stop()
        cls._loop.stop()
        logDebug("DataGateway stopped!")
