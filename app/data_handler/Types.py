class VarTypes:
    FLAG = 'flag'
    SERIE = 'serie'
    TIME_SERIE = 'time-serie'

class DataTypes:
    BOOL = 'bool'
    CHAR = 'char'
    INT8 = 'int8'
    INT16 = 'int16'
    INT32 = 'int32'
    INT64 = 'int64'
    FLOAT32 = 'float32'
    FLOAT64 = 'float64'
    ts_int16 = 'ts-int16'
    ts_int32 = 'ts-int32'
    ts_float32 = 'ts-float32'

    types = {
        # id of data type: string name of data type
        1: 'bool',
        2: 'char',
        3: 'int8',
        4: 'int16',
        5: 'int32',
        6: 'int64',
        7: 'float32',
        8: 'float64',
        9: 'ts-int16',
        10: 'ts-int32',
        11: 'ts-float32',
    }

    open_cmd = b'\x0e'
    close_cmd = b'\x0f'
    type_mask = b'\x0f'

    @classmethod
    def get_type_str(cls, type_int: int) -> str:
        return cls.types[type_int]

    @classmethod
    def get_type_int(cls, type_str: str) -> int:
        for tp_int, tp_str in cls.types.items():
            if tp_str == type_str:
                return tp_int
