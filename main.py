import os
from datetime import datetime
import json
from tkinter import *
from tkinter import Button, Label, Text, Scrollbar
from tkinter import messagebox
from tkinter import simpledialog


def get_notes_file_path():
    """Получение пути к файлу с заметками"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "notes.json")


def load_notes():
    """Загрузка заметок из файла"""
    notes_file = get_notes_file_path()
    
    if not os.path.exists(notes_file):
        return []
    
    try:
        with open(notes_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить заметки: {e}")
        return []


def save_notes(notes_list):
    """Сохранение заметок в файл"""
    notes_file = get_notes_file_path()
    
    try:
        with open(notes_file, "w", encoding="utf-8") as f:
            json.dump(notes_list, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить заметки: {e}")
        return False


def new_note():
    '''Очищение текстового поля'''
    text_fild.insert('end', '\n\nДобавленный текст по кнопке!')
    text_fild.delete("1.0", END)


def save_note():
    '''Сохранение заметок'''
    content = text_fild.get("1.0", END).strip()

    if not content:
        messagebox.showwarning("Внимание", "Оставь на стене хоть одно слово, чтоб знали — мы здесь были!")
        return

    # Подготовка данных
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    note_data = {
        "date": date_str,
        "text": content
    }

    notes_list = load_notes()
    notes_list.append(note_data)
    
    if save_notes(notes_list):
        messagebox.showinfo("Готово", "Я задержусь на этой земле, сколько смогу и успею!")
    else:
        messagebox.showerror("Ошибка", "Не удалось сохранить заметку")


def show_notes():
    '''Показ заметок'''
    notes_list = load_notes()
    
    if not notes_list:
        messagebox.showinfo("Информация", "Мой внутренний мир — это белый шум, это пустой экран.")
        return
    
    text_fild.delete("1.0", END)
    
    for i, note in enumerate(notes_list, 1):
        text_fild.insert(END, f"{i}. {note['date']}\n")
        text_fild.insert(END, f"{note['text']}\n")
        text_fild.insert(END, "-" * 20 + "\n")


def delete_note():
    '''Удаление заметок по номеру'''
    notes_list = load_notes()
    
    if not notes_list:
        messagebox.showinfo("Информация", "И не останется даже пыли, и не останется даже тени...")
        return

    # Очищение текстовое поле
    text_fild.delete("1.0", END)

    text_fild.insert(END, "СПИСОК ЗАМЕТОК ДЛЯ УДАЛЕНИЯ\n\n")
    # Вывод всех заметки с нумерацией
    for i, note in enumerate(notes_list, 1):
        text_fild.insert(END, f"{i}. {note['date']}\n")
        text_fild.insert(END, f"{note['text'][:100]}{'...' if len(note['text']) > 100 else ''}\n")
        text_fild.insert(END, "-" * 20 + "\n\n")

    # Запрашивание номера заметки для удаления
    note_number = simpledialog.askinteger(
        "Удаление заметки",
        f"Введите номер заметки для удаления (1-{len(notes_list)}):",
        minvalue=1,
        maxvalue=len(notes_list)
    )

    if note_number is None:  # Если пользователь нажал "Отмена"
        return

    # Подтверждение удаления
    note_to_delete = notes_list[note_number - 1]
    confirm = messagebox.askyesno(
        "Подтверждение",
        f"Вы уверены, что хотите удалить заметку №{note_number}?\n"
        f"Дата: {note_to_delete['date']}\n"
        f"Текст: {note_to_delete['text'][:50]}..."
    )

    if not confirm:
        return

    # Удаление заметку из списка
    notes_list.pop(note_number - 1)

    # Сохранение обновленный список
    if save_notes(notes_list):
        # Очищение текстовое поле и вывод результата
        text_fild.delete("1.0", END)
        text_fild.insert(END, f"Заметка №{note_number} успешно удалена!\n")

        if notes_list:
            text_fild.insert(END, "Оставшиеся заметки:\n")
            for i, note in enumerate(notes_list, 1):
                text_fild.insert(END, f"{i}. {note['date']}\n")
                text_fild.insert(END, f"{note['text'][:50]}...\n")
                text_fild.insert(END, "-" * 30 + "\n")
        else:
            text_fild.insert(END, "Больше нет сохранённых заметок.\n")
        
        messagebox.showinfo("Успех", "Я исчезну, и не будет боли.")


# Основное окно
root = Tk()
root.title('Мои заметки')
root.geometry('300x500')

root.iconbitmap('icon/-romb.ico')


# Верхний фрейм с кнопками
frame_top = Frame(root)
frame_top.pack(pady=10, padx=10)


# Кнопка "Новая заметка"
image_1 = PhotoImage(file="./icon/page.png")
button_new = Button(frame_top, image=image_1, padx=20, pady=10, command=new_note)
button_new.image = image_1
button_new.pack(side=LEFT, padx=5)

# Кнопка "Сохранить"
image_2 = PhotoImage(file="./icon/cabinet.png")
button_save = Button(frame_top, image=image_2, padx=20, pady=10, command=save_note)
button_save.image = image_2
button_save.pack(side=LEFT, padx=5)

# Кнопка "Показать"
image_3 = PhotoImage(file="./icon/openbook.png")
button_show = Button(frame_top, image=image_3, padx=20, pady=10, command=show_notes)
button_show.image = image_3
button_show.pack(side=LEFT, padx=5)

# Кнопка "Удалить"
image_4 = PhotoImage(file="./icon/delete.png")
button_delete = Button(frame_top, image=image_4, padx=20, pady=10, command=delete_note)
button_delete.image = image_4
button_delete.pack(side=LEFT, padx=5)


# Разделитель
frame_bottom = Frame(root)
frame_bottom.pack(pady=10)

image = PhotoImage(file="./icon/razdelitel.png")
separator = Label(frame_bottom, image=image)
separator.pack()
separator.image = image
separator.pack()


# Текстовое поле
f_text = Frame(root)
f_text.pack(fill="both", expand=1)

text_fild = Text(f_text, bg='Lavender',
                 fg='black',
                 font=('Times New Roman', 12),
                 padx=10,
                 pady=10,
                 wrap=WORD,
                 insertbackground='SlateGrey',
                 selectbackground='SlateGrey',
                 spacing3=10,
                 width=30,
                 )
text_fild.pack(expand=1, fill="both", side=LEFT) 

# Это безумно мило! Спасибо огромное за поздравление! Я тоже поздравляю тебя с праздником! =^.^=
# Оформление кода очень красивое! Функционал тоже классный! Желаю успехов в разработке!

initial_text = '''С наступающим новым годом! 
Пусть следующий год каждому из нас
принесет благополучие и успех, подарит новые
блестящие идеи и поможет их воплотить в жизнь.
Пусть в наших семьях царит мир и взаимопонимание,
а любовь близких людей неизменным горячим пламенем
будет согревать в любую минуту.'''


text_fild.insert('1.0', initial_text)

scroll = Scrollbar(f_text, command=text_fild.yview)
scroll.pack(side="right", fill="y")
text_fild.config(yscrollcommand=scroll.set)

root.mainloop()
