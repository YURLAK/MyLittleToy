import turtle
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import numpy as np
import re
import sympy as sp
from sympy import Abs, sqrt  # 导入 Abs 和 sqrt

# 创建主窗口
root = tk.Tk()
root.title("函数绘制工具")

functions = []

def add_function():
    function_str = simpledialog.askstring("输入函数", "请输入一个函数解析式，例如 '5*x + 1'")
    if function_str:
        functions.append(function_str)
        function_listbox.insert(tk.END, function_str)
    else:
        messagebox.showerror("错误", "函数解析式不能为空！")

def clear_functions():
    global functions
    functions = []
    function_listbox.delete(0, tk.END)
    turtle.clearscreen()

def parse_expression(expr_str):
    # 替换 sqrt() 和 abs()
    expr_str = re.sub(r'sqrt\(', 'sqrt(', expr_str)
    expr_str = re.sub(r'abs\(', 'Abs(', expr_str)
    return expr_str

def get_max_constant(function_str):
    try:
        expr = sp.sympify(parse_expression(function_str))
        constants = [abs(term.evalf()) for term in expr.as_ordered_terms() if term.is_constant()]
        return max(constants) if constants else 1
    except Exception as e:
        messagebox.showerror("错误", f"解析函数时出错: {e}")
        return 1

def dynamic_tick_spacing(value_range):
    if value_range > 20:
        return 5
    elif value_range > 10:
        return 2
    else:
        return 1

def plot_function():
    if not functions:
        messagebox.showerror("错误", "没有可绘制的函数！")
        return

    screen = turtle.Screen()
    screen.tracer(0)
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()

    # 根据最大常数项调整坐标轴范围
    max_constant = max(get_max_constant(f) for f in functions)
    x_min, x_max = -10, 10
    y_min, y_max = -max_constant * 1.5, max_constant * 1.5
    max_range = max(x_max - x_min, y_max - y_min) / 2
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    x_min, x_max = int(x_mid - max_range), int(x_mid + max_range)
    y_min, y_max = int(y_mid - max_range), int(y_mid + max_range)

    x_tick_spacing = dynamic_tick_spacing(x_max - x_min)
    y_tick_spacing = dynamic_tick_spacing(y_max - y_min)

    x_ticks = np.arange(x_min, x_max + 1, x_tick_spacing)
    y_ticks = np.arange(y_min, y_max + 1, y_tick_spacing)

    screen.setworldcoordinates(x_min, y_min, x_max, y_max)
    screen.title("函数图像绘制")

    pen.color("black")
    pen.pensize(3)

    pen.penup()
    pen.goto(x_min, 0)
    pen.pendown()
    pen.goto(x_max, 0)

    pen.penup()
    pen.goto(0, y_min)
    pen.pendown()
    pen.goto(0, y_max)

    pen.pensize(0.5)

    for i in x_ticks:
        pen.penup()
        pen.goto(i, -0.3)
        pen.pendown()
        pen.goto(i, 0.3)
        pen.penup()
        pen.goto(i, -0.6)
        pen.write(f'{i}', align='center')

    for i in y_ticks:
        pen.penup()
        pen.goto(-0.3, i)
        pen.pendown()
        pen.goto(0.3, i)
        pen.penup()
        pen.goto(-0.6, i)
        pen.write(f'{i}', align='center')

    pen.color("red")
    pen.pensize(2)

    for function_str in functions:
        pen.penup()
        x = np.linspace(x_min, x_max, 1000)
        try:
            # 解析函数表达式
            expr = sp.sympify(parse_expression(function_str))
            y = [float(expr.evalf(subs={'x': xi}).as_real_imag()[0]) for xi in x]  # 取实数部分
        except Exception as e:
            messagebox.showerror("错误", f"无效的函数解析式: {e}")
            screen.bye()
            return

        for i in range(len(x)):
            if y_min <= y[i] <= y_max:
                pen.goto(x[i], y[i])
                pen.pendown()
            else:
                pen.penup()

    screen.update()

def solve_function():
    function_str = simpledialog.askstring("求解函数", "请输入一个函数解析式，例如 '5*x + 1'")
    if not function_str:
        messagebox.showerror("错误", "函数解析式不能为空！")
        return

    try:
        # 解析函数表达式
        expr = sp.sympify(parse_expression(function_str))
        x_values = np.linspace(-10, 10, 1000)
        y_values = np.array([float(expr.evalf(subs={'x': xi}).as_real_imag()[0]) for xi in x_values])  # 取实数部分
        result = simpledialog.askstring("求解", "请输入要求解的值（例如 'x=5' 或 'y=10'）")

        if result.startswith('x='):
            x_value = float(result.split('=')[1])
            y_value = float(expr.evalf(subs={'x': x_value}).as_real_imag()[0])  # 取实数部分
            messagebox.showinfo("结果", f"当x={x_value}时，y={y_value}")
        elif result.startswith('y='):
            y_value = float(result.split('=')[1])
            x_solutions = x_values[np.isclose(y_values, y_value)]
            messagebox.showinfo("结果", f"当y={y_value}时，x={x_solutions}")
        else:
            messagebox.showerror("错误", "无效的输入格式！")
    except Exception as e:
        messagebox.showerror("错误", f"求解失败: {e}")

# 创建功能按钮
add_button = tk.Button(root, text="添加函数", command=add_function)
add_button.pack()

plot_button = tk.Button(root, text="绘制函数", command=plot_function)
plot_button.pack()

clear_button = tk.Button(root, text="清空函数", command=clear_functions)
clear_button.pack()

solve_button = tk.Button(root, text="求解函数", command=solve_function)
solve_button.pack()

# 创建函数列表框
function_listbox = tk.Listbox(root)
function_listbox.pack()

root.mainloop()
