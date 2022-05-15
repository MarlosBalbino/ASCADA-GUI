import numpy as np
from app import logDebug, logError, logWarn, logInfo
import asyncio
from struct import pack, unpack
from .data_types import DataTypes


class SerialStream:

    def __init__(self, port, out_queue, in_ts_queue, in_flag_queue):
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
            id: An interger in the interval: 1:13 (including);
            time: time sample (Number);
            value: value sample (Number);
        :param in_flag_queue: Receives data from serial to share trought DataGateway. Its elements
         are tuples in the format: (id, value). Where:
            id: An interger in the interval: 1:13 (including);
            value: value sample (Number);
        """
        self._port = port
        self._out_queue = out_queue
        self._in_ts_queue = in_ts_queue
        self._in_flag_queue = in_flag_queue
        self._keep = True
        asyncio.create_task(self._run())
        
        self._open_cmd = b'\x0d'
        self._close_cmd = b'\x0e'
        self._read_parsers = {
            'bool8': self._read_bool8,
            'uint8': self._read_uint8,
            'int8': self._read_int8,
            'uint16': self._read_uint16,
            'int16': self._read_int16,
            'uint32': self._read_uint32,
            'int32': self._read_int32,
            'float32': self._read_float32,
            'ts_int16': self._read_ts_int16,
            'ts_int32': self._read_ts_int32,
            'ts_float32': self._read_ts_float32,
        }
        self._write_parsers = {
            'bool8': self._write_bool8,
            'uint8': self._write_uint8,
            'int8': self._write_int8,
            'uint16': self._write_uint16,
            'int16': self._write_int16,
            'uint32': self._write_uint32,
            'int32': self._write_int32,
            'float32': self._write_float32,
        }

    def stop(self):
        self._keep = False
        while not self._keep:
            self._keep = False

    async def _run(self):
        await asyncio.sleep(3)
        await self._write_open()
        logInfo('Streaming open on port:', self._port.name)
        while self._keep:
            await self._read()
            await self._write()
        await self._write_close()
        logInfo('Streaming closed on port:', self._port.name)
        self._keep = True

    async def _write_open(self):
        self._port.write(self._open_cmd)

    async def _write_close(self):
        self._port.write(self._close_cmd)

    async def _read(self):
        if self._port.in_waiting > 0:
            id_type = int.from_bytes(self._port.read(size=1), 'big')
            id = id_type >> 4
            type_int = id_type & int.from_bytes('\x0f', 'big')
            try:
                self._read_parsers[DataTypes.get_type_str(type_int)](id)
            except KeyError:
                logError("Invalid data id read!. id:", id)
                logWarn('Reopening streaming...')
                await self._write_close()
                await self._write_close()
                logWarn('Streaming open!')

    async def _write(self):
        while not self._out_queue.empty():
            id, type_str, value = self._out_queue.get()
            self._write_parsers[type_str](id, value)

    async def _read_bool8(self, id):
        data = bool.from_bytes(self._port.read(size=1), 'big')
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_uint8(self, id):
        data = int.from_bytes(self._port.read(size=1), 'big', signed=False)
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_int8(self, id):
        data = int.from_bytes(self._port.read(size=1), 'big', signed=True)
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_uint16(self, id):
        data = int.from_bytes(self._port.read(size=2), 'big', signed=False)
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_int16(self, id):
        data = int.from_bytes(self._port.read(size=2), 'big', signed=True)
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_uint32(self, id):
        data = int.from_bytes(self._port.read(size=4), 'big', signed=False)
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_int32(self, id):
        data = int.from_bytes(self._port.read(size=4), 'big', signed=True)
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_float32(self, id):
        data = unpack('f', self._port.read(size=4))[0]
        await self._in_flag_queue.put((DataTypes.get_type_str(id), data))

    async def _read_ts_int16(self, id):
        time = int.from_bytes(self._port.read(size=2), 'big', signed=True)
        value = int.from_bytes(self._port.read(size=2), 'big', signed=True)
        await self._in_ts_queue.put((DataTypes.get_type_str(id), time, value))

    async def _read_ts_int32(self, id):
        time = int.from_bytes(self._port.read(size=4), 'big', signed=True)
        value = int.from_bytes(self._port.read(size=4), 'big', signed=True)
        await self._in_ts_queue.put((DataTypes.get_type_str(id), time, value))

    async def _read_ts_float32(self, id):
        time = unpack('f', self._port.read(size=4))[0]
        value = unpack('f', self._port.read(size=4))[0]
        await self._in_ts_queue.put((DataTypes.get_type_str(id), time, value))

    async def _write_bool8(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('bool8')).to_bytes(1, 'big')
        value = bool(value).to_bytes(1, 'big')
        self._port.write(id_type + value)
    
    async def _write_uint8(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('uint8')).to_bytes(1, 'big')
        value = int(value).to_bytes(1, 'big', signed=False)
        self._port.write(id_type + value)
    
    async def _write_int8(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('int8')).to_bytes(1, 'big')
        value = int(value).to_bytes(1, 'big', signed=True)
        self._port.write(id_type + value)
    
    async def _write_uint16(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('uint16')).to_bytes(1, 'big')
        value = int(value).to_bytes(2, 'big', signed=False)
        self._port.write(id_type + value)
    
    async def _write_int16(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('int16')).to_bytes(1, 'big')
        value = int(value).to_bytes(2, 'big', signed=True)
        self._port.write(id_type + value)
    
    async def _write_uint32(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('uint32')).to_bytes(1, 'big')
        value = int(value).to_bytes(4, 'big', signed=False)
        self._port.write(id_type + value)
    
    async def _write_int32(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('int32')).to_bytes(1, 'big')
        value = int(value).to_bytes(4, 'big', signed=True)
        self._port.write(id_type + value)
    
    async def _write_float32(self, id, value):
        id_type = (int(id) << 4 | DataTypes.get_type_int('uint32')).to_bytes(1, 'big')
        value = pack('f', float(value))
        self._port.write(id_type + value)
    

