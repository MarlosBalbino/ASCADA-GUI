# https://docs.python.org/3/library/asyncio.html
from time import sleep
from threading import Thread
import queue
import asyncio
from random import randint
from serial.tools.list_ports import comports as getComPorts
import serial

from app import logDebug, logError, logWarn, logInfo
from app.ts_chart import Colors
from .serial_stream import SerialStream

import csv


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
    _loop: asyncio.AbstractEventLoop = None
    _thread: Thread = None
    _serial_stream: SerialStream = None
    _port: serial.Serial = None
    _out_queue: queue.Queue = None
    _in_ts_queue: asyncio.Queue = None
    _in_flag_queue: asyncio.Queue = None
    
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
        cls._port = serial.Serial(port=port_name, baudrate=baud_rate, stopbits=stop_bits)

        cls._loop = asyncio.new_event_loop()
        cls._loop.set_exception_handler(cls._event_loop_exception_handler)
        cls._loop.set_debug(True)
        cls._in_ts_queue = asyncio.Queue(loop=cls._loop)
        cls._in_flag_queue = asyncio.Queue(loop=cls._loop)
        cls._out_queue = queue.Queue()
        cls._serial_stream = SerialStream(cls._port, cls._out_queue, cls._in_ts_queue,
                                          cls._in_flag_queue)

        cls._thread = Thread(target=cls._run_background_loop)
        cls._thread.daemon = True
        cls._thread.start()

    @classmethod
    def _run_background_loop(cls):
        async def start_streaming():
            await asyncio.gather(
                cls._serial_stream.run(),
                cls._run_in_ts_handler(),
                cls._run_in_flag_handler()
            )
        cls._loop.run_until_complete(start_streaming())

    @staticmethod
    def _event_loop_exception_handler(loop, context):
        logError("EventsLoopError:",
                 "\n\tMessage:", context['message'],
                 "\n\tException:", context['exception'],
                 "\n\tFuture:", context['future'],
                 "\n\tTask:", context['task'])

    @classmethod
    async def _run_in_ts_handler(cls):
        """
        Gets data from _in_ts_queue and puts it in ts_data. The data in _in_ts_queue is arrived
        throught serial.
        """
        while True:
            # Gets a pack of generated samples from SerialStream and appends it to ts_data.
            id, time, value = await cls._in_ts_queue.get()
            cls.ts_data[id]['time'].append(time)
            cls.ts_data[id]['values'].append(value)

    @classmethod
    async def _run_in_flag_handler(cls):
        """
        Gets data from _in_flag_queue and puts it in in_flag. The data in _in_flag_queue is arrived
        throught serial.
        """
        while True:
            id, value = await cls._in_flag_queue.get()
            cls.in_flag[id] = value

    @classmethod
    def send_flag(cls, id, type_str, value):
        """
        Puts data from user input to _out_queue, to be sent throught serial.
        :param type_str: Attribute of DataTypes (str).
        """
        cls._out_queue.put((id, type_str, value))

    @classmethod
    def stop(cls):
        cls._loop.call_soon_threadsafe(cls._serial_stream.stop)
        if not cls._serial_stream.stopped.wait(1):
            logWarn('Streamming took too long to stop! Forcing stop.')
        # cls.save_ts_data_to_csv()
        logInfo("DataGateway stopped!")

    @classmethod
    def save_ts_data_to_csv(cls, file_name='ts_1_0.csv'):
        logDebug('Saving to file...')

        with open(file_name, 'w') as f:
            csv_writer = csv.writer(f)
            time = cls.ts_data[1]['time']
            value = cls.ts_data[1]['values']
            time_sz = len(time)
            value_sz = len(value)
            csv_writer.writerow(('time', 'value'))
            for i in range(value_sz if value_sz > time_sz else time_sz):
                csv_writer.writerow((time[i], value[i]))

        logDebug('Saved!')
