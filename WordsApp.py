from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.core.window import Window
import pandas as pd
import random
import streamlit as st
from streamlit_gsheets import GSheetsConnection

Window.size = (400, 800)


class WordsApp(MDApp):
    conn = st.connection('gsheets', type=GSheetsConnection)
    data = conn.read(worksheet="dictionary")
    df = pd.DataFrame(data)
    percent_of_words = 0.2
    idx = random.randint(0, int(round(df.shape[0] * percent_of_words)))
    word = df.ENG[idx]
    blurr_translation = "? ? ? ? ? ? ? ?"
    translation = df.POL[idx]

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.root = Builder.load_string(screen_helper)
        return self.root


screen_helper = """

ScreenManager:
    MenuScreen:
    GameScreen:
    SettingsScreen:
    
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
        text: "Settings"
        pos_hint: {'center_x':0.5,'center_y':0.4}
        on_press: root.manager.current = 'settings'
        on_press: root.manager.transition.direction = 'left'
        size_hint: 0.5,None
        
<GameScreen>
    name: 'game'
    id: game
    MDRectangleFlatButton:
        text: 'End game and save progress'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        size_hint: 0.9, None
        on_press: root.end_game_dialog(self)
    MDRectangleFlatButton:
        id: word
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
        hint_text: "Enter your answer"
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: 0.9, None
        halign: 'center'
        mode: "rectangle"
        focus:True
    MDFillRoundFlatButton:
        id: check_btn
        font_size: "20"
        theme_text_color: "Custom"
        text_color: "black"
        text: "CHECK"
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: 0.9, None
        on_release: root.check_action(self)
        
<SettingsScreen>
    name: 'settings'
    id: settings
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        size_hint: 0.9, None
        on_press: root.manager.current = 'menu'
        on_press: root.manager.transition.direction = 'right'
    MDRectangleFlatButton:
        text: 'darkmode or smth'
        pos_hint: {'center_x':0.5,'center_y':0.9}
        size_hint: 0.9, None
        on_press: root.manager.current = 'menu'
        on_press: root.manager.transition.direction = 'right'
    MDRectangleFlatButton:
        text: 'setting2'
        pos_hint: {'center_x':0.5,'center_y':0.8}
        size_hint: 0.9, None
        on_press: root.manager.current = 'menu'
        on_press: root.manager.transition.direction = 'right'
        
"""


class MenuScreen(Screen):
    pass


class GameScreen(Screen):

    def end_game_dialog(self, obj):
        self.dialog = MDDialog(title='Are you sure ?',
                               buttons=[MDFlatButton(text="Yes, end game", on_release=self.menu_switch_and_save),
                                        MDFlatButton(text='Cancel', on_release=self.close_dialog)]
                               )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def menu_switch_and_save(self, obj):
        self.normalize_weights()
        WordsApp.conn.update(worksheet='dictionary', data=WordsApp.df)
        # WordsApp.df.to_csv("dictionary.csv")
        self.manager.current = 'menu'
        self.manager.transition.direction = "right"
        self.dialog.dismiss()

    def sort_weights(self):
        WordsApp.df = WordsApp.df.sort_values(by="weights").reset_index(drop=True)

    def normalize_weights(self):
        WordsApp.df.weights = (WordsApp.df.weights - WordsApp.df.weights.min() + 0.2) \
                              / (WordsApp.df.weights.max() - WordsApp.df.weights.min())

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

        yes_rate = 1.3
        WordsApp.df.weights[WordsApp.idx] *= yes_rate

        self.sort_weights()
        self.new_word()

        self.add_widget(self.ids.check_btn)
        pass

    def incorrect_action(self, obj):
        self.ids.user_translation.text = ''
        self.ids.translation.text = WordsApp.blurr_translation

        self.remove_widget(self.correct_btn)
        self.remove_widget(self.incorrect_btn)

        no_rate = 1.3
        WordsApp.df.weights[WordsApp.idx] *= no_rate

        self.sort_weights()
        self.new_word()

        self.add_widget(self.ids.check_btn)
        pass

    def new_word(self):
        percent_of_words = 0.2
        WordsApp.idx = random.randint(0, int(round(WordsApp.df.shape[0] * percent_of_words)))

        if random.randint(0, 1) == 0:
            WordsApp.translation = WordsApp.df.POL[WordsApp.idx]
            self.ids.word.text = WordsApp.df.ENG[WordsApp.idx]
        else:
            WordsApp.translation = WordsApp.df.ENG[WordsApp.idx]
            self.ids.word.text = WordsApp.df.POL[WordsApp.idx]
        self.ids.translation.text = WordsApp.blurr_translation

    pass


class SettingsScreen(Screen):

    pass


WordsApp().run()
