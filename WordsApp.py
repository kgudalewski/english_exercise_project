from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.core.window import Window

Window.size = (400, 800)


class WordsApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        screen = Builder.load_string(screen_helper)
        return screen

    word = "słowo do tłumaczenia"
    blurr_translation = "? ? ? ? ? ? ? ?"
    translation = "tłumaczenie"
    user_translation = "tłumaczenie użytkownika"


screen_helper = """

ScreenManager:
    MenuScreen:
    GameScreen:
    EvaluationScreen:
    AddScreen:
    RemoveScreen:

<MenuScreen>
    name: 'menu'
    MDLabel:
        text: "Learning App"
        halign: "center" 
        size_hint: (1,1.4)
        color: app.theme_cls.primary_color
        font_style: "H4"
    MDFillRoundFlatIconButton:
        text: "PLAY"
        pos_hint: {'center_x':0.5,'center_y':0.5}
        icon: "play"
        font_size: "20"
        theme_text_color: "Custom"
        text_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
        on_press: root.manager.current = 'game'
        size_hint: 0.5,None
        
    MDRectangleFlatButton:
        text: "Add words"
        pos_hint: {'center_x':0.5,'center_y':0.4}
        font_size: "12"
        on_press: root.manager.current = 'add_word'
        size_hint: 0.5,None
    MDRectangleFlatButton:
        text: "Remove words"
        pos_hint: {'center_x':0.5,'center_y':0.3}
        font_size: "12"
        on_press: root.manager.current = 'remove_word'
        size_hint: 0.5,None
        
        
<GameScreen>
    name: 'game'
    MDRectangleFlatButton:
        text: 'End game'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.end_game_dialog(self)
        size_hint: None, None
        width: root.width*0.9
    MDRectangleFlatButton:
        text: root.word
        pos_hint: {'center_x':0.5,'center_y':0.9}
        size_hint: None, None
        width: root.width*0.9
    MDRectangleFlatButton:
        id: translation
        name: 'translation'
        text: root.blurr_translation
        pos_hint: {'center_x':0.5,'center_y':0.8}
        size_hint: None, None
        width: root.width*0.9
    MDTextField:
        id: user_translation
        hint_text: "Enter your translation"
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: None, None
        width: root.width*0.9
        mode: "rectangle"
    MDFillRoundFlatButton:
        id: check_btn
        font_size: "20"
        theme_text_color: "Custom"
        text_color: "black"
        text: "CHECK"
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: None, None
        width: root.width*0.9
        on_release: root.check_action(self)
        
<EvaluationScreen>
    name: 'evaluation'
    MDRectangleFlatButton:
        text: root.word
        pos_hint: {'center_x':0.5,'center_y':0.9}
        size_hint: None, None
        width: root.width*0.9
    MDRectangleFlatButton:
        text: root.translation
        pos_hint: {'center_x':0.5,'center_y':0.8}
        size_hint: None, None
        width: root.width*0.9
    MDRectangleFlatButton:
        text: root.user_translation
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: None, None
        width: root.width*0.9
    MDRectangleFlatButton:
        id: yes
        text: "Correct"
        pos_hint: {'center_x':0.75,'center_y':0.6}
        size_hint: None, None
        width: root.width*0.4
        text_color: "green"
        line_color: "green"
        on_release: root.yes_action(self)
    MDRectangleFlatButton:
        id: no
        text: "Incorrect"
        pos_hint: {'center_x':0.25,'center_y':0.6}
        size_hint: None, None
        width: root.width*0.4
        text_color: "red"
        line_color: "red"
        on_release: root.no_action(self)
        
<AddScreen>
    name: 'add_word'
    MDTextField:
        id: text_field1
        hint_text: "Enter english word"
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: None, None
        width: root.width*0.9
        mode: "rectangle"
    MDTextField:
        id: text_field2
        hint_text: "Enter polish word"
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: None, None
        width: root.width*0.9
        mode: "rectangle"
    MDRectangleFlatButton:
        text: 'Add'
        pos_hint: {'center_x':0.75,'center_y':0.1}
        size_hint: None, None
        width: root.width*0.4
        on_release: root.add_confirm(self)
        on_release: root.clear_txt(self)
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.25,'center_y':0.1}
        on_press: root.manager.current = 'menu'
        size_hint: None, None
        width: root.width*0.4
        
<RemoveScreen>
    name: 'remove_word'
    MDLabel:
        text: "remove"
        halign: "center" 
        size_hint: (1,1.4)
        color: app.theme_cls.primary_color
        font_style: "H4"
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'menu'
"""


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    word = WordsApp.word
    blurr_translation = WordsApp.blurr_translation
    translation = WordsApp.translation
    user_translation = WordsApp.user_translation

    def end_game_dialog(self, obj):
        self.dialog = MDDialog(title='Are you sure ?',
                               buttons=[MDFlatButton(text="Yes, end game", on_release=self.menu_switch),
                                        MDFlatButton(text='Cancel', on_release=self.close_dialog)]
                               )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def menu_switch(self, obj):
        self.manager.current = 'menu'
        self.dialog.dismiss()

    def check_action(self, obj):
        WordsApp.user_translation = self.ids.user_translation.text
        self.ids.user_translation.text = ""
        self.manager.current = 'evaluation'

    pass


class EvaluationScreen(Screen):
    word = WordsApp.word
    translation = WordsApp.translation
    # user_translation = Screen.get_screen('game').ids.user_translation.text
    user_translation = WordsApp.user_translation

    def yes_action(self, obj):
        self.manager.current = 'game'
        # TODO ulpoad weight

    # TODO dialog confirmation window

    def no_action(self, obj):
        self.manager.current = 'game'
        # TODO ulpoad weight

    pass


class AddScreen(Screen):
    def clear_txt(self, obj):
        self.ids.text_field1.text = ""
        self.ids.text_field2.text = ""

    def add_confirm(self, obj):
        self.dialog = MDDialog(title='Translation added !',
                               buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)]
                               )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    pass


class RemoveScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(GameScreen(name="game"))
sm.add_widget(AddScreen(name="add_word"))
sm.add_widget(RemoveScreen(name="remove_word"))

WordsApp().run()
