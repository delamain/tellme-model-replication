import unittest
import sys

sys.path.append("")

from main.LoadGISData import LoadGISData

def mock_gis_data_object():
    return LoadGISData("GISdata/popn_density_uk_2015.asc")

class TestLoadGISData(unittest.TestCase):

    def test_LoadGISDataUK_ncols_rows(self):
        gisData = mock_gis_data_object()
        nrows = [int(s) for s in gisData.nrows.split() if s.isdigit()]
        ncols = [int(s) for s in gisData.ncols.split() if s.isdigit()]

        self.assertEqual(nrows[0], 312)
        self.assertEqual(ncols[0], 312)

    def test_numpy_count_of_non_zero_is_same_as_manual(self):
        gisData = mock_gis_data_object()

        count_non_zero_patch = 0

        for x in range(gisData.rows):
            for y in range(gisData.columns):
                if gisData.ascii_grid[x][y] != gisData.NODATA_value:
                    count_non_zero_patch += 1

        numpyCount = gisData.return_count_of_non_zero_patches()

        self.assertEqual(numpyCount, count_non_zero_patch)

    def test_return_correct_population(self):
        gisData = mock_gis_data_object()
        population = gisData.return_population("UK")
        self.assertEqual(population, 64)

    def test_return_incorrect_population(self):
        gisData = mock_gis_data_object()
        population = gisData.return_population("Italy")
        self.assertNotEqual(population, 64)

if __name__ == '__main__':
    unittest.main()
