import sqlite3
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox as mb
from tkcalendar import DateEntry
from dateutil.relativedelta import relativedelta
import re
from datetime import datetime, timedelta


def Autor():  # Информация об авторе
    about = Tk()
    about.title('Об авторе')
    labelAbout = Label(about,
                       text='Самсонова Юлия Евгеньевна 20-ИЭ-2\nВариант 36\nПС "Авиакомпания"\n\nЗадание:\nномер самолета, его тип, год выпуска, состояние (летает, в ремонте),\nколичество мест для каждого типа, дальность полета, крейсерская скорость,\nФИО служащего, его должность (пилот, инженер, стюардесса и т.д.),\nдата рождения, дата приема на работу, пол, дата рейса,\nсамолет, время рейса, город назначения, участники рейса.\n\nЗапросы: по ФИО служащего, по самолету, по рейсу.')
    labelAbout.grid(padx=10, pady=10)

def Help():  # Справка пользователя
    hel = Tk()
    hel.title('Справка')
    labelHelp = Label(hel,
                      text='Чтобы просмотреть кукую-либо таблицу, необходимо нажать на главном окне сверху кнопку,\nсоответствующую тематике таблицы.\nЧтобы задать какой-либо запрос, необходимо нажать на главном окне снизу\nсоответствующую кнопку.\n\nДля того чтобы добавить, изменить или удалить данные пользователю необходимо:\n1) войти в систему в качестве администратора, введя верный пароль;\n2) выбрать нужную таблицу и соответствующий пункт меню;\n3) ввести новые данные, изменить имеющиеся данные или удалить данные.')
    labelHelp.grid(padx=10, pady=10)

def is_valid(newval):  # Валидация введенного пароля
    return re.match("^\S{,6}$", newval) is not None

def loginAdmin():  # Вход в качестве администратора
    global entryPswdAdmin, admin
    admin = Toplevel(root)
    admin.title('Вход в качестве администратора')
    admin.resizable(0, 0)

    labelAdmin = Label(admin, text='Вход в режиме администратора', font=16)
    labelAdmin.grid(row=0, pady=10)

    labelPswd = Label(admin, text='Введите пароль:', font=13)
    labelPswd.grid(row=1, pady=10, padx=10)

    check = admin.register(is_valid)
    entryPswdAdmin = Entry(admin, show='*', font=14, validate="key", validatecommand=(check, "%P"))
    entryPswdAdmin.grid(row=2)

    buttonPswdAdmin = Button(admin, text='Войти', font=13, command=inputAdmin)
    buttonPswdAdmin.grid(row=3, pady=10, padx=10)

    admin.grab_set()

global table_frame1, plane_table1, pilots_table1, flights_table1, Admin, check, values, change_frame, change_frame1, change_frame2, hidef, hidef1, hidef2, hide2, hide1, hide, status
values = ()
check = 0
status = 0

def inputAdmin():  # Верный пароль администратора
    global Admin, plane_table1, pilots_table1, flights_table1, table_frame1, values, change_frame, change_frame1, change_frame2
    password = '123456'
    if entryPswdAdmin.get() != password:
        mb.showerror('Ошибка', 'Введён неверный пароль')
        entryPswdAdmin.delete(0, 'end')
    else:
        admin.destroy()
        Admin = Toplevel(root)
        Admin.geometry('900x500')
        Admin.title('Панель управления администратора')
        Admin.grab_set()
        btn_frame = LabelFrame(Admin, text='Выберете раздел', font=14, relief=FLAT)
        btn_frame.grid(row=1, column=1, sticky="w", padx=2, pady=4)

        table_frame1 = LabelFrame(Admin, height=230, width=840, relief=FLAT)
        table_frame1.grid(row=2, columnspan=2)
        table_frame1.grid_propagate(0)

        plane_table1 = ttk.Treeview(table_frame1, show='headings')
        pilots_table1 = ttk.Treeview(table_frame1, show='headings')
        flights_table1 = ttk.Treeview(table_frame1, show='headings')

        planes_btn = Button(btn_frame, text='Самолёты', font=14, command=planes1).grid(row=0, column=0, sticky="e")
        pilots_btn = Button(btn_frame, text='Сотрудники', font=14, command=pilots1).grid(row=0, column=1, sticky="e")
        flights_btn = Button(btn_frame, text='Рейсы', font=14, command=flights1).grid(row=0, column=2, sticky="w")

        btn_frame1 = LabelFrame(Admin, height=230, width=840, relief=FLAT)
        btn_frame1.grid(row=3, columnspan=2)
        btn_frame1.grid_propagate(0)

        btn1 = Button(btn_frame1, text='Изменить', font=14, command=change_info).grid(row=0, column=0, sticky="e")
        btn1 = Button(btn_frame1, text='Удалить', font=14, command=delete_info).grid(row=0, column=1, sticky="e")
        btn1 = Button(btn_frame1, text='Добавить', font=14, command=add_info).grid(row=0, column=2, sticky="w")
        Admin.protocol("WM_DELETE_WINDOW", on_closing)

