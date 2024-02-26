import os
import serial
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import threading

window = tk.Tk()
window.title('键盘插拔（多设备）v1.0')
window.geometry('430x130')
window.resizable(False, False)
# window.iconbitmap("32.ico")

ser = serial.Serial()
# ser.setDTR(True)
ser.baudrate = 115200
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.timeout = 0.5

kb_in = '68 08 00 FF 15 0F 23 16'
kb_out = '68 08 00 FF 15 00 14 16'
run_times = 0
choose_port = 'default'
pad_choose_device = "default"
input_times_1 = 0
input_verify_time = -1
input_wait_time = -1

path = tk.StringVar()
path.set(os.path.abspath("."))

input_result_path = 'default'

kb_in_hex = bytes.fromhex(kb_in)
kb_out_hex = bytes.fromhex(kb_out)

input_device = []
pad_input_device = []


# 判断是否是数字
def CheckValid(input):
    if input == "":
        return True
    else:
        return input.isdigit()  # 判断是否是数字,只有为True,Entry 才会显示输入在字符


times_check_valid_1 = window.register(CheckValid)
times_isnum_1 = tk.StringVar()

use_time_check_valid = window.register(CheckValid)
wait_time_check_valid = window.register(CheckValid)
use_time_isnum = StringVar()
wait_time_isnum = StringVar()

tips_str = StringVar()


# 串口
def find_port():
    port_list = []
    ret = os.popen('python -m serial.tools.list_ports').readlines()
    # print('ret={}'.format(ret))
    if 'no ports found' in ret:
        print('未识别到串口...')
        return port_list
    else:
        for n in ret:
            if '\tfound\n' not in n:
                port_1 = str(n).strip()
                # adb = str(n).split('\n')[0].strip()
                # adb = str(n).strip().split('\tdevice')[0].strip()
                port_list.append(str(port_1))
        # print('adb设备数量={}，adb_list={}'.format(len(adb_list), adb_list))
        return port_list


# print(find_port())


# 获取串口事件绑定
def port_choose_method(event):
    # 选中事件
    # print('选中的数据:{}'.format(combobox.get()))
    # print('value的值:{}'.format(value.get()))
    global choose_port
    choose_port = port_value.get()


# 线程
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !
    # t.setDaemon(True)废弃
    t.daemon = True
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()


name_pad_date_1 = '0'


def click_events(btn_num):
    # 验证串口
    if choose_port == 'default':
        tk.messagebox.showinfo(title='空值提示', message='请选择串口！')
        return False

    # 执行次数
    global input_times_1
    input_times_1 = e03.get()
    if input_times_1 == '':
        tk.messagebox.showinfo(title='空值提示', message='请输入执行次数！')
        return False
    elif int(input_times_1) > 0:
        pass
    else:
        tk.messagebox.showinfo(title='非法值提示', message='执行次数请输入大于0的整数！')
        return False

    # 验证时长
    global input_verify_time
    input_verify_time = use_time_pack.get()
    if input_verify_time == '':
        tk.messagebox.showinfo(title='空值提示', message='请输入验证时长！')
        return False
    elif int(input_verify_time) >= 0:
        pass
    else:
        tk.messagebox.showinfo(title='非法值提示', message='验证时长请输入大于等于0的整数！')
        return False

    # 电磁铁冷却时长
    global input_wait_time
    input_wait_time = wait_time_pack.get()
    if input_wait_time == '':
        tk.messagebox.showinfo(title='空值提示', message='请输入电磁铁冷却时长！')
        return False
    elif int(input_wait_time) >= 2:
        pass
    else:
        tk.messagebox.showinfo(title='非法值提示', message='电磁铁冷却时长请输入大于1的整数！')
        return False

    ser.port = choose_port
    ser.open()
    status = ser.isOpen()
    print("Serial Port Status is", status)

    global run_times
    run_times = 0

    debug = True
    # if debug:
    try:
        for x in range(int(input_times_1)):
            run_times += 1
            print(run_times)

            tips_str.set('正在执行第{}次接入键盘！'.format(run_times))

            kb_in_result = ser.write(kb_in_hex)

            time.sleep(1.5)

            time.sleep(int(input_verify_time))

            tips_str.set('正在执行第{}次拔出键盘！'.format(run_times))

            kb_out_result = ser.write(kb_out_hex)

            time.sleep(int(input_wait_time))


    # **************************************************************************************************

    except Exception as e_result:
        print("%s" % e_result)
    else:
        print("正常执行")
    finally:
        tips_str.set('已完成{}次键盘插拔！'.format(run_times))

    print('Code is finished!')
    # ser.setDTR(False)
    ser.close()
    status = ser.isOpen()
    print("Serial Port Status is", status)


