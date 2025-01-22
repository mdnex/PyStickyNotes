from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QPlainTextEdit,QHBoxLayout,QVBoxLayout,QFrame,QScrollArea,QMainWindow,QLineEdit,QColorDialog
from PyQt6.QtGui import QIcon, QShortcut,QAction,QGuiApplication,QIntValidator
from PyQt6.QtCore import Qt
#from PyQt6.QtCore.Qt import QTextDocument
import sys
import settings
import datetime

# main_path = "/home/mdnext/pysticky"
current_doc = ""
current_doc_text = ""
#mode = "list"
mode = "list"

def init_doc():
    global current_doc
    global current_doc_text
    current_doc = ""
    current_doc_text = ""

def reload_main():
    global window
    #global mode
    #print(mode)
    #print("vish")
    #window.reload_content()
    del window

    window = Main()

class Edit(QPlainTextEdit):
    """docstring for ."""

    def __init__(self):
        super().__init__()
        global current_doc_text
        self.setStyleSheet("border : 0;font-size: 16px;color: #fff;background-color:{}".format(settings.get_background()))
        self.setPlainText(current_doc_text)
        self.move(0,50)

    def save_text(self):
        text = self.toPlainText().strip()
        files = settings.get_files()
        
        # text = self.toPlainText().strip()
        global current_doc
        if not current_doc:
            dt = datetime.date.today()
            title = "{}-{}-{}-doc{}".format(dt.day,dt.month,dt.year,str(len(files)))
            current_doc = settings.get_notes_path() + title
        #text.split("\n")[0]
        # title = title[0:100].split(" ")[-1] if len(title)>100 else title
        # if title:
        file_ = open("{}".format(current_doc),'w')
        file_.write(text)
        file_.close()
            
        # print(text)
        global mode
        mode = "list"
        reload_main()

class List(QVBoxLayout):
    """docstring for ."""

    def __init__(self):
        super().__init__()


        self.create_widgets()

    def create_widgets(self):
        y = 50
        path = settings.get_notes_path()
        files = settings.get_files()
        for fl in files:
            # global current_doc
            # current_doc = path + fl
            bt = QPushButton("{}".format(fl))
            bt.clicked.connect((lambda fl=fl:lambda: self.edit_doc(path + fl))())
            #list[i].move(0,100)
            bt.move(100,y+400)
            y=y+50
            
            
            bt.setStyleSheet("color:{};border : 0;width:352%;height:50px;background-color:{}".format(settings.get_text_color(),settings.get_background()))
            #list[i].setStyleSheet("border : 0;")
            self.addWidget(bt)

    def edit_doc(self,id):
        global current_doc
        global current_doc_text
        
        current_doc = id
        file_ = open(id,'r')
        current_doc_text = file_.read()
        file_.close()
        
        global mode
        mode = "edit" if mode=="list" else "list"
        global reload_main
        reload_main()
        pass

