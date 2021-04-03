import numpy as np
import cv2
import unittest
import sys
sys.path.append("")

from main.LoadGISData import LoadGISData

class TestLoadGISData(unittest.TestCase):

    def test_GISData_matrix_is_square(self):
        loadedGISMatrix = np.loadtxt("GISdata/popn_density_uk_2015.asc", skiprows=6)
        rows = loadedGISMatrix.shape[0]
        columns = loadedGISMatrix.shape[1]
        self.assertEqual(rows, columns)

    def test_resampled_GISData_matrix_is_square(self):
        loadedGISMatrix = np.loadtxt("GISdata/popn_density_uk_2015.asc", skiprows=6)
        resampledMatrix = cv2.resize(loadedGISMatrix, dsize=(81, 81), interpolation=cv2.INTER_NEAREST)
        rows = resampledMatrix.shape[0]
        columns = resampledMatrix.shape[1]
        self.assertEqual(rows, columns)

    def test_LoadGISDataUK_ncols_rows(self):
        gisData = LoadGISData("GISdata/popn_density_uk_2015.asc")
        nrows = [int(s) for s in gisData.nrows.split() if s.isdigit()]
        ncols = [int(s) for s in gisData.ncols.split() if s.isdigit()]

        self.assertEqual(nrows[0], 312)
        self.assertEqual(ncols[0], 312)

    # Test comparison with NetLogo model (i.e. do same number of empty patches get obtained)
    # Test return_count_of_non_zero_patches is the same as NetLogo model

if __name__ == '__main__':
    unittest.main()