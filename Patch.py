from panaxea.core.Steppables import Steppable

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

    def increment_patch_agents(self):
        self.num_susceptible += 1
        self.population += 1

    def decrement_patch_agents(self):
        self.num_susceptible -= 1
        self.population -= 1

    def increment_infectious_agents_setup(self):
        self.num_infected += 1
        self.num_susceptible -= 1

    def number_of_agents_at_patch(self):
        return self.population

    # calculated the number of new exposures / infections and allocate to patches
    def make_infections(self, SEIR_beta):

        # [FIRST BLOCK WITHIN MAKE_INFECTIONS]
        # each patch calculates the number of new infections generated by itself
        # which are distributed as exposed
        self.num_travel_incases = 0

        # let PP max [ prop-protect-patch ] of reps-here    ; need to use 'max' as NetLogo cannot assume only one 'reps' agent is on patch
        # let PV max [ prop-vaccinate-patch ] of reps-here
        self.beta_local = SEIR_beta
        # error catching to avoid dividing by zero where no agents exist at patch
        if (self.population != 0):
            self.new_cases_made = self.num_infected * self.beta_local * (self.num_susceptible / self.population)
        else:
            self.new_cases_made = 0

        # [SECOND BLOCK WITHIN MAKE_INFECTIONS]
        # TBC
        # TBC

        # [THIRD BLOCK WITHIN MAKE_INFECTIONS]
        self.num_incidence = self.new_cases_made
        #self.num_incidence = self.num_incidence

        if (self.num_incidence > self.num_susceptible):
            self.num_incidence = self.num_susceptible

    # SEIR_beta force of infection in epidemic model (excluding protective behaviour)
    # SEIR_lambda transition rate from E to I
    # SEIR_gamma transition rate from I to R
    def update_SEIR_patches(self, SEIR_gamma, SEIR_lambda):
        self.num_immune = self.num_immune + (SEIR_gamma * self.num_infected)

        if (SEIR_gamma > 0):
            self.num_infected = ((1 - SEIR_gamma) * self.num_infected) + (SEIR_lambda * self.num_exposed)

            self.num_exposed = ((1 - SEIR_lambda) * self.num_exposed) + self.num_incidence

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