class Settings(QVBoxLayout):
    """docstring for ."""

    def __init__(self):
        super().__init__()
        # self.lineEdit = None

        self.create_widgets()

    def create_widgets(self):
        # lbl = QLabel(settings.get_init_path())
        # bt = QPushButton("change path")
        # bt.clicked.connect(self.change_path)
        # bt.setStyleSheet("color:{};border : 0;width:352%;height:50px;background-color:{}".format(settings.get_text_color(),settings.get_background()))
        
        hb = QHBoxLayout()
        lbl1 = QLabel("opacity (10 - 90)")
        
        self.lineEdit = QLineEdit()
        onlyInt = QIntValidator()
        onlyInt.setRange(10, 90)
        self.lineEdit.setValidator(onlyInt)
        self.lineEdit.setStyleSheet("height:50px;font-size:16px;border:1px solid {};".format(settings.get_text_color()))
        bt1 = QPushButton("Save")
        bt1.clicked.connect(self.save_transparency)
        bt1.setStyleSheet("color:{};border : 0;height:50px;background-color:{}".format(settings.get_text_color(),settings.get_background()))
        hb.addWidget(self.lineEdit)
        hb.addWidget(bt1)
        # wg = QWidget()
        # wg.addLayout(hb)
        
        lbl2 = QLabel("text color")
        bt2 = QPushButton("Change Foreground")
        bt2.clicked.connect(self.change_foreground)
        bt2.setStyleSheet("color:{};border : 0;width:352%;height:50px;background-color:{}".format(settings.get_text_color(),settings.get_background()))
        
        lbl3 = QLabel("background color")
        bt3 = QPushButton("Change Background")
        bt3.clicked.connect(self.change_background)
        bt3.setStyleSheet("color:{};border : 0;width:352%;height:50px;background-color:{}".format(settings.get_text_color(),settings.get_background()))

        # intV = QIntValidator()
        # intV.setRange(0, 4)
        
        
        # self.addWidget(lbl)
        # self.addWidget(bt)
        # self.addWidget(lbl1)
        
        # self.addWidget(self.lineEdit)
        # self.addWidget(bt1)
        self.addWidget(lbl1)
        self.addLayout(hb)
        self.addWidget(lbl2)
        self.addWidget(bt2)
        self.addWidget(lbl3)
        self.addWidget(bt3)
        
    def change_path(self):
        print("change path")
    
    def save_transparency(self):
        # print(self.lineEdit.text)
        settings.set_transparency(self.lineEdit.text() if self.lineEdit.text() else "50")
        self.lineEdit.setText("")
        reload_main()
        
    def change_foreground(self):
        color = QColorDialog.getColor()
        settings.set_text_color(color.name())
        # print(color)
        # color = QColorDialog.getColor()
        # print(color.name())
        reload_main()
        
    def change_background(self):
        
        color = (QColorDialog.getColor()).name().lstrip("#")
        color = str( tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) )[+1:-1]
        settings.set_background(color)
        # print(color.name())
        reload_main()
    
