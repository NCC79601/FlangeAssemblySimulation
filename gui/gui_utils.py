import json
import tkinter as tk
from math import cos, sin, pi, atan2
import os
current_path = os.path.join(os.path.abspath(__file__), '..')

def get_current_path():
    return current_path

def load_default_input():
    file_path = os.path.join(current_path, 'default_input.json')
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_default_input(data):
    with open(os.path.join(current_path, 'default_input.json'), 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True, separators=(', ', ': '))
    return

def draw_pie(canvas, x, y, radius, start_angle, end_angle, color):
    canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=start_angle, extent=end_angle - start_angle, fill=color)

def draw_line(canvas, p1: tuple, p2: tuple, color):
    canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

def draw_text(canvas, x, y, text, color='black', text_size=12):
    return canvas.create_text(x, y, text=text, fill=color, font=("微软雅黑", text_size))

def create_output_box(canvas, x, y, width, height):
    output_box = tk.Text(canvas, width=width, height=height, state='disabled', font=('consolas', 10))
    output_box.place(x=x, y=y)
    return output_box

def draw_hexagon(canvas, x, y, side_length, color):
    angle = 60
    points = []
    for i in range(6):
        angle_rad = (angle * i) * pi / 180
        point_x = x + side_length * cos(angle_rad)
        point_y = y + side_length * sin(angle_rad)
        points.append((point_x, point_y))
    canvas.create_polygon(points, fill=color)

def update_output_box(output_box, text):
    output_box.config(state='normal')
    output_box.delete('1.0', 'end')
    output_box.insert('end', text)
    output_box.config(state='disabled')
    return output_box

def draw_vector(canvas, x1, y1, x2, y2, color='black', thickness=1):
    return canvas.create_line(x1, y1, x2, y2, fill=color, arrow=tk.LAST, width=thickness)