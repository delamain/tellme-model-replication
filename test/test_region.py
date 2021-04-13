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


def infection_agent_mock(model, x, y):
    return InfectionAgent(model, x, y)


class TestRegion(unittest.TestCase):

    def test_revise_attitude_attitudeV_current_is_greater(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region = region_mock(xsize, ysize, model, r0, recovery_period, latency_period)

        for x in range(region.xsize):
            for y in range(region.ysize):
                region.patches[x][y] = patch_mock(x, y)

        patch = patch_mock(xcoord, ycoord)
        region.live_patches.add(patch)
        agent = infection_agent_mock(model, xcoord, ycoord)
        patch.agents.append(agent)

        agent.attitudeV_current = 10

        region.revise_attitude()

        self.assertEqual(agent.attitudeV_current, 1)

    def test_revise_attitude_attitudeV_current_is_negative(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region = region_mock(xsize, ysize, model, r0, recovery_period, latency_period)

        for x in range(region.xsize):
            for y in range(region.ysize):
                region.patches[x][y] = patch_mock(x, y)

        patch = patch_mock(xcoord, ycoord)
        region.live_patches.add(patch)
        agent = infection_agent_mock(model, xcoord, ycoord)
        patch.agents.append(agent)

        agent.attitudeV_current = -10

        region.revise_attitude()

        self.assertEqual(agent.attitudeV_current, 0)