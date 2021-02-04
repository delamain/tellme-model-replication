from panaxea.core.Model import Model
import InfectionAgent
import LoadGISData
import Region
import DisplayModel
import numpy as np

gisData = LoadGISData.LoadGISData("popn_density_uk_2015.asc")
xsize = ysize = gisData.return_grid_size()
population = gisData.return_population("UK")

# model constructor (number of iterations)
model = Model(5)
R0 = 2
recovery_period = 5.0
latency_period = 0

# Creating the grid automatically binds it to the model
region = Region.Region("agent_env", xsize, ysize, model, R0, recovery_period, latency_period)

ascii_grid = gisData.return_ascii_grid()
NODATA_value = gisData.return_NODATA_value()
rows = ascii_grid.shape[0]
columns = ascii_grid.shape[1]

# this to scale the model accordingly, so hard coded values are the same across the model
model_size_scalar = 1000/1000000

population_total = 0
count_of_pop_non_zero_squares = gisData.return_count_of_non_zero_patches()
sum_popn_of_patches_with_popn_greater_than_zero = gisData.return_sum_popn_of_patches_with_popn_greater_than_zero()
factor = (10000 * population) / sum_popn_of_patches_with_popn_greater_than_zero
print("Factor value:", factor)
print("Count of non-zero patches:", count_of_pop_non_zero_squares)
print("Sum of population, with patches with a popn > 0:", sum_popn_of_patches_with_popn_greater_than_zero)
count = 0

print("DOES THIS PRINT", ascii_grid.max() * factor)
#print(np.argmax(patch_populations_matrix_numpy))
a = ascii_grid  # Can be of any shape
indices = np.where(a == a.max())
print(indices)

agentsToBeAddedToSet = []

for x in range(rows):
    for y in range(columns):
        if (ascii_grid[x, y] != NODATA_value): # if there is a population value
            population_total += ascii_grid[x, y]
            region.patches[x][y].population = round((ascii_grid[x, y]) * factor)

            if (region.patches[x][y].population != 0):
                region.patches[x][y].within_border = True
                region.live_patches.add(region.patches[x][y])
                # region.visualised_patches[x][y] = region.patches[x][y].population

            # add all the agents to the patches
            for individualAgent in range(0, region.patches[x][y].population):
                region.patches[x][y].agents.append(InfectionAgent.InfectionAgent(model, x, y))

            # add the agents to the schedule
            for individualPatchAgent in region.patches[x][y].agents:
                model.schedule.agents.add(individualPatchAgent)

regionSteppableModel = Region.RegionSteppable(model)
displayModel = DisplayModel.DisplayModel(model)

model.schedule.helpers.append(displayModel)
model.schedule.helpers.append(regionSteppableModel)

DisplayModel.DisplayModel.color_patches_setup(displayModel, region, population_total)

for x in range(region.rows):
    for y in range(region.columns):
        region.visualised_patches[x][y] = region.patches[x][y].color



DisplayModel.DisplayModel.display_graphical_matrix(displayModel, region.visualised_patches)

model.run()

# DisplayModel.DisplayModel.display_result(displayModel)
DisplayModel.DisplayModel.create_video_from_images(displayModel)
