import numpy as np
from panaxea.core.Environment import ObjectGrid2D
from panaxea.core.Steppables import Steppable
import random
import Patch

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

        self.incidence_count_flag = 0
        self.susceptible_count_flag = 0

        if (latency_period == 0):
            self.SEIR_lambda =  0
        else:
            self.SEIR_lambda = 1.0 / latency_period

        self.SEIR_gamma = 1.0 / recovery_period
        self.start_epi_locations = 1
        self.start_epi_population = 0.001

        self.patches = np.zeros(shape=(xsize, ysize), dtype=object)
        self.visualised_patches = np.zeros([xsize, ysize, 3], dtype=np.uint8)

        for x in range(xsize):
            for y in range(ysize):
                self.patches[x][y] = Patch.Patch(x, y)

        self.rows = len(self.patches)
        self.columns = len(self.patches[0])

        self.live_patches = set([])

    def setup_infection(self, model):

        patch_populations_matrix = np.zeros(shape=(self.rows, self.columns), dtype=int)

        for x in range(self.rows):
            for y in range(self.columns):
                patch_populations_matrix[x][y] = self.patches[x][y].number_of_agents_at_patch()

        patch_populations_matrix_numpy = np.array(patch_populations_matrix)

        # finding the indexes of the 5 largest population elements within the matrix
        n = 5
        flat_indices = np.argpartition(patch_populations_matrix_numpy.ravel(), -n)[-n:]
        row_indices, col_indices = np.unravel_index(flat_indices, patch_populations_matrix_numpy.shape)

        # printing the maximum five elements and their indices
        for j in range(n):
            print(row_indices[j], col_indices[j], " ", end='')
            print(self.patches[row_indices[j]][col_indices[j]].number_of_agents_at_patch(), " ", end='')

        print("\nMaximum element value: ", patch_populations_matrix_numpy.max())
        #print(np.argmax(patch_populations_matrix_numpy))
        a = patch_populations_matrix_numpy  # Can be of any shape
        indices = np.where(a == a.max())
        print("Indices where maximum element value is found at:", indices)

        # selecting a random element from the top 5 largest
        i = random.randint(0, 4)

        # setting the infectious number of agents at that individual starting patch
        print("START POP, ", self.start_epi_population
                                                                                 * self.patches[row_indices[i]][
                                                                                     col_indices[
                                                                                         i]].number_of_agents_at_patch())

        self.patches[row_indices[i]][col_indices[i]].set_infectious_agents_setup(self.start_epi_population
                                                                                 * self.patches[row_indices[i]][
                                                                                     col_indices[
                                                                                         i]].number_of_agents_at_patch())

        # susceptible = patch population - number of infected
        self.patches[row_indices[i]][col_indices[i]].num_susceptible = self.patches[row_indices[i]][
                                                                           col_indices[i]].population - \
                                                                       self.patches[row_indices[i]][
                                                                           col_indices[i]].num_infected

    # this function will only be called once
    # increments global population and num susceptible to assist reporting
    def add_agent_to_patch(self, x, y):
        self.global_population += 1
        self.global_num_susceptible += 1
        self.patches[x][y].increment_patch_agents()

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

    def return_num_incidence(self):
        return self.global_num_incidence / self.global_population

    def return_global_num_incidence(self):
        return self.global_num_incidence

    def return_prevalence(self):
        return self.global_num_infected / self.global_population

    def reset_SEIR_variables(self):
        self.global_num_susceptible = 0
        self.global_num_exposed = 0
        self.global_num_infected = 0
        self.global_num_immune = 0

    def update_global_variables_from_given_patch(self, x, y):
        self.global_num_susceptible += self.patches[x][y].num_susceptible
        self.global_num_exposed += self.patches[x][y].num_exposed
        self.global_num_infected += self.patches[x][y].num_infected
        self.global_num_immune += self.patches[x][y].num_immune

        self.global_num_incidence += self.patches[x][y].num_incidence

    def random_xposition_within_grid(self, model):
        xlimit = model.environments["agent_env"].xsize - 1
        return random.randint(0, xlimit)

    def random_yposition_within_grid(self, model):
        ylimit = model.environments["agent_env"].ysize - 1
        return random.randint(0, ylimit)


    # WILL PRINT OUT MATRIX WITH AXIS
    # ------------------------------> (y) COLUMNS
    # | (0,0) (0,1) (0,2) (0,3) (0,4) ...
    # | (1,0) (1,1) (1,2) (1,3) (1,4) ...
    # | (2,0) ...........................
    # | (3,0) ...........................
    # | (4,0) ...........................
    # (x) .................................
    # ROWS
    def print_out_region_patches(self):
        for x in range(self.rows):
            for y in range(self.columns):
                print("[",self.patches[x][y].number_of_agents_at_patch(),"]", end="")
                if y == (self.columns - 1):
                    print(" ")