# def getevent_btn():
#     getevent()

def bright_btn():
    btn_num = 1
    click_events(btn_num)


def port_refresh():
    input_port = find_port()
    if len(input_port) > 0:
        # port_value.set(input_port[0])
        port_value.set('')
    else:
        port_value.set("未识别到串口")
    # port_value.set('')
    global choose_port
    choose_port = 'default'
    port_combobox.configure(values=input_port)


# ***************************************************************************************

# *****串口*******************************************************
father_frm1 = tk.Frame(window)
father_frm1.grid(row=1, column=1, padx=5, pady=5)

# refresh_pic = PhotoImage(file=r'img/refresh.png')
# Button(father_frm1, image=refresh_pic, border='0', command=lambda: thread_it(refresh_btn)).grid(row=1, column=0, padx=5, pady=5)

l01 = tk.Label(father_frm1, text='串口：')
l01.grid(row=1, column=1, padx=5, pady=5)

# ***串口选择框***********************************
port_value = tk.StringVar()
port_value.set('')
# port_values = input_port
port_combobox = ttk.Combobox(
    master=father_frm1,  # 父容器
    height=5,  # 高度,下拉显示的条目数量
    width=11,  # 宽度
    state="readonly",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
    cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
    # font=("", 20), # 字体
    textvariable=port_value,  # 通过StringVar设置可改变的值
    # values=port_values, # 设置下拉框的选项
    # values=[],
    postcommand=lambda: port_refresh()
)
# 绑定
port_combobox.bind('<<ComboboxSelected>>', port_choose_method)
# print(combobox.keys()) # 可以查看支持的参数
port_combobox.grid(row=1, column=2, padx=5, pady=5)

# *********************************************************************


l03 = tk.Label(father_frm1, text='执行次数：')
l03.grid(row=1, column=3, padx=5, pady=5)

e03 = tk.Entry(father_frm1, width=6, show=None, textvariable=times_isnum_1, validate="key",
               validatecommand=(times_check_valid_1, '%P'))
e03.grid(row=1, column=4, padx=5, pady=5)

# ***验证时长***********************************************************
tk.Label(father_frm1, text='验证时长：').grid(row=1, column=5, padx=5, pady=5)

use_time_pack = tk.Entry(father_frm1, width=4, show=None, textvariable=use_time_isnum, validate="key",
                         validatecommand=(use_time_check_valid, '%P'))  # show = None：输入字符可见， show = '*':
use_time_pack.grid(row=1, column=6, padx=5, pady=5)

father_frm2 = tk.Frame(window)
father_frm2.grid(row=2, column=1, padx=5, pady=5)

tk.Label(father_frm2, text='电磁铁冷却时长：').grid(row=1, column=1, padx=5, pady=5)

wait_time_pack = tk.Entry(father_frm2, width=5, show=None, textvariable=wait_time_isnum, validate="key",
                          validatecommand=(wait_time_check_valid, '%P'))  # show = None：输入字符可见， show = '*':
wait_time_pack.grid(row=1, column=2, padx=5, pady=5)

tk.Button(father_frm2, text="开始插拔", width=14, command=lambda: thread_it(bright_btn)).grid(row=1, column=3, padx=10,
                                                                                              pady=5)

father_frm3 = tk.Frame(window)
father_frm3.grid(row=3, column=1, padx=5, pady=5)

tips = tk.Label(father_frm3, textvariable=tips_str, fg='red')
tips.grid(row=1, column=1, padx=5, pady=0)

window.mainloop()
