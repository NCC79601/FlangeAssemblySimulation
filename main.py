import os
import csv
import datetime
import postprocess
import numpy as np
from guider import get_torque_correction
from convert import pretension_to_torque, torque_to_pretension
import comm
from colorama import Fore, Back, Style
from tqdm import tqdm

comm.init()

torque = np.array([4, 4, 4, 4, 4, 4])
pretension = list(torque_to_pretension(np.array(torque)))

iter_num = 20

now = datetime.datetime.now()
formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")
result_dir = 'results/' + 'test_' + formatted_now
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
csv_file = open(os.path.join(result_dir, 'results.csv'), 'w', newline='')
csv_writer = csv.writer(csv_file)
labels = ['A', 'B', 'C', 'D', 'E', 'F']
csv_writer.writerow([f'torque_{label}' for label in labels]
                  + ['concentricity', 'deflect_x', 'deflect_y'])

for i in tqdm(range(iter_num)):
    print(Fore.YELLOW + f' test ' + Fore.BLACK + Back.YELLOW + f' #{i + 1} ' + Style.RESET_ALL)

    print(f'torque: {torque}')

    result_dir = comm.ansys_test(pretension)
    concentricity, deflect_vector = postprocess.get_concentricity(data_dir=result_dir, enable_drawing=False)

    torque_correction, _ = get_torque_correction(deflect_vector)

    torque = torque + torque_correction

    # Write the results to the CSV file
    csv_writer.writerow([*torque] + [concentricity, deflect_vector[0], deflect_vector[1]])

    print(Fore.GREEN + f'test #{i + 1} complete.' + Style.RESET_ALL)

comm.close()