def change_info():  # Изменение информации в табилицах
    global check, plane_table1, pilots_table1, flights_table1, values, on_select, new_selection, change_frame, change_frame1, change_frame2, hide2, hide1, hide, status
    if check == 0:
        mb.showerror('Внимание!', 'Вы не выбрали таблицу для изменения данных!')
    if check == 1:
        if values:
            change_frame = LabelFrame(Admin, relief=FLAT)  # Рамка Изменить статус
            change_frame.grid(row=3, columnspan=2)
            combo_state = ttk.Combobox(change_frame,
                                       values=[
                                           "В ремонте",
                                           "Используется"], state='readonly')
            combo_state.current(1)
            combo_state.grid(column=1, row=1)

            combo_type = ttk.Combobox(change_frame,
                                      values=["Пассажирский", "Грузовой"], state='readonly')
            combo_type.current(1)
            combo_type.grid(column=0, row=1)

            people = Entry(change_frame)
            people.grid(column=2, row=1, padx=10)
            people.insert(END, values[4])
            # Лейблы
            l1 = Label(change_frame, text='Тип')
            l1.grid(column=0, row=0)
            l2 = Label(change_frame, text='Статус')
            l2.grid(column=1, row=0)
            l6 = Label(change_frame, text='Кол-во пассажиров')
            l6.grid(column=2, row=0, padx=10)

            def apply(): # обновление измененных данных в таблице с самолетами
                global check, plane_table1, pilots_table1, flights_table1, values, on_select, new_selection, change_frame, change_frame1, change_frame2
                selection = combo_state.get()
                selection1 = combo_type.get()
                if people.get().isdigit():
                    strsam = """UPDATE planes SET planetype = ?, daterelease = ?, planestate = ?, planeseats = ?, planerange=?, planespeed=? WHERE planeid = ?"""
                    data = (selection1, values[2], selection, people.get(), values[5], values[6], values[0])
                    cur.execute(strsam, data)
                    conn.commit()
                    planes1()
                    values = ()

                    change_frame.grid_forget()

                else:
                    mb.showerror('Внимание!', 'Вы не корректно ввели кол-во мест')

            def hide(): # скрыть поле ввода обновления в таблице с самолетами
                change_frame.grid_forget()

            btn1 = Button(change_frame, text='Применить', font=14, command=apply).grid(row=0, column=3, sticky="e")
            btn1 = Button(change_frame, text='Скрыть', font=14, command=hide).grid(row=1, column=3, sticky="e")

        else:
            mb.showerror('Внимание!', 'Вы не выбрали данные для изменения!')

    if check == 2:
        if values:
            change_frame1 = LabelFrame(Admin, relief=FLAT)  # Рамка Изменить статус
            change_frame1.grid(row=3, columnspan=2)
            combo1 = ttk.Combobox(change_frame1,
                                  values=["Пилот","Стюардесса", "Инженер"], state='readonly')
            combo1.current(1)
            combo1.grid(column=1, row=1)

            fio = Entry(change_frame1)
            fio.grid(column=0, row=1, padx=10)
            fio.insert(END, values[1])
            # Лейблы
            l1 = Label(change_frame1, text='ФИО')
            l1.grid(column=0, row=0)
            l2 = Label(change_frame1, text='Должность')
            l2.grid(column=1, row=0)

            def apply1(): # скрыть поле ввода обновления в таблице с сотрудниками
                global check, plane_table1, pilots_table1, flights_table1, values, on_select, new_selection, change_frame, change_frame1, change_frame2
                if not (re.search('[0-9]', fio.get())):
                    selection = combo1.get()
                    strsam = """UPDATE pilots SET pilotname = ?, pilotpost = ?, datebirth = ?, employedate = ?, pilotgender=? WHERE pilotid = ?"""
                    data = (fio.get(), selection, values[3], values[4], values[5], values[0])
                    cur.execute(strsam, data)
                    conn.commit()
                    values = ()
                    pilots1()
                    change_frame1.grid_forget()

            def hide1():
                change_frame1.grid_forget()

            btn1 = Button(change_frame1, text='Применить', font=14, command=apply1).grid(row=0, column=2, sticky="e")
            btn1 = Button(change_frame1, text='Скрыть', font=14, command=hide1).grid(row=1, column=2, sticky="e", padx=10)
        else:
            mb.showerror('Внимание!', 'Вы не выбрали данные для изменения!')
    if check == 3:
        if values:
            post = 'Пилот'
            sql_select_query = """select * from pilots where pilotpost = ?"""
            cur.execute(sql_select_query, (post,))
            pilot_values = cur.fetchall()
            values2 = [tup[1] for tup in pilot_values]
            change_frame2 = LabelFrame(Admin, relief=FLAT)  # Рамка Изменить статус
            change_frame2.grid(row=3, columnspan=2)
            combo2 = ttk.Combobox(change_frame2, values=values2, state='readonly')
            combo2.current(1)
            combo2.grid(column=0, row=1)

            town = Entry(change_frame2)
            town.grid(column=1, row=1, padx=10)
            town.insert(END, values[5])

            time = Entry(change_frame2)
            time.grid(column=2, row=1, padx=10)
            time.insert(END, values[4])
            # Лейблы
            l1 = Label(change_frame2, text='Пилот')
            l1.grid(column=0, row=0)
            l2 = Label(change_frame2, text='Город')
            l2.grid(column=1, row=0)
            l6 = Label(change_frame2, text='Время полёта')
            l6.grid(column=2, row=0, padx=10)

            def apply2(): # обновление измененных данных в таблице с рейсами
                global check, plane_table1, pilots_table1, flights_table1, values, on_select, new_selection, change_frame, change_frame1, change_frame2
                selection = combo2.get()

                sql_select_query = """select * from pilots where pilotname = ?"""
                cur.execute(sql_select_query, (selection,))
                records = cur.fetchall()

                if time.get().isdigit() and not (re.search('[0-9]', town.get())):
                    strsam = """UPDATE flights SET planeid = ?, pilotid = ?, flightsdate = ?, flightstime = ?, town = ?, flightspeople=? WHERE flightsid = ?"""
                    data = (values[1], records[0][0], values[3], time.get(), town.get(), values[6], values[0])
                    cur.execute(strsam, data)
                    conn.commit()
                    values = ()
                    flights1()
                    change_frame2.grid_forget()

                else:
                    mb.showerror('Внимание!', 'Проверьте корректность введённых данных!')

            def hide2(): # скрыть поле ввода обновления в таблице с рейсами
                change_frame2.grid_forget()

            btn1 = Button(change_frame2, text='Применить', font=14, command=apply2).grid(row=0, column=3, sticky="e")
            btn1 = Button(change_frame2, text='Скрыть', font=14, command=hide2).grid(row=1, column=3, sticky="e",
                                                                                     padx=10)
        else:
            mb.showerror('Внимание!', 'Вы не выбрали данные для изменения!')

