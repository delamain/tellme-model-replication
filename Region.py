from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D

class Region(ObjectGrid2D):

    def __init__(self, name, xsize, ysize, model):
        super(Region, self).__init__(name, xsize, ysize, model)

        #self.patches = list()

        # matrix of patches
        self.patches = [[Patch.__init__(self, x, y) for x in range(xsize)] for y in range(ysize)]

        # for x in range(xsize):
        #     for y in range(ysize):
        #         self.patches.insert()
        #         self.patches.append(Patch.__init__(self, x, y))

    def add_agent_to_patch(self, x, y):
        self.patches[x][y].Patch.increment_patch_agents()
        print("PRINTING PATCH X, Y:", self.patches[x][y].number_of_agents)

    def number_of_patches(self):
        rows = len(self.patches)
        columns = len(self.patches[0])
        return rows * columns

class Patch():

    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord
        self.susceptible = 0
        self.infected = 0
        self.recovered = 0
        self.number_of_agents = 0

        return self

    def increment_patch_agents(self):
        self.number_of_agents += 1

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