"""
A simple model which introduces the use of an ObjectGrid Environment to hold
an agent and a numerical environment to hold values. The agent moves through
the environment and reads off values.
"""
from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D
from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper
import random
import Region

class SimpleAgent(Agent):

    def __init__(self, model):
        super(SimpleAgent, self).__init__()
        randomX = self.random_xposition_within_grid(model)
        randomY = self.random_yposition_within_grid(model)
        #numerical_env.grid[(randomX, randomY)] += 1

        # automatically adds agent to the environment
        self.add_agent_to_grid("agent_env", (randomX, randomY), model)
        model.environments["agent_env"].add_agent_to_patch(randomX, randomY)

        self.end_of_grid = False

    def random_xposition_within_grid(self, model):
        xlimit = model.environments["agent_env"].xsize - 1
        return random.randint(0, xlimit)

    def random_yposition_within_grid(self, model):
        ylimit = model.environments["agent_env"].ysize - 1
        return random.randint(0, ylimit)

    def step_main(self, model):
        current_position = self.environment_positions["agent_env"]
        # grid_value = model.environments["value_env"].grid[current_position]
        #
        # print("Number of agents at poisition ({0}, {1}) is {2}".format(
        #     current_position[0], current_position[1], grid_value))

        number_of_agents_at_patch = model.environments["agent_env"].patches[current_position[0]][current_position[1]].number_of_agents_at_patch()
        print("Number of agents at patch ({0}, {1}) is {2}".format(
            current_position[0], current_position[1], number_of_agents_at_patch))

        self.__move_to_next_position(model)

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
        model.environments["agent_env"].remove_agent_from_patch(new_position[0], new_position[1])
        model.environments["agent_env"].add_agent_to_patch(new_position[0], new_position[1])
        self.move_agent("agent_env", new_position, model)

xsize = ysize = 3
model = Model(xsize * ysize + 5)

# Creating the grid automatically binds it to the model
Region.Region("agent_env", xsize, ysize, model, 1, 1, 1)
numerical_env = NumericalGrid2D("value_env", xsize, ysize, model)

agents = []
for x in range(0, 5):
    agents.append(SimpleAgent(model))
    model.schedule.agents.add(agents[x])
    numerical_env.grid[(0, 0)] += 1

model.schedule.helpers.append(Region.RegionHelper())

model.run()