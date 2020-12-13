from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D
from panaxea.core.Steppables import Steppable, Helper

class Region(ObjectGrid2D):

    def __init__(self, name, xsize, ysize, model, R0, recovery_period, latency_period):
        super(Region, self).__init__(name, xsize, ysize, model)
        self.global_num_susceptible = 0
        self.global_num_infected = 0
        self.global_num_exposed = 0
        self.global_num_immune = 0
        self.global_num_incidence = 0  # population to be converted to exposed
        self.global_number_of_agents = 0

        self.SEIR_beta = R0 / recovery_period

        if (latency_period == 0):
            SEIR_lambda =  0
        else:
            SEIR_lambda = 1 / latency_period

        self.SEIR_gamma = 1 / recovery_period


        # matrix of patches
        self.patches = [[Patch(x, y) for x in range(xsize)] for y in range(ysize)]

    def add_agent_to_patch(self, x, y):
        self.patches[x][y].increment_patch_agents()

    def remove_agent_from_patch(self, x, y):
        self.patches[x][y].decrement_patch_agents()

    def number_of_patches(self):
        rows = len(self.patches)
        columns = len(self.patches[0])
        return rows * columns

    def print_out_region_patches(self):
        rows = len(self.patches)
        columns = len(self.patches[0])
        for x in range(columns):
            for y in range(rows):
                print("[",self.patches[x][y].number_of_agents_at_patch(),"],", end="")
                if y == (columns - 1):
                    print(" ")

class RegionHelper(Helper):

    def __init__(self):
        super(Helper, self).__init__()

    def step_epilogue(self, model):
        agent_env = model.environments["agent_env"]
        model.environments["agent_env"].print_out_region_patches()


class Patch(Steppable):

    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord
        self.num_susceptible = 0
        self.num_infected = 0
        self.num_exposed = 0
        self.num_immune = 0
        self.num_incidence = 0 # population to be converted to exposed
        self.number_of_agents = 0

    def increment_patch_agents(self):
        self.number_of_agents += 1

    def decrement_patch_agents(self):
        self.number_of_agents -= 1

    def number_of_agents_at_patch(self):
        return self.number_of_agents

    # calculated the number of new exposures / infections and allocate to patches
    def make_infections(self):
        return

    # day t
    # n is the population
    # beta, gamma and delta are all adjustable
    def seir_calculations(self, y, t, N, beta, gamma, delta):
        S, E, I, R = y

        # number of susceptible
        dSdt = -beta * S * (I/N)

        # number of exposed
        dEdt = beta * S * (I / N) - (delta * E)

        # number of infected
        dIdt = (delta * E) - (gamma * R)

        # number of recoverd
        dRdt = gamma * I

        return dSdt, dEdt, dIdt, dRdt

    # SEIR_beta force of infection in epidemic model (excluding protective behaviour)
    # SEIR_lambda transition rate from E to I
    # SEIR_gamma transition rate from I to R
    def update_SEIR_patches(self, SEIR_gamma, SEIR_lambda):

        self.num_immune = self.num_immune + (SEIR_gamma * self.num_infected)

        if (SEIR_gamma > 0):
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + (SEIR_lambda * self.num_exposed)

            self.num_exposed = (1 - SEIR_lambda) * self.num_exposed + self.num_incidence

            if (self.num_exposed < 1):
                num_exposed = 0
        else:
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + num_incidence

            self.num_exposed = 0

            if (self.num_infected < 1):
                self.num_infected = 0

        self.num_susceptible = self.num_susceptible - self.num_incidence

        # def update_SEIR_patches(self, SEIR_gamma, SEIR_lambda, num_immune, num_infected, num_exposed, num_incidence,
        #                         num_susceptible):
        #
        #     num_immune = num_immune + (SEIR_gamma * num_infected)
        #
        #     if (SEIR_gamma > 0):
        #         num_infected = ((1 - SEIR_gamma) * num_infected) + (SEIR_lambda * num_exposed)
        #
        #         num_exposed = (1 - SEIR_lambda) * num_exposed + num_incidence
        #
        #         if (num_exposed < 1):
        #             num_exposed = 0
        #     else:
        #         num_infected = ((1 - SEIR_gamma) * num_infected) + num_incidence
        #
        #         num_exposed = 0
        #
        #         if (num_infected < 1):
        #             num_infected = 0
        #
        #     num_susceptible = num_susceptible - num_incidence

    #     ; calculate discounted cumulative incidence
    #       NEED TO IMPLEMENT

    # def step_main(self):