def add_info():  # ФУНКЦИЯ ДОБАВЛЕНИЯ ДАННЫХ. ДОБАВИТЬ ПОДПИСИ
    global check, plane_table1, pilots_table1, flights_table1, values, on_select, new_selection, change_frame, change_frame1, change_frame2, Admin, hidef, hidef1, hidef2, birth

    if check == 0:
        mb.showerror('Внимание!', 'Вы не выбрали таблицу для изменения данных!')
    if check == 1:

        add_frame = Frame(Admin)
        add_frame.grid(row=3, column=0, columnspan=2)
        # Открываем файл счётчик для чтения текущего значение из файла
        with open("plane_counter.txt", 'r') as f:
            file_counter = f.read().splitlines()
        file_counter = int(''.join(map(str, file_counter))) + 1
        # Открываем файл счётчик для записи данных в файл
        with open("plane_counter.txt", "w") as file:
            file.write(str(file_counter))
        combo_type = ttk.Combobox(add_frame, values=["Пассажирский", "Грузовой"], state='readonly')
        combo_type.current(1)
        combo_type.grid(column=0, row=1)

        date1 = DateEntry(add_frame, selectmode='day', date_pattern='dd-MM-yyyy', style='my.DateEntry', font=20, state='readonly')
        date1.grid(row=1, column=1)
        combo_state = ttk.Combobox(add_frame, values=["В ремонте", "Используется"], state='readonly')
        combo_state.current(1)
        combo_state.grid(column=2, row=1)
        seats = Entry(add_frame)
        seats.grid(row=1, column=3)
        range = Entry(add_frame)
        range.grid(row=1, column=4)
        speed = Entry(add_frame)
        speed.grid(row=1, column=5)
        # Лейблы
        l1 = Label(add_frame, text='Тип')
        l1.grid(row=0, column=0, padx=10)
        l2 = Label(add_frame, text='Дата выпуска')
        l2.grid(row=0, column=1, padx=10)
        l6 = Label(add_frame, text='Статус')
        l6.grid(column=2, row=0)
        l3 = Label(add_frame, text='Кол-во пассажиров')
        l3.grid(row=0, column=3, padx=10)
        l4 = Label(add_frame, text='Дальность')
        l4.grid(row=0, column=4, padx=10)
        l5 = Label(add_frame, text='Скорость')
        l5.grid(column=5, row=0, padx=10)

        def confirm(): # сохранение новой записи в таблице с самолетами
            global hidef, hidef1, hidef2
            if date1.get() != '' and seats.get() != '' and range.get() != '' and speed.get() != '' and seats.get().isdigit() and range.get().isdigit() and speed.get().isdigit():
                plane_list = (file_counter, combo_type.get(), date1.get(), combo_state.get(), seats.get(), range.get(), speed.get())
                cur.execute("INSERT INTO planes VALUES(?, ?, ?, ?, ?, ?, ?);", plane_list)
                conn.commit()
                date1.delete(0, END)
                seats.delete(0, END)
                range.delete(0, END)
                speed.delete(0, END)
                add_frame.grid_forget()
                planes1()
            else:
                mb.showerror('Внимание!', 'Вы заполнили не все поля\nПроверьте корректность данных!')

        def hidef(): # скрыть поле ввода добавления в таблицу с самолетами
            add_frame.grid_forget()

        hide_btn = Button(add_frame, text='Скрыть', command=hidef).grid(row=1, column=6)
        conf_btn = Button(add_frame, text='Выполнить', command=confirm).grid(row=0, column=6)

    if check == 2:
        add_frame1 = Frame(Admin)
        add_frame1.grid(row=3, column=0, columnspan=2)
        # Открываем файл счётчик для чтения текущего значение из файла
        with open("pilot_counter.txt", 'r') as f:
            file_counter = f.read().splitlines()
        file_counter = int(''.join(map(str, file_counter))) + 1
        # Открываем файл счётчик для записи данных в файл
        with open("pilot_counter.txt", "w") as file:
            file.write(str(file_counter))

        combo1 = ttk.Combobox(add_frame1,
                              values=[
                                  "Пилот",
                                  "Стюардесса", "Инженер"], state='readonly')
        combo1.current(1)
        combo1.grid(row=1, column=1, padx=10)
        pilot_name = Entry(add_frame1)
        pilot_name.grid(row=1, column=0, padx=10)
        combo_g = ttk.Combobox(add_frame1,
                               values=[
                                   "М",
                                   "Ж"], state='readonly')
        combo_g.current(1)
        combo_g.grid(column=5, row=1, padx=10)

        birth = DateEntry(add_frame1, selectmode='day', date_pattern='dd-MM-yyyy', style='my.DateEntry', font=20,
                          state='readonly')
        birth.grid(row=1, column=3, padx=20)
        # Даты

        emp_date = DateEntry(add_frame1, selectmode='day', date_pattern='dd-MM-yyyy', style='my.DateEntry', font=20,
                             state='readonly')
        emp_date.grid(row=1, column=4, padx=10)
        # Лейблы
        l1 = Label(add_frame1, text='ФИО')
        l1.grid(row=0, column=0, padx=10)
        l2 = Label(add_frame1, text='Должность')
        l2.grid(row=0, column=1, padx=10)
        l3 = Label(add_frame1, text='Дата рождения')
        l3.grid(row=0, column=3, padx=10)
        l4 = Label(add_frame1, text='Дата найма')
        l4.grid(row=0, column=4, padx=10)
        l5 = Label(add_frame1, text='Пол')
        l5.grid(column=5, row=0, padx=10)

        def confirm(): # сохранение новой записи в таблице с сотрудниками
            global birth

            current_datetime = datetime.now()
            birth = birth.get_date()
            user_age_check = relativedelta(current_datetime, birth)
            userage = birth.strftime("%d-%m-%Y")
            if pilot_name.get() != '' and not (re.search('[0-9]', pilot_name.get())):
                if user_age_check.years >= 18:
                    plane_list = (
                        file_counter, pilot_name.get(), combo1.get(), userage, emp_date.get(), combo_g.get())
                    cur.execute("INSERT INTO pilots VALUES(?, ?, ?, ?, ?, ?);", plane_list)
                    conn.commit()
                    pilot_name.delete(0, END)
                    add_frame1.grid_forget()
                    pilots1()

                else:
                    birth = DateEntry(add_frame1, selectmode='day', date_pattern='dd-MM-yyyy', style='my.DateEntry',
                                      font=20, state='readonly')
                    birth.grid(row=1, column=3, padx=20)
                    mb.showerror('Внимание!', 'Сотрудник не может быть младше 18!')
            else:
                birth = DateEntry(add_frame1, selectmode='day', date_pattern='dd-MM-yyyy', style='my.DateEntry',
                                  font=20, state='readonly')
                birth.grid(row=1, column=3, padx=20)
                mb.showerror('Внимание!', 'Вы заполнили не все поля\nПроверьте корректность данных!')

        def hidef1(): # скрыть поле ввода добавления в таблицу с сотрудниками

            add_frame1.grid_forget()

        hide_btn = Button(add_frame1, text='Скрыть', command=hidef1).grid(row=1, column=6)
        conf_btn = Button(add_frame1, text='Выполнить', command=confirm).grid(row=0, column=6)

    if check == 3:
        add_frame2 = Frame(Admin)
        add_frame2.grid(row=3, column=0, columnspan=2)
        # Открываем файл счётчик для чтения текущего значение из файла
        with open("flights_counter.txt", 'r') as f:
            file_counter = f.read().splitlines()
        file_counter = int(''.join(map(str, file_counter))) + 1
        # Открываем файл счётчик для записи данных в файл
        with open("flights_counter.txt", "w") as file:
            file.write(str(file_counter))

        post = 'Пилот'
        # запрашиваем пилотов
        sql_select_query = """select * from pilots where pilotpost = ?"""
        cur.execute(sql_select_query, (post,))
        pilot_values = cur.fetchall()
        values2 = [tup[1] for tup in pilot_values]
        # запрашиваем самолёты
        sql_select_query1 = """select * from planes"""
        cur.execute(sql_select_query1)
        plane_values = cur.fetchall()
        values3 = [tup[0] for tup in plane_values]
        # Заполняемые окна
        combo_plane = ttk.Combobox(add_frame2,
                                   values=values3, state='readonly', width=10)
        combo_plane.current(1)
        combo_plane.grid(column=0, row=1, padx=5)

        combo2 = ttk.Combobox(add_frame2,
                              values=values2, state='readonly')
        combo2.current(1)
        combo2.grid(column=1, row=1, padx=5)

        emp_date = DateEntry(add_frame2, selectmode='day', date_pattern='dd-MM-yyyy', style='my.DateEntry', font=20)
        emp_date.grid(row=1, column=2, padx=5)
        flights_time = Entry(add_frame2, width=10)
        flights_time.grid(row=1, column=3)
        town = Entry(add_frame2)
        town.grid(row=1, column=4)
        personal = Entry(add_frame2)
        personal.grid(row=1, column=5)
        # Лейблы
        l1 = Label(add_frame2, text='№ Самолёта')
        l1.grid(column=0, row=0, padx=5)
        l2 = Label(add_frame2, text='Пилот')
        l2.grid(column=1, row=0, padx=5)
        l3 = Label(add_frame2, text='Дата рейса')
        l3.grid(row=0, column=2, padx=5)
        l4 = Label(add_frame2, text='Время полёта')
        l4.grid(row=0, column=3)
        l5 = Label(add_frame2, text='Город')
        l5.grid(row=0, column=4)
        l6 = Label(add_frame2, text='Экипаж')
        l6.grid(row=0, column=5)

        def confirm(): # сохранение новой записи в таблице с рейсами
            pilot_name = combo2.get()
            sql_select_query = """select * from pilots where pilotname = ?"""
            cur.execute(sql_select_query, (pilot_name,))
            pilot_date = cur.fetchall()
            if flights_time.get().isdigit() and flights_time.get() != '' and town.get() != '' and personal.get() != '' and not (re.search('[0-9]', town.get())) and not (re.search('[0-9]', personal.get())):
                plane_list = (
                    file_counter, combo_plane.get(), pilot_date[0][0], emp_date.get(), flights_time.get(), town.get(),
                    personal.get())
                cur.execute("INSERT INTO flights VALUES(?, ?, ?, ?, ?, ?,?);", plane_list)
                conn.commit()
                emp_date.delete(0, END)
                town.delete(0, END)
                add_frame2.grid_forget()
                flights1()
            else:
                mb.showerror('Внимание!', 'Вы заполнили не все поля\nПроверьте корректность данных!')

        def hidef2(): # скрыть поле ввода добавления в таблицу с рейсами
            add_frame2.grid_forget()

        hide_btn = Button(add_frame2, text='Скрыть', command=hidef2).grid(row=1, column=6)
        conf_btn = Button(add_frame2, text='Выполнить', command=confirm).grid(row=0, column=6)


