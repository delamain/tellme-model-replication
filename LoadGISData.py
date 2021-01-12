import numpy as np
import linecache
import scipy
import cv2

class LoadGISData:
    def __init__(self, popn_density_file):
        self.ncols = linecache.getline(popn_density_file, 1)
        self.nrows = linecache.getline(popn_density_file, 2)
        self.xllcorner = linecache.getline(popn_density_file, 3)
        self.yllcorner = linecache.getline(popn_density_file, 4)
        self.cellsize = linecache.getline(popn_density_file, 5)
        self.NODATA_value = linecache.getline(popn_density_file, 6)
        self.ascii_grid = np.loadtxt(popn_density_file, skiprows=6)


        self.ascii_grid = self.resample_ascii_grid(self.ascii_grid)
        self.rows = self.ascii_grid.shape[0]
        self.columns = self.ascii_grid.shape[1]

    def return_grid_size(self):

        if (len(self.ascii_grid) == len(self.ascii_grid[0])):
            return len(self.ascii_grid)
        else:
            print("Sizes do not match")

    def return_population(self, country):
        if (country == "UK"):
            return 64

    def return_ascii_grid(self):
        return self.ascii_grid

    def resample_ascii_grid(self, ascii_grid):
        return cv2.resize(ascii_grid, dsize=(81, 81), interpolation=cv2.INTER_NEAREST)

    def return_sum_popn_of_patches_with_popn_greater_than_zero(self):
        sum_popn = 0
        for x in range(self.rows):
            for y in range(self.columns):
                if (self.ascii_grid[x, y] != -9999):
                    sum_popn += self.ascii_grid[x, y]

        return sum_popn

    def return_count_of_non_zero_patches(self):
        return np.count_nonzero(self.ascii_grid != -9999)



