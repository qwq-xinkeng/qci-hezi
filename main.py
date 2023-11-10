import os
import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector
import math
from tkinter import messagebox
import subprocess
import psutil
import winreg
import threading
import pyperclip
import webbrowser

print('我们的官网:https://ikunshare.link')
print('本软件仅用于学习交流,请勿用于商业用途')

# MySQL数据库信息
db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

cursor = db.cursor()

# 创建主窗口
root = tk.Tk()
root.title("qci盒子---普通用户端")

# 创建标签页
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# 账号页面
share_frame = tk.Frame(notebook)
notebook.add(share_frame, text="账号")

# 列表框
listbox = tk.Listbox(share_frame, selectmode=tk.SINGLE, width=50, height=20)
listbox.pack(side=tk.LEFT, padx=10, pady=10)

# 信息显示区域
info_text = tk.Text(share_frame, height=27, width=50)
info_text.pack(side=tk.RIGHT, padx=10, pady=10)

# 复制按钮
def copy_account():
    selected_item = listbox.get(listbox.curselection())
    username = ""
    password = ""
    for line in selected_item.split('\n'):
        if line.startswith("账户:"):
            username = line.replace("账户:", "")
        if line.startswith("密码:"):
            password = line.replace("密码:", "")
    pyperclip.copy(username)

def copy_password():
    selected_item = listbox.get(listbox.curselection())
    password = ""
    for line in selected_item.split('\n'):
        if line.startswith("密码:"):
            password = line.replace("密码:", "")
    pyperclip.copy(password)

copy_account_button = tk.Button(share_frame, text="复制账户", command=copy_account)
copy_account_button.pack()

copy_password_button = tk.Button(share_frame, text="复制密码", command=copy_password)
copy_password_button.pack()

# 翻页按钮
current_page = 0
total_accounts = 0

def next_page():
    global current_page
    current_page += 1
    update_listbox()
    update_page_label()
    update_page_buttons()

def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        update_listbox()
        update_page_label()
        update_page_buttons()

next_button = tk.Button(share_frame, text="下一页", command=next_page)
next_button.pack()

prev_button = tk.Button(share_frame, text="上一页", command=prev_page)
prev_button.pack()

# 页数标签
page_label = tk.Label(share_frame, text="")
page_label.pack()

def update_page_label():
    page_label.config(text=f"第 {current_page + 1} 页")

def update_page_buttons():
    if current_page == 0:
        prev_button.config(state=tk.DISABLED)
    else:
        prev_button.config(state=tk.NORMAL)

    max_pages = math.ceil(total_accounts / 20)  # 计算最大页数
    if current_page > max_pages:
        next_button.config(state=tk.DISABLED)
    else:
        next_button.config(state=tk.NORMAL)

# 更新列表框中的内容
def update_listbox():
    listbox.delete(0, tk.END)
    offset = current_page * 20  # 每页显示20个条目
    cursor.execute(f"SELECT game_name, app_id, uploader, username, password FROM steam_accounts LIMIT {offset}, 20")
    for (game_name, app_id, uploader, username, password) in cursor:
        data = f"游戏:{game_name} appid:{app_id} 上传者:{uploader}\n账户:{username}\n密码:{password}"
        listbox.insert(tk.END, data)

# 获取账户总数
def get_total_accounts():
    cursor.execute("SELECT COUNT(*) FROM steam_accounts")
    return cursor.fetchone()[0]

total_accounts = get_total_accounts()

# 初始更新列表框中的内容
update_listbox()
update_page_label()
update_page_buttons()

# 显示选中项的详细信息
def show_info(event):
    if listbox.curselection():
        selected_item = listbox.get(listbox.curselection())
        info_text.delete(1.0, tk.END)
        lines = selected_item.split("\n")
        for line in lines:
            info_text.insert(tk.END, line + "\n")
    else:
        info_text.delete(1.0, tk.END)

listbox.bind('<<ListboxSelect>>', show_info)

# 刷新按钮
def refresh():
    total_accounts = get_total_accounts()
    update_listbox()
    update_page_label()
    update_page_buttons()

refresh_button = tk.Button(share_frame, text="刷新", command=refresh)
refresh_button.pack()

