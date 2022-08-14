from inspect import classify_class_attrs
import numpy as np
from time import time
import random

from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool, QThread, QTimer

from .ts_chart import TsChart
from .ts_chart import ChartController
from .Types import DataTypes, VarTypes


class DataGateway:

    _data_gateway = None
    _arriving_flags_handlers = {}       # Ex.: {var_id_1: var_handler_1, var_id_2: var_handler_2, ...}
    _variables = {}                     # Ex.: {var_id: {"name": str, "description": str, "var_type": str, "data_type": str}, ...}

    def __init__(self) -> None:
        raise SyntaxError("This is a static class. You should never instantiate it!")

    @classmethod
    def setup(cls):
        cls._data_gateway = _DataGateway()

        # Para teste

        cls._variables =  {
            1: {'var_type': VarTypes.FLAG, 'data_type': DataTypes.BOOL},
            2: {'var_type': VarTypes.FLAG, 'data_type': DataTypes.CHAR},
            3: {'var_type': VarTypes.FLAG, 'data_type': DataTypes.INT16},
            4: {'var_type': VarTypes.FLAG, 'data_type': DataTypes.FLOAT32}
        }

        # #   Simula slot de widget para teste.
        # for var_id in range(1, 5):
        #     cls.add_flag_widget(var_id, lambda value: print(value))

        #   Emite um valor para cada widget conectado. Simula chegada de dados do Arduino
        value_generators = {
            DataTypes.BOOL: lambda: bool(random.randint(0, 1)),
            DataTypes.CHAR: lambda: random.choice('ABCDEFGHIJKLMOPQRSTUVWXYZ'),
            DataTypes.INT8: lambda: random.randint(0,255),
            DataTypes.INT16: lambda: random.randint(0,int(pow(2, 16))),
            DataTypes.INT32: lambda: random.randint(0,int(pow(2, 32))),
            DataTypes.INT64: lambda: random.randint(0, int(pow(2, 64))),
            DataTypes.FLOAT32: lambda: random.random() * 100,
            DataTypes.FLOAT64: lambda: random.random() * 200,
        }

        def vars_mock():
            for var_id, handler in cls._arriving_flags_handlers.items():
                print(var_id)
                data_type = cls._variables[var_id]['data_type']
                handler(value_generators[data_type]())

        cls.timer = QTimer()
        cls.timer.timeout.connect(vars_mock)
        cls.timer.start(1000)

    @classmethod
    def add_variable(cls, var_id: int, var_type: str, data_type: str, name: str = None, description: str = None):        
        assert isinstance(var_id, int)
        assert var_id in range(256)
        assert var_id not in cls._variables.keys()
        cls._variables[var_id] = {
            'var_type': var_type,
            'data_type': data_type,
            'name': name,
            'description': description
        }

    @classmethod
    def rm_variable(cls, var_id):
        cls._variables.pop(var_id)

    @classmethod
    def get_new_chart(cls):
        return cls._data_gateway.get_new_chart()

    @classmethod
    def stop(cls):
        cls._data_gateway.stop()

    @classmethod
    def add_flag_widget(cls, var_id: int, flag_handler: Slot):
        """
        Este método conecta a entrada de dados de uma variável do tipo flag a um widget que exibe o valor da variável.
        A conexão é feita através da emissão de um sinal (Signal) que chama um método (Slot) implementado no widget
        para receber o valor sempre que um novo valor for recebido do Arduino.

        Arguments:
            var_id: Um inteiro no intervalo [0, 255], que identifica a variável
            flag_handler:   Um Slot que recebe o valor da variável.
                            Considere os tipos de dados e os respectivos tipos que devem ser aceitos pelo Slot (tipo em C: tipo em Python):
                                bool: bool
                                char: str
                                int (8, 16, 32, 64): int
                                float32, float64: float
        """
        # Verifica se o id da variável é um inteiro no intervalo [0, 255], se existe uma variável cadastrada com o id e se não existe nenhum widget (Slot) associado à variável
        assert isinstance(var_id, int)
        assert var_id in range(256)
        assert var_id in cls._variables.keys()
        assert var_id not in cls._arriving_flags_handlers.keys()

        cls._arriving_flags_handlers[var_id] = flag_handler

    @classmethod
    def rm_flag_widget(cls, var_id):
        """
        Desconecta entrada de dados para o widget.
        """
        try:
            cls._arriving_flags_handlers.pop(var_id)
        except KeyError:
            raise ValueError(f'The variable with id "{var_id}" is not connected to widget Slot!')

    @classmethod
    @Slot(int, bool)
    def handle_bool_flag_from_widget(cls, var_id, value):
        """
        Este método deve ser usado no widget, quando o usuário clica para enviar o valor.
        Ex.: widget.clicked.connect(DataGateway.handle_bool_flag_from_widget)
        """
        assert var_id in cls._variables.keys()
        print(f'var_id: {var_id}\tBooleanValue: {value}')

    @classmethod
    @Slot(int, str)
    def handle_chart_flag_from_widget(cls, var_id, value):
        """
        Este método deve ser usado no widget, quando o usuário clica para enviar o valor.
        Ex.: widget.clicked.connect(DataGateway.handle_chart_flag_from_widget)
        """
        assert var_id in cls._variables.keys()
        print(f'var_id: {var_id}\tCharValue: {value}')

    @classmethod
    @Slot(int, int)
    def handle_int_flag_from_widget(cls, var_id, value):
        """
        Este método deve ser usado no widget, quando o usuário clica para enviar o valor.
        Ex.: widget.clicked.connect(DataGateway.handle_int_flag_from_widget)
        """
        assert var_id in cls._variables.keys()
        print(f'var_id: {var_id}\tIntValue: {value}')

    @classmethod
    @Slot(int, float)
    def handle_float_flag_from_widget(cls, var_id, value):
        """
        Este método deve ser usado no widget, quando o usuário clica para enviar o valor.
        Ex.: widget.clicked.connect(DataGateway.handle_float_flag_from_widget)
        """
        assert var_id in cls._variables.keys()
        print(f'var_id: {var_id}\tFloatValue: {value}')


