import gui
from measure import get_concentricity
from guider import get_torque_correction
from guider import get_normalized_deflect_vector_at_index, \
                   get_all_normalized_deflect_vectors

gui = gui.GUI()

def concentricity_provider(data):
    concentricity, deflect_vector = get_concentricity(data)
    return concentricity, deflect_vector

def guide_provider(deflect_vector):
    '''
    return: ['紧' or '松', ...], deflect_vector, all_deflect_vectors
    '''
    torque_correction, index = get_torque_correction(deflect_vector)
    print(torque_correction)

    guide = []
    for torque in torque_correction:
        if torque >= max(torque_correction):
            guide.append('紧')
        elif torque <= min(torque_correction):
            guide.append('松')
    
    return guide, \
           get_normalized_deflect_vector_at_index(index), \
           get_all_normalized_deflect_vectors()

gui.init(concentricity_provider=concentricity_provider, guide_provider=guide_provider)