# 捐赠账号页面
donate_frame = tk.Frame(notebook)
notebook.add(donate_frame, text="捐献账号")

# 游戏名
game_name_label = tk.Label(donate_frame, text="游戏名:")
game_name_label.grid(row=0, column=0, padx=10, pady=10)

game_name_entry = tk.Entry(donate_frame, width=30)
game_name_entry.grid(row=0, column=1, padx=10, pady=10)

# App ID
appid_label = tk.Label(donate_frame, text="App ID(只能填数字):")
appid_label.grid(row=1, column=0, padx=10, pady=10)

appid_entry = tk.Entry(donate_frame, width=30)
appid_entry.grid(row=1, column=1, padx=10, pady=10)

# 用户名
username_label = tk.Label(donate_frame, text="用户名:")
username_label.grid(row=2, column=0, padx=10, pady=10)

username_entry = tk.Entry(donate_frame, width=30)
username_entry.grid(row=2, column=1, padx=10, pady=10)

# 密码
password_label = tk.Label(donate_frame, text="密码:")
password_label.grid(row=3, column=0, padx=10, pady=10)

password_entry = tk.Entry(donate_frame, width=30)
password_entry.grid(row=3, column=1, padx=10, pady=10)

# 上传者
uploader_label = tk.Label(donate_frame, text="上传者:")
uploader_label.grid(row=4, column=0, padx=10, pady=10)

uploader_entry = tk.Entry(donate_frame, width=30)
uploader_entry.grid(row=4, column=1, padx=10, pady=10)

# QQ
contact_label = tk.Label(donate_frame, text="你的QQ:")
contact_label.grid(row=5, column=0, padx=10, pady=10)

contact_entry = tk.Entry(donate_frame, width=30)
contact_entry.grid(row=5, column=1, padx=10, pady=10)

# 捐献按钮
def donate():
    game_name = game_name_entry.get()
    appid = appid_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    uploader = uploader_entry.get()
    contact = contact_entry.get()

    if not game_name or not appid or not username or not password or not uploader:
        tk.messagebox.showerror("错误", "所有字段都必须填写")
        return

    try:
# 自己写上传逻辑，很简单
        tk.messagebox.showinfo("成功", "捐献成功")

# 清空输入字段

        game_name_entry.delete(0, tk.END)
        appid_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        uploader_entry.delete(0, tk.END)
        contact_entry.delete(0,tk.END)

        refresh()  # 刷新数据库内容

    except mysql.connector.Error as err:
        tk.messagebox.showerror("错误", f"数据库错误: {err}")

donate_button = tk.Button(donate_frame, text="捐献", command=donate)
donate_button.grid(row=6, column=1, padx=10, pady=10)

def get_steam_path():
    try:
        hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam')
        steam_path = winreg.QueryValueEx(hkey, 'SteamPath')[0]
        winreg.CloseKey(hkey)
        return os.path.join(steam_path, "steam.exe")
    except Exception as e:
        messagebox.showerror("错误", f"无法获取Steam安装路径: {e}")
        return None

def login_to_steam():
    steam_path = get_steam_path()
    if steam_path:
        selected_item = listbox.get(listbox.curselection())
        username = ""
        password = ""
        for line in selected_item.split('\n'):
            if line.startswith("账户:"):
                username = line.replace("账户:", "")
            if line.startswith("密码:"):
                password = line.replace("密码:", "")
        
        # 检测并结束 steam.exe 进程
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == 'steam.exe':
                try:
                    process.terminate()
                except psutil.AccessDenied:
                    messagebox.showerror("错误", "无法结束 Steam 进程")
        
    def login_steam_thread():
        login_command = f'"{steam_path}" -login {username} {password}'
        subprocess.Popen(login_command, shell=True)

    steam_login_thread = threading.Thread(target=login_steam_thread)
    steam_login_thread.start()

login_button = tk.Button(share_frame, text="登录Steam", command=login_to_steam)
login_button.pack()

# 官网按钮
def open_web1():
    webbrowser.open("https://ikunshare.link")

open_web1_button = tk.Button(share_frame, text="官网", command=open_web1)
open_web1_button.pack()

root.mainloop()
