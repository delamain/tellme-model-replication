from panaxea.core.Steppables import Steppable
from random import shuffle, random


class Patch(Steppable):

    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord
        self.num_travel_incases = 0
        self.num_susceptible = 0
        self.num_infected = 0
        self.num_exposed = 0
        self.num_immune = 0
        self.num_incidence = 0 # population to be converted to exposed
        self.population = 0
        self.beta_local = 0
        self.new_cases_made = 0
        self.selfisolation_ticks = 0
        self.agents = []
        self.within_border = False

    def increment_patch_agents(self):
        self.num_susceptible += 1

    def set_infectious_agents_setup(self, numberOfInfectiousAgents):
        if (numberOfInfectiousAgents < 100):
            numberOfInfectiousAgents = 100

        self.num_infected = numberOfInfectiousAgents
        self.num_susceptible = self.num_susceptible - numberOfInfectiousAgents

        for agentToBeInfected in range(0, int(round(self.num_infected))):
            self.agents[agentToBeInfected].set_agent_infected()

    def number_of_agents_at_patch(self):
        return self.population

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
        # error catching to avoid dividing by zero where no agents exist at patch
        if (self.population != 0):
            self.new_cases_made = self.num_infected * self.beta_local * (self.num_susceptible / self.population)
            # if (self.new_cases_made != 0):
            #     tempVar = self.num_susceptible / self.population
            #     print("sus / pop: {0}".format((tempVar)))
        else:
            self.new_cases_made = 0

        return self.new_cases_made

    def make_infections_second_patch_travelling(self, model, travel_rate, travel_short):
        num_distribute = self.new_cases_made * travel_rate * travel_short
        neighbours = self.get_moore_neighbourhood(model, self.x, self.y)
        nbr_popn = 0
        for neighbour in neighbours:

            # if the neighbour patch is within live patches
            # add that neighbour's population to nbr_popn
            if (model.environments["agent_env"].patches[neighbour[0]][
                neighbour[1]] in model.environments["agent_env"].live_patches and model.environments["agent_env"].patches[neighbour[0]][
                neighbour[1]].within_border == True):

                individual_neighbour_population = model.environments["agent_env"].patches[neighbour[0]][
                    neighbour[1]].number_of_agents_at_patch()

                nbr_popn += individual_neighbour_population

        for neighbour in neighbours:
            if (model.environments["agent_env"].patches[neighbour[0]][
                neighbour[1]] in model.environments["agent_env"].live_patches):

                model.environments["agent_env"].patches[neighbour[0]][
                    neighbour[1]].num_travel_incases = model.environments["agent_env"].patches[neighbour[0]][
                    neighbour[1]].num_travel_incases + (num_distribute * (self.population / nbr_popn))

        #self.num_travel_incases = self.num_travel_incases + (num_distribute * (self.population / nbr_popn))


    def make_infections_third_calculate_incidence(self, travel_rate, migrate_infections, global_population):
        self.num_incidence = self.new_cases_made * (1 - travel_rate)
        self.num_incidence = self.num_incidence + (migrate_infections * (self.population / global_population)) + \
                                                + self.num_travel_incases
        if (self.num_incidence > self.num_susceptible):
            self.num_incidence = self.num_susceptible

    # calculated the number of new exposures / infections and allocate to patches
    def make_infections(self, model, global_num_infected, SEIR_beta, travel_rate, travel_short):

        # [FIRST BLOCK WITHIN MAKE_INFECTIONS]
        num_travel_incases = 0
        self.beta_local = SEIR_beta
        # error catching to avoid dividing by zero where no agents exist at patch
        if (self.population != 0):
            self.new_cases_made = self.num_infected * self.beta_local * (self.num_susceptible / self.population)
        else:
            self.new_cases_made = 0

        # [SECOND BLOCK WITHIN MAKE_INFECTIONS]
        num_distribute = self.new_cases_made * travel_rate * travel_short
        neighbours = self.get_moore_neighbourhood(model, self.x, self.y)
        #print(neighbours)

        nbr_popn = 0
        for neighbour in neighbours:
            individual_neighbour_population = model.environments["agent_env"].patches[neighbour[0]][neighbour[1]].number_of_agents_at_patch()
            if (individual_neighbour_population != 0):
                nbr_popn += individual_neighbour_population

        if (nbr_popn == 0):
            nbr_popn = 1

        num_travel_incases = num_travel_incases + (num_distribute * (self.population / nbr_popn))
        if (num_distribute != 0):
            print(num_distribute)
        #


        # [THIRD BLOCK WITHIN MAKE_INFECTIONS]
        self.num_incidence = self.new_cases_made + num_travel_incases
        #self.num_incidence = self.num_incidence

        if (self.num_incidence > self.num_susceptible):
            self.num_incidence = self.num_susceptible

    # SEIR_beta force of infection in epidemic model (excluding protective behaviour)
    # SEIR_lambda transition rate from E to I
    # SEIR_gamma transition rate from I to R
    def update_SEIR_patches(self, SEIR_gamma, SEIR_lambda):

        self.num_immune = self.num_immune + (SEIR_gamma * self.num_infected)

        if (SEIR_lambda > 0):
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + (SEIR_lambda * self.num_exposed)

            self.num_exposed = ((1 - SEIR_lambda) * self.num_exposed) + self.num_incidence

            # if (self.num_exposed != 0):
            #     print("Travelling in cases detected at patch [{0},{1}], {2}".format(self.x, self.y, self.num_exposed))

            if (self.num_exposed < 1):
                self.num_exposed = 0
        else:
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + self.num_incidence

            self.num_exposed = 0

            if (self.num_infected < 1):
                self.num_infected = 0

        self.num_susceptible = self.num_susceptible - self.num_incidence

        #print("Patch [{0},{1}], S:{2}, E:{3}, I:{4}, R:{5}".format(self.x, self.y, self.num_susceptible, self.num_exposed, self.num_infected, self.num_immune))

    #     ; calculate discounted cumulative incidence
    #       NEED TO IMPLEMENT

    def update_SEIR_persons(self, SEIR_lambda):
        for agent in self.agents:
            if (agent.check_agent_not_exposed_not_infected_not_immune == False):
                random_float = random.uniform(0, 1.0)
                if (random_float < (self.num_incidence / self.population)):
                    if (SEIR_lambda > 0):
                        agent.set_agent_exposed()
                    else:
                        agent.set_agent_infected()

