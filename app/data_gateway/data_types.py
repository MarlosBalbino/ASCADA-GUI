class DataTypes:
    bool8 = 'bool8'
    uint8 = 'uint8'
    int8 = 'int8'
    uint16 = 'uint16'
    int16 = 'int16'
    uint32 = 'uint32'
    int32 = 'int32'
    float32 = 'float32'
    ts_int16 = 'ts_int16'
    ts_int32 = 'ts_int32'
    ts_float32 = 'ts_float32'

    types = {
        # id of data type: string name of data type
        1: 'bool8',
        2: 'uint8',
        3: 'int8',
        4: 'uint16',
        5: 'int16',
        6: 'uint32',
        7: 'int32',
        8: 'float32',
        9: 'ts_int16',
        10: 'ts_int32',
        11: 'ts_float32',
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
