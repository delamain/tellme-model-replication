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
        region_mock(10, 10, model, 1, 2, 5)

        patch.agents.append(infection_agent_mock(model, x, y))
        patch.agents.append(infection_agent_mock(model, x, y))

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

        self.assertEqual(len(patch.visible_patches), 0)

    def test_visible_patches_people_occupied(self):
        model = model_mock(10)
        region = region_mock(10, 10, model, 1, 2, 5)

        for x in range(region.xsize):
            for y in range(region.ysize):
                region.patches[x][y] = patch_mock(x, y)

        centre_patch = region.patches[2][2]

        adjacent_patches = [region.patches[3][2],
                            region.patches[2][3],
                            region.patches[1][2],
                            region.patches[2][1]]

        for patch in adjacent_patches:
            patch.within_border = True

        centre_patch.set_visible_patches(model)

        self.assertEqual(len(centre_patch.visible_patches), 4)

    def test_update_SEIR_persons_first_infected_day_count(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region_mock(xsize, ysize, model, r0, recovery_period, latency_period)
        patch = patch_mock(xcoord, ycoord)
        patch.agents.append(infection_agent_mock(model, xcoord, ycoord))

        patch.agents[0].disease_day = 0
        patch.agents[0].infected = True

        patch.update_SEIR_persons_first(SEIR_lambda, SEIR_gamma)

        self.assertEqual(patch.agents[0].disease_day, 1)

    def test_update_SEIR_persons_first_not_infected_day_count(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region_mock(xsize, ysize, model, r0, recovery_period, latency_period)
        patch = patch_mock(xcoord, ycoord)
        patch.agents.append(infection_agent_mock(model, xcoord, ycoord))

        patch.agents[0].disease_day = 0
        patch.agents[0].infected = False

        patch.update_SEIR_persons_first(SEIR_lambda, SEIR_gamma)

        self.assertEqual(patch.agents[0].disease_day, 0)

    def test_make_infections_third_calculate_incidence_no_new_cases_made(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        travel_rate = 0.25
        migrate_infections = 5
        global_population = 25
        count = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region_mock(xsize, ysize, model, r0, recovery_period, latency_period)
        patch = patch_mock(xcoord, ycoord)
        patch.new_cases_made = 0
        patch.population = 10
        patch.num_travel_incases = 0
        patch.num_susceptible = 10

        returned_count = patch.make_infections_third_calculate_incidence(travel_rate, migrate_infections, global_population, count)

        self.assertEqual(returned_count, 1)

    def test_make_infections_third_calculate_incidence_some_new_cases_made(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        travel_rate = 0.25
        migrate_infections = 5
        global_population = 25
        count = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region_mock(xsize, ysize, model, r0, recovery_period, latency_period)
        patch = patch_mock(xcoord, ycoord)
        patch.new_cases_made = 5
        patch.population = 10
        patch.num_travel_incases = 0
        patch.num_susceptible = 5

        returned_count = patch.make_infections_third_calculate_incidence(travel_rate, migrate_infections,
                                                                         global_population, count)

        self.assertEqual(returned_count, 0)

    def test_make_infections_third_calculate_incidence_greater_than_susceptible(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        travel_rate = 0.25
        migrate_infections = 5
        global_population = 25
        count = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region_mock(xsize, ysize, model, r0, recovery_period, latency_period)
        patch = patch_mock(xcoord, ycoord)
        patch.new_cases_made = 5
        patch.population = 10
        patch.num_travel_incases = 15
        patch.num_susceptible = 5

        patch.make_infections_third_calculate_incidence(travel_rate, migrate_infections,
                                                                         global_population, count)

        self.assertEqual(patch.num_susceptible, patch.num_incidence)

    def test_make_infections_third_calculate_incidence_less_than_susceptible(self):
        number_of_epochs = 10
        xsize = ysize = 10
        r0 = 1
        recovery_period = 1
        latency_period = 1
        xcoord = ycoord = 0
        travel_rate = 0.25
        migrate_infections = 5
        global_population = 25
        count = 0
        SEIR_lambda = 1.0 / latency_period
        SEIR_gamma = 1.0 / recovery_period

        model = model_mock(number_of_epochs)
        region_mock(xsize, ysize, model, r0, recovery_period, latency_period)
        patch = patch_mock(xcoord, ycoord)
        patch.new_cases_made = 3
        patch.population = 10
        patch.num_travel_incases = 0
        patch.num_susceptible = 5

        patch.make_infections_third_calculate_incidence(travel_rate, migrate_infections,
                                                                         global_population, count)

        self.assertNotEqual(patch.num_susceptible, patch.num_incidence)

if __name__ == '__main__':
    unittest.main()
