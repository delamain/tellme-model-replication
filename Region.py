import numpy as np
from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D
from panaxea.core.Steppables import Steppable, Helper
import Patch as patch
import random

class Region(ObjectGrid2D):

    # setup_fixed_globals
    def __init__(self, name, xsize, ysize, model, R0, recovery_period, latency_period):
        super(Region, self).__init__(name, xsize, ysize, model)
        self.global_num_susceptible = 0
        self.global_num_infected = 0
        self.global_num_exposed = 0
        self.global_num_immune = 0
        self.global_num_incidence = 0  # population to be converted to exposed
        self.global_population = 0
        self.travel_rate = 0.25
        self.travel_short = 0.6

        self.SEIR_beta = R0 / recovery_period

        if (latency_period == 0):
            self.SEIR_lambda =  0
        else:
            self.SEIR_lambda = 1 / latency_period

        self.SEIR_gamma = 1 / recovery_period
        self.start_epi_locations = 1
        self.start_epi_population = 0.5

        # matrix of patches
        self.patches = [[patch.Patch(x, y) for x in range(xsize)] for y in range(ysize)]
        self.rows = len(self.patches)
        self.columns = len(self.patches[0])

    def setup_infection(self, model):

        # calculating the index of the 5 patches with the most number of agents
        patch_populations_matrix = [[self.patches[x][y].number_of_agents_at_patch() for x in range(self.columns)] for y in range(self.rows)]
        patch_populations_matrix_numpy = np.array(patch_populations_matrix)
        # np.savetxt("np.txt", patch_populations_matrix_numpy)

        n = 5
        flat_indices = np.argpartition(patch_populations_matrix_numpy.ravel(), -n)[-n:]
        row_indices, col_indices = np.unravel_index(flat_indices, patch_populations_matrix_numpy.shape)

        for j in range(n):
            #print("[{0},{1}], pop:{2}".format(col_indices[j], row_indices[j]), self.patches[col_indices[j]][row_indices[j]].number_of_agents_at_patch())
            print(self.patches[col_indices[j]][row_indices[j]].number_of_agents_at_patch())

        print(patch_populations_matrix_numpy.max())

        # print(random.randint(0, 4))
        i = random.randint(0, 4)
        self.patches[col_indices[i]][row_indices[i]].set_infectious_agents_setup(self.start_epi_population
                                                                                 * self.patches[col_indices[i]][
                                                                                     row_indices[
                                                                                         i]].number_of_agents_at_patch())

        # for i in range(n):
        #     print(self.patches[col_indices[i]][row_indices[i]].number_of_agents_at_patch())
        #     self.patches[col_indices[i]][row_indices[i]].set_infectious_agents_setup(self.start_epi_population
        #                                                                                  * self.patches[col_indices[i]][row_indices[i]].number_of_agents_at_patch())

        # for i in range(n):
        #     print(self.patches[row_indices[i]][col_indices[i]].number_of_agents_at_patch())


        # randomly add the infected number to the grid

        # for x in range(self.global_num_infected):
        #     randomX = self.random_xposition_within_grid(model)
        #     randomY = self.random_yposition_within_grid(model)
        #     self.patches[randomX][randomY].increment_infectious_agents_setup()
        # print(self.global_population)

        self.global_num_susceptible = self.global_population - self.global_num_infected

    def add_agent_to_patch(self, x, y):
        self.global_population += 1
        self.global_num_susceptible += 1
        self.patches[x][y].increment_patch_agents()

    def remove_agent_from_patch(self, x, y):
        self.patches[x][y].decrement_patch_agents()

    def number_of_patches(self):
        return self.rows * self.columns

    def return_travel_rate_travel_short(self):
        return self.travel_rate, self.travel_short

    def return_beta_lambda_gamma(self):
        return self.SEIR_beta, self.SEIR_lambda, self.SEIR_gamma

    def return_global_population(self):
        return self.global_population

    def return_global_num_infected(self):
        return self.global_num_infected

    def return_SEIR_variables(self):
        return self.global_num_susceptible, self.global_num_exposed, self.global_num_infected, self.global_num_immune

    def reset_SEIR_variables(self):
        self.global_num_susceptible = 0
        self.global_num_exposed = 0
        self.global_num_infected = 0
        self.global_num_immune = 0

    def update_global_variables_from_given_patch(self, x, y):
        if (self.patches[x][y].num_infected != 0):
            print("{0},{1}".format(x, y))


        self.global_num_susceptible += self.patches[x][y].num_susceptible
        self.global_num_exposed += self.patches[x][y].num_exposed
        self.global_num_infected += self.patches[x][y].num_infected
        self.global_num_immune += self.patches[x][y].num_immune

    def random_xposition_within_grid(self, model):
        xlimit = model.environments["agent_env"].xsize - 1
        return random.randint(0, xlimit)

    def random_yposition_within_grid(self, model):
        ylimit = model.environments["agent_env"].ysize - 1
        return random.randint(0, ylimit)


    # WILL PRINT OUT MATRIX WITH AXIS
    # ------------------------------> (y) ROWS
    # | (0,0) (0,1) (0,2) (0,3) (0,4) ...
    # | (1,0) (1,1) (1,2) (1,3) (1,4) ...
    # | (2,0) ...........................
    # | (3,0) ...........................
    # | (4,0) ...........................
    # (x) .................................
    # COLUMNS
    def print_out_region_patches(self):
        for x in range(self.columns):
            for y in range(self.rows):
                print("[",self.patches[x][y].number_of_agents_at_patch(),"]", end="")
                if y == (self.columns - 1):
                    print(" ")