def planes1():  # Таблица с самолётами в окне админ
    global table_frame1, plane_table1, pilots_table1, flights_table1, Admin, check, values, change_frame, change_frame1, change_frame2, hidef, hidef1, hidef2, hide2, hide1, hide, status

    values = ()
    check = 1
    status = 2
    pilots_table1.grid_forget()
    flights_table1.grid_forget()
    cur.execute("SELECT * FROM planes;")
    planes_lst = cur.fetchall()
    heads = ['№ самолёта', 'Тип', 'Дата выпуска', 'Статус', 'Кол-во пассажиров', 'Дальность полёта (км)',
             'Скорость (км/ч)']
    plane_table1 = ttk.Treeview(table_frame1, show='headings')
    plane_table1['columns'] = heads
    plane_table1["show"] = "headings"

    def on_select(event):
        global values
        if not plane_table1.selection():
            return
        # Получаем id первого выделенного элемента
        selected_item = plane_table1.selection()[0]
        # Получаем значения в выделенной строке
        values = plane_table1.item(selected_item, option="values")

    plane_table1.bind('<<TreeviewSelect>>', on_select)

    for header in heads:
        plane_table1.heading(header, text=header, anchor='center')
        plane_table1.column(header, anchor='center', width=110)
    for row in planes_lst:
        plane_table1.insert('', END, values=row)
    # Скроллер
    scroller = Scrollbar(table_frame1, command=plane_table1.yview)
    scroller.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")
    # Дополнения для таблицы и её упаковка
    plane_table1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    plane_table1.configure(yscrollcommand=scroller.set)


