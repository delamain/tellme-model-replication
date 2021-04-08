from panaxea.core.Model import Model
from main.InfectionAgent import InfectionAgent
from main.LoadGISData import LoadGISData
from main.Region import Region, RegionSteppable
from main.DisplayModel import DisplayModel
import time

number_of_epochs = 150
R0 = 3
recovery_period = 5.0
latency_period = 1.0
population_normalisation_total = 1000000
numPP_persons = 5000
min_agents_per_patch = 10

# loading GIS data
gisData = LoadGISData("GISdata/popn_density_uk_2015.asc")
xsize = ysize = gisData.return_grid_size()
population = gisData.return_population("UK")
ascii_grid = gisData.return_ascii_grid()
NODATA_value = gisData.return_NODATA_value()
rows, columns = ascii_grid.shape[0], ascii_grid.shape[1]
sum_popn_of_patches_with_popn_greater_than_zero = gisData.return_sum_popn_of_patches_with_popn_greater_than_zero()

model = Model(number_of_epochs)
region = Region("agent_env", xsize, ysize, model, R0, recovery_period, latency_period)

# normalise to population count
factor = (population_normalisation_total * population) / sum_popn_of_patches_with_popn_greater_than_zero
print("Factor value:", factor)
print("Count of non-zero patches:", gisData.return_count_of_non_zero_patches())
print("Sum of population, with patches with a popn > 0:", sum_popn_of_patches_with_popn_greater_than_zero)
print("Greatest patch population value:", ascii_grid.max() * factor)

agentsToBeAddedToSet = []
population_total = 0
region.global_population = 0
region.global_num_susceptible = 0
for x in range(rows):
    for y in range(columns):
        if (ascii_grid[x, y] != NODATA_value):
            population_total += ascii_grid[x, y]
            region.patches[x][y].population = round((ascii_grid[x, y]) * factor)
            region.patches[x][y].num_susceptible = region.patches[x][y].population
            region.global_population += region.patches[x][y].population
            region.global_num_susceptible += region.patches[x][y].population

            if (region.patches[x][y].population != 0):
                region.patches[x][y].within_border = True
                region.live_patches.add(region.patches[x][y])

                numberOfAgents = max(region.patches[x][y].population / numPP_persons, min_agents_per_patch)
                region.patches[x][y].numberOfAgents = int(numberOfAgents)

                # add all the agents to the patches make-agents
                for individualAgent in range(0, region.patches[x][y].numberOfAgents):
                    region.patches[x][y].agents.append(InfectionAgent(model, x, y))

                region.patches[x][y].set_visible_patches(model)

                # add the agents to the schedule
                for individualPatchAgent in region.patches[x][y].agents:
                    model.schedule.agents.add(individualPatchAgent)

# need to assign visible patches once all patches have been created
for x in range(rows):
    for y in range(columns):
        region.patches[x][y].set_visible_patches(model)

displayModel = DisplayModel(model)
regionSteppableModel = RegionSteppable(model, displayModel)

model.schedule.helpers.append(displayModel)
model.schedule.helpers.append(regionSteppableModel)

displayModel.color_patches_setup(region, population_total)

for x in range(region.rows):
    for y in range(region.columns):
        region.visualised_patches[x][y] = region.patches[x][y].color

displayModel.display_graphical_matrix(region.visualised_patches)

start_time = time.time()
model.run()
print("--- %s seconds ---" % (time.time() - start_time))

displayModel.end_routine()

