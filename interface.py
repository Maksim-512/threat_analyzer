import tkinter
from functools import partial
from tkinter import *
from tkinter import ttk
from connection_bd import connect
from selecting_data_db import get_device_type, get_sp_protection, get_device_name, get_sp_ubi, get_sp_number, \
    get_sp_description, get_threat_with_description, get_list_device_variation
from nlp_test import device_detection


def show_message(cur):
    mess = txt.get(1.0, END).replace('\n', ' ')
    # mess = txt.get()
    return res(cur, mess)


def res(cur, message):
    window2 = Tk()
    window2.state('zoomed')
    window2.title("Добро пожаловать в приложение определения угроз")
    window2.resizable(False, False)

    # Create A Main Frame
    main_frame = Frame(window2)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    # my_canvas.pack(side=TOP, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_scrollbar2 = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbar2.pack(side=BOTTOM, fill=X)

    my_canvas.pack(side=TOP, fill=BOTH, expand=1)
    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set, xscrollcommand=my_scrollbar2.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    second_frame = Frame(my_canvas)

    # Add that New frame To a Window In The Canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    device_variation = device_detection(cur, message)
    lbl_variation = Label(second_frame,
                          text=f"Из вашего сообщения: '{message}' были получены следующие устройства: {', '.join(device_variation)}",
                          font=("Arial", 14, 'bold'),
                          justify=LEFT, )
    lbl_variation.grid(row=0, column=0, sticky='w')

    i = 0

    for device in device_variation:
        device_name = get_device_name(cur, device)
        device_type = get_device_type(cur, device_name)
        sp_number = get_sp_number(cur, device_name)

        string = f"\n{device_variation.index(device) + 1}. Устройство {device} относится к типу устройств '{device_name}', которое входит в класс '{device_type}.'"

        lbl_device_type = Label(second_frame,
                                text=string,
                                font=("Arial", 14, 'bold'),
                                justify=LEFT,
                                fg="#B22222"
                                )
        lbl_device_type.grid(row=i + 1, column=0, sticky='w')

        string2 = f"Этому устройству соответствуют следующие способы реализации угроз: {', '.join(sp_number)}."

        lbl_device_type = Label(second_frame,
                                text=string2,
                                font=("Arial", 14, 'underline'),
                                justify=LEFT)
        lbl_device_type.grid(row=i + 2, column=0, sticky='w')

        for sp in sp_number:
            sp_ubi = get_sp_ubi(cur, sp)

            string3 = f"{sp} соответствует следующие возможные реализуемые угрозы: {', '.join(sp_ubi)}."

            lbl_sp_ubi = Label(second_frame,
                               text=string3,
                               font=("Arial Bold", 14),
                               justify=LEFT)
            lbl_sp_ubi.grid(row=i + 3, column=0, sticky='w')

            btn_ubi_description = Button(second_frame, text=f"Описание УБИ для {sp}",
                                         command=partial(ubi_description, cur, sp, sp_ubi))
            btn_ubi_description.grid(row=i + 3, column=1, padx=10, pady=5)

            btn_sp_protection = Button(second_frame, text=f"Меры защиты и их описание для {sp}",
                                       command=partial(sp_protection, cur, sp))
            btn_sp_protection.grid(row=i + 3, column=2, padx=10, pady=5)

            i += 1

        i += 3

    window2.mainloop()

    # text2 = Text(window2)
    # text2.insert('1.0',
    #              f"Из вашего сообщения: '{message}' были получены следующие устройства: {', '.join(device_name)}")
    # text2.configure(state='disabled')


def ubi_description(cur, sp, ubi_list):
    window3 = Tk()
    window3.state('zoomed')
    window3.title(f"Описание УБИ для {sp}")
    window3.resizable(False, False)

    # Create A Main Frame
    main_frame = Frame(window3)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    # my_canvas.pack(side=TOP, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_scrollbar2 = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbar2.pack(side=BOTTOM, fill=X)

    my_canvas.pack(side=TOP, fill=BOTH, expand=1)
    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set, xscrollcommand=my_scrollbar2.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    second_frame = Frame(my_canvas)

    # Add that New frame To a Window In The Canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    for i in range(len(ubi_list)):
        ubi = ubi_list[i]
        ubi_description = get_threat_with_description(cur, ubi)
        lbl_description = Label(second_frame,
                                text=f'{ubi} - {ubi_description}',
                                font=("Arial Bold", 14),
                                justify=LEFT
                                )
        lbl_description.grid(row=i, column=0, sticky='w')

    window3.mainloop()


def sp_protection(cur, sp):
    window4 = Tk()
    window4.state('zoomed')
    window4.title(f"Меры защиты и их описание для {sp}")
    window4.resizable(False, False)

    # Create A Main Frame
    main_frame = Frame(window4)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    # my_canvas.pack(side=TOP, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_scrollbar2 = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbar2.pack(side=BOTTOM, fill=X)

    my_canvas.pack(side=TOP, fill=BOTH, expand=1)
    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set, xscrollcommand=my_scrollbar2.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    second_frame = Frame(my_canvas)

    # Add that New frame To a Window In The Canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    protections = get_sp_protection(cur, sp)

    for i in range(len(protections)):
        protection_method = protections[i][0]
        protection_realize = protections[i][1]
        lbl_protections = Label(second_frame,
                                text=f'{protection_method} - {protection_realize}',
                                font=("Arial Bold", 14),
                                justify=LEFT
                                )
        lbl_protections.grid(row=i, column=0, sticky='w')

    window4.mainloop()


def all_devices(cur):
    window0 = Tk()
    window0.state('zoomed')
    window0.title("Добро пожаловать в приложение определения угроз")
    window0.resizable(False, False)

    # Create A Main Frame
    main_frame = Frame(window0)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    # my_canvas.pack(side=TOP, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_scrollbar2 = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbar2.pack(side=BOTTOM, fill=X)

    my_canvas.pack(side=TOP, fill=BOTH, expand=1)
    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set, xscrollcommand=my_scrollbar2.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    second_frame = Frame(my_canvas)

    # Add that New frame To a Window In The Canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    devices = get_list_device_variation(cur)
    for i in range(len(devices)):
        device = devices[i]
        lbl_protections = Label(second_frame,
                                text=f'{i+1}){device}',
                                font=("Arial Bold", 14),
                                justify=LEFT
                                )
        lbl_protections.grid(row=i, column=0, sticky='w')


window = Tk()
window.state('zoomed')
window.title("Добро пожаловать в приложение определения угроз")
window.resizable(False, False)

con, cur = connect()

lbl = Label(window, text="Введите свою аппаратуру/комплекс аппаратур", font=("Arial", 34, 'bold'))
lbl.grid(column=0, row=0)
lbl.place(x=500, y=50)

txt = Text(window, width=10, font=("Arial Bold", 18))
# txt = Entry(window, width=10, font=("Arial Bold", 18))
txt.grid()
txt.place(x=70, y=150, width=1800, height=300)

btn = Button(window, text="Отправить!", command=partial(show_message, cur), font=("Arial Bold", 28))
btn.grid()
btn.place(x=1600, y=500)

lbl_all_devices = Label(window,
                        text='Сомневаешься, есть ли твои устройства в нашей базе? Нажимай на кнопку ниже и смотри все наши девайсы:',
                        font=("Arial Bold", 24),
                        justify=LEFT
                        )
lbl_all_devices.place(x=120, y=800)

btn2 = Button(window, text="Список возможных устройств", command=partial(all_devices, cur), font=("Arial Bold", 28))
btn2.grid()
btn2.place(x=690, y=900)

window.mainloop()
