import numpy as np
import linecache
import cv2

class LoadGISData:
    def __init__(self, popn_density_file):
        self.ncols = linecache.getline(popn_density_file, 1)
        self.nrows = linecache.getline(popn_density_file, 2)

        self.xllcorner = linecache.getline(popn_density_file, 3)
        self.yllcorner = linecache.getline(popn_density_file, 4)
        self.cellsize = linecache.getline(popn_density_file, 5)

        # TBC - manipulating this string to dynamically read NODATA_value
        # self.NODATA_value = linecache.getline(popn_density_file, 6)

        self.NODATA_value = np.float64(-9999)

        self.ascii_grid = np.loadtxt(popn_density_file, skiprows=6)

        self.ascii_grid = self.resample_ascii_grid(self.ascii_grid)
        self.rows = self.ascii_grid.shape[0]
        self.columns = self.ascii_grid.shape[1]

        # checking the data is square
        assert self.rows == self.columns

    def return_grid_size(self):

        if len(self.ascii_grid) == len(self.ascii_grid[0]):
            return len(self.ascii_grid)
        else:
            print("Sizes do not match")

    def return_population(self, country):
        if (country == "Austria"):
            return 8.6
        elif (country == "Belgium"):
            return 11.2
        elif (country == "Bulgaria"):
            return 7.1
        elif (country == "Croatia"):
            return 4.26
        elif (country == "Cyprus"):
            return 1.16
        elif(country == "Czech Republic"):
            return 10.8
        elif (country == "Denmark"):
            return 5.7
        elif (country == "Estonia"):
            return 1.3
        elif (country == "Finland"):
            return 5.46
        elif (country == "France"):
            return 65
        elif (country == "Germany"):
            return 82.6
        elif (country == "Greece"):
            return 11.1
        elif (country == "Hungary"):
            return 9.9
        elif (country == "Ireland"):
            return 4.73
        elif (country == "Italy"):
            return 61
        elif (country == "Latvia"):
            return 2
        elif (country == "Lithuania"):
            return 3
        elif (country == "Luxembourg"):
            return 0.54
        elif (country == "Malta"):
            return 0.45
        elif (country == "Netherlands"):
            return 16.8
        elif (country == "Poland"):
            return 38
        elif (country == "Portugal"):
            return 10.6
        elif (country == "Romania"):
            return 21.6
        elif (country == "Slovakia"):
            return 5.5
        elif (country == "Slovenia"):
            return 2.1
        elif (country == "Spain"):
            return 47
        elif (country == "Sweden"):
            return 9.7
        elif (country == "UK"):
            return 64
        else:
            return print("Please enter a European state.")

    def return_NODATA_value(self):
        return self.NODATA_value

    def return_ascii_grid(self):
        return self.ascii_grid

    def resample_ascii_grid(self, ascii_grid):
        return cv2.resize(ascii_grid, dsize=(81, 81), interpolation=cv2.INTER_NEAREST)

    def return_sum_popn_of_patches_with_popn_greater_than_zero(self):
        sum_popn = 0
        for x in range(self.rows):
            for y in range(self.columns):
                if (self.ascii_grid[x, y] != self.NODATA_value):
                    sum_popn += self.ascii_grid[x, y]

        return sum_popn

    def return_count_of_non_zero_patches(self):
        return np.count_nonzero(self.ascii_grid != self.NODATA_value)