def pilots1():  # Таблица с персоналом в окне админ
    global table_frame1, plane_table1, pilots_table1, flights_table1, check, values, change_frame, change_frame1, change_frame2, hidef, hidef1, hidef2, hide2, hide1, hide

    check = 2
    status = 2
    values = ()
    plane_table1.grid_forget()
    flights_table1.grid_forget()
    cur.execute("SELECT * FROM pilots;")
    pilots_lst = cur.fetchall()
    heads = ['ID', 'ФИО', 'Должность', 'Дата рождения', 'Дата найма', 'Пол']
    pilots_table1 = ttk.Treeview(table_frame1, show='headings')
    pilots_table1['columns'] = heads
    pilots_table1["show"] = "headings"

    def on_select(event):
        global values
        if not pilots_table1.selection():
            return
        # Получаем id первого выделенного элемента
        selected_item = pilots_table1.selection()[0]
        # Получаем значения в выделенной строке
        values = pilots_table1.item(selected_item, option="values")

    pilots_table1.bind('<<TreeviewSelect>>', on_select)

    for header in heads:
        pilots_table1.heading(header, text=header, anchor='center')
        pilots_table1.column(header, anchor='center', width=135)
    for row in pilots_lst:
        pilots_table1.insert('', END, values=row)
    # Скроллер
    scroller = Scrollbar(table_frame1, command=pilots_table1.yview)
    scroller.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")
    # Дополнения для таблицы и её упаковка
    pilots_table1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    pilots_table1.configure(yscrollcommand=scroller.set)


def flights1():  # Таблица с рейсами в окне админ
    global table_frame1, plane_table1, pilots_table1, flights_table1, check, values, change_frame, change_frame1, change_frame2, hidef, hidef1, hidef2, hide2, hide1, hide, status

    check = 3
    status = 3
    values = ()

    plane_table1.grid_forget()
    pilots_table1.grid_forget()
    cur.execute("""SELECT flights.flightsid, planes.planeid, pilots.pilotname, flights.flightsdate, flights.flightstime, flights.town, flights.flightspeople FROM flights 
        LEFT JOIN pilots ON pilots.pilotid = flights.pilotid
        LEFT JOIN planes ON planes.planeid = flights.planeid;""")
    flights_lst = cur.fetchall()
    heads = ['№ рейса', '№ самолёта', 'Пилот', 'Дата рейса', 'Время полёта (мин)', 'Город', 'Экипаж']
    flights_table1 = ttk.Treeview(table_frame1, show='headings')
    flights_table1['columns'] = heads
    flights_table1["show"] = "headings"

    def list_replace(lst: list, value_search, value_replace):
        res = []
        for item in lst:  # Итерируем входной список
            if isinstance(item, (list, set, tuple)):
                res.append(
                    list_replace(item, value_search,
                                 value_replace))  # На этом уровне уходим в список, сет, кортеж глубже
            else:
                res.append(
                    item if item != value_search else value_replace)  # добавляем значение в результирующий список, если совпадает с искомым значением, то меняем его
        return type(lst)(res)

    flights_lst = list_replace(flights_lst, None, '(Уволен)')

    def on_select(event):
        global values
        if not flights_table1.selection():
            return
        # Получаем id первого выделенного элемента
        selected_item = flights_table1.selection()[0]
        # Получаем значения в выделенной строке
        values = flights_table1.item(selected_item, option="values")

    flights_table1.bind('<<TreeviewSelect>>', on_select)

    for header in heads:
        flights_table1.heading(header, text=header, anchor='center')
        flights_table1.column(header, anchor='center', width=110)
    for row in flights_lst:
        flights_table1.insert('', END, values=row)
    # Скроллер
    scroller = Scrollbar(table_frame1, command=flights_table1.yview)
    scroller.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")
    # Дополнения для таблицы и её упаковка
    flights_table1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    flights_table1.configure(yscrollcommand=scroller.set)


def delete_info():  # ФУНКЦИЯ УДАЛЕНИЯ ДАННЫХ
    global check, plane_table1, pilots_table1, flights_table1, values, on_select, new_selection, change_frame, change_frame1, change_frame2
    if check == 0:
        mb.showerror('Внимание!', 'Вы не выбрали таблицу для изменения данных!')

    if check == 1:
        if values:
            answer = mb.askyesno("Вопрос", "Вы уверены что хотите УДАЛИТЬ данные?")
            if answer:
                sql_delete_query = """DELETE from planes where planeid = ?"""
                cur.execute(sql_delete_query, (values[0],))
                conn.commit()
                selected_item = plane_table1.selection()[0]
                plane_table1.delete(selected_item)
                mb.showinfo("Ошибка","Запись успешно удалена")
                values = ()
        else:
            mb.showerror("Внимание!", "Вы не выбрали данные для удаления!")

    if check == 2:
        if values:
            answer = mb.askyesno("Вопрос", "Вы уверены что хотите УДАЛИТЬ данные?")
            if answer:
                sql_delete_query = """DELETE from pilots where pilotid = ?"""
                cur.execute(sql_delete_query, (values[0],))
                conn.commit()
                selected_item = pilots_table1.selection()[0]
                pilots_table1.delete(selected_item)
                mb.showinfo(
                    "Ошибка",
                    "Запись успешно удалена")
                values = ()
        else:
            mb.showerror("Внимание!", "Вы не выбрали данные для удаления!")

    if check == 3:
        if values:
            answer = mb.askyesno("Вопрос", "Вы уверены что хотите УДАЛИТЬ данные?")
            if answer:
                sql_delete_query = """DELETE from flights where flightsid = ?"""
                cur.execute(sql_delete_query, (values[0],))
                conn.commit()
                selected_item = flights_table1.selection()[0]
                flights_table1.delete(selected_item)
                mb.showinfo(
                    "Ошибка",
                    "Запись успешно удалена")
                values = ()
        else:
            mb.showerror("Внимание!", "Вы не выбрали данные для удаления!")


