import numpy as np

# Set a different seed for the first call
max_level = 100 
rng = np.random.default_rng(1461296) 

rand = rng.uniform(-1, 1, max_level)

print(100*rand)
