from panaxea.core.Steppables import Agent

class InfectionAgent(Agent):

    def __init__(self, model, xpos, ypos):
        self.environment_positions = dict()
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

    # def __move_to_next_position(self, model):
    #
    #     current_position = self.environment_positions["agent_env"]
    #
    #     xlimit = model.environments["agent_env"].xsize - 1
    #     ylimit = model.environments["agent_env"].ysize - 1
    #
    #     # return a shuffled random list of the adjacent positions
    #     adjacentPositions = Region.Region.get_moore_neighbourhood(model.environments["agent_env"], current_position, True)
    #
    #     # if it is a valid position to move to
    #     if (model.environments["agent_env"].valid_position(adjacentPositions[0])):
    #         new_position = adjacentPositions[0]
    #
    #     # before moving, need to update the number of agents at that patch
    #     #model.environments["agent_env"].remove_agent_from_patch(new_position[0], new_position[1])
    #     #model.environments["agent_env"].add_agent_to_patch(new_position[0], new_position[1])
    #     self.move_agent("agent_env", new_position, model)

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