class Main(QWidget):
    """docstring for ."""

    def __init__(self):
        super().__init__()


        self.setWindowTitle("PyStickyNotes")
        self.setWindowIcon(QIcon('./settings/assets/pysticky.png'))
        # self.setWindowIcon(QIcon("PyStickyNotes"))
        # self.setFixedHeight(200)
        # self.setFixedWidth(200)
        
        self.setGeometry(1000,300,400,300)
        #self.setStyleSheet("background-color:red")

        # style = (
        #     'background-color:rgba(100,100,100,50)'
        # )
        # self.setStyleSheet(style)
        #self.setWindowOpacity(0.4);
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground,True)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop, True)
        
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt::FramelessWindowHint)


        self.create_widgets()
        self.show()


    def create_widgets(self):
        global mode

        box = QHBoxLayout()
        self.add_buttons(box)

        self.main_panel = QVBoxLayout()

        self.main_panel.addLayout(box)
        #________________________________________
        
        if(mode == "list"):
            self.content_box = List()

            #main_panel.addLayout(self.content_box)
            #self.setCentralWidget(self.content_box)
            #self.setLayout(main_panel)
            #main_panel.addWidget(self.content_box)
            #main_panel.addWidget(self.content_box)
            scroller = QScrollArea()
            scroller.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroller.setStyleSheet("border : 0;background: transparent;width:100%;color:{};".format(settings.get_text_color()))
            widget = QWidget()
            widget.setLayout( self.content_box)
            widget.setStyleSheet("width:100%;")
            scroller.setWidget(widget)
            self.main_panel.addWidget(scroller)
            init_doc()
            
        elif(mode == "settings"):
            self.content_box = Settings()
            scroller = QScrollArea()
            scroller.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroller.setStyleSheet("border : 0;background: transparent;width:100%;color:{};".format(settings.get_text_color()))
            widget = QWidget()
            widget.setLayout( self.content_box)
            widget.setStyleSheet("width:100%;")
            scroller.setWidget(widget)
            self.main_panel.addWidget(scroller)
        else:
            print("modo:",mode)
            self.content_box = Edit()
            #self.content_box.setStyleSheet("width:100%;")
            self.main_panel.addWidget(self.content_box)

        #________________________________________

        self.setLayout(self.main_panel)

    def add_buttons(self,box):
        global mode
        
        btn_style = "color:{};border : 0;padding-bottom:15px;padding-top:15px;background-color:{}".format(settings.get_text_color(),settings.get_background())
        
        btn_new = QPushButton("")
        btn_new.setIcon(QIcon(settings.get_init_path() + "settings/assets/plus.png"))
        btn_new.setGeometry(0,0,50,50)
        btn_new.setStyleSheet(btn_style)
        btn_new.clicked.connect(self.btn_new_action)

        btn_save = QPushButton("")
        btn_save.setIcon(QIcon(settings.get_init_path() + "settings/assets/check.png"))
        btn_save.setGeometry(0,0,50,50)
        btn_save.setStyleSheet(btn_style)
        btn_save.clicked.connect(self.btn_save_action)

        btn_back = QPushButton("")
        btn_back.setIcon(QIcon(settings.get_init_path() + "settings/assets/back.png"))
        btn_back.setGeometry(50,0,50,50)
        btn_back.setStyleSheet(btn_style)
        btn_back.clicked.connect(self.btn_back_action)

        btn_back = QPushButton("")
        btn_back.setIcon(QIcon(settings.get_init_path() + "settings/assets/back.png"))
        btn_back.setGeometry(100,0,50,50)
        btn_back.setStyleSheet(btn_style)
        btn_back.clicked.connect(self.btn_new_action)

        btn_exit = QPushButton("")
        btn_exit.setIcon(QIcon(settings.get_init_path() + "settings/assets/exit.png"))
        btn_exit.setGeometry(150,0,50,50)
        btn_exit.setStyleSheet(btn_style)
        btn_exit.clicked.connect(self.btn_exit_action)

        btn_hide = QPushButton("")
        btn_hide.setIcon(QIcon(settings.get_init_path() + "settings/assets/hide.png"))
        btn_hide.setGeometry(200,0,50,50)
        btn_hide.setStyleSheet(btn_style)
        btn_hide.clicked.connect(self.btn_hide_action)

        btn_push_side = QPushButton("")
        btn_push_side.setIcon(QIcon(settings.get_init_path() + "settings/assets/right.png"))
        btn_push_side.setGeometry(250,0,50,50)
        btn_push_side.setStyleSheet(btn_style)
        btn_push_side.clicked.connect(self.btn_push_action)
        
        btn_setting = QPushButton("")
        btn_setting.setIcon(QIcon(settings.get_init_path() + "settings/assets/settings.png"))
        btn_setting.setGeometry(250,0,50,50)
        btn_setting.setStyleSheet(btn_style)
        btn_setting.clicked.connect(self.btn_setting_action)

        if(mode == "list"):
            print("list")
            box.addWidget(btn_new)
            box.addWidget(btn_setting)
            # box.addWidget(btn_hide)
            # box.addWidget(btn_exit)
            # box.addWidget(btn_push_side)
        elif(mode == "settings"):
            print("settings")
            # box.addWidget(btn_save)
            box.addWidget(btn_back)
            # box.addWidget(btn_hide)
            # box.addWidget(btn_exit)
            # box.addWidget(btn_push_side)
        else:
            print("edit")
            box.addWidget(btn_save)
            box.addWidget(btn_back)
            # box.addWidget(btn_hide)
            # box.addWidget(btn_exit)
            # box.addWidget(btn_push_side)

    def btn_new_action(self):
        global mode
        mode = "edit" if mode=="list" else "list"
        global reload_main
        reload_main()
        pass

    def btn_save_action(self):
        self.content_box.save_text()
        pass

    def btn_exit_action(self):
        self.close()
        #sys.exit(0)
        pass

    def btn_hide_action(self):
        self.showMinimized()

    def btn_push_action(self):
        top_right = QGuiApplication.primaryScreen().availableGeometry().topRight()
        self.move(top_right)
        pass

    def btn_back_action(self):
        # print("sssssss")
        # global mode
        # if mode=="list":
        #     mode = "edit"
        # else:
        #     mode = "list"
        # global reload_main
        # reload_main()
        pass

    def btn_setting_action(self):
        global mode
        mode = "settings"
        global reload_main
        reload_main()
        pass

    def remove_all(self):
        self.main_panel.setParent(None)

    def reload_content(self):
        # global mode
        # if mode=="list":
        #     mode = "edit"
        # else:
        #     mode = "list"
        self.remove_all()
        self.create_widgets()

app = QApplication([])
window = Main()



sys.exit(app.exec())