class RegionSteppable(Steppable):

    def __init__(self, model):
        super(Steppable, self).__init__()
        self.model = model

        self.model.environments["agent_env"].setup_infection(model)

    def step_main(self, model):
        global_num_infected = model.environments["agent_env"].return_global_num_infected()
        global_population = model.environments["agent_env"].return_global_population()
        beta_lambda_gamma = model.environments["agent_env"].return_beta_lambda_gamma()
        travel_rate_travel_short = model.environments["agent_env"].return_travel_rate_travel_short()
        patches = model.environments["agent_env"].patches
        rows = len(patches)
        columns = len(patches[0])

        # need to rest global variables before counting them again
        model.environments["agent_env"].reset_SEIR_variables()

        # for x in range(rows):
        #     for y in range(columns):
        #         patch.Patch.make_infections(patches[x][y], model, global_num_infected, beta_lambda_gamma[0], travel_rate_travel_short[0], travel_rate_travel_short[1])
        #         patch.Patch.update_SEIR_patches(patches[x][y], beta_lambda_gamma[2], beta_lambda_gamma[1])
        #         model.environments["agent_env"].update_global_variables_from_given_patch(x, y)

        new_cases_made = 0

        for x in range(rows):
            for y in range(columns):
                patch_new_cases_made = patch.Patch.make_infections_first_patch_self_generated(patches[x][y], beta_lambda_gamma[0])
                if(patch_new_cases_made != 0):
                    print("[{0},{1}]".format(x, y))

                new_cases_made += patch_new_cases_made

        for x in range(rows):
            for y in range(columns):
                patch.Patch.make_infections_second_patch_travelling(patches[x][y], model, travel_rate_travel_short[0], travel_rate_travel_short[1])

        migrate_infections = travel_rate_travel_short[0] * (1 - travel_rate_travel_short[1]) * new_cases_made

        for x in range(rows):
            for y in range(columns):
                patch.Patch.make_infections_third_calculate_incidence(patches[x][y], travel_rate_travel_short[0], migrate_infections, global_population)

        for x in range(rows):
            for y in range(columns):
                patch.Patch.update_SEIR_patches(patches[x][y], beta_lambda_gamma[2], beta_lambda_gamma[1])
                model.environments["agent_env"].update_global_variables_from_given_patch(x, y)

    def step_epilogue(self, model):
        agent_env = model.environments["agent_env"]
        #model.environments["agent_env"].print_out_region_patches()

        SEIR_variables = model.environments["agent_env"].return_SEIR_variables()

        total_people = SEIR_variables[0] + SEIR_variables[1] + SEIR_variables[2] + SEIR_variables[3]

        print("S:{0:.2f}, E:{1:.2f}, I:{2:.2f}, R:{3:.2f}".format(SEIR_variables[0], SEIR_variables[1], SEIR_variables[2], SEIR_variables[3]))

        print("TOTAL: {0}".format(round(total_people)))


