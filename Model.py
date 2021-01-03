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

class InfectionAgent(Agent):

    def __init__(self, model):
        super(InfectionAgent, self).__init__()
        randomX = model.environments["agent_env"].random_xposition_within_grid(model)
        randomY = model.environments["agent_env"].random_yposition_within_grid(model)

        # automatically adds agent to the environment
        self.add_agent_to_grid("agent_env", (randomX, randomY), model)
        model.environments["agent_env"].add_agent_to_patch(randomX, randomY)

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

xsize = ysize = 5
model = Model(150)

population = 500
R0 = 20
recovery_period = 7
latency_period = 20

# Creating the grid automatically binds it to the model
Region.Region("agent_env", xsize, ysize, model, population, R0, recovery_period, latency_period)
numerical_env = NumericalGrid2D("value_env", xsize, ysize, model)

agents = []
for x in range(0, population):
    agents.append(InfectionAgent(model))
    model.schedule.agents.add(agents[x])
    numerical_env.grid[(0, 0)] += 1

model.schedule.helpers.append(Region.RegionSteppable())
model.environments["agent_env"].setup_infection(model)

displayModel = DisplayModel.DisplayModel(model)
model.schedule.helpers.append(displayModel)

model.run()

DisplayModel.DisplayModel.display_result(displayModel)