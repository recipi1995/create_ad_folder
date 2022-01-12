import tkinter as tk
import schedule
import time
from tkinter.ttk import *
import configparser
import subprocess
import os
import random
import tkinter.messagebox as mb
from sh_task import create_folder
#########################################################################<Интерфейс программы>###############################################################################

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# create the application
myapp = App()

# Создается новое окно с заголовком "DNS имя сервера AD:"
myapp.master.title("Создание папок для пользователей")
myapp.master.maxsize(1000, 400)
def createConfig(dns_name,login_name,password,scheme,full_path,folder):
    """
    Create a config file
    """
    path = "settings.ini"
    a = dns_name
    b = login_name
    c = password
    d = scheme
    e = full_path
    f = folder
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "dns_name", a)
    config.set("Settings", "login_name", b)
    config.set("Settings", "password", c)
    config.set("Settings", "scheme", d)
    config.set("Settings", "full_path", e)
    config.set("Settings", "folder", f)
    
    with open(path, "w") as config_file:
        config.write(config_file)

def start_task():
    print("run task")
    dns_name = ent_dns_name.get()
    login_name = ent_login_name.get()
    password = ent_password.get()
    scheme = ent_scheme.get()
    full_path = ent_full_path.get()
    folder = ent_folder.get()
    createConfig(dns_name,login_name,password,scheme,full_path,folder)
    myapp.master.destroy()
    create_folder()
    #create_folder(dns_name,login_name,password,scheme,full_path,folder)
    #print(dns_name, login_name,password,scheme,full_path,folder)


def reset():
    print('удалить')
    schedule.clear('daily-tasks')
    myapp.master.destroy()

def schedule_task():
    min_hor = int(n_text.get())
    date = t_text.get()
    choice = var.get()
    dns_name = ent_dns_name.get()
    login_name = ent_login_name.get()
    password = ent_password.get()
    scheme = ent_scheme.get()
    full_path = ent_full_path.get()
    folder = ent_folder.get()
    createConfig(dns_name,login_name,password,scheme,full_path,folder)
    task_name = f'"Create user folder{random.randint(1,999)}{random.randint(1,999)}"'
    get_path = os.getcwd()
    path_py = f"{get_path}\sh_task.py"
    script = f"@echo off\n{get_path}\env\Scripts\python.exe {path_py}"
    a = r'\run.bat'
    with open("run.bat", "w") as file:
        file.write(script)
        file.close()
    path = f"{get_path}{a}"

    if choice == 1:
        print(f'SCHTASKS /Create /SC MINUTE /MO {min_hor} /TN {task_name} /tr {path} /ST {date} /RU  {login_name} /RP {password} ')
        myapp.master.destroy()
        command = subprocess.run(f'SCHTASKS /Create /SC MINUTE /MO {min_hor} /TN {task_name} /tr {path} /ST {date} /RU  {login_name} /RP {password} ', shell=True, check=True)
        command = subprocess.run("exit()")
    elif choice == 2:
        myapp.master.destroy()
        command = subprocess.run(f'SCHTASKS /Create /SC HOURLY /MO {min_hor} /TN {task_name} /tr {path} /ST {date}  /RU  {login_name} /RP {password} ', shell=True, check=True)
        command = subprocess.run("exit()")
    elif choice == 3:
        myapp.master.destroy()
        command = subprocess.run(f'SCHTASKS /Create /SC DAILY /TN {task_name} /tr {path} /ST {date}  /RU  {login_name} /RP {password} ', shell=True, check=True)
        command = subprocess.run("exit()")
    else:
        msg = "Не указан режим работы расписания"
        mb.showinfo("Информация", msg)
        myapp.master.destroy()
# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
    while True:
        schedule.run_pending()
        time.sleep(1)

# Создается новая рамка `frm_form` для ярлыков с текстом и
# Однострочных полей для ввода информации об адресе.
frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# Помещает рамку в окно приложения.
frm_form.pack()

frm_form2 = tk.Frame(relief=tk.SUNKEN, borderwidth=1)
# Помещает рамку в окно приложения.
frm_form2.pack()
 
# Создает ярлык и текстовок поле для ввода Пользователь (логин) в AD:.
lbl_dns_name = tk.Label(master=frm_form, text="DNS имя сервера AD:")
ent_dns_name = tk.Entry(master=frm_form, width=50)
ent_dns_name.insert(0, "pcnttdc1a")
# Использует менеджер геометрии grid для размещения ярлыка и
# однострочного поля для ввода текста в первый и второй столбец
# первой строки сетки.
lbl_dns_name.grid(row=0, column=0, sticky="e")
ent_dns_name.grid(row=0, column=1)

