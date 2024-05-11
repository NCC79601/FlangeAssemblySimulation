# 拟合模块
import numpy as np

def circle_fit(X, Y):
    '''
    X: np.array, x坐标
    Y: np.array, y坐标
    return: center_x, center_y, radius
    '''
    A = np.column_stack((X, Y, np.ones_like(X)))
    b = X**2 + Y**2
    x = np.linalg.lstsq(A, b, rcond=None)[0]
    center_x, center_y = x[:2] / 2
    radius = np.sqrt(center_x**2 + center_y**2 + x[2])
    return center_x, center_y, radius