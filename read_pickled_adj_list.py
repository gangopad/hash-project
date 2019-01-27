import sys 
import os 
import pickle 

def try_to_load_as_pickled_object_or_None(filepath):
    """
    This is a defensive way to write pickle.load, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    print(filepath)
    input_size = os.path.getsize(filepath)
    bytes_in = bytearray(0)
    with open(filepath, 'rb') as f_in:
        for _ in range(0, input_size, max_bytes):
            bytes_in += f_in.read(max_bytes)
    obj = pickle.loads(bytes_in)
    # try:
    #     input_size = os.path.getsize(filepath)
    #     bytes_in = bytearray(0)
    #     with open(filepath, 'rb') as f_in:
    #         for _ in range(0, input_size, max_bytes):
    #             bytes_in += f_in.read(max_bytes)
    #     obj = pickle.loads(bytes_in)
    # except:
    #     e = sys.exc_info()[0]
    #     print(e)
    #     return None
    return obj

print("loading dict...")
adj_list = try_to_load_as_pickled_object_or_None(sys.argv[1])

print("sorting dict...")
distro = sorted(list(adj_list.values()))

print("computing stats...")
print("Number of unique keys: " + str(len(distro)))
print("Mean key frequeny:     " + str((sum(distro) / len(distro))))
#print("Std dev key frequeny:  " + numpy.std(distro))
print("Top 25 values:         " + str(distro[-65:]))

import matplotlib.pyplot as plt
plt.plot(distro)
plt.ylabel('frequeny')
plt.show()
