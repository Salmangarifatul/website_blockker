from tkinter import *
from tkinter import messagebox
import webbrowser as wb
import requests
from math import ceil
from queue_DS import history_queue
from platform import system

host_path ='C:\Windows\System32\drivers\etc\hosts' 
ip_address = '127.0.0.1'

class commands:
    @staticmethod
    def block_command(web_var, s_lbl, block_btn, GUI_cls, btm_frame):
        website = web_var.get()
        s_lbl["text"] = "Searching..."
        block_btn["state"] = "disabled"
        if website.startswith("www."):
            second_link = website[4:]
        else:
            second_link = website
            website = f"www.{website}"
        if url_check(f"https://{website}") or url_check(f"https://{second_link}"):
            block_web(second_link, GUI_cls, btm_frame, web_var=web_var)
        else:
            messagebox.showerror(title="Website salah!", message="Website input tidak ditemukan")
        s_lbl["text"] = ""
        block_btn["state"] = "normal"


    @staticmethod
    def unblock_command(web, GUI_cls, location):
        GUI_cls.blocked_webs = list(filter(lambda block_web: web not in block_web, GUI_cls.blocked_webs))
        with open(host_path, 'w') as host_file:
            for block_web in GUI_cls.blocked_webs:
                host_file.write(block_web)
        messagebox.showinfo(title="Website unblock!", message="Website ini sekarang sudah diunblock!")
        for widget in GUI_cls.btm_widgets_list:
            widget.place_forget()
        GUI_cls.page_amt = ceil(len(GUI_cls.blocked_webs) / 5)
        if len(GUI_cls.blocked_webs[(GUI_cls.page_num - 1) * 5: GUI_cls.page_num * 5]) == 0:
            GUI_cls.page_num = GUI_cls.page_num - 1 if GUI_cls.page_num != 1 else GUI_cls.page_num
        GUI_cls.create_bottom_frame(location) 

    @staticmethod
    def switch(GUI_cls, location, reset_func, is_forward):

        for widget in GUI_cls.btm_widgets_list:
            widget.place_forget()
        if is_forward:
            GUI_cls.page_num += 1
        else:
            GUI_cls.page_num -= 1
        reset_func(location) 


    @staticmethod
    def test_web(url):
        if url_check(f"https://{url}"):
            wb.open_new(f"https://{url}")
        else:
            wb.open_new(f"https://www.{url}")

    @staticmethod
    def history(hist_btn, GUI_cls, btm_frame):
        hist_btn["state"] = "disabled"
        hist_root = Tk()
        hist_root.title("Histori Pemblokiran")
        hist_root.resizable(0, 0)
        hist_root.geometry("380x268")
        hist_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(hist_btn, hist_root))

        x = 0
        y = 0
        for blocked_web in GUI_cls.block_history.queue:
            block_web_btn = Button(hist_root, text=blocked_web, width=25,
                             bg="cyan", command=lambda blocked_web=blocked_web: block_web(blocked_web, GUI_cls, btm_frame,
                                                                                          protocol=lambda :on_closing(hist_btn, hist_root)))
            block_web_btn.grid(column=x, row=y)
            y += 1
            if y == 10: 
                x += 1
                y = 0



def url_check(url):
    try:
            site_ping = requests.head(url)
            if site_ping.status_code < 400:
                return True
            else:
                return False
    except Exception:
        return False


def get_blocked_web():
    with open(host_path, "r") as file:
        block_list = list(filter(lambda line: False if "#" in line or line.startswith("\n") else True, file.readlines()))
    return block_list


def get_block_history():
    hist_list = history_queue()
    with open("history.txt", "r") as file:
        for line in file.readlines():
            if "\n" in line:
                hist_list.queue.append(line[:-1])
            else:
                hist_list.queue.append(line)
    return hist_list


def on_closing(btn, GUI):
    try:
        btn["state"] = "normal"
        GUI.destroy()
    except Exception as e: 
        GUI.destroy()


def block_web(second_link, GUI_cls, btm_frame, web_var=None, protocol=None):
    website = f"www.{second_link}"
    with open(host_path, 'r+') as host_file:
        file_content = host_file.read()
       
        if website in file_content:
            messagebox.showinfo(title="Website ini sudah diblokir!",
                                message="Domain website yang telah kamu masukkan sudah diblokir.")
        else:
            host_file.write(ip_address + " " + website + " " + second_link + '\n')
            if web_var is not None:
                web_var.set("")
            messagebox.showinfo(title="Website diblokir!", message="Website yang sudah diinputkan sekarang terblock!")
            GUI_cls.block_history.modify(second_link)
            for widget in GUI_cls.btm_widgets_list:
                widget.place_forget()
            GUI_cls.blocked_webs.append(f"{ip_address} {website} {second_link}\n")
            GUI_cls.page_amt = ceil(len(GUI_cls.blocked_webs) / 5)
            GUI_cls.create_bottom_frame(btm_frame) 
        if protocol is not None:
            protocol()