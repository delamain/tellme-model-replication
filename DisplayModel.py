from panaxea.core.Steppables import Steppable
import matplotlib.pyplot as plt

class DisplayModel(Steppable):

    def __init__(self, model):
        self.model = model.environments["agent_env"]
        self.number_of_epochs_count = 0
        self.global_number_of_epochs = []
        self.global_num_susceptible_array = []
        self.global_num_infected_array = []
        self.global_num_exposed_array = []
        self.global_num_immune_array = []
        self.global_num_incidence_array = []
        self.global_prevalence_array = []

    def step_prologue(self, model):
        S, E, I, R = self.model.return_SEIR_variables()
        incidence = self.model.return_num_incidence()
        prevalance = self.model.return_prevalence()

        self.global_number_of_epochs.append(self.number_of_epochs_count)
        self.global_num_susceptible_array.append(S)
        self.global_num_exposed_array.append(E)
        self.global_num_infected_array.append(I)
        self.global_num_immune_array.append(R)
        self.global_num_incidence_array.append(incidence)
        self.global_prevalence_array.append(prevalance)
        self.number_of_epochs_count += 1

    def display_result(self):
        plt.plot(self.global_number_of_epochs, self.global_num_susceptible_array, "-b", label="susceptible")
        plt.plot(self.global_number_of_epochs, self.global_num_exposed_array, "-y", label="exposed")
        plt.plot(self.global_number_of_epochs, self.global_num_infected_array, "-r", label="infected")
        plt.plot(self.global_number_of_epochs, self.global_num_immune_array, "-g", label="immune")

        # incidence and prevalence are displayed in the TELL ME model
        # plt.plot(self.global_number_of_epochs, self.global_num_incidence_array, "-c", label="incidence")
        # plt.plot(self.global_number_of_epochs, self.global_prevalence_array, "-m", label="prevalence")

        plt.legend(loc="upper left")

        plt.show()