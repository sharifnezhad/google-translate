import io
import random
from functools import partial
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *
def database():
    try:
        myfile = io.open('database.txt', mode="r", encoding="utf-8")
    except:
        print('file not find ://')
        exit()
    words = myfile.read()
    myfile.close()
    words_list = words.split('\n')
    WORDS = []
    for i in range(len(words_list)):
        word = words_list[i].split(',')
        mydic = {}
        WORDS.append({'en': word[0], 'pr': word[1]})
    return WORDS

class Main_window(QMainWindow):
    def __init__(self,word_list):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('menu.ui',None)
        self.ui.show()
        self.ui.btn_add.clicked.connect(self.add_new_word)
        self.ui.btn_entope.clicked.connect(self.english_to_persion)
        self.ui.btn_petoen.clicked.connect(self.persion_to_english)
        self.ui.btn_exit.clicked.connect(self.exit_and_save)
        self.database=word_list

    def add_new_word(self):
        self.ui=Add_new_word(self.database)
    def english_to_persion(self):
        self.ui=English_to_persin(self.database)
    def persion_to_english(self):
        self.ui=Persion_to_english(self.database)
    def exit_and_save(self):
        my_file = io.open('database.txt', mode="w", encoding="utf-8")
        for i in range(len(self.database)):
            if i != len(self.database) - 1:
                my_file.write(
                    str(self.database[i]['en']) + ',' + self.database[i]['pr'] + '\n')
            else:
                my_file.write(
                    str(self.database[i]['en']) + ',' + self.database[i]['pr'])
        my_file.close()
        exit()
class Add_new_word(QWidget):
    def __init__(self,word_list):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('addNewWord.ui',None)
        self.ui.show()
        self.word_list=word_list
        self.ui.btn_back.clicked.connect(self.back)
        self.ui.btn_save.clicked.connect(self.save_words)

    def back(self):
        self.ui=Main_window(self.word_list)
    def save_words(self):
        found=False
        text=self.ui.text_english.toPlainText()
        for i in self.word_list:
            if text==i['en']:
                found=True
                break
        if found==True:
            self.ui.message.setText('This word is in the dictionary')
            self.ui.message.setStyleSheet('color:red')
        else:
            text_pr=self.ui.text_persian.toPlainText()
            self.word_list.append({'en':text,'pr':text_pr})
            self.ui.message.setText('The word was successfully registered')
            self.ui.message.setStyleSheet('color:#2ecc71')
class English_to_persin(QWidget):
    def __init__(self,word_list):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('englishToPersian.ui',None)
        self.ui.show()
        self.ui.btn_back.clicked.connect(self.back)
        self.ui.btn_translate.clicked.connect(self.translate)
        self.word_list=word_list
    def back(self):
        self.ui=Main_window(self.word_list)
    def translate(self):
        sentence=self.ui.text_english.toPlainText()
        verb=[]
        
        if '. ' in sentence:
            sentence = sentence.split('. ')
            for i in range(len(sentence)):
                verb.append(sentence[i].split(' '))
        else:
            verb.append(sentence.split(' '))
        word_str = []
        str_words = ' '
        for i in range(len(verb)):
            for k in range(len(verb[i])):
                for j in range(len(self.word_list)):
                    if verb[i][k]==verb[i][k].capitalize():
                        verb[i][j]=verb[i][k].lower()
                    if verb[i][k] == self.word_list[j]['en']:
                        word_str.append(self.word_list[j]['pr'])
                        break
                    elif j==len(self.word_list)-1 and verb[i][k] != self.word_list[j]['en']:
                        word_str.append(verb[i][k])
                        break
            word_str.append('.')
        self.ui.text_persian.setText(str_words.join(word_str))
class Persion_to_english(QWidget):
    def __init__(self, word_list):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('persianToEnglish.ui',None)
        self.ui.show()
        self.ui.btn_back.clicked.connect(self.back)
        self.ui.btn_translate.clicked.connect(self.translate)
        self.word_list=word_list


    def back(self):
        self.ui=Main_window(self.word_list)
    def translate(self):
        sentence=self.ui.text_persian.toPlainText()
        verb=[]
        if '. ' in sentence:
            sentence = sentence.split('. ')
            for i in range(len(sentence)):
                verb.append(sentence[i].split(' '))
        else:
            verb.append(sentence.split(' '))
        word_str = []
        str_words = ' '
        for i in range(len(verb)):
            for k in range(len(verb[i])):
                for j in range(len(self.word_list)):

                    if verb[i][k] == self.word_list[j]['pr']:
                        word_str.append(self.word_list[j]['en'])
                        break
                    elif j==len(self.word_list)-1 and verb[i][k] != self.word_list[j]['pr']:
                        word_str.append(verb[i][k])
                        break



            word_str.append('.')
        self.ui.text_english.setText(str_words.join(word_str))

app=QApplication()
window=Main_window(database())
app.exec()