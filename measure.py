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
        X[i] = (readings[i] + r0) * np.cos((i - 1) * np.pi / 3 + phase_offset)
        Y[i] = (readings[i] + r0) * np.sin((i - 1) * np.pi / 3 + phase_offset)

    xc, yc, r = circle_fit(X, Y)

    return xc, yc, r0

def get_concentricity(data, phase_offset=0):
    '''
    data: `[[dis_from_up_up, [A, B, ...]], ...]`
    '''
    # TODO: finish the rest

if __name__ == '__main__':
    readings = list(np.array([100, 200, 300, 200, 100, 0]) * 1e-4)
    xc, yc, r0 = get_center(readings)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_aspect('equal')  # Set x-axis and y-axis to be equal
    ax.axhline(0, color='black')  # 显示x轴
    ax.axvline(0, color='black')  # 显示y轴

    def draw_circle(cx, cy, r, color='black'):
        theta = np.linspace(0, 2 * np.pi, 100)
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        ax.plot(x, y, color=color)
    
    draw_circle(xc, yc, 35e-3)
    draw_circle(0, 0, r0)

    plt.show()
