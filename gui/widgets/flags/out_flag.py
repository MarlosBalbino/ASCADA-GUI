from PySide6.QtWidgets import QSpinBox, QDoubleSpinBox, QHBoxLayout, QFrame, QPushButton, QComboBox
from PySide6.QtCore import Signal


class OutBoolFlag(QFrame):
    send_value = Signal(int, bool)       # variable_id, value

    def __init__(self, var_id: int):        
        super().__init__()
        self.var_id = var_id
        #
        value = QComboBox()
        value.addItems(('True', 'False'))
        #
        btn = QPushButton(text='Send Bool Flag')
        btn.clicked.connect(lambda: self.send_value.emit(self.var_id, value.currentText() == 'True'))
        #
        lyt = QHBoxLayout(self)
        lyt.addWidget(value)
        lyt.addWidget(btn)
        
        
class OutCharFlag(QFrame):
    send_value = Signal(int, str)       # variable_id, value

    def __init__(self, var_id: int):        
        super().__init__()
        self.var_id = var_id
        #
        value = QComboBox()
        value.addItems('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,PQ,R,S,T,U,V,W,X,Y,Z'.split(','))
        #
        btn = QPushButton(text='Send Char Flag')
        btn.clicked.connect(lambda: self.send_value.emit(self.var_id, value.currentText()))
        #
        lyt = QHBoxLayout(self)
        lyt.addWidget(value)
        lyt.addWidget(btn)
        
        
class OutIntFlag(QFrame):
    send_value = Signal(int, int)       # variable_id, value

    def __init__(self, var_id: int):        
        super().__init__()
        self.var_id = var_id
        #
        value = QSpinBox()
        value.setRange(-2**15, 2**15)
        #
        btn = QPushButton(text='Send Int Flag')
        btn.clicked.connect(lambda: self.send_value.emit(self.var_id, value.value()))
        #
        lyt = QHBoxLayout(self)
        lyt.addWidget(value)
        lyt.addWidget(btn)
        
        
class OutFloatFlag(QFrame):
    send_value = Signal(int, float)       # variable_id, value

    def __init__(self, var_id: int):        
        super().__init__()
        self.var_id = var_id
        #
        value = QDoubleSpinBox()
        value.setRange(-2**15, 2**15)
        value.setDecimals(3)
        #
        btn = QPushButton(text='Send Float Flag')
        btn.clicked.connect(lambda: self.send_value.emit(self.var_id, value.value()))
        #
        lyt = QHBoxLayout(self)
        lyt.addWidget(value)
        lyt.addWidget(btn)
        
        


