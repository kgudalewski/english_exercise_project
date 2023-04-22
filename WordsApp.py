from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window
import pandas as pd
import random

Window.size = (400, 800)


class WordsApp(MDApp):
    df = pd.read_csv("dictionary.csv", index_col=0)
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
        on_press: root.remove_words_action(self)
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
        on_press: root.back_action(self)
    MDRectangleFlatButton:
        text: 'Remove'
        pos_hint: {'center_x':0.75,'center_y':0.1}
        size_hint: 0.4, None
        on_press: root.remove_btn_action(self)
"""


class MenuScreen(Screen):
    remove_list = []

    def remove_words_action(self, obj):
        self.table = MDDataTable(
            check=True,
            pos_hint={"center_y": 0.575, "center_x": 0.5},
            size_hint=(0.9, 0.8),
            rows_num=WordsApp.df.shape[0] + 1,
            column_data=[
                ("ENG", 35),
                ("POL", 30)
            ],
            row_data=list(zip(WordsApp.df.ENG, WordsApp.df.POL))

        )
        self.table.bind(on_check_press=self.create_list)

        self.manager.get_screen(name="remove_word").add_widget(self.table)

    def create_list(self, obj, current_row):
        idx = WordsApp.df.loc[WordsApp.df.ENG == current_row[0]].index[0]
        if idx not in self.remove_list:
            self.remove_list.append(idx)
        else:
            self.remove_list.remove(idx)
        print(self.remove_list)

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
        WordsApp.df.to_csv("dictionary.csv")
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


class AddScreen(Screen):
    def add_btn_action(self, obj):
        weight = WordsApp.df.weights.min()
        new_row = {"ENG": self.ids.text_field1.text, "POL": self.ids.text_field2.text, "weights": weight}
        WordsApp.df = WordsApp.df.append(new_row, ignore_index=True)
        self.sort_weights()
        self.normalize_weights()
        WordsApp.df.to_csv("dictionary.csv")
        self.dialog = MDDialog(title='Translation added !',
                               text=f"{self.ids.text_field1.text} - {self.ids.text_field2.text}",
                               buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)]
                               )
        self.dialog.open()
        self.ids.text_field1.text = ""
        self.ids.text_field2.text = ""

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def sort_weights(self):
        WordsApp.df = WordsApp.df.sort_values(by="weights").reset_index(drop=True)

    def normalize_weights(self):
        WordsApp.df.weights = (WordsApp.df.weights - WordsApp.df.weights.min() + 0.2) \
                              / (WordsApp.df.weights.max() - WordsApp.df.weights.min())

    pass


class RemoveScreen(Screen):

    def remove_btn_action(self, obj):

        #deleting
        WordsApp.df = WordsApp.df.drop(index=self.manager.get_screen(name="menu").remove_list)

        WordsApp.df.to_csv("dictionary.csv")

        self.dialog = MDDialog(title='Translations deleted !',
                               buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)]
                               )
        self.manager.current = 'menu'
        self.manager.transition.direction = 'right'
        self.manager.get_screen(name='menu').remove_list = []
        self.dialog.open()


    def close_dialog(self, obj):
        self.dialog.dismiss()

    def back_action(self, obj):
        self.manager.get_screen(name='menu').remove_list = []


WordsApp().run()
