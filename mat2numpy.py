from scipy.io import loadmat
from os import listdir
import numpy as np


#Loads .mat file into dictionary 
def load_mat(filename):
    file = loadmat("Dataset/" + filename)

    return file

#Uses recursion to convert to simpler arrays
def tree(data): 
    if isinstance(data, (np.void, np.ndarray)):

        if len(data) == 1:
            out = tree(data[0])

        else:       
            out = np.array([tree(x) for x in data])
    else:
        out = data

    return out

#Resizes all .mat data in "Dataset" and writes each to "Dataset_np"
def convert_data(target_dir='Dataset_np'):
    print("[*] Finding files")
    pathnames = listdir("Dataset/")

    print("[*] Removing .DS_Store and README.txt from list")
    try:
        pathnames.remove("README.txt")
        pathnames.remove(".DS_Store")
    except:
        pass

    num_paths = len(pathnames)
    
    print("[*] Converting files to NumPy arrays")
    print()

    #Loops over data files eg. B0005.mat
    for i, pathname in enumerate(pathnames):
        file = load_mat(pathname)

        pathname = pathname.replace(".mat", '')

        x = file[pathname]

        print("[*] Searching nested object {}".format(pathname))
        print("Progress {}/{}".format(i+1, num_paths))

        new_data = tree(x)
        new_data = np.array(new_data)

        np.save("Dataset_np/" + pathname, new_data, allow_pickle=True)

#Recursively enters first element in array
#Depth corresponds to x(n) on the diagram
#Depth=-1 goes to the bottom
def traverse(x, depth=-1, start_level=0):

    print('x' + str(start_level))
    print(type(x))
    print(x.shape)
    print()

    start_level += 1

    if depth == start_level-1:
        print("[*] Depth reached")
        return x

    try:
        return traverse(x[0], depth=depth, start_level=start_level)
    except Exception as e:
        print("[*] Hit bottom ({})".format(e))
        return x

    