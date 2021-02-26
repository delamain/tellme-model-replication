from panaxea.core.Steppables import Steppable
from random import shuffle, random


class Patch(Steppable):

    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord
        self.num_travel_incases = 0
        self.num_susceptible = 0
        self.num_infected = 0
        self.cumulative_infected = 0
        self.num_exposed = 0
        self.num_immune = 0
        self.num_incidence = 0 # population to be converted to exposed
        self.population = 0
        self.beta_local = 0
        self.new_cases_made = 0
        self.selfisolation_ticks = 0
        self.agents = []
        self.within_border = False
        self.color = 0

    def increment_patch_agents(self):
        self.num_susceptible += 1

    def set_infectious_agents_setup(self, numberOfInfectiousAgents):
        if (numberOfInfectiousAgents < 10):
            numberOfInfectiousAgents = 10

        self.num_infected = numberOfInfectiousAgents
        self.num_susceptible = self.num_susceptible - numberOfInfectiousAgents

        for agentToBeInfected in range(0, int(round(self.num_infected))):
            self.agents[agentToBeInfected].set_agent_infected()

    def number_of_agents_at_patch(self):
        return self.population

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

    def make_infections_first_patch_self_generated(self, SEIR_beta):
        self.num_travel_incases = 0
        self.beta_local = SEIR_beta

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

            # if (nbr_popn == 0):
            #     print("NEIGHBOUR POPULATION IS ZERO at", self.x, self.y)

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

            # if (self.num_susceptible == 0):
            #     count += 1
            #print("INCIDENCE IS GREATER THAN SUCEPTIBLE", self.num_susceptible)
            self.num_incidence = self.num_susceptible

        return count

    # SEIR_beta force of infection in epidemic model (excluding protective behaviour)
    # SEIR_lambda transition rate from E to I
    # SEIR_gamma transition rate from I to R
    def update_SEIR_patches(self, SEIR_gamma, SEIR_lambda):

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

        seirValue = self.num_susceptible + self.num_exposed + self.num_infected + self.num_immune

        if ((self.num_susceptible or self.num_exposed or self.num_infected or self.num_immune) < 0):
            print("ERROR", self.x, self.y)

    def update_SEIR_persons(self, SEIR_lambda):
        for agent in self.agents:
            if (agent.check_agent_not_exposed_not_infected_not_immune == False):
                random_float = random.uniform(0, 1.0)
                if (random_float < (self.num_incidence / self.population)):
                    if (SEIR_lambda > 0):
                        agent.set_agent_exposed()
                    else:
                        agent.set_agent_infected()

