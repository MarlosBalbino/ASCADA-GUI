# https://pyserial.readthedocs.io/en/stable/

from queue import Queue

from app import logDebug, logError, logWarn, logInfo
from struct import pack, unpack
from ... import DataTypes


class SerialStream:
    """
    
    """

    def __init__(self, port):
        """
        Desciption.

        :param port: An instance of serial.Serial().
        :param out_queue: Receives data from DataGateway to sent througth serial. Its elements are
         tuples in the format: (id, type, value). Where:
            id: An interger in the interval: 1:13 (including);
            type: Ane of the intens of DataTypes;
            value: A number that can be represented in the specified type
        :param in_ts_queue: Receives TimeSeries samples from serial to share trought DataGateway.
         Its elements are tuples in the format: (id, time, value). Where:
            id: An interger in the interval: 1:14 (including);
            time: time sample (Number);
            value: value sample (Number);
        :param in_flag_queue: Receives data from serial to share trought DataGateway. Its elements
         are tuples in the format: (id, value). Where:
            id: An interger in the interval: 1:14 (including);
            value: value sample (Number);
        """
        self._port = port
        self.out_flag_queue = Queue()
        self.in_ts_data = {}            # {id: (t,x)}
        self.in_flag_data = {}          # {id: value}

        self._read_parsers = {
            DataTypes.BOOL: self._read_bool,
            DataTypes.INT8: self._read_int8,
            DataTypes.INT16: self._read_int16,
            DataTypes.INT32: self._read_int32,
            DataTypes.FLOAT32: self._read_float32,
            DataTypes.ts_int16: self._read_ts_int16,
            DataTypes.ts_int32: self._read_ts_int32,
            DataTypes.ts_float32: self._read_ts_float32,
        }
        self._write_parsers = {
            DataTypes.BOOL: self._write_bool,
            DataTypes.INT8: self._write_int8,
            DataTypes.INT16: self._write_int16,
            DataTypes.INT32: self._write_int32,
            DataTypes.FLOAT32: self._write_float32,
        }

    # async def run(self):
    #     await asyncio.sleep(3)
    #     self._port.reset_input_buffer()
    #     self._write_open()
    #     while self._keep_running:
    #         await asyncio.create_task(self._read())
    #         await asyncio.create_task(self._write())
    #     self._write_close()
    #     self.stopped.set()

    def open_communication(self):
        self._port.reset_input_buffer()
        self._write_open()

    def close_communication(self):
        self._write_close()

    def flush_data(self):
        """
        ts_data: {
            1: ([0], [0]),
            2: ([10], [0])
        }
        """
        self._read()

    def _write_open(self):
        self._port.write(DataTypes.open_cmd)
        logInfo('Streaming open on _port:', self._port.name)

    def _write_close(self):
        self._port.write(DataTypes.close_cmd)
        logInfo('Streaming closed on _port:', self._port.name)

    """READ DATA FROM SERIAL"""

    async def _read(self):
        while self._port.in_waiting > 0:
            id_type = int.from_bytes(self._port.read(size=1), 'little')
            id = id_type >> 4
            type_int = id_type & int.from_bytes(DataTypes.type_mask, 'little')
            try:
                self._read_parsers[DataTypes.get_type_str(type_int)](id)
            except KeyError:
                logError("Invalid data type read!. Type:", type_int)
                logWarn('Reopening streaming...')
                self._write_close()
                self._write_open()
                logWarn('Streaming open!')

    def _read_bool(self, id):
        value = bool.from_bytes(self._port.read(size=1), 'little')
        self.in_flag_queue.put((id, value))

    def _read_uint8(self, id):
        value = int.from_bytes(self._port.read(size=1), 'little', signed=False)
        self.in_flag_queue.put((id, value))

    def _read_int8(self, id):
        value = int.from_bytes(self._port.read(size=1), 'little', signed=True)
        self.in_flag_queue.put((id, value))

    def _read_uint16(self, id):
        value = int.from_bytes(self._port.read(size=2), 'little', signed=False)
        self.in_flag_queue.put((id, value))

    def _read_int16(self, id):
        value = int.from_bytes(self._port.read(size=2), 'little', signed=True)
        self.in_flag_queue.put((id, value))

    def _read_uint32(self, id):
        value = int.from_bytes(self._port.read(size=4), 'little', signed=False)
        self.in_flag_queue.put((id, value))

    def _read_int32(self, id):
        value = int.from_bytes(self._port.read(size=4), 'little', signed=True)
        self.in_flag_queue.put((id, value))

    def _read_float32(self, id):
        value, = unpack('f', self._port.read(size=4))
        self.in_flag_queue.put((id, value))

    def _read_ts_int16(self, id):
        time = int.from_bytes(self._port.read(size=2), 'little', signed=True)
        value = int.from_bytes(self._port.read(size=2), 'little', signed=True)
        self.in_ts_queue.put((id, time, value))

    def _read_ts_int32(self, id):
        time = int.from_bytes(self._port.read(size=4), 'little', signed=True)
        value = int.from_bytes(self._port.read(size=4), 'little', signed=True)
        self.in_ts_queue.put((id, time, value))

    def _read_ts_float32(self, id):
        time, = unpack('f', self._port.read(size=4))
        value, = unpack('f', self._port.read(size=4))
        self.in_ts_queue.put((id, time, value))

    """WRITE DATA TO SERIAL"""

    async def _write(self):
        while not self.out_flag_queue.empty():
            id, type_str, value = self.out_flag_queue.get()
            try:
                self._write_parsers[type_str](id, value)
            except KeyError:
                logError("Invalid data type! Can't be writen! Type:", type_str)
            except OverflowError:
                logError(
                    f"Value can't be encoded to type! "
                    f"Id: {id} Type: {type_str} Value: {value}"
                )

    def _write_bool(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.bool8)).to_bytes(1, 'little')
        value = bool(value).to_bytes(1, 'little')
        self._port.write(id_type + value)

    def _write_uint8(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.uint8)).to_bytes(1, 'little')
        value = int(value).to_bytes(1, 'little', signed=False)
        self._port.write(id_type + value)

    def _write_int8(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.int8)).to_bytes(1, 'little')
        value = int(value).to_bytes(1, 'little', signed=True)
        self._port.write(id_type + value)

    def _write_uint16(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.uint16)).to_bytes(1, 'little')
        value = int(value).to_bytes(2, 'little', signed=False)
        self._port.write(id_type + value)

    def _write_int16(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.int16)).to_bytes(1, 'little')
        value = int(value).to_bytes(2, 'little', signed=True)
        self._port.write(id_type + value)

    def _write_uint32(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.uint32)).to_bytes(1, 'little')
        value = int(value).to_bytes(4, 'little', signed=False)
        self._port.write(id_type + value)

    def _write_int32(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.int32)).to_bytes(1, 'little')
        value = int(value).to_bytes(4, 'little', signed=True)
        self._port.write(id_type + value)

    def _write_float32(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int(DataTypes.float32)).to_bytes(1, 'little')
        value = pack('f', float(value))
        self._port.write(id_type + value)
