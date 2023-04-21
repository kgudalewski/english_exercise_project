from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window

Window.size = (400, 800)


class WordsApp(MDApp):
    word = "słowo do tłumaczenia"
    blurr_translation = "? ? ? ? ? ? ? ?"
    translation = "tłumaczenie"
    user_translation = "tłumaczenie użytkownika"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.root = Builder.load_string(screen_helper)
        return self.root

    def save_user_translation(self, obj):
        self.user_translation = self.root.get_screen('game').ids.user_translation.text


screen_helper = """

ScreenManager:
    MenuScreen:
    GameScreen:
    AddScreen:
    RemoveScreen:
    
<MenuScreen>
    name: 'menu'
    id: menu
    MDLabel:
        text: "Learning App"
        halign: "center" 
        size_hint: (1,1.4)
        color: app.theme_cls.primary_color
        font_style: "H4"
    MDFillRoundFlatIconButton:
        text: "PLAY"
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint: 0.5,None
        icon: "play"
        font_size: "20"
        theme_text_color: "Custom"
        text_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
        on_press: root.manager.current = 'game'
        on_press: root.manager.transition.direction = 'left'
    MDRectangleFlatButton:
        text: "Add words"
        pos_hint: {'center_x':0.5,'center_y':0.4}
        font_size: "12"
        on_press: root.manager.current = 'add_word'
        on_press: root.manager.transition.direction = 'left'
        size_hint: 0.5,None
    MDRectangleFlatButton:
        text: "Remove words"
        pos_hint: {'center_x':0.5,'center_y':0.3}
        font_size: "12"
        on_press: root.manager.current = 'remove_word'
        on_press: root.manager.transition.direction = 'left'
        on_release: root.press_action(self)
        size_hint: 0.5,None
        
        
<GameScreen>
    name: 'game'
    id: game
    MDRectangleFlatButton:
        text: 'End game'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        size_hint: 0.9, None
        on_press: root.end_game_dialog(self)
    MDRectangleFlatButton:
        text: app.word
        pos_hint: {'center_x':0.5,'center_y':0.9}
        size_hint: 0.9, None
    MDRectangleFlatButton:
        id: translation
        name: 'translation'
        text: app.blurr_translation
        pos_hint: {'center_x':0.5,'center_y':0.8}
        size_hint: 0.9, None
    MDTextField:
        id: user_translation
        hint_text: "Enter your translation"
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: 0.9, None
        halign: 'center'
        mode: "rectangle"
    MDFillRoundFlatButton:
        id: check_btn
        font_size: "20"
        theme_text_color: "Custom"
        text_color: "black"
        text: "CHECK"
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: 0.9, None
        on_press: app.save_user_translation(self)
        on_release: root.check_action(self)
        
<AddScreen>
    name: 'add_word'
    id: add
    MDTextField:
        id: text_field1
        hint_text: "Enter english word"
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: 0.9, None
        mode: "rectangle"
    MDTextField:
        id: text_field2
        hint_text: "Enter polish word"
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: 0.9, None
        mode: "rectangle"
    MDRectangleFlatButton:
        text: 'Add'
        pos_hint: {'center_x':0.75,'center_y':0.1}
        size_hint: 0.4, None
        on_press: root.add_btn_action(self)
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.25,'center_y':0.1}
        size_hint: 0.4, None
        on_press: root.manager.current = 'menu'
        on_press: root.manager.transition.direction = 'right'
        
        
<RemoveScreen>
    name: 'remove_word'
    id: remove
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.25,'center_y':0.1}
        size_hint: 0.4, None
        on_press: root.manager.current = 'menu'
        on_press: root.manager.transition.direction = 'right'
    MDRectangleFlatButton:
        text: 'Remove'
        pos_hint: {'center_x':0.75,'center_y':0.1}
        size_hint: 0.4, None
        on_press: root.remove_btn_action(self)
"""


class MenuScreen(Screen):
    pass


class GameScreen(Screen):

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
        self.manager.transition.direction = "right"
        self.dialog.dismiss()

    def check_action(self, obj):
        self.ids.translation.text = WordsApp.translation
        self.ids.translation.size_hint = (0.9, None)

        self.remove_widget(self.ids.check_btn)

        self.correct_btn = MDRectangleFlatButton(
            id="correct_btn",
            text="Correct",
            pos_hint={'center_x': 0.75, 'center_y': 0.6},
            size_hint=(0.4, None),
            text_color="green",
            line_color="green",
            on_release=self.correct_action
        )

        self.incorrect_btn = MDRectangleFlatButton(
            id="incorrect_btn",
            text="Incorrect",
            pos_hint={'center_x': 0.25, 'center_y': 0.6},
            size_hint=(0.4, None),
            text_color="red",
            line_color="red",
            on_release=self.incorrect_action
        )

        self.add_widget(self.correct_btn)
        self.add_widget(self.incorrect_btn)

    def correct_action(self, obj):
        self.ids.user_translation.text = ''
        self.ids.translation.text = WordsApp.blurr_translation

        self.remove_widget(self.correct_btn)
        self.remove_widget(self.incorrect_btn)

        self.add_widget(self.ids.check_btn)
        pass

    def incorrect_action(self, obj):
        self.ids.user_translation.text = ''
        self.ids.translation.text = WordsApp.blurr_translation

        self.remove_widget(self.correct_btn)
        self.remove_widget(self.incorrect_btn)

        self.add_widget(self.ids.check_btn)
        pass

    pass


class AddScreen(Screen):
    def add_btn_action(self, obj):
        self.dialog = MDDialog(title='Translation added !',
                               text=f"{self.ids.text_field1.text} - {self.ids.text_field2.text}",
                               buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)]
                               )
        self.dialog.open()
        self.ids.text_field1.text = ""
        self.ids.text_field2.text = ""

    def close_dialog(self, obj):
        self.dialog.dismiss()

    pass


class RemoveScreen(Screen):
    def remove_btn_action(self, obj):
        self.dialog = MDDialog(title='Translation deleted !',
                               text="eng_word - pol_word",
                               buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)]
                               )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    pass


sm = ScreenManager()
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(GameScreen(name="game"))
sm.add_widget(AddScreen(name="add_word"))
sm.add_widget(RemoveScreen(name="remove_word"))

WordsApp().run()
