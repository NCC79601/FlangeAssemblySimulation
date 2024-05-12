import numpy as np
from fit import circle_fit
import matplotlib.pyplot as plt

def get_center(readings, phase_offset=0):
    '''
    readings: [A, B, C, D, E, F]
    phase_offset: in radians
    return: xc, yc, r0 (baseline)
    '''
    # 单位均为米
    d = 70e-3
    d0 = d - sum(readings) / 3
    r0 = d0 / 2

    X = np.zeros(6)
    Y = np.zeros(6)

    for i in range(6):
        X[i] = (readings[i] + r0) * np.cos((-i - 2) * np.pi / 3 + phase_offset)
        Y[i] = (readings[i] + r0) * np.sin((-i - 2) * np.pi / 3 + phase_offset)

    xc, yc, _ = circle_fit(X, Y)

    return xc, yc, r0

def get_concentricity(data, phase_offset=0):
    '''
    data: 
    ```
    [
        {
            'dis_to_up_up': ...,
            'readings': [A, B, ...]
        },
        ...
    ]
    ```
    '''
    center_list = []
    for data_pack in data:
        dis_to_up_up = data_pack['dis_to_up_up']
        readings = data_pack['readings']
        xc, yc, _ = get_center(readings)
        center_list.append([xc, yc, dis_to_up_up + 10e-3])
    
    # 定义点的坐标
    points = np.array([*center_list])
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
    return concentricity, deflect_vector

if __name__ == '__main__':
    
    # data = [
    #     {
    #         'dis_to_up_up': 20e-3,
    #         'readings': [2.68e-3, 1.64e-3, 0.96e-3, 1.26e-3, 2.27e-3, 3.01e-3]
    #     },
    #     {
    #         'dis_to_up_up': 40e-3,
    #         'readings': [3.14e-3, 1.41e-3, 0.28e-3, 0.77e-3, 2.45e-3, 3.69e-3]
    #     },
    #     {
    #         'dis_to_up_up': 60e-3,
    #         'readings': [4.59e-3, 2.16e-3, 0.60e-3, 1.28e-3, 3.62e-3, 5.37e-3]
    #     }
    # ]

    data = [
        {
            'dis_to_up_up': 40e-3,
            'readings': [382e-6, 384e-6, 384e-6, 384e-6, 383e-6, 382e-6]
        },
        {
            'dis_to_up_up': 50e-3,
            'readings': [381e-6, 381e-6, 381e-6, 381e-6, 381e-6, 381e-6]
        },
        {
            'dis_to_up_up': 60e-3,
            'readings': [378e-6, 379e-6, 379e-6, 379e-6, 379e-6, 378e-6]
        }
    ]

    get_concentricity(data)
