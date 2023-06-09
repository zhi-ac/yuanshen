# 姓名 zzs
# 时间： 2023/5/28 15:41
import cv2
from skimage.metrics import structural_similarity as ssim
import pyautogui
import numpy as np
import keyboard
import time
import threading
import tkinter as tk
from tkinter import ttk
import winsound

#关闭鼠标在边界时检测
pyautogui.FAILSAFE = False

# 定义一个全局变量，用于表示当前是否暂停
paused = False

# 滚轮图标的中心位置和长宽
mul_x = 1062  # 中心点 x 坐标
mul_y = 539  # 中心点 y 坐标
mul_width = 24  # 矩形区域的宽度
mul_height = 44  # 矩形区域的高度

#聊天图标
chat_x = 1189  # 中心点 x 坐标
chat_y = 538  # 中心点 y 坐标
chat_width = 22  # 矩形区域的宽度
chat_height = 7  # 矩形区域的高度

# F图标
f_x = 1118  # 中心点 x 坐标
f_y = 537  # 中心点 y 坐标
f_width = 20  # 矩形区域的宽度
f_height = 22  # 矩形区域的高度

#开关键
switch = 'h'

#是否开启提示音
prompt_tone_switch = 1




# 加载滚轮图片
mul_reference_image = cv2.imread('image\\mulImage.png')
# 加载聊天图片
chat_reference_image = cv2.imread('image\\chatImage.png')
chat_reference_image_1 = cv2.imread('image\\chatImage1.png')
# 加载F图片
f_reference_image = cv2.imread('image\\fimage.png')

# 将图片转换为灰度图像
chat_gray_reference = cv2.cvtColor(chat_reference_image, cv2.COLOR_BGR2GRAY)
chat_1_gray_reference = cv2.cvtColor(chat_reference_image_1, cv2.COLOR_BGR2GRAY)
f_gray_reference = cv2.cvtColor(f_reference_image, cv2.COLOR_BGR2GRAY)
mul_gray_reference = cv2.cvtColor(mul_reference_image, cv2.COLOR_BGR2GRAY)

# 设置图片相似度阈值
f_similarity_threshold = 0.5
mul_similarity_threshold = 0.3
chat_similarity_threshold = 0.5
chat_1_similarity_threshold = 0.3

# 定义按下h键时的回调函数
def on_g_key(event):
    global paused
    if event.name.lower() == switch.lower():
        paused = not paused
        if paused:
            if prompt_tone_switch == 1:
                winsound.Beep(100, 100)  # 播放100Hz的声音，持续0.1秒钟
            top.withdraw()  # 隐藏窗口
        else:
            if prompt_tone_switch == 1:
                winsound.Beep(200, 100)
            top.deiconify()  # 显示窗口