class RegionSteppable(Steppable):

    def __init__(self, model):
        super(Steppable, self).__init__()
        model.environments["agent_env"].setup_infection(model)

    def step_prologue(self, model):
        SEIR_variables = model.environments["agent_env"].return_SEIR_variables()
        global_incidence = model.environments["agent_env"].return_global_num_incidence()

        total_people = SEIR_variables[0] + SEIR_variables[1] + SEIR_variables[2] + SEIR_variables[3]

        print(
            "S:{0:.2f}, E:{1:.2f}, I:{2:.2f}, R:{3:.2f}".format(SEIR_variables[0], SEIR_variables[1], SEIR_variables[2],
                                                                SEIR_variables[3]))
        print("GLOBAL INCIDENCE: ", global_incidence)

        print("TOTAL: {0}".format(round(total_people)))

    def step_main(self, model):
        global_population = model.environments["agent_env"].return_global_population()
        beta_lambda_gamma = model.environments["agent_env"].return_beta_lambda_gamma()
        travel_rate_travel_short = model.environments["agent_env"].return_travel_rate_travel_short()
        patches = model.environments["agent_env"].patches

        # need to rest global variables before counting them again
        model.environments["agent_env"].reset_SEIR_variables()

        new_cases_made = 0

        live_patches_list = list(model.environments["agent_env"].live_patches)
        random.shuffle(live_patches_list)
        for currentPatch in live_patches_list:
            patch_new_cases_made = Patch.Patch.make_infections_first_patch_self_generated(currentPatch, beta_lambda_gamma[0])
            new_cases_made += patch_new_cases_made

        for currentPatch in live_patches_list:
            Patch.Patch.make_infections_second_patch_travelling(currentPatch, model, travel_rate_travel_short[0], travel_rate_travel_short[1])

        migrate_infections = travel_rate_travel_short[0] * (1 - travel_rate_travel_short[1]) * new_cases_made

        self.count_of_patches_with_incidence_greater_than_susceptible = 0

        for currentPatch in live_patches_list:
            self.count_of_patches_with_incidence_greater_than_susceptible = Patch.Patch.make_infections_third_calculate_incidence(currentPatch, travel_rate_travel_short[0], migrate_infections, global_population, self.count_of_patches_with_incidence_greater_than_susceptible)
            model.environments["agent_env"].global_num_incidence += currentPatch.num_incidence

        if (model.environments["agent_env"].global_num_incidence < 1):
            exit()

        print("NUMBER OF PATCHES WITH NEW CASES MADE = 0 ", self.count_of_patches_with_incidence_greater_than_susceptible)


        for currentPatch in live_patches_list:
            Patch.Patch.update_SEIR_patches(currentPatch, beta_lambda_gamma[2], beta_lambda_gamma[1])
            model.environments["agent_env"].update_global_variables_from_given_patch(currentPatch.x, currentPatch.y)

    def step_epilogue(self, model):
        agent_env = model.environments["agent_env"]
        #model.environments["agent_env"].print_out_region_patches()

        # SEIR_variables = model.environments["agent_env"].return_SEIR_variables()
        #
        # total_people = SEIR_variables[0] + SEIR_variables[1] + SEIR_variables[2] + SEIR_variables[3]
        #
        # print("S:{0:.2f}, E:{1:.2f}, I:{2:.2f}, R:{3:.2f}".format(SEIR_variables[0], SEIR_variables[1], SEIR_variables[2], SEIR_variables[3]))
        #
        # print("TOTAL: {0}".format(round(total_people)))


