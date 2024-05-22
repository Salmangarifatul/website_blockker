from tkinter import *
from GUI_commands import commands as cm
from GUI_commands import get_blocked_web as gb_web
from GUI_commands import get_block_history as gb_hist
from threading import Thread
from math import ceil


width = 600
height = 500


def prct(percent, length):
    return (percent * length) // 100

class GUI:
    web_var = None
    select_web = None
    page_num = 1
    blocked_webs = gb_web() 
    block_history = gb_hist() 
    y_place = 6 
    page_amt = ceil(len(blocked_webs) / 5) 
    btm_widgets_list = None 


    @staticmethod
    def create_middle_frame(location, btm_frame):
        enter_web_lbl = Label(location, text="Masukkan Domain Website:", font="Poppins 10", bg="#D3D3D3").place(
            x=prct(35, width), y=prct(2, height))
        search_lbl = Label(location, font=("Poppins Bold", 12), bg="#D3D3D3")
        search_lbl.place(x=prct(20, width), y=prct(22, height)) 
        block_btn = Button(location, text="Block", font=("Poppins Bold", 8),
                           command=lambda: Thread(target=cm.block_command, daemon=True,
                                                  args=(GUI.web_var, search_lbl, block_btn, GUI, btm_frame)).start())
        block_btn.place(x=prct(46, width), y=prct(22, height))

        GUI.web_var = StringVar(value="www.google.com")
        url_entry = Entry(location, textvariable=GUI.web_var, width=80, font="Poppins 8")
        url_entry.place(x=25, y=40, height=40)


    @staticmethod
    def create_bottom_frame(location):
        GUI.btm_widgets_list = list()

        list_lbl = Label(location, text="List website yang diblock", font=("Poppins Bold", 10), bg="white").place(
            x=prct(38, width), y=prct(1, height)
        )
        page_lbl = Label(location, text=f"Halaman {GUI.page_num}", bg="white")
        page_lbl.place(x=prct(20, width), y=prct(40,height))

        #buttons
        back_btn = Button(location, text="<<", command=lambda:cm.switch(GUI, location, GUI.create_bottom_frame, False))
        forward_btn = Button(location, text=">>", command=lambda: cm.switch(GUI, location, GUI.create_bottom_frame, True))
        his_btn = Button(location, text="History", width=10, command=lambda: cm.history(his_btn, GUI, location))

        if GUI.page_num == 1:
            back_btn["state"] = "disabled"
        if GUI.page_num == GUI.page_amt:
            forward_btn["state"] = "disabled"

        GUI.btm_widgets_list.append(back_btn)
        GUI.btm_widgets_list.append(forward_btn)
        GUI.btm_widgets_list.append(page_lbl)

        back_btn.place(x=prct(10, width), y=prct(40, height))
        forward_btn.place(x=prct(32, width), y=prct(40, height))
        his_btn.place(x=prct(80, width), y=prct(40, height))

        GUI.select_web = StringVar(value="None")
        block_weblist = list(map(lambda web: web.split()[1], GUI.blocked_webs[(GUI.page_num - 1) * 5 : GUI.page_num * 5]))
        GUI.y_place = 6 
        for b_web in block_weblist:
            web_rbtn = Radiobutton(location, text=b_web, value=b_web,
                                   variable=GUI.select_web, indicator=0, font=("Poppins", 10),
                                   width=30, background ="light blue", selectcolor="light green",
                                   command= lambda: GUI.set_unblocktest(location, GUI.select_web.get(), GUI.btm_widgets_list))
            web_rbtn.place(x=prct(30, width), y=prct(GUI.y_place, height))
            GUI.btm_widgets_list.append(web_rbtn)
            GUI.y_place += 5

    @staticmethod
    def set_unblocktest(location, url, btn_list):
        test_btn = Button(location, text="Coba website", command=lambda:cm.test_web(url))
        unblock_btn = Button(location, text="Unblock", command=lambda:cm.unblock_command(url, GUI, location))
        test_btn.place(x=prct(60, width), y=prct(40, height))
        unblock_btn.place(x=prct(45, width), y=prct(40, height))
        btn_list.append(test_btn)
        btn_list.append(unblock_btn)


    @staticmethod
    def main_closing(main_GUI):
        with open("history.txt", "w") as file:
            for web in GUI.block_history.queue:
                file.write(web)
                file.write("\n")
        main_GUI.destroy()