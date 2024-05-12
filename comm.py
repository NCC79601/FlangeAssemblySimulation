# 通信模块，用于与 ANSYS 程序进行通信

import socket
import json

client_socket = None
ansys_running = False

def init():
    with open('./config.json', 'r') as config:
        config  = json.load(config)
        port    = config['comm_port']
        timeout = config['comm_timeout']

    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', port))
    client_socket.settimeout(timeout)
    print(f'已连接至 ANSYS 程序')
    ansys_running = True

    try:
        welcome_message = client_socket.recv(1024).decode()
        print(welcome_message)
    except socket.timeout:
        print("Connection timed out. Please try again later.")
        exit(1)

def close():
    if ansys_running:
        ansys_exit()
    global client_socket
    client_socket.close()

def ansys_solve(pretensions: list) -> str:
    '''
    return: result_dir
    '''
    global client_socket
    cmd = {
        'cmd': 'solve',
        'pretensions': pretensions
    }
    client_socket.send(json.dumps(cmd).encode())
    print('已发送求解命令')
    # 等待求解完成
    ret_data_str = client_socket.recv(1024).decode()
    ret_data = json.loads(ret_data_str)
    if ret_data['status'] == 'success':
        print('求解成功')
    return ret_data['result_dir']


def ansys_test(pretensions: list) -> str:
    '''
    return: result_dir
    '''
    global client_socket
    cmd = {
        'cmd': 'test',
        'pretensions': pretensions
    }
    client_socket.send(json.dumps(cmd).encode())
    print('已发送求解命令')
    # 等待求解完成
    ret_data_str = client_socket.recv(1024).decode()
    ret_data = json.loads(ret_data_str)
    if ret_data['status'] == 'success':
        print('求解成功')
    return ret_data['result_dir']


def ansys_exit() -> None:
    global client_socket
    cmd = { 'cmd': 'exit' }
    client_socket.send(json.dumps(cmd).encode())
    # 等待退出完成
    ret_data_str = client_socket.recv(1024).decode()
    ret_data = json.loads(ret_data_str)
    if ret_data['status'] == 'success':
        print('退出成功')

if __name__ == '__main__':
    init()

    # testing cmd1
    ansys_solve(pretensions=[2100, 1200, 1300, 2400, 4500, 5000])
    
    # testing cmd2
    ansys_exit()

    close()