def on_closing():
    global table_frame1, plane_table1, pilots_table1, flights_table1, Admin, check, values, change_frame, change_frame1, change_frame2
    values = ()
    check = 0
    Admin.destroy()


global table_frame, plane_table, pilots_table, flights_table


def planes():  # Таблица с самолётами
    global table_frame, plane_table, pilots_table, flights_table
    pilots_table.grid_forget()
    flights_table.grid_forget()
    cur.execute("SELECT * FROM planes;")
    planes_lst = cur.fetchall()
    heads = ['№ самолёта', 'Тип', 'Дата выпуска', 'Статус', 'Кол-во пассажиров', 'Дальность полёта', 'Скорость']
    plane_table = ttk.Treeview(table_frame, show='headings')
    plane_table['columns'] = heads
    plane_table["show"] = "headings"
    for header in heads:
        plane_table.heading(header, text=header, anchor='center')
        plane_table.column(header, anchor='center', width=110)
    for row in planes_lst:
        plane_table.insert('', END, values=row)
    # Скроллер
    scroller = Scrollbar(table_frame, command=plane_table.yview)
    scroller.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")
    # Дополнения для таблицы и её упаковка
    plane_table.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    plane_table.configure(yscrollcommand=scroller.set)


def pilots():  # Таблица с персоналом
    global table_frame, plane_table, pilots_table, flights_table
    plane_table.grid_forget()
    flights_table.grid_forget()
    cur.execute("SELECT * FROM pilots;")
    pilots_lst = cur.fetchall()
    heads = ['ID', 'ФИО', 'Должность', 'Дата рождения', 'Дата найма', 'Пол']
    pilots_table = ttk.Treeview(table_frame, show='headings')
    pilots_table['columns'] = heads
    pilots_table["show"] = "headings"
    for header in heads:
        pilots_table.heading(header, text=header, anchor='center')
        pilots_table.column(header, anchor='center', width=135)
    for row in pilots_lst:
        pilots_table.insert('', END, values=row)
    # Скроллер
    scroller = Scrollbar(table_frame, command=pilots_table.yview)
    scroller.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")
    # Дополнения для таблицы и её упаковка
    pilots_table.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    pilots_table.configure(yscrollcommand=scroller.set)


def flights():  # Таблица с рейсами
    global table_frame, plane_table, pilots_table, flights_table
    plane_table.grid_forget()
    pilots_table.grid_forget()
    cur.execute("""SELECT flights.flightsid, planes.planeid, pilots.pilotname, flights.flightsdate, flights.flightstime, flights.town, flights.flightspeople, flights.flightsdate, flights.town FROM flights 
        LEFT JOIN pilots ON pilots.pilotid = flights.pilotid
        LEFT JOIN planes ON planes.planeid = flights.planeid;""")
    flights_lst = cur.fetchall()
    def list_replace(lst: list, value_search, value_replace):
        res = []
        for item in lst:  # Итерируем входной список
            if isinstance(item, (list, set, tuple)):
                res.append(
                    list_replace(item, value_search,
                                 value_replace))  # На этом уровне уходим в список, сет, кортеж глубже
            else:
                res.append(
                    item if item != value_search else value_replace)  # добавляем значение в результирующий список, если совпадает с искомым значением, то меняем его
        return type(lst)(res)

    flights_lst = list_replace(flights_lst, None, '(Уволен)')
    heads = ['№ рейса', '№ самолёта', 'Пилот', 'Дата рейса', 'Время полёта', 'Город', 'Экипаж']
    flights_table = ttk.Treeview(table_frame, show='headings')
    flights_table['columns'] = heads
    flights_table["show"] = "headings"
    for header in heads:
        flights_table.heading(header, text=header, anchor='center')
        flights_table.column(header, anchor='center', width=110)
    for row in flights_lst:
        flights_table.insert('', END, values=row)
    # Скроллер
    scroller = Scrollbar(table_frame, command=flights_table.yview)
    scroller.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")
    # Дополнения для таблицы и её упаковка
    flights_table.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    flights_table.configure(yscrollcommand=scroller.set)

conn = sqlite3.connect('aeroflot.db')
cur = conn.cursor()
# Три основные таблицы
cur.execute("""CREATE TABLE IF NOT EXISTS planes(
       planeid INT PRIMARY KEY,
       planetype TEXT,
       daterelease TEXT,
       planestate TEXT,
       planeseats INT,
       planerange FLOAT,
       planespeed FLOAT);
    """)

cur.execute("""CREATE TABLE IF NOT EXISTS pilots(
       pilotid INT PRIMARY KEY,
       pilotname TEXT,
       pilotpost TEXT,
       datebirth TEXT,
       employedate TEXT,
       pilotgender TEXT);
    """)

cur.execute("""CREATE TABLE IF NOT EXISTS flights(
       flightsid INT PRIMARY KEY,
       planeid TEXT,
       pilotid TEXT,
       flightsdate TEXT,
       flightstime TEXT,
       town TEXT,
       flightspeople TEXT);
    """)

conn.commit()

global ent_req_pil, req_pil, pilots_frame1, pilot_frame, req_pl_frame, req_fli, plane_frame, flights_frame

# Запросы
def clear_plane():
    global ent_req_pil, req_pil, pilots_frame1, pilot_frame, req_pl_frame, plane_frame
    plane_frame.grid_forget()
    plane_frame = LabelFrame(req_pl, height=230, width=840, relief=FLAT)
    plane_frame.grid(row=2, columnspan=2)


