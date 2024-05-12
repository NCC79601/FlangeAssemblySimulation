# ANSYS 输出结果的后处理模块
import os
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from utils.fit import circle_fit

with open('./config.json', 'r') as config:
    config  = json.load(config)
    top_plane_z = config['top_plane_z']

def extract_csv(data_dir) -> object:
    csv_data = {}
    with open(data_dir, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for i, row in enumerate(reader):
            for j, element in enumerate(row):
                if i == 0:
                    csv_data[element] = []
                else:
                    csv_data[list(csv_data.keys())[j]].append(element)
    return csv_data


def get_section_data(section_id, data_dir):
    '''
    return: X, Y, Z, U, V
    '''
    file_name_x = os.path.join(data_dir, f'截面{section_id}x.csv')
    file_name_y = os.path.join(data_dir, f'截面{section_id}y.csv')

    data_x = extract_csv(file_name_x)
    data_y = extract_csv(file_name_y)
    
    X = np.array(data_x['X坐标 (m)'], dtype=float)
    Y = np.array(data_x['Y坐标 (m)'], dtype=float)
    Z = np.array(data_x['Z坐标 (m)'], dtype=float)
    Z = Z + 90e-3 - top_plane_z
    U = np.array(data_x['定向变形 (m)'], dtype=float)
    V = np.array(data_y['定向变形 (m)'], dtype=float)

    # 计算凸包
    points_2d = np.column_stack((X, Y))
    hull = ConvexHull(points_2d)
    convex_hull_indices = hull.vertices
    
    # 提取凸包上的点
    X_convex = X[convex_hull_indices]
    Y_convex = Y[convex_hull_indices]
    Z_convex = Z[convex_hull_indices]
    U_convex = U[convex_hull_indices]
    V_convex = V[convex_hull_indices]

    return X_convex, Y_convex, Z_convex, U_convex, V_convex


def get_concentricity(data_dir, enable_drawing=False, deform_scale=1, deflect_arrow_scale=1000):
    '''
    return: concentricity, deflect_vector
    '''
    # 截面 1:
    X1, Y1, Z1, U1, V1 = get_section_data(1, data_dir)
    cx1, cy1, r1 = circle_fit(X=X1+deform_scale*U1, Y=Y1+deform_scale*V1)
    cz1 = Z1[0]

    # 截面 2:
    X2, Y2, Z2, U2, V2 = get_section_data(2, data_dir)
    cx2, cy2, r2 = circle_fit(X=X2+deform_scale*U2, Y=Y2+deform_scale*V2)
    cz2 = Z2[0]

    # 截面 3 (最靠下):
    X3, Y3, Z3, U3, V3 = get_section_data(3, data_dir)
    cx3, cy3, r3 = circle_fit(X=X3+deform_scale*U3, Y=Y3+ deform_scale*V3)
    cz3 = Z3[0]

    # 定义点的坐标
    points = np.array([[cx1, cy1, cz1], [cx2, cy2, cz2], [cx3, cy3, cz3]])
    # 拟合线性模型
    x_fit = np.polyfit(points[:, 2], points[:, 0], 1)
    y_fit = np.polyfit(points[:, 2], points[:, 1], 1)
    # 预测z=0和z=0.09时的x和y的值
    z_values = np.array([0, 0.09])
    x_values = np.polyval(x_fit, z_values)
    y_values = np.polyval(y_fit, z_values)
    
    x0, y0, z0 = x_values[0], y_values[0], z_values[0]
    x1, y1, z1 = x_values[1], y_values[1], z_values[1]
    
    # 同轴度计算：
    concentricity  = np.sqrt((x1 - x0)**2 + (y1 - y0)**2) * 2
    deflect_vector = np.array([x1 - x0, y1 - y0])

    print(f'concentricity:  {concentricity * 1e3}')
    print(f'deflect_vector: {deflect_vector}')

    if enable_drawing:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制时用到的工具函数
        def draw_circle(cx, cy, z, r, color='black'):
            theta = np.linspace(0, 2 * np.pi, 100)
            x = cx + r * np.cos(theta)
            y = cy + r * np.sin(theta)
            z = z * np.ones_like(x)
            ax.plot(x, y, z, color=color)
        def draw_cylinder(xc, yc, radius, height, resolution=25, color='gray', alpha=0.5):
            theta = np.linspace(0, 2 * np.pi, resolution)
            z = np.linspace(0, height, resolution)
            Theta, Z = np.meshgrid(theta, z)
            X = radius * np.cos(Theta)
            Y = radius * np.sin(Theta)
            ax.plot_surface(xc + X, yc + Y, Z, color=color, alpha=alpha)

        # 画各个截面
        ax.quiver(X1, Y1, Z1, deform_scale * U1, deform_scale * V1, np.zeros_like(U1), color='red', arrow_length_ratio=0.3)
        draw_circle(cx1, cy1, cz1, r1, color='red')
        ax.scatter(cx1, cy1, cz1, color='red')

        ax.quiver(X2, Y2, Z2, deform_scale * U2, deform_scale * V2, np.zeros_like(U2), color='green', arrow_length_ratio=0.3)
        draw_circle(cx2, cy2, cz2, r2, color='green')
        ax.scatter(cx2, cy2, cz2, color='green')

        ax.quiver(X3, Y3, Z3, deform_scale * U3, deform_scale * V3, np.zeros_like(U3), color='blue', arrow_length_ratio=0.3)
        draw_circle(cx3, cy3, cz3, r3, color='blue')
        ax.scatter(cx3, cy3, cz3, color='blue')
    
        # 绘制参考轴线
        ax.plot([cx3, cx3], [cy3, cy3], [cz1, cz3], color='gray', linestyle='dashed')

        # 绘制实际轴线
        ax.plot(x_values, y_values, z_values)
    
        # 画圆柱
        draw_cylinder(x0, y0, radius=concentricity/2, height=0.09)
        draw_cylinder(x0, y0, radius=0.035, height=0.09, alpha=0.2)

        # 画出偏向箭头：
        ax.quiver(x0, y0, z1, deflect_vector[0] * deflect_arrow_scale, deflect_vector[1] * deflect_arrow_scale, 0, color='red', arrow_length_ratio=0.3, linewidth=2)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()
    
    return concentricity, deflect_vector


if __name__ == '__main__':
    deform_scale = 1

    data_dir = 'D:/学习/课程/设计与制造2/大作业/仿真/法兰仿真/falanA-A_files/user_files/1'
    
    get_concentricity(data_dir, enable_drawing=True, deform_scale=deform_scale)