class DataGatewaySignals(QObject):
    update_charts = Signal(dict)

    # # Exemplo de como pode conectar widgets para envio de valores (do ASCADA para o Arduino):
    # # No widget crie um objeto Signal que emitirá o valor quando o usuário clicar para enviar
    # _widget_flag_bool = Signal(int, bool)
    # _widget_flag_char = Signal(int, str)
    # _widget_flag_int = Signal(int, int)
    # _widget_flag_float = Signal(int, float)

    # def __init__(self, parent = None) -> None:
    #     super().__init__(parent=parent)

    # #   Conecte o sinal do widget ao método estático adequado (depende do tipo) da classe DataGateway
    #     self._widget_flag_bool.connect(DataGateway.handle_bool_flag_from_widget)
    #     self._widget_flag_char.connect(DataGateway.handle_chart_flag_from_widget)
    #     self._widget_flag_int.connect(DataGateway.handle_int_flag_from_widget)
    #     self._widget_flag_float.connect(DataGateway.handle_float_flag_from_widget)

    #     def emit_values():
    # #       Quando o usuário clica no botão para enviar o widget emita o id da variável e o valor valor
    #         self._widget_flag_bool.emit(5, True)
    #         self._widget_flag_char.emit(6, 'C')
    #         self._widget_flag_int.emit(7, 123)
    #         self._widget_flag_float.emit(8, 123.123)

    #     self._timer = QTimer()
    #     self._timer.timeout.connect(emit_values)
    #     self._timer.setSingleShot(True)
    #     self._timer.start(3000)


class _DataGateway(QRunnable):

    def __init__(self):
        super().__init__()
        self.next_chart_id = 1
        self.ts_info = {
            1: {'legend': 'TimeSeries-1', 'color': (100, 200, 230)},
            2: {'legend': 'TimeSeries-2', 'color': (250, 200, 150)}
        }
        self.ts_data = {
            1: ([0], [0]),
            2: ([10], [0])
        }
        self.params = {
            1: {'f': 2*np.pi/2, 'step': 4e-3, 'frm_n': 25},
            2: {'f': 2*np.pi/3, 'step': 4.1e-3, 'frm_n': 25}
        }
        self.update_freq = 20       # Flushes the icomming data and updates the plots "update_freq" times per second

        self.controllers = {}
        self._signals = DataGatewaySignals()
        self._signals.update_charts.connect(self._update_charts)

        self.keep = None
        self.thread_pool = QThreadPool()
        self.thread_pool.start(self)

    def run(self):
        self.keep = True
        while self.keep:
            t0 = time()

            self._flush_data_streaming()

            # build data and update charts
            data_to_plot = {}
            for chart_id, controller in self.controllers.items():
                data_to_plot[chart_id] = controller.build_chart_data(self.ts_data)
            self._signals.update_charts.emit(data_to_plot)

            processing_time = time() - t0
            if processing_time < 1/self.update_freq:
                QThread.msleep(round((1/self.update_freq - processing_time) * 1000))
            else:
                print(
                    f"Data processing took too long: {processing_time}s."
                    f"Max expected: {1/self.update_freq}s."
                )

    def _flush_data_streaming(self):
        """
        It is a mock for data streaming.
        """
        for id, (t, x) in self.ts_data.items():
            f, step, frm_n = self.params[id].values()
            new_t = np.linspace(t[-1]+step, t[-1]+step + step*frm_n, frm_n)
            new_x = np.sin(f*new_t)
            t.extend(new_t)
            x.extend(new_x)

    @Slot(dict)
    def _update_charts(self, data_to_plot):
        for chart_id, chart_data in data_to_plot.items():
            self.controllers[chart_id].update_plot(chart_data)

    @Slot()
    def get_new_chart(self):
        chart = TsChart(self.next_chart_id, self.ts_info)        
        controller = ChartController(chart.update_lines)

        chart.t_sz_changed.connect(controller.t_sz_changed)
        chart.t_max_changed.connect(controller.t_max_changed)
        chart.ts_enable_changed.connect(controller.ts_enable_changed)
        chart.closing.connect(self._detach_chart)
        self.controllers[self.next_chart_id] = controller

        self.next_chart_id += 1

        return chart

    @Slot(int)
    def _detach_chart(self, chart_id):
        self.controllers.pop(chart_id)

    @Slot()
    def stop(self):
        self.keep = False
