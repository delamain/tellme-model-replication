import os
import cv2
import csv

from panaxea.core.Steppables import Steppable
import matplotlib.pyplot as plt
from natsort import natsorted

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

        self.regions_affected_by_epidemic = []

        self.iteration_count = 0

    def step_prologue(self, model):
        S, E, I, R = self.model.return_SEIR_variables()
        incidence = self.model.return_num_incidence()
        prevalance = self.model.return_prevalence()
        regions_affected_by_epidemic = self.regions_affected_by_epidemic_calculation()

        self.global_number_of_epochs.append(self.number_of_epochs_count)
        self.global_num_susceptible_array.append(S)
        self.global_num_exposed_array.append(E)
        self.global_num_infected_array.append(I)
        self.global_num_immune_array.append(R)
        self.global_num_incidence_array.append(incidence)
        self.global_prevalence_array.append(prevalance)
        self.regions_affected_by_epidemic.append(regions_affected_by_epidemic)
        self.number_of_epochs_count += 1

        region = model.environments["agent_env"]

        self.color_patches(region.live_patches, region.global_population)

        for x in range(region.rows):
            for y in range(region.columns):
                region.visualised_patches[x][y] = region.patches[x][y].color

        self.display_graphical_matrix(region.visualised_patches)


        self.iteration_count += 1

    def regions_affected_by_epidemic_calculation(self):
        regions_affected_count = 0

        for currentPatch in self.model.live_patches:
            if currentPatch.num_susceptible < (0.95 * currentPatch.population):
                regions_affected_count += 1

        print(regions_affected_count / len(self.model.live_patches))

        return regions_affected_count / len(self.model.live_patches)

    def write_results_to_csv(self):

        with open('model_results.csv', mode='w') as model_results:
            employee_writer = csv.writer(model_results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['epoch_number', 'incidence', 'prevalence', 'regions_affected_by_pandemic'])

            for int in range(0, self.number_of_epochs_count):
                employee_writer.writerow([self.global_number_of_epochs[int], self.global_num_incidence_array[int], self.global_prevalence_array[int], self.regions_affected_by_epidemic[int]])


    def display_graphical_matrix(self, gis_matrix):
        #plt.imshow(gis_matrix)

        fileName = "epoch"+ str(self.iteration_count) + ".png"

        dst = cv2.resize(gis_matrix, None, fx = 10, fy = 10, interpolation = cv2.INTER_NEAREST)
        cv2.imwrite("visualisations/"+fileName, dst)
        # cv2.imshow("image", dst)
        # cv2.waitKey()

        # plt.savefig("visualisations/" + fileName)
        #plt.show()

    def create_video_from_images(self):
        image_folder = 'visualisations'
        video_name = 'video.avi'

        images = [img for img in natsorted(os.listdir(image_folder)) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, 1, (width, height))

        print(images)

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

        # for filename in os.listdir('visualisations/'):
        #     if filename.endswith('.png'):
        #         os.remove(os.path.join('visualisations/', filename))

    def color_patches_setup(self, region, max_popn):
        for x in range(region.rows):
            for y in range(region.columns):
                currentPatch = region.patches[x][y]
                if (currentPatch.num_infected > 0.03 * currentPatch.population):
                    currentPatch.color = [0, 0, 209]
                elif (currentPatch.num_infected >= 1):
                    currentPatch.color = [68, 68, 230]# red

                elif (currentPatch.num_immune < currentPatch.num_susceptible):
                    # varying degrees of blue, relative to population density
                    if (currentPatch.population < 0.01 * max_popn):
                        currentPatch.color = [255, 200, 200]
                    elif (currentPatch.population < 0.05 * max_popn):
                        currentPatch.color = [255, 160, 160]
                    elif (currentPatch.population < 0.20 * max_popn):
                        currentPatch.color = [220, 120, 120]
                    elif (currentPatch.population < 0.80 * max_popn):
                        currentPatch.color = [220, 60, 60]
                    elif (currentPatch.population < 1.00 * max_popn):
                        currentPatch.color = [220, 000, 000]


    def color_patches(self, patches_to_color, max_popn):
        for currentPatch in patches_to_color:
            if (currentPatch.num_infected > 0.03 * currentPatch.population):
                currentPatch.color = [0, 0, 209]
            elif (currentPatch.num_infected >= 1):
                currentPatch.color = [68, 68, 230]  # red

            elif (currentPatch.num_immune < currentPatch.num_susceptible):
                # varying degrees of blue, relative to population density
                if (currentPatch.population < 0.01 * max_popn):
                    currentPatch.color = [255, 200, 200]
                elif (currentPatch.population < 0.05 * max_popn):
                    currentPatch.color = [255, 160, 160]
                elif (currentPatch.population < 0.20 * max_popn):
                    currentPatch.color = [220, 120, 120]
                elif (currentPatch.population < 0.80 * max_popn):
                    currentPatch.color = [220, 60, 60]
                elif (currentPatch.population < 1.00 * max_popn):
                    currentPatch.color = [220, 000, 000]


    def display_result(self):

        seir_plot = plt.figure(1)
        plt.plot(self.global_number_of_epochs, self.global_num_susceptible_array, "-b", label="susceptible")
        plt.plot(self.global_number_of_epochs, self.global_num_exposed_array, "-y", label="exposed")
        plt.plot(self.global_number_of_epochs, self.global_num_infected_array, "-r", label="infected")
        plt.plot(self.global_number_of_epochs, self.global_num_immune_array, "-g", label="immune")
        plt.legend(loc="upper left")

        incidence_prevalence_plot = plt.figure(2)
        plt.plot(self.global_number_of_epochs, self.global_num_incidence_array, "-c", label="incidence")
        plt.plot(self.global_number_of_epochs, self.global_prevalence_array, "-m", label="prevalence")

        plt.legend(loc="upper left")

        plt.show()

    def end_routine(self):
        self.create_video_from_images()
        self.write_results_to_csv()
        self.display_result()

