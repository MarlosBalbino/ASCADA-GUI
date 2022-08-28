from PySide6.QtWidgets import QHBoxLayout, QFrame, QLabel


class InFlag(QFrame):

    def __init__(self, var_id: int, flag_type:str):        
        super().__init__()
        #
        label = QLabel(text=f'Id: {var_id}\tType: {flag_type}')
        self.value = QLabel()
        #
        lyt = QHBoxLayout(self)
        lyt.addWidget(label)
        lyt.addWidget(self.value)

    def update_value(self, value):
        self.value.setText(str(value))
