import os
import wbjn
import socket
import json

port = 65500
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', port))
server_socket.listen(5)
print('waiting for connection...')
client_socket, client_address = server_socket.accept()
print('comm service connected.')

client_socket.send("Test message from ANSYS".encode())

model       = ExtAPI.DataModel.Project.Model
geom        = model.Geometry
mesh        = model.Mesh
connections = model.Connections
materials   = model.Materials
analysis    = model.Analyses[0]

# get user_files directory
cmd = '''returnValue(GetUserFilesDirectory())'''
user_dir = wbjn.ExecuteCommand(ExtAPI, cmd)
print('user_dir:')
print(user_dir)

# user_dir = os.path.curdir

simulation_count = 0

while True:
    recv_data_str = client_socket.recv(1024).decode()
    recv_data = json.loads(recv_data_str)

    if recv_data['cmd'] == 'exit':
        # send response to client
        response = { 'status': 'success' }
        client_socket.send(json.dumps(response).encode())
        client_socket.close()
        server_socket.close()
        break

    elif recv_data['cmd'] == 'solve':
        simulation_count += 1

        # get pretensions from data packet
        pretensions = recv_data['pretensions']
        pretensions_str = ['{}[N]'.format(pretension) for pretension in pretensions]
        
        # set pretensions
        print('setting pretensions...')
        bolt_pretension_ids = [577, 578, 579, 580, 581, 582]
        for i in range(0, 6):
            id = bolt_pretension_ids[i]
            bolt_pretension = DataModel.GetObjectById(bolt_pretension_ids[i])
            bolt_pretension.Preload.Inputs[0].DiscreteValues = [Quantity('1[s]')]
            bolt_pretension.Preload.Output.DiscreteValues = [Quantity(pretensions_str[i])]
        
        # solve the analysis
        print('solving analysis...')
    
        analysis.Solve()

        # export results
        print('exporting results...')
        result_dir = None
        for analysis in ExtAPI.DataModel.AnalysisList:
            #Get All direction Deformation Objects in all the Analyses in the Tree
            DirectionDeformationResults = [child for child in analysis.Solution.Children if child.DataModelObjectCategory == DataModelObjectCategory.DirectionalDeformation]
            for result in DirectionDeformationResults:
                result.Activate()
                result_dir = user_dir + "/" + str(simulation_count)
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)
                filename = os.path.join(result_dir, result.Name + ".csv")
                result.ExportToTextFile(filename)
        
        simulation_result_str = "simulation " + str(simulation_count) + " completed."
        print(simulation_result_str)

        # send response to client
        response = {
            'status': 'success',
            'result_dir': result_dir
        }
        client_socket.send(json.dumps(response).encode())

    else:
        print('unknown command')
        client_socket.close()
        server_socket.close()
        exit(1)

