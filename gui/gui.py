from .gui_utils import *
import tkinter as tk
from math import cos, sin, pi
import numpy as np
import json
import os
current_path = os.path.join(os.path.abspath(__file__), '..')

with open(os.path.join(current_path, 'gui_config.json'), 'r') as f:
    config = json.load(f)

    canvas_width     = config['canvas_width']
    canvas_height    = config['canvas_height']

    radius           = config['radius']
    label_radius     = config['label_radius']
    input_box_radius = config['input_box_radius']
    screw_radius     = config['screw_radius']
    screw_hexagon_side_length = config['screw_hexagon_side_length']
    input_box_width  = config['input_box_width']
    input_box_height = config['input_box_height']
    button_width     = config['button_width']
    button_height    = config['button_height']

angles = [(-i - 2) * 60 for i in range(6)]
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
labels = ['A', 'B', 'C', 'D', 'E', 'F']
default_distances = [40, 50, 60]

class GUI:
    def __init__(self):
        # do nothing
        pass

    def init(self, concentricity_provider = None, guide_provider = None):
        self.concentricity_provider = concentricity_provider
        self.guide_provider = guide_provider

        self.root = tk.Tk()
        current_path = os.path.join(get_current_path(), '..', 'resources')
        ico_path = os.path.join(current_path, 'smile.ico')
        self.root.iconbitmap(ico_path)
        self.root.resizable(False, False)
        self.root.title("法兰装配辅助工具 by zhw & lcx")

        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.input_boxes = []  # List to store the input boxes
        self.vector_elements = []  # List to store the vector elements
        self.output_element = None

        # draw the outer frame
        draw_line(self.canvas, (300, 80), (300, 400 - 60), 'grey')
        draw_line(self.canvas, (600, 80), (600, 400 - 60), 'grey')
        draw_line(self.canvas, (20, 350), (canvas_width - 20, 350), 'grey')

        # show a png
        image = tk.PhotoImage(file="./resources/illustration.png")
        resized_image = image.subsample(5)  # Change the subsample value to adjust the size
        self.canvas.create_image(150, 500, image=resized_image)

        # draw concentricity output box
        draw_text(self.canvas, 450, 370, "同轴度输出", 'black', 14)
        self.output_box = create_output_box(self.canvas, 320, 390, 38, 6)
        self.output_box = update_output_box(self.output_box, "Waiting for input...")

        # draw screws
        self.screw_text_element = []
        center_x = 750
        center_y = 500
        self.screw_center = (center_x, center_y)
        # draw coordinate axis
        draw_vector(self.canvas, center_x - 140, center_y, center_x + 140, center_y, color='grey')
        draw_vector(self.canvas, center_x, center_y + 140, center_x, center_y - 140, color='grey')
        for i, angle in enumerate(angles):
            start_angle = angles[i]
            end_angle = angles[i] + 60
            screw_x = center_x + screw_radius * cos((start_angle + end_angle) / 2 * pi / 180)
            screw_y = center_y - screw_radius * sin((start_angle + end_angle) / 2 * pi / 180)
            draw_hexagon(self.canvas, screw_x, screw_y, screw_hexagon_side_length, colors[i])
            draw_text(self.canvas, screw_x, screw_y, labels[i], 'black', 14)
        self.draw_screws_texts(['-' for i in range(6)])
        
        # draw legends
        draw_vector(self.canvas, 700, 660, 720, 660, color='magenta', thickness=3)
        draw_text(self.canvas, 800, 660, "当前偏向", 'magenta', 12)
        draw_vector(self.canvas, 700, 680, 720, 680, color='cyan', thickness=3)
        draw_text(self.canvas, 800, 680, "拧后变化方向", 'cyan', 12)

        # draw final output
        self.draw_final_output()

        # draw sections
        for section_id in range(3):
            center_x = 150 + section_id * 300
            center_y = 200

            # draw title
            draw_text(self.canvas, center_x, 20, f"截面 #{section_id + 1}", text_size=16, color='black')

            # draw input boxes for section distances to the upper face of upper section
            input_box = tk.Entry(self.root)
            draw_text(self.canvas, center_x - 50, 50, "距离:")
            draw_text(self.canvas, center_x + 50, 50, "mm")
            input_box.place(x=center_x - input_box_width + 10,
                    y=50 - input_box_height / 2,
                    width=input_box_width * 1.5, height=input_box_height)
            self.input_boxes.append(input_box)

            # draw pie chart
            for i in range(len(angles)):
                start_angle = angles[i]
                end_angle = angles[i] + 60
                draw_pie(self.canvas, center_x, center_y, radius, start_angle, end_angle, colors[i])

            # draw labels
            for i in range(len(angles)):
                start_angle = angles[i]
                end_angle = angles[i] + 60
                label_x = center_x + label_radius * cos((start_angle + end_angle) / 2 * pi / 180)
                label_y = center_y - label_radius * sin((start_angle + end_angle) / 2 * pi / 180)
                text = self.canvas.create_text(label_x, label_y, text=labels[i], font=('Arial', 16))
                self.canvas.tag_raise(text)  # Raise the text element to the top layer

            # draw split lines
            for i in range(len(angles)):
                start_point = (center_x, center_y)
                end_point = (center_x + input_box_radius * cos(angles[i] * pi / 180), center_y + input_box_radius * sin(angles[i] * pi / 180))
                draw_line(self.canvas, start_point, end_point, 'black')

            # draw input boxes at split lines
            for i in range(len(angles)):
                start_angle = angles[i]
                end_angle = angles[i] + 60
                # Create and place the input box next to the label
                input_box = tk.Entry(self.root)
                input_box.place(x=center_x + input_box_radius * cos((start_angle + end_angle - 60) / 2 * pi / 180) - input_box_width / 2,
                                y=center_y - input_box_radius * sin((start_angle + end_angle - 60) / 2 * pi / 180) - input_box_height / 2,
                                width=input_box_width, height=input_box_height)
                self.input_boxes.append(input_box)  # Add the input box to the list
        
        # set default values for all input boxes
        default_input = load_default_input()
        if default_input == None or default_input == []:
            default_input = [0 for i in range(len(self.input_boxes))]
        for i in range(len(self.input_boxes)):
            self.input_boxes[i].insert(0, default_input[i])

        # Create and place the button
        calc_button = tk.Button(self.root, text="计算", command=self.calc_button_click_hander, bg="green", fg="white")
        calc_button.place(x=canvas_width/2-button_width/2 - 50, y=canvas_height-50+button_height/2, width=button_width, height=button_height)
        save_button = tk.Button(self.root, text="保存输入", command=self.save_button_click_hander)
        save_button.place(x=canvas_width/2-button_width-10 + 100, y=canvas_height-50+button_height/2, width=button_width, height=button_height)

        self.root.mainloop()
    
    def draw_screws_texts(self, screw_text = ['紧' for i in range(6)]):
        # draw screws
        center_x = 750
        center_y = 500

        if len(self.screw_text_element) > 0:
            for element in self.screw_text_element:
                self.canvas.delete(element)
        self.screw_text_element = []
        for i, angle in enumerate(angles):
            start_angle = angles[i]
            end_angle = angles[i] + 60
            screw_text_x = center_x + (screw_radius + 40) * cos((start_angle + end_angle) / 2 * pi / 180)
            screw_text_y = center_y - (screw_radius + 40) * sin((start_angle + end_angle) / 2 * pi / 180)
            text = screw_text[i]
            text_element = draw_text(self.canvas, screw_text_x, screw_text_y, screw_text[i], 'red' if text == '紧' else ('green' if text == '松' else 'black'), 12)
            self.screw_text_element.append(text_element)
    
    def draw_final_output(self, output_text = '等待中...'):
        if self.output_element is not None:
            self.canvas.delete(self.output_element)
        self.output_element = draw_text(self.canvas, canvas_width / 2, canvas_height - 120, output_text, 'black', 20)
    
    def get_input_data(self):
        input_data = []
        for input_box in self.input_boxes:
            try:
                float(input_box.get())
            except ValueError:
                self.output_box = update_output_box(self.output_box, "[ERROR] Input must be a number!")
                return None
            input_data.append(float(input_box.get()))
        return input_data
    
    def calc_button_click_hander(self):
        input_data = self.get_input_data()
        if input_data is None:
            return

        data = [
            {
                'dis_to_up_up': input_data[0] * 1e-3,
                'readings': [input_data[i] * 1e-6 for i in range(1, 1 + 6)]
            },
            {
                'dis_to_up_up': input_data[7] * 1e-3,
                'readings': [input_data[i] * 1e-6 for i in range(8, 8 + 6)]
            },
            {
                'dis_to_up_up': input_data[14] * 1e-3,
                'readings': [input_data[i] * 1e-6 for i in range(15, 15 + 6)]
            }
        ]

        if self.concentricity_provider is None or self.guide_provider is None:
            return
        
        concentricity, deflect_vector = self.concentricity_provider(data)
        self.output_box = update_output_box(self.output_box, f"concentricity:\n{concentricity * 1e3:.4f} mm\n-----\ndeflect_vector:\n{deflect_vector}")
        self.draw_final_output(f'同轴度: {concentricity * 1e3:.4f} mm')

        new_screw_texts, target_deflect_vector, all_deflect_vectors = self.guide_provider(deflect_vector)

        # draw vector map
        for element in self.vector_elements:
            self.canvas.delete(element)  # clear previous vectors
        self.vector_elements = []
        for vector in all_deflect_vectors:
            element = draw_vector(self.canvas, \
                                  self.screw_center[0], \
                                  self.screw_center[1], \
                                  self.screw_center[0] + vector[0] * 100, \
                                  self.screw_center[1] - vector[1] * 100, \
                                  color='grey')
            self.vector_elements.append(element)
        
        # current deflect vector
        normalized_deflect_vector = deflect_vector / np.sqrt(np.sum(deflect_vector ** 2))
        element = draw_vector(self.canvas, \
                              self.screw_center[0], \
                              self.screw_center[1], \
                              self.screw_center[0] + normalized_deflect_vector[0] * 100, \
                              self.screw_center[1] - normalized_deflect_vector[1] * 100, \
                              color='magenta', thickness=3)
        self.vector_elements.append(element)
        #target deflect vector
        element = draw_vector(self.canvas, \
                              self.screw_center[0], \
                              self.screw_center[1], \
                              self.screw_center[0] + target_deflect_vector[0] * 100, \
                              self.screw_center[1] - target_deflect_vector[1] * 100, \
                              color='cyan', thickness=3)
        self.vector_elements.append(element)
        
        # redraw screw texts
        self.draw_screws_texts(new_screw_texts)
    
    def save_button_click_hander(self):
        input_data = self.get_input_data()
        if input_data is None:
            return
        save_default_input(input_data)


if __name__ == '__main__':
    gui = GUI()
    gui.init()
