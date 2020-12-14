from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D
from panaxea.core.Steppables import Steppable, Helper
import Patch as patch
import random

class Region(ObjectGrid2D):

    # setup_fixed_globals
    def __init__(self, name, xsize, ysize, model, population, R0, recovery_period, latency_period):
        super(Region, self).__init__(name, xsize, ysize, model)
        self.global_num_susceptible = 0
        self.global_num_infected = 0
        self.global_num_exposed = 0
        self.global_num_immune = 0
        self.global_num_incidence = 0  # population to be converted to exposed
        self.global_population = 0

        self.SEIR_beta = R0 / recovery_period

        if (latency_period == 0):
            self.SEIR_lambda =  0
        else:
            self.SEIR_lambda = 1 / latency_period

        self.SEIR_gamma = 1 / recovery_period

        # matrix of patches
        self.patches = [[patch.Patch(x, y) for x in range(xsize)] for y in range(ysize)]

    def setup_infection(self, model):
        self.global_num_infected = 10

        # randomly add the infected number to the grid

        for x in range(self.global_num_infected):
            randomX = self.random_xposition_within_grid(model)
            randomY = self.random_yposition_within_grid(model)
            self.patches[randomX][randomY].increment_infectious_agents_setup()

        self.global_num_susceptible = self.global_population - self.global_num_infected

    def add_agent_to_patch(self, x, y):
        self.global_population += 1
        self.global_num_susceptible += 1
        self.patches[x][y].increment_patch_agents()

    def remove_agent_from_patch(self, x, y):
        self.patches[x][y].decrement_patch_agents()

    def number_of_patches(self):
        rows = len(self.patches)
        columns = len(self.patches[0])
        return rows * columns

    def return_beta_lambda_gamma(self):
        return self.SEIR_beta, self.SEIR_lambda, self.SEIR_gamma

    def return_SEIR_variables(self):
        return self.global_num_susceptible, self.global_num_exposed, self.global_num_infected, self.global_num_immune

    def update_global_variables_from_given_patch(self, x, y):
        self.global_num_susceptible -= self.patches[x][y].num_exposed + self.patches[x][y].num_infected
        self.global_num_exposed += self.patches[x][y].num_exposed
        self.global_num_infected += self.patches[x][y].num_infected
        self.global_num_immune += self.patches[x][y].num_immune

    def random_xposition_within_grid(self, model):
        xlimit = model.environments["agent_env"].xsize - 1
        return random.randint(0, xlimit)

    def random_yposition_within_grid(self, model):
        ylimit = model.environments["agent_env"].ysize - 1
        return random.randint(0, ylimit)

    def print_out_region_patches(self):
        rows = len(self.patches)
        columns = len(self.patches[0])
        for x in range(columns):
            for y in range(rows):
                print("[",self.patches[x][y].number_of_agents_at_patch(),"]", end="")
                if y == (columns - 1):
                    print(" ")

class RegionSteppable(Steppable):

    def __init__(self):
        super(Steppable, self).__init__()

    def step_main(self, model):
        beta_lambda_gamma = model.environments["agent_env"].return_beta_lambda_gamma()
        patches = model.environments["agent_env"].patches
        rows = len(patches)
        columns = len(patches[0])

        for x in range(rows):
            for y in range(columns):
                patch.Patch.make_infections(patches[x][y], beta_lambda_gamma[0])
                patch.Patch.update_SEIR_patches(patches[x][y], beta_lambda_gamma[2], beta_lambda_gamma[1])
                model.environments["agent_env"].update_global_variables_from_given_patch(x, y)

    def step_epilogue(self, model):
        agent_env = model.environments["agent_env"]
        model.environments["agent_env"].print_out_region_patches()

        SEIR_variables = model.environments["agent_env"].return_SEIR_variables()
        print("S:{0}, E:{1}, I:{2}, R:{3}".format(SEIR_variables[0], SEIR_variables[1], SEIR_variables[2], SEIR_variables[3]))



