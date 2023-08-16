import tkinter as tk
from tkinter import ttk
import requests
import os


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        self.notebook = 0

        self.desktop_path = os.path.join(
            os.path.join(os.environ['USERPROFILE']), 'Desktop')

        # ======================================================== #
        # FRAME ONE LEVEL

        notebook = tk.Frame(bg='#f4874b', bd=2)
        notebook.pack(side=tk.TOP, fill=tk.X)

        btn_tool = tk.Button(notebook, text='Инструмент',
                             command=self.tool, bg='#72c57b',
                             bd=2, compound=tk.TOP)

        btn_tool.pack(side=tk.LEFT)

        btn_issuance_of_a_tool = tk.Button(
            notebook, text='Выдача инст.',
            bg='#72c57b', bd=2, compound=tk.TOP,
            command=self.issuance_of_a_tool)

        btn_issuance_of_a_tool.pack(side=tk.LEFT)

        btn_history = tk.Button(notebook, text='История выдачи',
                                bg='#72c57b', bd=2, compound=tk.TOP,
                                command=self.extradition)

        btn_history.pack(side=tk.LEFT)

        btn_worker = tk.Button(notebook, text='Работники',
                               bg='#72c57b', bd=2, compound=tk.TOP,
                               command=self.workers)

        btn_worker.pack(side=tk.LEFT)

        # ======================================================== #
        # FRAME TWO LEVEL

        self.toolbar = tk.Frame(bg='#f4874b', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.zero_image = tk.PhotoImage(file='icon/0.png')

        self.btn_open_dialog = tk.Button(
            self.toolbar, text='Добавить позицию',
            command=self.open_dialog, bg='#ADD8E6',
            bd=2, compound=tk.TOP,
            image=self.zero_image)

        self.btn_open_dialog.pack(side=tk.LEFT)

        self.one_image = tk.PhotoImage(file='icon/1.png')

        self.btn_edit_dialog = tk.Button(
            self.toolbar, text='Редактировать',
            bg='#ADD8E6', bd=2, compound=tk.TOP,
            command=self.open_update_dialog,
            image=self.one_image)

        self.btn_edit_dialog.pack(side=tk.LEFT)

        self.two_image = tk.PhotoImage(file='icon/2.png')

        self.btn_delete = tk.Button(
            self.toolbar, text='Удалить',
            bg='#ADD8E6', bd=2, compound=tk.TOP,
            command=self.delete_records,
            image=self.two_image)

        self.btn_delete.pack(side=tk.LEFT)

        self.three_image = tk.PhotoImage(file='icon/3.png')

        self.btn_search = tk.Button(
            self.toolbar, text='Поиск',
            bg='#ADD8E6', bd=2, compound=tk.TOP,
            command=self.open_search_dialog,
            image=self.three_image)

        self.btn_search.pack(side=tk.LEFT)

        self.four_image = tk.PhotoImage(file='icon/4.png')

        self.btn_refrash = tk.Button(
            self.toolbar, text='Обновление базы данных',
            bg='#ADD8E6', bd=2, compound=tk.TOP,
            command=self.view_records,
            image=self.four_image)

        self.btn_refrash.pack(side=tk.LEFT)

        self.five_image = tk.PhotoImage(file='icon/5.png')

        self.btn_excel = tk.Button(
            self.toolbar,
            text='Сохранить данные в виде таблицы excel',
            bg='#ADD8E6', bd=2, compound=tk.TOP,
            command=self.excel_table,
            image=self.five_image)

        self.btn_excel.pack(side=tk.LEFT)

        # ======================================================== #
        # FRAME THREE LEVEL

        self.title_frame = tk.Frame(self.root, bg='#f4874b')
        self.title_frame.pack(side=tk.TOP, fill=tk.X)

        self.text_title = tk.Label(self.title_frame, text='Tipo', bg='#f4874b')
        self.text_title.pack()

        self.text_title.destroy()

        # ======================================================== #
        # FRAME FOUR LEVEL

        self.frame = tk.Frame(self.root, bg='#f4874b')
        self.frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # ======================================================== #
        # FRAME FIVE LEVEL

        avtor = tk.Frame(self.root, bg='#f4874b')
        avtor.pack(side=tk.TOP, fill=tk.X)

        avtor_text = tk.Label(avtor, text='Made by Elieren', bg='#f4874b')
        avtor_text.configure(font=('Arial', 7))
        avtor_text.pack(side=tk.RIGHT)

        self.column()

    def column(self):
        if self.notebook == 0:
            self.tree = ttk.Treeview(self.frame, columns=(
                'ID', 'main', 'subcategory', 'name', 'value', 'date'
                ), show='headings')
            self.tree.column('ID', anchor=tk.CENTER, stretch=False)
            self.tree.column('main', anchor=tk.CENTER)
            self.tree.column('subcategory', anchor=tk.CENTER)
            self.tree.column('name', anchor=tk.CENTER)
            self.tree.column('value', anchor=tk.CENTER)
            self.tree.column('date', anchor=tk.CENTER)

            self.tree.heading('ID', text='ID')
            self.tree.heading('main', text='Основаная категория')
            self.tree.heading('subcategory', text='Доп. категория')
            self.tree.heading('name', text='• Наименование')
            self.tree.heading('value', text='Кол-во')
            self.tree.heading('date', text='Дата')
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.text_title = tk.Label(self.title_frame, text='Инструмент',
                                       bg='#f4874b')
            self.text_title.pack()

            self.enable_button()

            self.scroll_set()

        elif self.notebook == 1:
            self.tree = ttk.Treeview(self.frame, columns=(
                'ID', 'worker', 'tool', 'value', 'date'
                ), height=30, show='headings')
            self.tree.column('ID', anchor=tk.CENTER, stretch=False)
            self.tree.column('worker', anchor=tk.CENTER)
            self.tree.column('tool', anchor=tk.CENTER)
            self.tree.column('value', anchor=tk.CENTER)
            self.tree.column('date', anchor=tk.CENTER)

            self.tree.heading('ID', text='ID')
            self.tree.heading('worker', text='• Работник')
            self.tree.heading('tool', text='Инструмент')
            self.tree.heading('value', text='Кол-во')
            self.tree.heading('date', text='Дата')
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.text_title = tk.Label(self.title_frame, text='Выдача инст.',
                                       bg='#f4874b')
            self.text_title.pack()

            self.enable_button()

            self.scroll_set()
        elif self.notebook == 2:
            self.tree = ttk.Treeview(self.frame, columns=(
                'ID', 'worker', 'tool', 'value', 'date', 'date_delete'
                ), height=30, show='headings')
            self.tree.column('ID', anchor=tk.CENTER, stretch=False)
            self.tree.column('worker', anchor=tk.CENTER)
            self.tree.column('tool', anchor=tk.CENTER)
            self.tree.column('value', anchor=tk.CENTER)
            self.tree.column('date', anchor=tk.CENTER)
            self.tree.column('date_delete', anchor=tk.CENTER)

            self.tree.heading('ID', text='ID')
            self.tree.heading('worker', text='• Работник')
            self.tree.heading('tool', text='Инструмент')
            self.tree.heading('value', text='Кол-во')
            self.tree.heading('date', text='Дата создания')
            self.tree.heading('date_delete', text='Дата удаления')
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.text_title = tk.Label(self.title_frame, text='История выдачи',
                                       bg='#f4874b')
            self.text_title.pack()

            self.disable_button()
            self.btn_search.config(state='normal')
            self.btn_refrash.config(state='normal')
            self.btn_excel.config(state='normal')

            self.scroll_set()
        elif self.notebook == 3:
            self.tree = ttk.Treeview(self.frame, columns=(
                'ID', 'worker', 'room', 'date'
                ), height=30, show='headings')
            self.tree.column('ID', anchor=tk.CENTER, stretch=False)
            self.tree.column('worker', anchor=tk.CENTER)
            self.tree.column('room', anchor=tk.CENTER)
            self.tree.column('date', anchor=tk.CENTER)

            self.tree.heading('ID', text='ID')
            self.tree.heading('worker', text='• Работник')
            self.tree.heading('room', text='Цех')
            self.tree.heading('date', text='Дата')
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.text_title = tk.Label(self.title_frame, text='Работники',
                                       bg='#f4874b')
            self.text_title.pack()

            self.enable_button()

            self.scroll_set()

    def scroll_set(self):
        self.scroll = tk.Scrollbar(self.frame, command=self.tree.yview)

        self.scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.tree.configure(yscrollcommand=self.scroll.set)

    def enable_button(self):
        self.btn_open_dialog.config(state='normal')
        self.btn_edit_dialog.config(state='normal')
        self.btn_delete.config(state='normal')
        self.btn_search.config(state='normal')
        self.btn_refrash.config(state='normal')
        self.btn_excel.config(state='normal')

    def disable_button(self):
        self.btn_open_dialog.config(state='disabled')
        self.btn_edit_dialog.config(state='disabled')
        self.btn_delete.config(state='disabled')
        self.btn_search.config(state='disabled')
        self.btn_refrash.config(state='disabled')
        self.btn_excel.config(state='disabled')

# ======================================================== #
# RECOED

    def record_tool(self, main, subcategory, name, value):
        self.db.tool(main, subcategory, name, value)
        self.view_records()

    def record_issuance_of_a_tool(self, worker, tool, value):
        self.db.issuance_of_a_tool(worker, tool, value)
        self.view_records()

    def record_workers(self, worker, room):
        self.db.workers(worker, room)
        self.view_records()

# ======================================================== #
# UPDATE

    def update_record_tool(self, main, subcategory, name, value):
        data = {'id': self.tree.set(self.tree.selection()[0], '#1'),
                'main': main, 'subcategory': subcategory,
                'name': name, 'value': value}
        requests.post('http://127.0.0.1:5000/update_tool', data=data)
        self.view_records()

    def update_record_issuance_of_a_tool(self, worker, tool, value):
        data = {'id': self.tree.set(self.tree.selection()[0], '#1'),
                'worker': worker, 'tool': tool, 'value': value}
        requests.post(
            'http://127.0.0.1:5000/update_issuance_of_a_tool', data=data)
        self.view_records()

    def update_record_worker(self, worker, room):
        data = {'id': self.tree.set(self.tree.selection()[0], '#1'),
                'worker': worker, 'room': room}
        requests.post(
            'http://127.0.0.1:5000/update_workers', data=data)
        self.view_records()

# ======================================================== #
# VIEW RECORDS

    def view_records(self):
        self.tree.destroy()
        self.scroll.destroy()
        self.text_title.destroy()
        self.column()
        row = []
        if self.notebook == 0:
            html = requests.get('http://127.0.0.1:5000/get_tool')
            data = html.json()
            for i in data:
                info = (i['id'], i['main'], i['subcategory'],
                        i['name'], i['value'], i['date'])
                row.append(info)
        elif self.notebook == 1:
            html = requests.get(
                'http://127.0.0.1:5000/get_issuance_of_a_tool')
            data = html.json()
            for i in data:
                info = (i['id'], i['worker'], i['tool'],
                        i['value'], i['date'])
                row.append(info)
        elif self.notebook == 2:
            html = requests.get('http://127.0.0.1:5000/get_delete_data')
            data = html.json()
            for i in data:
                info = (i['id'], i['data_one'],
                        i['data_two'],
                        i['data_three'], i['data_date'], i['date'])
                row.append(info)
        elif self.notebook == 3:
            html = requests.get('http://127.0.0.1:5000/get_workers')
            data = html.json()
            for i in data:
                info = (i['id'], i['worker'], i['room'], i['date'])
                row.append(info)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in row]

