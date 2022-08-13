from ctypes import alignment
from qt_core import *
from gui.widgets.py_push_button import PyPushButton


class MyWidgets(object):

    def leftHiddenMenu(self, parent=None):
        # LEFT HIDDEN MENU
        #////////////////////////////////////////////////////////////////////
        # HIDDEN FRAME
        self.hidden_frame = QFrame(parent=parent)
        self.hidden_frame.setStyleSheet("background-color: transparent")
        self.hidden_frame.setMaximumWidth(3840)
        self.hidden_frame.setMinimumWidth(3840)
        self.hidden_frame.setMinimumHeight(2160)
        self.hidden_frame.hide()

        # HIDDEN FRAME LAYOUT
        self.hidden_layout = QHBoxLayout(self.hidden_frame)
        self.hidden_layout.setContentsMargins(0,0,0,0)
        self.hidden_layout.setSpacing(0)

        # HIDDEN MENU
        self.hidden_menu = QFrame()
        self.hidden_menu.setStyleSheet("background-color: #44475a")
        self.hidden_menu.setMaximumWidth(0)
        self.hidden_menu.setMinimumWidth(0)
        self.hidden_menu.setMaximumHeight(2160)

        # HIDDEN BTN FRAME
        self.hidden_btn_frame = QFrame()
        self.hidden_btn_frame.setStyleSheet("background-color: transparent")
        self.hidden_btn_frame.setMaximumHeight(2160)

        # HIDDEN BTN
        self.hidden_btn = QPushButton(self.hidden_btn_frame)
        self.hidden_btn.setStyleSheet("background-color: transparent")
        self.hidden_btn.setFixedSize(3840, 3840)
        
        # ADD HIDDEN BTN TO HIDDEN FRAME
        self.hidden_layout.addWidget(self.hidden_menu)
        self.hidden_layout.addWidget(self.hidden_btn_frame)

    def textBox(self, 
        parent=None, 
        label_text="", 
        btn_text="", 
        size=QSize(500, 250),
        text_box_color="#282a36"
        ):
        # TEXT BOX
        #////////////////////////////////////////////////////////////////////
        # TEXT BOX FRAME
        self.text_box_frame = QFrame(parent=parent)
        self.text_box_frame.setStyleSheet("background-color: #44475a; border-radius: 5")
        self.text_box_frame.setMaximumSize(size)
        self.text_box_frame.setMinimumSize(size)

        # LABEL TEXT
        self.text_label = QLabel(self.text_box_frame)
        self.text_label.setText(label_text)
        self.text_label.setStyleSheet("font: 700 12pt Segoe UI; color: rgb(255, 255, 255)")

        # CUSTOM VERTICAL SCROLL BAR
        self.vertical_scroll_bar = MyScrollBar()

        # TEXT BOX
        self.text_box = QTextEdit(self.text_box_frame)
        self.text_box.setMaximumSize(QSize(482, 178))
        self.text_box.setMinimumSize(QSize(482, 178))
        self.text_box.setStyleSheet(f"""color: white; font-size: 12pt; 
            border-radius: 5; background-color: {text_box_color}""")
        self.text_box.setVerticalScrollBar(self.vertical_scroll_bar)
        self.text_box.setAcceptRichText(True)

        # DONE BUTTON
        self.done_btn = QPushButton(btn_text)
        self.done_btn.setStyleSheet("""
            QPushButton {
                background-color: #8489a6;
                border-radius: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #c3ccdf;
            }    
            QPushButton:pressed {
                background-color: #44475a;
            }        
        """)
        self.done_btn.setMaximumWidth(72)
        self.done_btn.setMaximumHeight(20)

        # TEXT BOX LAYOUT
        self.text_box_layout = QVBoxLayout(self.text_box_frame)
        self.text_box_layout.addWidget(self.text_label)
        self.text_box_layout.addWidget(self.text_box)
        self.text_box_layout.addWidget(self.done_btn)


class MyScrollBar(QScrollBar):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            /*VERTICAL SCROLL BAR*/
            QScrollBar:vertical {
                border: none;
                background-color: #282a36;
                width: 10px;
                margin: 10px 0 10px 0;
                border-radius: 0px;
            }

            /*VERTICAL SCROLL BAR HENDLE*/
            QScrollBar::handle:vertical {
                background-color: #8489a6;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #c3ccdf;
            }
            QScrollBar::handle:vertical:pressed {
                background-color: #44475a
            }

            /*SCROLL BAR TOP BUTTOM*/
            QScrollBar::sub-line:vertical {
                border: none;
                background-color: #8489a6;
                height: 10px;
                /*
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                */
                border-radius: 5px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical:hover {
                background-color: #c3ccdf;
            }
            QScrollBar::sub-line:vertical:pressed {
                background-color: #44475a;
            }

            /*SCROLL BAR BOTTOM BUTTOM*/
            QScrollBar::add-line:vertical {
                border: none;
                background-color: #8489a6;
                height: 10px;
                /*
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                */
                border-radius: 5px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical:hover {
                background-color: #c3ccdf;
            }
            QScrollBar::add-line:vertical:pressed {
                background-color: #44475a;
            }

            /*RESET ARROW*/
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)


class ChartWindow(QFrame): 

    def __init__(self, height=500, color="#707070"):

        super().__init__()
        
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self.setStyleSheet(f"background-color: {color}")

        self.frame_layout = QVBoxLayout(self)
        self.frame_layout.setContentsMargins(0,0,0,0)

        self.top_frame = QFrame()
        self.top_frame.setMaximumHeight(30)
        self.top_frame.setMinimumHeight(30)
        self.top_frame.setStyleSheet("background-color: black")

        self.top_frame_layout = QHBoxLayout(self.top_frame)
        self.top_frame_layout.setContentsMargins(0,0,0,0)
        self.top_frame_layout.setSpacing(0)

        self.spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.btn = QPushButton("X")
        self.btn.setStyleSheet("""
            QPushButton { background-color: transparent; font: 700 12pt 'Segoe UI'; }
            QPushButton:hover { background-color: #a9000f; }
            QPushButton:pressed { background-color: transparent; }
        """)
        self.btn.setMaximumSize(QSize(70, 25))
        self.btn.setMinimumSize(QSize(70, 25))

        self.top_frame_layout.addSpacerItem(self.spacer)
        self.top_frame_layout.addWidget(self.btn, 0, Qt.AlignTop)

        self.bottom_frame = QFrame()
        self.bottom_frame.setStyleSheet(f"background-color: {color}")

        self.bottom_frame_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_frame_layout.setContentsMargins(0,0,0,0)
        self.bottom_frame_layout.setSpacing(0)

        self.frame_layout.addWidget(self.top_frame)
        self.frame_layout.addWidget(self.bottom_frame)

    def add_widget(self, widget: QFrame):
        self.bottom_frame_layout.addWidget(widget)
        self.destroyed.connect(widget.close)
        self.btn.clicked.connect(lambda: self.deleteLater())