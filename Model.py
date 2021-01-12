"""
A simple model which introduces the use of an ObjectGrid Environment to hold
an agent and a numerical environment to hold values. The agent moves through
the environment and reads off values.
"""
from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D
from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper
import Region
import DisplayModel
import LoadGISData

class InfectionAgent(Agent):

    def __init__(self, model, xpos, ypos):
        super(InfectionAgent, self).__init__()
        self.x_coord = xpos
        self.y_coord = ypos
        self.susceptible = True
        self.exposed = False
        self.infected = False
        self.immune = False

        # randomX = model.environments["agent_env"].random_xposition_within_grid(model)
        # randomY = model.environments["agent_env"].random_yposition_within_grid(model)

        # automatically adds agent to the environment
        self.add_agent_to_grid("agent_env", (xpos, ypos), model)
        model.environments["agent_env"].add_agent_to_patch(xpos, ypos)

        self.end_of_grid = False

    def step_main(self, model):
        current_position = self.environment_positions["agent_env"]

        number_of_agents_at_patch = model.environments["agent_env"].patches[current_position[0]][current_position[1]].number_of_agents_at_patch()

    def __move_to_next_position(self, model):

        current_position = self.environment_positions["agent_env"]

        xlimit = model.environments["agent_env"].xsize - 1
        ylimit = model.environments["agent_env"].ysize - 1

        # return a shuffled random list of the adjacent positions
        adjacentPositions = Region.Region.get_moore_neighbourhood(model.environments["agent_env"], current_position, True)

        # if it is a valid position to move to
        if (model.environments["agent_env"].valid_position(adjacentPositions[0])):
            new_position = adjacentPositions[0]

        # before moving, need to update the number of agents at that patch
        #model.environments["agent_env"].remove_agent_from_patch(new_position[0], new_position[1])
        #model.environments["agent_env"].add_agent_to_patch(new_position[0], new_position[1])
        self.move_agent("agent_env", new_position, model)

    def set_agent_exposed(self):
        self.susceptible = False
        self.exposed = True

    def set_agent_infected(self):
        self.susceptible = False
        self.exposed = False
        self.infected = True

    def set_agent_recovered(self):
        self.exposed = False
        self.infected = False
        self.immune = True

    def check_agent_not_exposed_not_infected_not_immune(self):
        if (self.exposed or self.infected or self.immune == True):
            return False

gisData = LoadGISData.LoadGISData("popn_density_uk_2015.asc")
xsize = ysize = gisData.return_grid_size()
population = gisData.return_population("UK")

# xsize = ysize = 5
# population = 1000

model = Model(50)
R0 = 3
recovery_period = 5
latency_period = 1

# Creating the grid automatically binds it to the model
region = Region.Region("agent_env", xsize, ysize, model, R0, recovery_period, latency_period)

# adding all the agents within the population to the model
# for x in range(0, population):
#     agents.append(InfectionAgent(model))
#     model.schedule.agents.add(agents[x])

ascii_grid = gisData.return_ascii_grid()
rows = ascii_grid.shape[0]
columns = ascii_grid.shape[1]

population_total = 0
count_of_pop_non_zero_squares = gisData.return_count_of_non_zero_patches()
sum_popn_of_patches_with_popn_greater_than_zero = gisData.return_sum_popn_of_patches_with_popn_greater_than_zero()
factor = (1000 * population) / sum_popn_of_patches_with_popn_greater_than_zero

print("Count of non-zero patches:", count_of_pop_non_zero_squares)
print("Sum of population, with patches with a popn > 0:", sum_popn_of_patches_with_popn_greater_than_zero)
count = 0

for x in range(rows):
    for y in range(columns):
        if (ascii_grid[x, y] != -9999): # if there is a population value
            population_total += ascii_grid[x, y]
            region.patches[x][y].population = round((ascii_grid[x, y]) * factor)

            # add all the agents to the patches
            for individualAgent in range(0, region.patches[x][y].population):
                region.patches[x][y].agents.append(InfectionAgent(model, x, y))

            # add the agents to the schedule
            for individualPatchAgent in region.patches[x][y].agents:
                model.schedule.agents.add(individualPatchAgent)
        else:
            pass



regionSteppableModel = Region.RegionSteppable(model)
displayModel = DisplayModel.DisplayModel(model)

model.schedule.helpers.append(displayModel)
model.schedule.helpers.append(regionSteppableModel)

model.run()

DisplayModel.DisplayModel.display_result(displayModel)