def find_plane():  # запрос по самолётам
    global ent_req_pl, req_pl, req_fli, plane_frame
    palane_numb = ent_req_pl.get()
    sql_select_query = """select * from planes where planeid = ?"""
    cur.execute(sql_select_query, (palane_numb,))
    planes_lst = cur.fetchall()

    if palane_numb.isdigit():
        if planes_lst:  # Если список не пустой
            plane_frame = LabelFrame(req_pl, height=230, width=840, relief=FLAT)
            plane_frame.grid(row=2, columnspan=2)
            heads = ['№ самолёта', 'Тип', 'Дата выпуска', 'Статус', 'Кол-во пассажиров', 'Дальность полёта', 'Скорость']
            plane_table = ttk.Treeview(plane_frame, show='headings')
            plane_table['columns'] = heads
            plane_table["show"] = "headings"
            for header in heads:
                plane_table.heading(header, text=header, anchor='center')
                plane_table.column(header, anchor='center', width=110)
            for row in planes_lst:
                plane_table.insert('', END, values=row)
            # Скроллер
            scroller = Scrollbar(plane_frame, command=plane_table.yview)
            scroller.grid(row=1, column=1, padx=0, pady=15, sticky="nsew")
            # Дополнения для таблицы и её упаковка
            plane_table.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
            plane_table.configure(yscrollcommand=scroller.set)
        else:
            clear_plane()
            ent_req_pl.delete(0, END)
            mb.showinfo('Внимание!', 'Такого самолёта нет!')
    else:
        clear_plane()
        ent_req_pl.delete(0, END)
        mb.showerror('Внимание!', 'Вы не корректно ввели номер самолёта!')

def clear():
    global ent_req_pil, req_pil, pilots_frame1, pilot_frame, req_pl_frame
    pilot_frame.grid_forget()
    pilots_frame1.grid_forget()
    pilot_frame = LabelFrame(req_pil, height=230, width=840, relief=FLAT)
    pilot_frame.grid(row=2, columnspan=2)
    pilots_frame1 = LabelFrame(req_pil, height=230, width=840, relief=FLAT)
    pilots_frame1.grid(row=3, columnspan=2)

def clear2():
    global ent_req_pil, req_pil, pilots_frame1, pilot_frame, req_pl_frame
    pilots_frame1.grid_forget()
    pilots_frame1 = LabelFrame(req_pil, height=230, width=840, relief=FLAT)
    pilots_frame1.grid(row=3, columnspan=2)

def find_pilot():  # запрос по работникам
    global ent_req_pil, req_pil, pilots_frame1, pilot_frame, pilot_flights, pilots_lst, d, req_pl_frame

    pilot_fio = ent_req_pil.get()
    sql_select_query = """select * from pilots where pilotname = ?"""
    cur.execute(sql_select_query, (pilot_fio,))
    pilots_name = cur.fetchall()
    dolzhnost = 'Пилот'

    if [item for item in pilots_name if item[2] == dolzhnost]:
        heads = ['Личный №', 'ФИО', 'Должность', 'Дата рождения', 'Дата найма', 'Пол']
        pilot_table = ttk.Treeview(pilot_frame, show='headings')
        pilot_table['columns'] = heads
        pilot_table["show"] = "headings"
        for header in heads:
            pilot_table.heading(header, text=header, anchor='center')
            pilot_table.column(header, anchor='center', width=110)
        for row in pilots_name:
            pilot_table.insert('', END, values=row)
        # Скроллер
        scroller = Scrollbar(pilot_frame, command=pilot_table.yview)
        scroller.grid(row=1, column=1, padx=0, pady=15, sticky="nsew")
        # Дополнения для таблицы и её упаковка
        pilot_table.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        pilot_table.configure(yscrollcommand=scroller.set)
        # таблица с рейсами
        cur.execute("""SELECT  planes.planeid, flights.flightsdate, flights.flightstime, flights.town, pilots.pilotname FROM flights
                     LEFT JOIN pilots ON pilots.pilotid = flights.pilotid
                     LEFT JOIN planes ON planes.planeid = flights.planeid;""")
        pilot_flights = cur.fetchall()
        d = [item for item in pilot_flights if item[4] == pilot_fio]
        if d:
            if pilot_flights and [item for item in pilot_flights if item[4] == pilot_fio]:
                heads = ['№ Самолёта', 'Дата рейса', 'Время полёта', 'Место назначения']
                plane_table = ttk.Treeview(pilots_frame1, show='headings')
                plane_table['columns'] = heads
                plane_table["show"] = "headings"
                pilot_flights = [item for item in pilot_flights if item[4] == pilot_fio]
                for header in heads:
                    plane_table.heading(header, text=header, anchor='center')
                    plane_table.column(header, anchor='center', width=110)
                for row in pilot_flights:
                    plane_table.insert('', END, values=row)
                # Скроллер
                scroller = Scrollbar(pilots_frame1, command=plane_table.yview)
                scroller.grid(row=1, column=1, padx=0, pady=15, sticky="nsew")
                # Дополнения для таблицы и её упаковка
                plane_table.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
                plane_table.configure(yscrollcommand=scroller.set)
        else:
            clear2()
    else:
        ent_req_pil.delete(0, END)
        clear()
        mb.showinfo('Внимание!','Такого пилота нет!')

def clear_flights():
    global ent_req_pil, req_pil, pilots_frame1, pilot_frame, req_pl_frame, req_fli, plane_frame, flights_frame
    flights_frame.grid_forget()
    flights_frame = LabelFrame(req_fli, height=230, width=840, relief=FLAT)
    flights_frame.grid(row=2, columnspan=2)

def find_fligts():  # запрос по рейсам
    global ent_req_fli, req_fli, flights_frame
    plane_numb = ent_req_fli.get()
    sql_select_query = """select * from flights where flightsid = ?"""
    cur.execute(sql_select_query, (plane_numb,))

    cur.execute("""SELECT flights.flightsid, planes.planeid, pilots.pilotname, flights.flightsdate, flights.flightstime, flights.town, flights.flightspeople, flights.flightsdate, flights.town FROM flights
              LEFT JOIN pilots ON pilots.pilotid = flights.pilotid
              LEFT JOIN planes ON planes.planeid = flights.planeid;""")
    d = []
    flights_lst = cur.fetchall()
    if plane_numb.isdigit():
        d = [item for item in flights_lst if item[0] == int(plane_numb)]
        if d:  # Если список не пустой
            flights_frame = LabelFrame(req_fli, height=230, width=840, relief=FLAT)
            flights_frame.grid(row=2, columnspan=2)
            heads = ['№ рейса', '№ самолёта', 'Пилот', 'Дата рейса', 'Время полёта', 'Город', 'Экипаж']
            plane_table = ttk.Treeview(flights_frame, show='headings')
            plane_table['columns'] = heads
            plane_table["show"] = "headings"
            for header in heads:
                plane_table.heading(header, text=header, anchor='center')
                plane_table.column(header, anchor='center', width=110)
            for row in d:
                plane_table.insert('', END, values=row)
            # Скроллер
            scroller = Scrollbar(flights_frame, command=plane_table.yview)
            scroller.grid(row=1, column=1, padx=0, pady=15, sticky="nsew")
            # Дополнения для таблицы и её упаковка
            plane_table.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
            plane_table.configure(yscrollcommand=scroller.set)
        else:
            clear_flights()
            ent_req_fli.delete(0, END)
            mb.showinfo('Внимание!', 'Такого рейса не существует!')
    else:
        clear_flights()
        ent_req_fli.delete(0, END)
        mb.showerror('Внимание!', 'Вы не корректно ввели номер рейса!')

