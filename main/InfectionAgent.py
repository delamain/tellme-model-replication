import math
import random

from panaxea.core.Steppables import Agent

class InfectionAgent(Agent):

    def __init__(self, model, xpos, ypos):
        region = model.environments["agent_env"]
        self.environment_positions = dict()
        self.x_coord = xpos
        self.y_coord = ypos

        # attitudes and behaviour values
        self.attitudeV_initial = None
        self.attitudeV_current = None
        self.behaviourV_value = None
        self.behave_vaccinate = None
        self.attitudeNV_initial = None
        self.attitudeNV_current = None
        self.behave_protect = False
        self.behave_vaccinate = False
        self.frezied = False

        self.trust = None
        self.attitudeV_change = None
        self.attitudeNV_change = None
        self.info_receieved = False
        self.normsV_change = None
        self.normsNV_change = None
        self.rec_vaccinate = False
        self.rec_protect = False

        # disease progression
        self.susceptible = True
        self.exposed = False
        self.infected = False
        self.disease_day = 0
        self.immune = False
        self.vaccinated = False

        # media reception information
        if (random.uniform(0, 1.0) < region.prop_in_target):
            self.in_target = True
        else:
            self.in_target = False

        if (random.uniform(0, 1.0) < (region.popn_hcw / 1000)):
            self.hcw = True
        else:
            self.hcw = False

        if (random.uniform(0, 1.0) < region.prop_social_media):
            self.use_social_media = True
        else:
            self.use_social_media = False

        # automatically adds agent to the environment
        self.add_agent_to_grid("agent_env", (xpos, ypos), model)

        self.initial_attitude(model)
        self.end_of_grid = False

    def check_agent_not_exposed_not_infected_not_immune(self):
        if (self.exposed or self.infected or self.immune == True):
            return False

    def triangular0to1(self, MM, UU):
        if (UU < MM):
            return math.sqrt(UU * MM)
        else:
            return (1 - math.sqrt((1 - UU) * (1 - MM)))

    def initial_attitude(self, model):
        region = model.environments["agent_env"]

        random_float = random.uniform(0, 1.0)
        if (random_float < region.prop_antivax):
            self.attitudeV_initial = self.triangular0to1(0.125, random.uniform(0, 1.0))
        else:
            self.attitudeV_initial = self.triangular0to1(0.75, random.uniform(0, 1.0))

        self.attitudeNV_initial = self.triangular0to1(0.75, random.uniform(0, 1.0))

        if (self.in_target == True):
            self.attitudeV_initial = min(
                self.attitudeV_initial + ((1 - region.prop_in_target) * region.in_target_attitude), 1)
            self.attitudeNV_initial = min(
                self.attitudeNV_initial + ((1 - region.prop_in_target) * region.in_target_attitude), 1)
        else:
            self.attitudeV_initial = max((
                self.attitudeV_initial - (region.prop_in_target * region.in_target_attitude)), 0)
            self.attitudeNV_initial = max((
                self.attitudeNV_initial - (region.prop_in_target * region.in_target_attitude)), 0)

        self.attitudeV_current = self.attitudeV_initial
        self.attitudeNV_current = self.attitudeNV_initial

    def seek_vaccination(self, region):

        if ((region.restrict_vaccine == False or region.epidemic_declared == True)):
            self.behave_vaccinate = True

            random_float = random.uniform(0, 1.0)
            if (random_float < region.efficacy_vaccine):
                self.vaccinated = True

