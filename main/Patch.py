from panaxea.core.Steppables import Steppable
from random import shuffle, random
from main import Reps
import random

class Patch(Steppable):

    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord

        # epidemic model operations
        self.beta_local = 0
        self.new_cases_made = 0
        self.num_susceptible = 0
        self.num_infected = 0
        self.num_exposed = 0
        self.num_incidence = 0  # population to be converted to exposed
        self.num_travel_incases = 0
        self.num_immune = 0

        # accessed by people on patch for behaviour
        self.visible_patches = None
        self.normsV = None
        self.normsNV = None
        self.cumulative_incidence = 0
        self.patch_risk = None

        # my own implementation variables
        self.cumulative_infected = 0
        self.population = 0
        self.within_border = False
        self.color = 0
        self.reps_own = Reps.Reps()
        self.agents = []

        self.selfisolation_ticks = 0

        self.visible_patches = []
        self.attitudeV_current_set = []
        self.attitudeNV_current_set = []
        self.numberOfAgents = 0

    def set_infectious_agents_setup(self, numberOfInfectiousAgents):
        if (numberOfInfectiousAgents < 100):
            numberOfInfectiousAgents = 100

        self.num_infected = numberOfInfectiousAgents
        self.num_susceptible = self.num_susceptible - numberOfInfectiousAgents

    def set_visible_patches(self, model):
        neighbourhood = self.get_moore_neighbourhood(model, self.x, self.y)
        region = model.environments["agent_env"]

        for neighbour in neighbourhood:
            individualPatch = region.patches[neighbour[0], neighbour[1]]
            if (individualPatch.within_border == True):
                self.visible_patches.append(individualPatch)

    def make_reps(self):
        self.reps_own.ave_attitudeV = 0
        self.reps_own.max_attitudeV = 0
        self.reps_own.min_attitudeV = 0
        self.reps_own.prop_protect_patch = 0

        for agent in self.agents:
            if (agent.behave_protect == True):
                self.reps_own.prop_protect_patch += 1

    def return_x_coord(self):
        return self.x

    def return_y_coord(self):
        return self.y

    def valid_position(self, model, position):
        return model.environments["agent_env"].xsize > position[0] >= 0 and model.environments["agent_env"].ysize > position[1] >= 0

    def get_moore_neighbourhood(self, model, positionx, positiony, shuffle_neigh=True):
        position = [positionx, positiony]
        neigh = [
            (position[0] + 1, position[1] - 1),
            (position[0] + 1, position[1]),
            (position[0] + 1, position[1] + 1),
            (position[0], position[1] - 1),
            (position[0], position[1] + 1),
            (position[0] - 1, position[1] - 1),
            (position[0] - 1, position[1]),
            (position[0] - 1, position[1] + 1),
        ]

        neigh = [n for n in neigh if self.valid_position(model, n)]

        if shuffle_neigh:
            shuffle(neigh)

        return neigh

    def make_infections_first_patch_self_generated(self, SEIR_beta, efficacy_protect, efficacy_vaccine):
        self.num_travel_incases = 0

        PP = self.reps_own.prop_protect_patch
        PV = self.reps_own.prop_vaccinate_patch

        #print("PP:", PP, " PV:", PV)

        self.beta_local = SEIR_beta #* (1 - (PP * efficacy_protect)) * (1 - (PV * efficacy_vaccine))

        self.new_cases_made = self.num_infected * self.beta_local * (self.num_susceptible / self.population)

        return self.new_cases_made

    def make_infections_second_patch_travelling(self, model, travel_rate, travel_short):
        num_distribute = self.new_cases_made * travel_rate * travel_short
        neighbours = self.get_moore_neighbourhood(model, self.x, self.y)
        nbr_popn = 0
        for neighbour in neighbours:

            # if the neighbour patch is within live patches
            # add that neighbour's population to nbr_popn
            if (model.environments["agent_env"].patches[neighbour[0]][
                neighbour[1]] in model.environments["agent_env"].live_patches):

                individual_neighbour_population = model.environments["agent_env"].patches[neighbour[0]][
                    neighbour[1]].population

                nbr_popn += individual_neighbour_population

        for neighbour in neighbours:
            if (model.environments["agent_env"].patches[neighbour[0]][
                neighbour[1]] in model.environments["agent_env"].live_patches):

                model.environments["agent_env"].patches[neighbour[0]][
                    neighbour[1]].num_travel_incases = model.environments["agent_env"].patches[neighbour[0]][
                    neighbour[1]].num_travel_incases + (num_distribute * (self.population / nbr_popn))

        #self.num_travel_incases = self.num_travel_incases + (num_distribute * (self.population / nbr_popn))


    def make_infections_third_calculate_incidence(self, travel_rate, migrate_infections, global_population, count):
        self.num_incidence = self.new_cases_made * (1 - travel_rate)

        if (self.new_cases_made == 0):
            count += 1

        self.num_incidence = self.num_incidence + (migrate_infections * (self.population / global_population)) + \
                                                + self.num_travel_incases

        if (self.num_incidence > self.num_susceptible):
            self.num_incidence = self.num_susceptible

        return count

    # SEIR_beta force of infection in epidemic model (excluding protective behaviour)
    # SEIR_lambda transition rate from E to I
    # SEIR_gamma transition rate from I to R
    def update_SEIR_patches(self, SEIR_gamma, SEIR_lambda, incidence_dicount):

        self.num_immune = self.num_immune + (SEIR_gamma * self.num_infected)

        if (SEIR_lambda > 0):
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + (SEIR_lambda * self.num_exposed)

            self.num_exposed = ((1 - SEIR_lambda) * self.num_exposed) + self.num_incidence

            # this causes the total number of people to decrease (i.e. through continually rounding down)
            if (self.num_exposed < 1):
                self.num_exposed = 0
        else:
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + self.num_incidence

            self.cumulative_infected += self.num_infected

            self.num_exposed = 0

            if (self.num_infected < 1):
                self.num_infected = 0

        self.num_susceptible = self.num_susceptible - self.num_incidence

        num_incidence_visble_patches = 0
        sum_population_visible_patches = 0

        for neighbour_patch in self.visible_patches:
            num_incidence_visble_patches += neighbour_patch.num_incidence
            sum_population_visible_patches += neighbour_patch.population

        if (sum_population_visible_patches != 0):
            self.cumulative_incidence = (num_incidence_visble_patches / sum_population_visible_patches) \
                                        + (1 - incidence_dicount) * self.cumulative_incidence

            if self.cumulative_incidence != 0:
                pass

        else:
            #print(len(self.visible_patches))
            # no visible patches and so get division by 0 error for the neighbouring populations
            # artificial value is set for cumulative incidence
            self.cumulative_incidenc = 0.1


        seirValue = self.num_susceptible + self.num_exposed + self.num_infected + self.num_immune

        if ((self.num_susceptible or self.num_exposed or self.num_infected or self.num_immune) < 0):
            print("ERROR", self.x, self.y)

    def update_SEIR_persons_first(self, SEIR_lambda, SEIR_gamma):
        for agent in self.agents:
            if (agent.infected == True or agent.exposed == True):
                agent.disease_day += 1

            if (SEIR_lambda > 0 and agent.exposed == True):
                random_float = random.uniform(0, 1.0)
                if (random_float < SEIR_lambda):
                    agent.exposed = False
                    agent.infected = True

                random_float = random.uniform(0, 1.0)
                if (agent.infected == True and random_float < SEIR_gamma):
                    agent.infected = False
                    agent.immune = True

    def update_SEIR_persons_new_infections_second(self, SEIR_lambda):
        for agent in self.agents:
            if (agent.exposed == False and agent.infected == False and agent.immune == False and agent.vaccinated == False):
                random_float = random.uniform(0, 1.0)
                if (random_float < (self.num_incidence / self.population)):
                    if (SEIR_lambda > 0):
                        agent.exposed = True
                    else:
                        agent.infected = True