# ======================================================== #
# DELETE RECORDS

    def delete_records(self):
        for selection_item in self.tree.selection():
            if self.notebook == 0:
                data = {'id': (self.tree.set(selection_item, '#1'),)}
                requests.post('http://127.0.0.1:5000/del_tool',
                              data=data)
            elif self.notebook == 1:
                data = {'id': (self.tree.set(selection_item, '#1'),)}
                requests.post(
                    'http://127.0.0.1:5000/del_issuance_of_a_tool',
                    data=data)
            elif self.notebook == 3:
                data = {'id': (self.tree.set(selection_item, '#1'),)}
                requests.post(
                    'http://127.0.0.1:5000/del_workers',
                    data=data)
            self.view_records()

# ======================================================== #
# SEARCH RECORDS

    def search_records(self, description):
        # description = ('%' + description + '%',)
        row = []
        if self.notebook == 0:
            data = {'name': description}
            html = requests.post('http://127.0.0.1:5000/get_tool_search',
                                 data=data)
            data = html.json()
            for i in data:
                info = (i['id'], i['main'], i['subcategory'],
                        i['name'], i['value'], i['date'])
                row.append(info)
        elif self.notebook == 1:
            data = {'worker': description}
            html = requests.post(
                'http://127.0.0.1:5000/get_issuance_of_a_tool_search',
                data=data)
            data = html.json()
            for i in data:
                info = (i['id'], i['worker'], i['tool'], i['value'], i['date'])
                row.append(info)
        elif self.notebook == 2:
            data = {'worker': description}
            html = requests.post(
                'http://127.0.0.1:5000/get_delete_data_search',
                data=data)
            data = html.json()
            for i in data:
                info = (i['id'], i['data_one'], i['data_two'],
                        i['data_three'], i['data_date'], i['date'])
                row.append(info)
        if self.notebook == 3:
            data = {'worker': description}
            html = requests.post(
                'http://127.0.0.1:5000/get_workers_search',
                data=data)
            data = html.json()
            for i in data:
                info = (i['id'], i['worker'], i['room'], i['date'])
                row.append(info)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in row]

