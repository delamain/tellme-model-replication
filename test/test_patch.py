import unittest
import sys
sys.path.append("")

from main.Patch import Patch
from main.InfectionAgent import InfectionAgent
from main.Region import Region
from panaxea.core.Model import Model

def model_mock(test_number_of_epochs):
    return Model(test_number_of_epochs)

def region_mock(xsize, ysize, model, R0, recovery_period, latency_period):
    return Region("agent_env", xsize, ysize, model, R0, recovery_period, latency_period)

def patch_mock(x, y):
    return Patch(x, y)

def InfectionAgent_mock(model, x, y):
    return InfectionAgent(model, x, y)

class TestPatch(unittest.TestCase):

    def test_patch_xy(self):
        testX = patch_mock(1, 0)
        testY = patch_mock(0, 1)

        self.assertEqual(testX.return_x_coord(), 1)
        self.assertEqual(testY.return_y_coord(), 1)

    def test_number_of_agents_at_patch(self):
        x = 0
        y = 0

        patch = patch_mock(x, y)
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)

        patch.agents.append(InfectionAgent_mock(model, x, y))
        patch.agents.append(InfectionAgent_mock(model, x, y))

        self.assertEqual(len(patch.agents), 2)

    def test_infectious_agents_startup_less(self):
        patch = patch_mock(0, 0)
        patch.set_infectious_agents_setup(90)
        self.assertEqual(patch.num_infected, 100)

    def test_infectious_agents_startup_more(self):
        patch = patch_mock(0, 0)
        patch.set_infectious_agents_setup(110)
        self.assertEqual(patch.num_infected, 110)

    def test_visible_patches_empty(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)

        for x in range(region.xsize):
            for y in range(region.ysize):
                region.patches[x][y] = patch_mock(x, y)

        patch = region.patches[2][2]
        patch.set_visible_patches(model)
        for patch in patch.visible_patches:
            print(patch.x, patch.y)

        self.assertEqual(len(patch.visible_patches), 0)

    def test_visible_patches_people_occupied(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)

        for x in range(region.xsize):
            for y in range(region.ysize):
                region.patches[x][y] = patch_mock(x, y)

        centre_patch = region.patches[2][2]

        adjacent_patches = []
        adjacent_patches.append(region.patches[3][2])
        adjacent_patches.append(region.patches[2][3])
        adjacent_patches.append(region.patches[1][2])
        adjacent_patches.append(region.patches[2][1])

        for patch in adjacent_patches:
            patch.within_border = True

        centre_patch.set_visible_patches(model)

        self.assertEqual(len(centre_patch.visible_patches), 4)

    # def test_make_infections_first_patch_self_generated(self):
    #     pass

if __name__ == '__main__':
    unittest.main()