def req_planes():  # Запрос по самолёту
    global ent_req_pl, req_pl, req_pl_frame, plane_frame
    req_pl = Toplevel(root)
    req_pl.geometry('800x400')
    req_pl.title('Запрос по самолёту')
    req_pl_frame = Frame(req_pl)
    req_pl_frame.grid(row=0, column=0)
    plane_frame = LabelFrame(req_pl, height=230, width=840, relief=FLAT)
    plane_frame.grid(row=2, columnspan=2)
    label_req_pl = Label(req_pl_frame, text='Введите номер самолёта:').grid(row=0, column=0, padx=10, pady=10)
    ent_req_pl = Entry(req_pl_frame)
    ent_req_pl.grid(row=0, column=1, padx=10, pady=10)
    but_req_pl = Button(req_pl_frame, text='Найти', command=find_plane).grid(row=0, column=2, padx=10, pady=10)
    req_pl.grab_set()

def req_pilots():  # Запрос по пилоту
    global ent_req_pil, req_pil, pilot_frame, pilots_frame1
    req_pil = Toplevel(root)
    req_pil.geometry('1020x400')
    req_pil.title('Запрос по пилоту')
    req_pil_frame = Frame(req_pil)
    req_pil_frame.grid(row=0, column=0)
    pilot_frame = LabelFrame(req_pil, height=230, width=840, relief=FLAT)
    pilot_frame.grid(row=2, columnspan=2)
    pilots_frame1 = LabelFrame(req_pil, height=230, width=840, relief=FLAT)
    pilots_frame1.grid(row=3, columnspan=2)
    label_req_pil = Label(req_pil_frame, text='Введите ФИО пилота:').grid(row=0, column=0, padx=10, pady=10)
    ent_req_pil = Entry(req_pil_frame)
    ent_req_pil.grid(row=0, column=1, padx=10, pady=10)
    but_req_pil = Button(req_pil_frame, text='Найти', command=find_pilot).grid(row=0, column=2, padx=10, pady=10)
    req_pil.grab_set()

def req_flights():  # Запрос по рейсу
    global ent_req_fli, req_fli, flights_frame
    req_fli = Toplevel(root)
    req_fli.geometry('800x400')
    req_fli.title('Запрос по рейсу')
    req_fli_frame = Frame(req_fli)
    req_fli_frame.grid(row=0, column=0)
    flights_frame = LabelFrame(req_fli, height=230, width=840, relief=FLAT)
    flights_frame.grid(row=2, columnspan=2)
    label_req_fli = Label(req_fli_frame, text='Введите номер рейса:').grid(row=0, column=0, padx=10, pady=10)
    ent_req_fli = Entry(req_fli_frame)
    ent_req_fli.grid(row=0, column=1, padx=10, pady=10)
    but_req_fli = Button(req_fli_frame, text='Найти', command=find_fligts).grid(row=0, column=2, padx=10, pady=10)
    req_fli.grab_set()

# Главное окно
root = Tk()
root.geometry('850x400')
root.title('ПС «Авиакомпания»')
root.resizable(0, 0)

# Frame с конопками, выводящих таблицы
btn_frame = LabelFrame(root, text='Выберете раздел', font=14, relief=FLAT)
btn_frame.grid(row=1, column=1, sticky="w", padx=2, pady=4)
planes_btn = Button(btn_frame, text='Самолёты', font=14, command=planes).grid(row=0, column=0, sticky="e")
pilots_btn = Button(btn_frame, text='Сотрудники', font=14, command=pilots).grid(row=0, column=1, sticky="e")
flights_btn = Button(btn_frame, text='Рейсы', font=14, command=flights).grid(row=0, column=2, sticky="w")

# Frame с конопками для запросов
request_frame = LabelFrame(root, text='Ваш запрос', font=14, relief=FLAT)
request_frame.grid(row=3, column=1, sticky="w", padx=2, pady=4)
req_planes_btn = Button(request_frame, text='Найти самолёт', font=14, command=req_planes).grid(row=0, column=0, sticky="e")
req_pilots_btn = Button(request_frame, text='Найти пилота', font=14, command=req_pilots).grid(row=0, column=1, sticky="e")
req_flights_btn = Button(request_frame, text='Найти рейс', font=14, command=req_flights).grid(row=0, column=2, sticky="w")
# Frame для таблиц
table_frame = LabelFrame(root, height=230, width=840, relief=FLAT)
table_frame.grid(row=2, columnspan=2)
table_frame.grid_propagate(0)

plane_table = ttk.Treeview(table_frame, show='headings')
pilots_table = ttk.Treeview(table_frame, show='headings')
flights_table = ttk.Treeview(table_frame, show='headings')

# Главное меню
mainmenu = Menu(root)
root.config(menu=mainmenu)
mainmenu.add_command(label='Об авторе', command=Autor)
mainmenu.add_command(label='Справка', command=Help)

# Кнопка входв в качестве администратора
buttonAdmin = Button(root, text='Администратор', font=12, width=15, command=loginAdmin)
buttonAdmin.grid(row=0, column=0, sticky=W, )

root.mainloop()