# ======================================================== #
# EXCEL

    def excel_table(self):

        html = requests.get('http://127.0.0.1:5000/excel')
        with open(os.path.join(f'{self.desktop_path}/output.xlsx'), 'wb') as f:
            f.write(html.content)

# ======================================================== #

    def open_dialog(self):
        Child(self.notebook)

# ======================================================== #

    def open_update_dialog(self):
        Update(self.notebook)

# ======================================================== #

    def open_search_dialog(self):
        Search()

# ======================================================== #

    def tool(self):
        self.notebook = 0
        self.view_records()

    def issuance_of_a_tool(self):
        self.notebook = 1
        self.view_records()

    def extradition(self):
        self.notebook = 2
        self.view_records()

    def workers(self):
        self.notebook = 3
        self.view_records()
# ======================================================== #


class Child(tk.Toplevel):
    def __init__(self, notebook):
        super().__init__(root)
        if notebook == 0:
            self.init_child_tool()
        elif notebook == 1:
            self.instrument_array = []
            self.worker_array = []
            html = requests.get('http://127.0.0.1:5000/get_tool')
            data = html.json()
            for i in data:
                info = (i['name'])
                self.instrument_array.append(info)
            html = requests.get('http://127.0.0.1:5000/get_workers')
            data = html.json()
            for i in data:
                info = (i['worker'])
                self.worker_array.append(info)
            self.init_child_issuance_of_a_tool()
        elif notebook == 3:
            self.init_child_workers()

        self.view = app

    # ======================================================== #
    # TOOL

    def init_child_tool(self):
        self.title('Инструмент')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        self.main_array = [
                u'Пластины тв сплава',
                u'Фрезы', u'Сверла', u'Развертки', u'Резцы долбежные',
                u'Фрезы червячные', u'Плазма', u'Кристалл',
                u'Мерительный инструмент',
                u'Круги алмазные, шлифовочные, и тд',
                u'Круги УШМ', u'Электро-инструмент',
                u'Расходный инструмент и запчасти 51 цех', u'Оснвстка',
                u'Оснвстка ЦКО',
                u'Ручной инструмент', u'Пилы кольцевые', u'Лазер']

        self.subcategory_array = [
                u'Токарные', u'Расточные', u'Фрезерные', u'Резьбовые',
                u'Отрезные', u'На кромкорез', u'Концевые',
                u'Шпоночные', u'Дисковые', u'Тв сплавные.',
                u'Сопло', u'Электрод', u'Завихритель', u'Колпак', u'Корпус',
                u'Плазматрон', u'Мундштуки', u'Резак', u'Запчасти',
                u'Матрица, Пуансон']

        label_select = tk.Label(self, text='Основная категория')
        label_select.place(x=50, y=50)

        label_sum = tk.Label(self, text='Под категория:')
        label_sum.place(x=50, y=80)

        label_sum = tk.Label(self, text='Наименование:')
        label_sum.place(x=50, y=110)

        label_sum = tk.Label(self, text='Кол-во:')
        label_sum.place(x=50, y=140)

        self.combobox = ttk.Combobox(
            self,
            values=self.main_array)
        self.combobox.current(0)
        self.combobox.place(x=200, y=50)

        self.entry_money = ttk.Combobox(
            self,
            values=self.subcategory_array)
        self.entry_money.current(0)
        self.entry_money.place(x=200, y=80)

        self.name = ttk.Entry(self)
        self.name.place(x=200, y=110)

        self.value = ttk.Entry(self)
        self.value.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.record_tool(
                                                    self.combobox.get(),
                                                    self.entry_money.get(),
                                                    self.name.get(),
                                                    self.value.get()
                                                    ))

        self.grab_set()
        self.focus_set()

    # ======================================================== #
    # ISSUANCE OF A TOOL

    def init_child_issuance_of_a_tool(self):

        self.title('Выдача инст.')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_select = tk.Label(self, text='Работник:')
        label_select.place(x=50, y=40)

        label_sum = tk.Label(self, text='Инструмент:')
        label_sum.place(x=50, y=70)

        label_sum = tk.Label(self, text='Кол-во:')
        label_sum.place(x=50, y=100)

        self.worker = ttk.Combobox(
            self,
            values=self.worker_array)
        self.worker.current(0)
        self.worker.place(x=200, y=40, width=180)

        self.tool = ttk.Combobox(
            self,
            values=self.instrument_array)
        self.tool.current(0)
        self.tool.place(x=200, y=70, width=180)

        self.value = ttk.Entry(self)
        self.value.place(x=200, y=100)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.record_issuance_of_a_tool(
                                                    self.worker.get(),
                                                    self.tool.get(),
                                                    self.value.get()
                                                    ))

        self.grab_set()
        self.focus_set()

    def init_child_workers(self):

        self.title('Работник')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_select = tk.Label(self, text='Работник:')
        label_select.place(x=50, y=40)

        label_sum = tk.Label(self, text='Помещение:')
        label_sum.place(x=50, y=70)

        self.worker = ttk.Entry(self)
        self.worker.place(x=200, y=40, width=180)

        self.room = ttk.Combobox(self, values=[u'53 цех', u'ОТК',
                                               u'51 цех', u'54 цех'])
        self.room.current(0)
        self.room.place(x=200, y=70, width=180)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.record_workers(
                                                    self.worker.get(),
                                                    self.room.get()
                                                    ))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self, notebook):
        super().__init__(notebook)
        self.view = app
        self.db = db
        if notebook == 0:
            self.init_edit_tool()
            self.default_data_tool()
        elif notebook == 1:
            self.init_edit_issuance_of_a_tool()
            self.default_data_issuance_of_a_tool()
        elif notebook == 3:
            self.init_edit_workers()
            self.default_data_workers()

    # ======================================================== #
    # TOOL

    def init_edit_tool(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>',
                      lambda event: self.view.update_record_tool(
                                                        self.combobox.get(),
                                                        self.entry_money.get(),
                                                        self.name.get(),
                                                        self.value.get()
                                                        ))

        self.btn_ok.destroy()

    def default_data_tool(self):
        data = {'id': (
            self.view.tree.set(self.view.tree.selection()[0], '#1'),)}
        html = requests.post(
            'http://127.0.0.1:5000/get_tool_id', data=data)
        row = html.json()
        self.combobox.current(self.main_array.index(row['main']))
        self.entry_money.current(
            self.subcategory_array.index(row['subcategory']))
        self.name.insert(0, row['name'])
        self.value.insert(0, row['value'])

    # ======================================================== #
    # ISSUANCE OF A TOOL

    def init_edit_issuance_of_a_tool(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>',
                      lambda event: self.view.update_record_issuance_of_a_tool(
                                                            self.worker.get(),
                                                            self.tool.get(),
                                                            self.value.get(),
                                                            ))

    def default_data_issuance_of_a_tool(self):
        data = {'id': (
            self.view.tree.set(self.view.tree.selection()[0], '#1'),)}
        html = requests.post(
            'http://127.0.0.1:5000/get_issuance_of_a_tool_id', data=data)
        row = html.json()
        self.worker.current(self.worker_array.index(row['worker']))
        self.tool.current(self.instrument_array.index(row['tool']))
        self.value.insert(0, row['value'])

    # ======================================================== #
    # WORKERS

    def init_edit_workers(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>',
                      lambda event: self.view.update_record_worker(
                                                        self.worker.get(),
                                                        self.room.get()
                                                        ))

        self.btn_ok.destroy()

    def default_data_workers(self):
        room = [u'53 цех', u'ОТК', u'51 цех', u'54 цех']
        data = {'id': (
            self.view.tree.set(self.view.tree.selection()[0], '#1'),)}
        html = requests.post(
            'http://127.0.0.1:5000/get_workers_id', data=data)
        row = html.json()
        self.worker.insert(0, row['worker'])
        self.room.current(room.index(row['room']))


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x120+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=80)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=120, y=80)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(
            self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()


class DB:
    def __init__(self):
        pass

    def tool(self, main, subcategory, name, value):
        data = {'main': main, 'subcategory': subcategory,
                'name': name, 'value': value}
        requests.post('http://127.0.0.1:5000/set_tool', data=data)

    def issuance_of_a_tool(self, worker, tool, value):
        data = {'worker': worker, 'tool': tool, 'value': value}
        requests.post('http://127.0.0.1:5000/set_issuance_of_a_tool',
                      data=data)

    def workers(self, worker, room):
        data = {'worker': worker, 'room': room}
        requests.post('http://127.0.0.1:5000/set_workers',
                      data=data)


if __name__ == '__main__':
    try:
        root = tk.Tk()
        db = DB()
        app = Main(root)
        app.pack()
        root.title("Учет инструментов")
        root.geometry("945x730+300+200")
        root.resizable(True, True)
        root.configure(bg='#f4874b')
        root.mainloop()
    except Exception:
        root.destroy()
        error = tk.Tk()
        error.geometry("120x100+300+200")
        error.configure(bg='#f4874b')
        error.resizable(False, False)
        text = tk.Label(error, text='Ошибка', bg='#f4874b')
        text.configure(font=('Arial', 15))
        text.place(x=20, y=25)
        text = tk.Label(error, text='Сервер не отвечает', bg='#f4874b')
        text.configure(font=('Arial', 8))
        text.place(x=7, y=55)
        error.mainloop()
