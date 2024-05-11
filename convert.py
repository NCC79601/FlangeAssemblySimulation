# 预紧力和拧紧力矩的转换

import json
with open('./config.json', 'r') as config:
    config  = json.load(config)
    bolt_diameter = config['bolt_diameter']

def pretension_to_torque(pretension):
    return 0.2 * pretension * bolt_diameter

def torque_to_pretension(torque):
    return 5 * torque / bolt_diameter

if __name__ == '__main__':
    print(f'2100N pretension = {pretension_to_torque(2100)} Nm')
    print(f'5Nm torque = {torque_to_pretension(5)} N')