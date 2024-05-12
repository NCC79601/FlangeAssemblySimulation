import os
import csv
import datetime
import postprocess
import comm
from convert import pretension_to_torque, torque_to_pretension
import itertools
import numpy as np
from colorama import Fore, Back, Style
from tqdm import tqdm

def batch_simulation(lower_torque=3, upper_torque=4, step=1):
    # 生成所有可能的预紧力组合
    valid_torques = range(lower_torque, upper_torque+1, step)
    torques = list(itertools.product(valid_torques, repeat=6))
    pretensions = [list(torque_to_pretension(np.array(torque))) for torque in torques]
    print(f'number of pretension combinations: {len(pretensions)}')
    
    # create a csv to write results
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")
    result_dir = 'results/' + formatted_now
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    csv_file = open(os.path.join(result_dir, 'results.csv'), 'w', newline='')
    csv_writer = csv.writer(csv_file)
    labels = ['A', 'B', 'C', 'D', 'E', 'F']
    csv_writer.writerow([f'torque_{label}' for label in labels]
                      + ['concentricity', 'deflect_x', 'deflect_y'])
    
    simulation_num = 0

    comm.init()

    for i in tqdm(range(len(torques))):
        simulation_num += 1
        print(Fore.YELLOW + f' simulation ' + Fore.BLACK + Back.YELLOW + f' #{simulation_num} ' + Style.RESET_ALL)

        pretension = pretensions[i]
        torque = torques[i]

        print(f'torque: {torque}')

        result_dir = comm.ansys_solve(pretension)
        concentricity, deflect_vector = postprocess.get_concentricity(data_dir=result_dir, enable_drawing=False)

        # Write the results to the CSV file
        csv_writer.writerow([*torque] + [concentricity, deflect_vector[0], deflect_vector[1]])

        print(Fore.GREEN + f'simulation #{simulation_num} complete.' + Style.RESET_ALL)

    csv_file.close()

    comm.ansys_exit()


if __name__ == '__main__':
    batch_simulation(lower_torque=2, upper_torque=5, step=3)
