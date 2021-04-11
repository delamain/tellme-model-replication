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


def infectionAgent_mock(model, x, y):
    return InfectionAgent(model, x, y)


class MyTestCase(unittest.TestCase):

    def test_agent_x_and_y_coord(self):
        x = 0
        y = 0

        patch = patch_mock(x, y)
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)

        patch.agents.append(infectionAgent_mock(model, x, y))

        self.assertEqual(patch.agents[0].x_coord, x)
        self.assertEqual(patch.agents[0].x_coord, y)

    def test_seek_vaccination_restrict_vaccine_false(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)
        patch = patch_mock(0, 0)
        patch.agents.append(infectionAgent_mock(model, 0, 0))

        region.restrict_vaccine = False

        patch.agents[0].seek_vaccination(region)
        self.assertEqual(patch.agents[0].behave_vaccinate, True)

    def test_seek_vaccination_epidemic_declared_true(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)
        patch = patch_mock(0, 0)
        patch.agents.append(infectionAgent_mock(model, 0, 0))

        region.epidemic_declared = True

        patch.agents[0].seek_vaccination(region)
        self.assertEqual(patch.agents[0].behave_vaccinate, True)

    def test_seek_vaccination_behave_vaccinate_false(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)
        patch = patch_mock(0, 0)
        patch.agents.append(infectionAgent_mock(model, 0, 0))

        region.restrict_vaccine = True
        region.epidemic_declared = False

        patch.agents[0].seek_vaccination(region)
        self.assertEqual(patch.agents[0].behave_vaccinate, False)

    def test_check_agent_not_exposed_not_infected_not_immune(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)
        patch = patch_mock(0, 0)
        patch.agents.append(infectionAgent_mock(model, 0, 0))

        # need to fix
        self.assertEqual(patch.agents[0].check_agent_not_exposed_not_infected_not_immune(), None)


if __name__ == '__main__':
    unittest.main()