# Создает ярлык и текстовок поле для ввода Пользователь (логин) в AD:.
lbl_login_name = tk.Label(master=frm_form, text="Пользователь (логин) в AD:")
ent_login_name = tk.Entry(master=frm_form, width=50)
ent_login_name.insert(0, "centervospi\\romanov")
# Использует менеджер геометрии grid для размещения ярлыка и
# однострочного поля для ввода текста в первый и второй столбец
# первой строки сетки.
lbl_login_name.grid(row=1, column=0, sticky="e")
ent_login_name.grid(row=1, column=1)

# Создает ярлык и текстовок поле для ввода Пароль:.
lbl_password = tk.Label(master=frm_form, text="Пароль:")
ent_password = tk.Entry(master=frm_form, width=50)
ent_password.insert(0, "Gfhjkm1234")
# Размещает виджеты на вторую строку сетки
lbl_password.grid(row=2, column=0, sticky="e")
ent_password.grid(row=2, column=1)
 
# Создает ярлык и текстовок поле для ввода первого адреса.
lbl_scheme = tk.Label(master=frm_form, text="Схема AD:")
ent_scheme = tk.Entry(master=frm_form, width=50)
ent_scheme.insert(0, "dc=centervospi,dc=local")
# Размещает виджеты на третьей строке сетки.
lbl_scheme.grid(row=3, column=0, sticky="e")
ent_scheme.grid(row=3, column=1)
 
# Создает ярлык и текстовок поле для ввода второго адреса.
lbl_full_path = tk.Label(master=frm_form, text="Полный путь к создаваемой директории:")
ent_full_path = tk.Entry(master=frm_form, width=50)
ent_full_path.insert(0, "C:\\Users\\root3\\Desktop\\ad\\")
# Размещает виджеты на четвертой строке сетки.
lbl_full_path.grid(row=4, column=0, sticky=tk.E)
ent_full_path.grid(row=4, column=1)
 
# Создает ярлык и текстовок поле для ввода города.
lbl_folder = tk.Label(master=frm_form, text="Какие папки необходимо создать внутри директории:")
ent_folder = tk.Entry(master=frm_form, width=50)
ent_folder.insert(0, "Общие документы, Сканер, Отчеты")
# Размещает виджеты на пятой строке сетки.
lbl_folder.grid(row=5, column=0, sticky=tk.E)
ent_folder.grid(row=5, column=1)
var =tk.IntVar()
# Создает ярлык и текстовок поле для ввода города.
lbl_sheduller = tk.Label(master=frm_form2, text="Запуск по расписанию:")
# Размещает виджеты на пятой строке сетки.
rad1 = Radiobutton(master=frm_form2,text='Каждые n минут',variable=var, value=1)
rad2 = Radiobutton(master=frm_form2,text='Каждые n часов',variable=var, value=2)
rad3 = Radiobutton(master=frm_form2,text='Ежедневно в t часов',variable=var, value=3)
n = tk.Label(master=frm_form2, text="Минуты/Часы (n):")
t = tk.Label(master=frm_form2, text="Время начала:")
n_text = tk.Entry(master=frm_form2, width=10)
n_text.insert(0, "30")
t_text = tk.Entry(master=frm_form2, width=10)
t_text.insert(0, "14:00")
lbl_sheduller.grid(row=6, column=0, sticky=tk.E)
rad1.grid(row=6, column=1)
rad2.grid(row=6, column=2)
rad3.grid(row=6, column=3)
n.grid(row=8, column=0, sticky=tk.E)
t.grid(row=9, column=0, sticky=tk.E)
n_text.grid(row=8, column=1, sticky=tk.E)
t_text.grid(row=9, column=1, sticky=tk.E)

# Создает новую рамку `frm_buttons` для размещения
# кнопок "Отправить" и "Очистить". Данная рамка заполняет
# все окно в горизонтальном направлении с
# отступами в 5 пикселей горизонтально и вертикально.
frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
 
# Создает кнопку "Отправить" и размещает ее
# справа от рамки `frm_buttons`.

btn_insert = tk.Button(master=frm_buttons, text="Поставить в расписание", command=schedule_task)
btn_insert.pack(side=tk.RIGHT, ipadx=10)

btn_submit = tk.Button(master=frm_buttons, text="Запустить задачу", command=start_task)
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
 

# Запуск приложения.
if __name__ == "__main__":
    myapp.mainloop()
