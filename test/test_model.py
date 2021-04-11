import unittest
import sys

sys.path.append("")

from panaxea.core.Model import Model
from main.Region import Region
from main.InfectionAgent import InfectionAgent


def region_mock(xsize, ysize, model, R0, recovery_period, latency_period):
    region = Region("agent_env", xsize, ysize, model, R0, recovery_period, latency_period)


def model_mock(test_number_of_epochs):
    return Model(test_number_of_epochs)


def agent_mock(model, x, y):
    return InfectionAgent(model, x, y)


class TestModel(unittest.TestCase):

    def test_add_people_to_schedule(self):
        model = model_mock(10)
        region_mock(10, 10, model, 1, 2, 5)

        number_of_people = 10
        for x in range(0, number_of_people):
            model.schedule.agents.add(InfectionAgent(model, x, x))

        self.assertEqual(len(model.schedule.agents), 10)


if __name__ == '__main__':
    unittest.main()
