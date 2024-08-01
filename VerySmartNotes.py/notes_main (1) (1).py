# Імпортуємо всі потрібні нам віджети з бібліотеки PyQt5.QtWidgets
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLabel,QListWidget,QLineEdit,QTextEdit,QVBoxLayout,QHBoxLayout, QInputDialog       
from PyQt5 import QtGui
# Імпортуємо Джисон бібліотеку
import json

from tkinter import *
from tkinter import ttk

# Cтворюємо вікно додатка та змінну notes + відкриваємо її та кидаємо до notes_data.json 
app = QApplication([])
app.setWindowIcon(QtGui.QIcon('image.png'))

notes = {
  "Список покупок" :{
    "текст" : "Купити рибу, курку і вино",
    "теги" : ["покупки","продукти"]
  },
  "Канікули" :{
    "текст" : "Я буду сидіти з дітьми(",
    "теги" : ["депресія","літо"]
  },

}
with open("notes_data.json", "w") as file:
    json.dump(notes, file)

style = ttk.Style()
#створення вікна notes_window
notes_window = QWidget()
notes_window.setWindowTitle("Poзумні замітки")
notes_window.resize(900,600)
notes_window.setWindowIcon(QtGui.QIcon('image.png'))
#створення всіх кнопок, віджетів та вікон програми
list_label = QLabel("Список заміток")
list_label.setStyleSheet('background: rgb(255, 128, 0); color: rgb(255, 255, 255);')
list_notes = QListWidget()
btn_create = QPushButton("Cтворити замітку")
btn_del = QPushButton("Видалити замітку")
btn_save = QPushButton("Зберегти замітку")

text_field = QTextEdit()

tags_label = QLabel("Список тегів")
tags_label.setStyleSheet('background: rgb(255, 128, 0); color: rgb(255, 255, 255);')
tags_list = QListWidget()
tag_field = QLineEdit()
tag_field.setPlaceholderText("Введіть тег...")
btn_tag_add = QPushButton("Додати до замітки")
btn_tag_del = QPushButton("Відкріпити від замітки")
btn_tag_search = QPushButton("Шукати замітку по тегу")




# Створюємо лінії та приєднюємо їх до кнопок
col_1 = QVBoxLayout()
col_1.addWidget(text_field)
col_2 = QVBoxLayout()
col_2.addWidget(list_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(btn_create)
row_1.addWidget(btn_del)
col_2.addLayout(row_1)
col_2.addWidget(btn_save)
col_2.addWidget(tags_label)
col_2.addWidget(tags_list)
col_2.addWidget(tag_field)

row_2= QHBoxLayout()
row_2.addWidget(btn_tag_add)
row_2.addWidget(btn_tag_del)

col_2.addLayout(row_2)
col_2.addWidget(btn_tag_search)

layout_notes = QHBoxLayout()
layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)
notes_window.setLayout(layout_notes)




# Створюємо функції зв`язані з нотатками (показати, додати, видалити та зберегти нотатку)
def show_note():
    name = list_notes.selectedItems()[0].text()
    text_field.setText(notes[name]["текст"])
    tags_list.clear()
    tags_list.addItems(notes[name]["теги"])

def add_note():
    note_name, ok =QInputDialog.getText(notes_window, "Додати заміту", "Введіть замітку:")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)

def del_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        list_notes.clear()
        text_field.clear()
        list_notes.addItems(notes)
    else:
        print("Замітка для видалення не обрана")
        
def save_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]["текст"] = text_field.toPlainText () 
        with open("notes_data.json", "w") as file:
          json.dump(notes, file)
    else:
        print("Замітка не обрана!!!!!")

# Створюємо функції зв`язані з тегами (додати, видалити та знайти тег)
def add_tag():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = tag_field.text()
        notes[name]["теги"].append(tag)
        tag_field.clear()
        tags_list.addItem(tag)
        with open("notes_data.json", "w") as file:
          json.dump(notes, file)
    else:
        print("Замітка не обрана!!!!!")

def del_tag():
        if tags_list.selectedItems():
            name = list_notes.selectedItems()[0].text()
            tag = tags_list.selectedItems()[0].text()
            notes[name]["теги"].remove(tag)
            tags_list.clear()
            tags_list.addItems(notes[name]["теги"])
            with open("notes_data.json", "w") as file:
                json.dump(notes, file)
        else:
            print("Тег не обрали!!!!")
def search_tag():
    tag = tag_field.text()
    if btn_tag_search.text() == "Шукати замітку по тегу" and tag:
        notes_filtered = {} # тут будуть замітки з виділеним тегом
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        btn_tag_search.setText("Скинути пошук")
        list_notes.clear()
        tags_list.clear()
        list_notes.addItems(notes_filtered)
    elif btn_tag_search.text() == "Скинути пошук":
        tag_field.clear()
        list_notes.clear()
        tags_list.clear()
        list_notes.addItems(notes)
        btn_tag_search.setText("Шукати замітку по тегу")
    else:
        pass




# З`єднюємо кнопки з нашими функціями
list_notes.itemClicked.connect(show_note)
btn_del.clicked.connect(del_note)
btn_create.clicked.connect(add_note)
btn_save.clicked.connect(save_note)
btn_tag_add.clicked.connect(add_tag)
btn_tag_del.clicked.connect(del_tag)
btn_tag_search.clicked.connect(search_tag)


# Відкриваємо Джисон файл для читання
with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)




# Відкриваємо програму та запускаємо її, готово!
notes_window.show()
app.exec()