# 实时截取图片的代码  替换掉了
def mul_capture_image():
    # 获取屏幕的尺寸
    screen_width, screen_height = pyautogui.size()
    # 计算截图区域的左上角和右下角坐标
    left = max(0, mul_x - mul_width // 2)
    top = max(0, mul_y - mul_height // 2)
    right = min(screen_width, left + mul_width)
    bottom = min(screen_height, top + mul_height)
    # time.sleep(5)
    # 使用 PyAutoGUI 进行屏幕截图
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    # screenshot.save("2.png")
    # 将截图转换为 OpenCV 格式
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    return image

#截取屏幕上的聊天和F图标
def chat_f_capture_image():
    # 获取屏幕的尺寸
    screen_width, screen_height = pyautogui.size()
    # 截取屏幕
    screenshot = pyautogui.screenshot()
    new_width = 1920
    new_height = 1080
    screenshot = screenshot.resize((new_width, new_height))
    # 计算截图区域的左上角和右下角坐标
    x1 = chat_x - (chat_width >> 1)
    y1 = chat_y - (chat_height >> 1)
    x2 = x1 + chat_width
    y2 = y1 + chat_height
    chat_image = np.array(screenshot.crop((x1, y1, x2, y2)))

    x1 = f_x - (f_width >> 1)
    y1 = f_y - (f_height >> 1)
    x2 = x1 + f_width
    y2 = y1 + f_height
    f_image = np.array(screenshot.crop((x1, y1, x2, y2)))

    chat_image = cv2.cvtColor(chat_image, cv2.COLOR_RGB2BGR)
    f_image = cv2.cvtColor(f_image, cv2.COLOR_RGB2BGR)
    return chat_image, f_image

def mul_isSimilar(image):
    # 将实时截取的图片调整为参考图片的尺寸
    image = cv2.resize(image, mul_reference_image.shape[:2][::-1])


    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算结构相似性指数
    ssim_score, _ = ssim(mul_gray_reference, gray_image, full=True)

    # print(ssim_score)

    # 判断相似度是否高于阈值
    if ssim_score > mul_similarity_threshold:
        return True
    else:
        return False


def chat_isSimilar(image):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算结构相似性指数
    ssim_score, _ = ssim(chat_gray_reference, gray_image, full=True)

    # print(ssim_score)

    # 判断相似度是否高于阈值
    if ssim_score > chat_similarity_threshold:
        return True
    else:
        return False

def chat_isSimilar1(image):

    # 将图片转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算结构相似性指数
    ssim_score, _ = ssim(chat_1_gray_reference, gray_image, full=True)

    # print(ssim_score)

    # 判断相似度是否高于阈值
    if ssim_score > chat_1_similarity_threshold:
        return True
    else:
        return False

def f_isSimilar(image):

    # 将图片转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算结构相似性指数
    ssim_score, _ = ssim(f_gray_reference, gray_image, full=True)

    # print(ssim_score)

    # 判断相似度是否高于阈值
    if ssim_score > f_similarity_threshold:
        return True
    else:
        return False

# 实时截取图片的代码
def mul():

    # 实时截取图片并进行相似度比较
    # 截取屏幕  将截取到的图片分辨率调整为1920 * 1080
    screenshot = pyautogui.screenshot()
    new_width = 1920
    new_height = 1080
    screenshot = screenshot.resize((new_width, new_height))
    # 计算截图区域的左上角和右下角坐标
    x1 = mul_x - (mul_width >> 1)
    y1 = mul_y - (mul_height >> 1)
    x2 = x1 + mul_width
    y2 = y1 + mul_height
    image = np.array(screenshot.crop((x1, y1, x2, y2)))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 调用 isSimilar 函数进行相似度比较
    if mul_isSimilar(image):
        return True
    else:
        return False

# 定义任务C的操作
def task_c():
    while True:
        if paused:
            time.sleep(0.1)
        elif not paused:
            # 执行任务C的操作
            result_c = mul()

            # 根据任务C的结果进行相应操作
            if result_c:
                mulF()
            # 可以在任务C执行的适当位置添加等待时间，以控制任务C的执行频率
            time.sleep(0.1)

#不断点击F
def mulF():
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')
    # 向下滚动鼠标
    pyautogui.scroll(-1)
    keyboard.press('f')
    keyboard.release('f')


def task_one():
    while True:
        if paused:
            time.sleep(0.1)
        elif not paused:
            chat_image, f_image = chat_f_capture_image()
            result_chat, result_chat_1, result_f = chat_isSimilar(chat_image), chat_isSimilar1(chat_image), f_isSimilar(f_image)
            if (not (result_chat or result_chat_1)) and result_f:
                keyboard.press('f')
                keyboard.release('f')
            time.sleep(0.1)



def read_data():
    # global f_x, f_y, chat_x, chat_y, mul_x, mul_y
    # 从文件中读取数据
    global switch
    global prompt_tone_switch
    with open("config\\autoconfig.txt", "r") as file:
        data = file.readlines()
        switch = data[0].strip() if len(data) > 0 else ""
        prompt_tone_switch = int(data[1].strip()) if len(data) > 1 else 1
    # 在界面上显示默认值
    #F图标
    switch_entry.delete(0, tk.END)
    switch_entry.insert(0, switch)
    checkbox_var.set(prompt_tone_switch)

def update_data():
    global switch, prompt_tone_switch
    switch = switch_entry.get()
    prompt_tone_switch = checkbox_var.get()
    with open("config\\autoconfig.txt", "w") as file:
        file.write(switch + "\n")
        file.write(str(prompt_tone_switch))
    # result_label.config(text=f"更新成功")

def start_data():

    # 隐藏所有控件
    switch_label.place_forget()
    switch_entry.place_forget()
    checkbox.place_forget()
    output_button.place_forget()
    result_label.place_forget()
    # 显示启动中的文本
    loading_label = ttk.Label(window, text="启动成功...")
    loading_label.place(relx=0.5, rely=0.5, anchor="center")

    #开关键
    global switch
    switch = switch_entry.get()

    # 注册按下键盘事件的回调函数
    global prompt_tone_switch
    prompt_tone_switch = checkbox_var.get()
    update_data()
    keyboard.on_press(on_g_key)
    # 启动线程执行任务C
    thread1 = threading.Thread(target=task_c)
    thread1.daemon = True
    thread1.start()
    thread2 = threading.Thread(target=task_one)
    thread2.daemon = True
    thread2.start()

    top.deiconify()  # 显示窗口
# 创建主窗口
window = tk.Tk()
window.title("原神自动拾取功能")
window.geometry("600x400")

# 创建Canvas组件并设置背景图片
canvas = tk.Canvas(window, width=600, height=400)
bg_image = tk.PhotoImage(file="image\\background.png")
canvas.create_image(0, 0, anchor="nw", image=bg_image)
canvas.pack()

# 创建F图标的标签和输入框
#x坐标
switch_label = ttk.Label(window, text="开关键:")
switch_label.place(x=50, y=50)
switch_entry = ttk.Entry(window)
switch_entry.place(x=150, y=50)

checkbox_var = tk.IntVar(value=True)
checkbox = tk.Checkbutton(window, text="是否开启提示音", variable=checkbox_var)
checkbox.place(x=150, y=100)

# 创建输出按钮
output_button = ttk.Button(window, text="启动", command=start_data)
output_button.place(x=150, y=200)

#y坐标
copyright_label = ttk.Label(window, text="Copyright © 2023 small郑")
copyright_label.place(x=150, y=350)

# 创建结果标签
result_label = ttk.Label(window, text="")
result_label.place(x=50, y=150)

# 读取默认数据
read_data()

# 提示窗口
top = tk.Toplevel()
top.overrideredirect(True)  # 隐藏标题栏和边框
x = window.winfo_screenwidth() - 60
top.geometry("60x20+" + str(x) + "+100")
label = tk.Label(top, text="自动拾取")
label.pack()
top.attributes('-topmost', True)  # 将窗口置于屏幕的最顶层
top.withdraw()  # 初始状态下隐藏窗口

# 启动 Tkinter 主循环
window.mainloop()


