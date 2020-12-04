import pandas as pd
from enum import Enum, unique

    
def makeHeatmap(_normtype=False, _datapath="./data.csv"):
    ddata = pd.read_csv(_datapath)
    ddata.columns = range(0,1601)
    # separate by class
    smiles = ddata[ddata[0] == 0].iloc[:,1:]
    hearts = ddata[ddata[0] == 1].iloc[:,1:]
    # squish data into single row
    smap = smiles.sum()
    hmap = hearts.sum()
    maps_ = {"smiles":smap, "hearts":hmap}

    mins = getMins(maps_)
    maxs = getMaxs(maps_)
    for key, map in maps_.items():
        args_ = (mins[key], maxs[key])
        maps_[key] = map.apply(minmaxNorm, args=args_)
        maps_[key] = maps_[key].to_list()
        
    smap = ""
    hmap = ""
    for element in maps_["hearts"]:
        hmap = f"{hmap},{element}"

    with open("hmap.csv","w") as file_out:
        file_out.write(hmap)

    for element in maps_["smiles"]:
        smap = f"{smap},{element}"

    with open("smap.csv","w") as file_out:
        file_out.write(smap)

    return maps_
    # if don't want to normalize sums
    # if not _normtype:
    #     return maps_
    # else: # normalize all the things
    #     try:

    #     except ValueError:
    #         print("Invalid normalization type. Import NormMethods enum and use it.")
    #         return 1

def normalizeMaps(_normtype, _maps):
    '''
        this is a normalization method dispatch function
        takes a NormMethods enum and applies it to the maps in the _maps dict
    '''
    # aliases for key lookup
    s = "smiles"
    h = "hearts"
    if _normtype is NormMethods.MAX:
        args_ = getMaxs(_maps)

    elif _normtype is NormMethods.MEAN:
        mins = getMins(_maps)
        maxs = getMaxs(_maps)
        means = getMeans(_maps)
        args_ = {s:(means[s], mins[s], maxs[s]), h:(means[s],mins[h], maxs[h])}

    elif _normtype is NormMethods.MINMAX:
        mins = getMins(_maps)
        maxs = getMaxs(_maps)
        args_ = {s:(mins[s], maxs[s]), h:(mins[h], maxs[h])}

    else:
        raise ValueError

    maps_ = {}
    for key, map in _maps.items():
        maps_[key] = map.apply(_normtype, args=args_[key])

    return maps_

def getMaxs(_maps):
    # get max of each entry
    maps_ = {}
    for key, map in _maps.items():
        maps_[key] = map.max()

    return maps_

def getMins(_maps):
    # get min of each entry
    maps_ = {}
    for key, map in _maps.items():
        maps_[key] = map.min()

    return maps_

def getMeans(_maps):
    # get avg of each entry
    maps_ = {}
    for key, map in _maps.items():
        maps_[key] = map.mean()
    
    return maps_

def meanNorm(x, mu, max, min):
    ''' returns the mean normalized value for a given entry
        x is data point for a given feature i.e. the entry at (row, column)
        mu is mean of that feature (sum of all instances for that feature)
        max is the largest data point for that feature
        min is the smallest data point for that feature
    '''
    return ((x - mu)/(max - min))

def minmaxNorm(x, min, max):
    ''' returns the max normalized value for a given entry
        x is data point for a given feature i.e. the entry at (row, column)
        min is the smallest data point for that feature
        max is the largest data point for that feature
    '''
    return ((x-min)/(max-min))

def maxNorm(x, max):
    ''' returns the max normalized value for a given entry
        x is data point for a given feature i.e. the entry at (row, column)
        max is the largest data point for that feature
    '''
    return (x/max)

@unique
class NormMethods(Enum):
    MINMAX = minmaxNorm # ifu want minmaxNorm
    MAX = maxNorm # if u want maxNorm
    MEAN = meanNorm # if u want meanNorm

if __name__ == "__main__":
    makeHeatmap()
    # print("You should not be here. Import the func and run it elsewhere.")