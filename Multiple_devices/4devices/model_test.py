import Model as ml
import numpy as np
from Data import sliding_window
from collections import deque

"""**********************Initial**********************"""
test_data = sliding_window()
"""(16,12,16,3)"""
frames = test_data[0]
"""(16,12,16,20)"""
opt_flows = test_data[1]

frames = frames.astype(dtype=np.uint8)
opt_flows = opt_flows.astype(dtype=np.uint8)

"""convert to bytes for transporting"""
frames = frames.tobytes()
opt_flows = opt_flows.tobytes()

"""*************Spatial CNNs and Temporal CNNs******************"""
frames = np.fromstring(frames, np.uint8).reshape(16, 12, 16, 3)
opt_flows = np.fromstring(opt_flows, np.uint8).reshape(16, 12, 16, 20)

s_model = ml.spatial_model_multi()
t_model = ml.temporal_model_multi()

s_output = s_model.predict(np.array([frames]))
t_output = t_model.predict(np.array([opt_flows]))
"""(16, 256)x2"""

s_output = s_output.tostring()
t_output = t_output.tostring()

"""*******************Maxpoolings and 1/2 Dense***************"""
s_output = np.fromstring(s_output, np.float32).reshape(16, 256)
t_output = np.fromstring(t_output, np.float32).reshape(16, 256)

_input = deque()
_input.append(s_output)
_input.append(t_output)

mp_model = ml.maxpoolings()
s_output = mp_model.predict(np.array([_input[0]]))
t_output = mp_model.predict(np.array([_input[1]]))
"""(15, 256)x2"""

con_model = ml.temporal_pyramid_concate()
X = con_model.predict([np.array([s_output]), np.array([t_output])])
"""(2, 15, 256)"""

final_dense = ml.half_dense_layers()
X = final_dense.predict(X)

print X

