from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from jnius import autoclass
from threading import *


KV = ('''
ScreenManager:
    id: 'manager'
    Download
        name: 'download'
        
    ControlScreen:
        name: 'control'
        id: control 
    
    DataScreen:
        name: 'data' 
        id: data
        
<DataScreen>
    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientation: 'vertical'
            MDTopAppBar:
                title: 'Показания'
            MDTabs:
                id: tabs

        MDBottomAppBar:
            MDTopAppBar:
                on_action_button:                 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'control'
                icon: "swap-horizontal"
                type: "bottom"
        
        
<ControlScreen>
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            orientation: 'vertical'
            MDTopAppBar:
                title: 'Контроль'
            MDTabs:
                id: tabs


        MDBottomAppBar:
            MDTopAppBar:
                on_action_button: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'data'
                icon: "swap-horizontal"
                type: "bottom"
            
            
<Tab>
    grid: grid
    MDScrollView:
        do_scroll_x: False
        do_scroll_y: True

        MDGridLayout:
            id: grid
            spacing: 100
            padding: 100, 100, 50, 0
            size_hint_y: 1.1
            height: self.minimum_height
            cols: 1 


<ButtonExsitDigotal>
    orientation: 'horizontal' 
    size_hint_y: None
    MDLabel:
        id: button
        font_size: '30sp'

    MDSwitch:
        id: switch
        on_active: app.write_message(self.parent.message_get(self))
        pin: 0
        pos_hint: {'center_x': .5, 'center_y': .5}
        pos_hint_y: 'center_y'
        width: dp(60)

<ButtonExsitAnalog>
    orientation: 'vertical'
    size_hint_y: None
    MDLabel:
        font_size: '30sp'
        id: button
        
    MDLabel:
        text: ' '
        
    MDSlider:
        ac: 0
        value: 0
        show_off: False
        on_touch_up: 
            app.write_message(self.parent.message_get(self))
        hint_bg_color: (0, 0, 0, 255)
        id: switch
        pin: 0
        

<Information>
    orientation: 'vertical'
    size_hint_y: None
    number: 0
    MDLabel:
        id: name
        font_size: '25sp'
        halign: 'center'
    MDLabel:
        text: ' '
    MDLabel:
        id: value
        font_size: '35sp'
        halign: 'center'
        

<Download>
    MDBoxLayout:
        orientation: 'vertical'
        padding: [100, 100, 100, 800]
        MDLabel:
            id: info
            text: ''
            font_size: '35sp'
            halign: 'center'
        MDFillRoundFlatButton:
            font_size: '35sp'
            padding: [100, 100, 100, 100]
            color: [255, 0, 0, 255]
            text: 'Подключиться'
            on_press: app.connect("HC-06")

''')


class ControlScreen(MDScreen):
    pass

class DataScreen(MDScreen):
    pass

class Tab(MDBoxLayout, MDTabsBase):
    pass

class Information(MDBoxLayout):
    pass

class Download(MDScreen):
    pass


class ButtonExsitDigotal(MDBoxLayout):
    def message_get(self, switch):
        if switch.active:
            return str(switch.pin) + ',' + '1'
        else:
            return str(switch.pin) + ',' + '0'


class ButtonExsitAnalog(MDBoxLayout):
    def message_get(self, switch):
        if switch.ac == 2:
            switch.ac = 0
            return str(switch.pin) + ',' + str(int(switch.value))
        else:
            switch.ac = 2
            return '|'


groups_control = {
'Яркие':
        ((ButtonExsitDigotal, '1 синий', 0), (ButtonExsitDigotal, '2 синий', 1),
         (ButtonExsitDigotal, '3 синий', 2)),

'Тусклые':
        ((ButtonExsitDigotal, 'зелный 1', 6), (ButtonExsitDigotal, 'жёлтый 1', 7),
         (ButtonExsitDigotal, 'зелёный 2', 8), (ButtonExsitDigotal, 'жёлтый 2', 9)),

'RGB': ((ButtonExsitAnalog, 'Красный', 3), (ButtonExsitAnalog, 'Синий', 4),
        (ButtonExsitAnalog, 'Зелëный', 5))
}

data = []
groups_data = {
    'тестовая': (('влажность', '34%'), ('температура', '-8'), ('название', 'значение')),
    '1 группа': (('tttrrgetedfh', 'значение'), ('название', 'значение'), ('название', 'значение'),
                 ('название', 'значение'), ('название', 'значение'), ('название', 'значение'),
                 ('название', 'значение'), ('название', 'значение'), ('название', 'значение')),
    '2 группа': (('название', 'значение'), ('название', 'значение'), ('название', 'значение')),
    '3 группа': (('название', 'значение'), ('название', 'значение'), ('название', 'значение'))
}


class CoontrolApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        return Builder.load_string(KV)

    def on_start(self):
        for i in range(len(groups_data)):
            group = Tab(title=list(groups_data.keys())[i])
            widgets_data = groups_data[list(groups_data.keys())[i]]
            for widget_name, widget_data in widgets_data:
                widget = Information()
                widget.ids.value.text = widget_data
                widget.ids.name.text = widget_name
                group.grid.add_widget(widget)
                data.append(widget)
            self.root.ids.data.ids.tabs.add_widget(group)

        for i in range(len(groups_control)):
            group = Tab(title=list(groups_control.keys())[i])
            widgets_data = groups_control[list(groups_control.keys())[i]]
            for widget_class, widget_text, pin in widgets_data:
                widget = widget_class()
                widget.ids.button.text = widget_text
                widget.ids.switch.pin = pin
                group.grid.add_widget(widget)
            self.root.ids.control.ids.tabs.add_widget(group)

        self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
        self.UUID = autoclass('java.util.UUID')

        self.CharBuilder = autoclass('java.lang.Character')


    def get_socket_stream(self, name):
        paired_devices = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        self.socket = None
        for device in paired_devices:
            if device.getName() == name:
                self.socket = device.createRfcommSocketToServiceRecord(
                    self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                recv_stream = self.socket.getInputStream()
                send_stream = self.socket.getOutputStream()
                break
        self.socket.connect()
        return recv_stream, send_stream

    def connect(self, name):
        while True:
            try:
                self.recv_stream, self.send_stream = self.get_socket_stream(name)
                break
            except: pass
        self.read = Thread(target=self.recv_data)
        self.read.start()
        self.root.current = 'control'

    def recv_data(self):
        data_read = ''
        errors = 0
        while True:
            try:
                read = self.recv_stream.read()
                theChar = self.CharBuilder.toChars(read)
                data_read += theChar[0]
                if theChar[0] == '>':
                    self.data_set(data_read)
                    data_read = ''
                errors = 0
            except:
                errors += 1
            if errors == 1000:
                self.root.current = 'download'


    def pars(self, data):
        for i in range(len(data)):
            if data[i] == "<":
                start = i
            elif data[i] == ">":
                end = i
        return data[start + 1:end].split(",")

    def data_set(self, data_):
        data_s = self.pars(data_)
        for i in range(len(data_s)):
            data[i].ids.value.text = data_s[i]

    def write_message(self, message):
        message += '|'
        mes = []
        for i in message:
            mes.append(ord(i))
        mes = bytearray(mes)
        self.send_stream.write(mes)
        self.send_stream.flush()


if __name__ == "__main__":
    CoontrolApp().run()
