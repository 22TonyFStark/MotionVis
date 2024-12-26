
import numpy as np

data = dict(np.load('smplx_data\intergen\gt.npz'.replace("\\", "/")).items())

for key in data.keys():
    print(key, data[key].shape)
