"""
A simple model which introduces the use of an ObjectGrid Environment to hold
an agent and a numerical environment to hold values. The agent moves through
the environment and reads off values.
"""
from panaxea.core.Environment import ObjectGrid, ObjectGrid2D, NumericalGrid2D, Grid2D
from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent
import random
import Region

class SimpleAgent(Agent):

    def __init__(self, model):
        super(SimpleAgent, self).__init__()
        randomX = self.random_xposition_within_grid(model)
        randomY = self.random_yposition_within_grid(model)
        numerical_env.grid[(randomX, randomY)] += 1

        # automatically adds agent to the environment
        self.add_agent_to_grid("agent_env", (randomX, randomY), model)
        model.environments["agent_env"].add_agent_to_patch(randomX, randomY)

        print("Num of patches", model.environments["agent_env"].number_of_patches())
        self.end_of_grid = False

    def random_xposition_within_grid(self, model):
        xlimit = model.environments["agent_env"].xsize - 1
        return random.randint(0, xlimit)

    def random_yposition_within_grid(self, model):
        ylimit = model.environments["agent_env"].ysize - 1
        return random.randint(0, ylimit)

    def step_main(self, model):
        current_position = self.environment_positions["agent_env"]
        grid_value = model.environments["value_env"].grid[current_position]


        print("Number of agents at poisition ({0}, {1}) is {2}".format(
            current_position[0], current_position[1], grid_value))

        self.__move_to_next_position(model)

    def __move_to_next_position(self, model):
        """
        Moves the agent to the next position in the grid. Movement occurs
        along the x-axis, once the end of the x-axis is reached it proceeds
        to th next y-axis position until the end of the grid is reached.
        Then the agent stops.
        Parameters
        ----------
        model : Model
            The current model instance
        """

        if self.end_of_grid:
            return

        current_position = self.environment_positions["agent_env"]

        xlimit = model.environments["agent_env"].xsize - 1
        ylimit = model.environments["agent_env"].ysize - 1

        if current_position == (xlimit, ylimit):
            self.end_of_grid = True
            return

        # return a shuffled random list of the adjacent positions
        adjacentPositions = Region.Region.get_moore_neighbourhood(model.environments["agent_env"], current_position, True)

        if (model.environments["agent_env"].valid_position(adjacentPositions[0])):
            new_position = adjacentPositions[0]

        self.move_agent("agent_env", new_position, model)


xsize = ysize = 5

model = Model(xsize * ysize + 5)

# Creating the grid automatically binds it to the model
Region.Region("agent_env", xsize, ysize, model)
numerical_env = NumericalGrid2D("value_env", xsize, ysize, model)

agents = []
for x in range(0, 9):
    agents.append(SimpleAgent(model))
    model.schedule.agents.add(agents[x])
    numerical_env.grid[(0, 0)] += 1

model.run()