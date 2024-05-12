import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
import json

with open('./config.json', 'r') as config:
    config  = json.load(config)
    used_result_foldername = config['used_result_foldername']

data = pd.read_csv(f'./results/{used_result_foldername}/results.csv')

torque_A      = data['torque_A']
torque_B      = data['torque_B']
torque_C      = data['torque_C']
torque_D      = data['torque_D']
torque_E      = data['torque_E']
torque_F      = data['torque_F']
concentricity = data['concentricity']
deflect_x     = data['deflect_x']
deflect_y     = data['deflect_y']

# vectorize
deflect_vectors = np.column_stack((deflect_x, deflect_y))
deflect_ref = deflect_vectors[0] # 均布预紧力作为参考
deflect_vectors_rlt = deflect_vectors - deflect_ref # 相对的
normalized_deflect_vectors = deflect_vectors_rlt / (np.linalg.norm(deflect_vectors_rlt, axis=1)[:, np.newaxis] + 1e-20)
torque_vectors = np.column_stack((torque_A, torque_B, torque_C, torque_D, torque_E, torque_F))

kdtree = cKDTree(normalized_deflect_vectors)

def get_torque_correction(measured_deflect_vector):
    '''
    return: torque_correction, index_of_nearest_deflect_vector
    '''
    normalized_vector = measured_deflect_vector / np.sqrt(np.sum(measured_deflect_vector ** 2) + 1e-20)  # 归一化测量向量
    print(f'normalized_vector: {normalized_vector}')
    _, index = kdtree.query( - normalized_vector)
    torque_correction_direction = torque_vectors[index].astype('float64')
    # torque_correction_direction -= torque_correction_direction.mean()
    print(f'queried closest deflect_vector (original): {deflect_vectors[index]}')
    print(f'measured deflect_vector: {measured_deflect_vector}')
    torque_correction_coeff = np.dot(deflect_vectors_rlt[index] * 1e5, -measured_deflect_vector * 1e5)
    # torque_correction = torque_correction_coeff * torque_correction_direction
    torque_correction = torque_correction_direction
    return torque_correction, index

def get_normalized_deflect_vector_at_index(index):
    return normalized_deflect_vectors[index]

def get_all_normalized_deflect_vectors():
    return normalized_deflect_vectors

if __name__ == '__main__':
    # plot_all_deflect_vectors()

    test_deflect_vector = np.array([-4.50017143e-06, 1.03921935e-05])
    normalized_test_deflect_vector = test_deflect_vector / np.linalg.norm(test_deflect_vector)

    torque, index = get_torque_correction(test_deflect_vector)
    print(f'Correction torque: {torque} @ index {index}')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    X = normalized_deflect_vectors[:, 0]
    Y = normalized_deflect_vectors[:, 1]
    zeros = np.zeros_like(X)
    ax.quiver(zeros, zeros, X, Y, scale=2, color='blue')

    ax.quiver(0, 0, normalized_test_deflect_vector[0], normalized_test_deflect_vector[1], scale=2, color='red')
    ax.quiver(0, 0, normalized_deflect_vectors[index, 0], normalized_deflect_vectors[index, 1], scale=2, color='green')

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Normalized Deflect Vectors')

    plt.show()