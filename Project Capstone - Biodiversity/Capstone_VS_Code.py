from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
import sys

# CodeCademy Capstone Project 2 - National Parks Biodiversity Analysis

def main():
    # set pandas display options, else output not showing enough data
    # used answer from stackoverflow - https://stackoverflow.com/questions/11707586/python-pandas-how-to-widen-output-display-to-see-more-columns
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    
    # STEP 2 - inspecting our data
    print("STEP 1 AND STEP 2:\n")
    # 1) load and save "species_info.csv" into dataframe species
    # 2) inspect the dataframe via df.head() method 
    species = pd.read_csv("species_info.csv")
    print("First few rows of species dataframe: ")
    print(species.head())
    print("\n")
    #print("Statistical information about our species dataframe: ")
    #print(species.info()) # displays statistical info about our dataframe
    #print("\n")

    # STEP 3 - learn more about our data
    print("\nSTEP 3:\n")
    # 1) how many different species are in 'species' dataframe?
    # 2) what are the different values of the 'category' column
    # 3) what are the different values of 'conservation_status'
    print("Number of different species in our dataframe is {} \n".format(species.scientific_name.nunique()))

    unique_category_values = species.category.unique()
    print("The unique values for the category column are :")
    print(unique_category_values)
    print("\n")

    unique_conservation_status_values = species.conservation_status.unique()
    print("The unique values for the conservation_status column are :")
    print(unique_conservation_status_values)
    print("\n")

    # NOTE - we can get also all the values of conservation status by grouping each value in terms of another column's value counts
    #conservation_status_values = species.groupby("conservation_status").scientific_name.count().reset_index()
    #print(conservation_status_values)

    # STEP 4 - do some analysis
    print("\nSTEP 4:\n")
    #1) Count how many 'scientific_name' values meet each criteria in the 'conservation_status' column
    scientific_name_per_conservation_status = species.groupby("conservation_status").scientific_name.nunique().reset_index()
    print("A breakdown of scientific names per conservation status category is as follows :")
    print(scientific_name_per_conservation_status)
    print("\n")

    #2) Many species in our data have a conservation_status value of None, which is hence being excluded from our analysis above. 
    # ---> We will include this data by changing the conservation_status value of each of these species to "No Intervention" in our dataframe
    # ---> as well as making sure we don't add another index
    species.fillna("No Intervention", inplace=True)
    # just inspect the updated dataframe
    print("First few rows of updated species dataframe: ")
    print(species.head())
    print("\n")

    #3) run the same analysis from step 1 to show a more accurate breakdown
    scientific_name_per_conservation_status = species.groupby("conservation_status").scientific_name.nunique().reset_index()
    print("A breakdown of scientific names per conservation status category is as follows :")
    print(scientific_name_per_conservation_status)
    print("\n")

    #4) create new dataframe, named protection_counts, which sorts the columns by how many unique species are in each conservation_status category
    
    #print("Un-sorted dataframe of counts per protection status: ")
    #protection_counts_1 = species.groupby("conservation_status").scientific_name.count().reset_index()
    #protection_counts_1 = species.groupby("conservation_status").scientific_name.nunique().reset_index()
    #print("\n")
    
    # we sort s.t our bar graph for step 5 is easier to read
    print("Sorted dataframe of counts per protection status: ")
    #protection_counts = species.groupby("conservation_status").scientific_name.count().reset_index().sort_values(by="scientific_name")
    protection_counts = species.groupby("conservation_status").scientific_name.nunique().reset_index().sort_values(by="scientific_name")
    print(protection_counts)
    print("\n")

    #5) using data from our protection_counts dataframe --> create a bar chart that describes the total species count for each conservation_status value
    # hence each bar height will correspond to the values under the protection_counts.scientific_name column
    # the x-axis values will correspond to each value under the protection_counts.conservation_status column
   
    # create list for each of our dataframe columns we will be using for the y and x axis, in order to pass these lists to our plt.bar() function 
    species_counts_per_status_list = protection_counts["scientific_name"].tolist()
    conservation_status_values_list = protection_counts["conservation_status"].tolist()
    # good habit -> clear any figs using plt.close("all")
    plt.close("all")
    plt.figure(figsize=(10, 4))
    # save axes object of our particular subplot, in order to modify the axes (in our case the x-axis)
    ax = plt.subplot()
    plt.bar(range(len(conservation_status_values_list)), species_counts_per_status_list)
    # modify the x-axis s.t we switch the number values with the string values corresponding to our conservation_status categories
    # need to first set the xticks value to the number of vals used, and then switch with the correpsonding string values
    ax.set_xticks(range(len(conservation_status_values_list)))
    #ax.set_xticklabels(conservation_status_values_list, rotation=30) # rotation optional - only for appearences
    ax.set_xticklabels(conservation_status_values_list)
    # label the y axis (no need to label x - just use conservation_status values), and then title our bar graph
    #plt.xlabel("Conservation Status")
    plt.ylabel("Number of Species")
    plt.title("Conservation Status by Species")
    plt.savefig("conservation_status_by_species.png")
    plt.show() # NOTE!! - need to save and close image before following code can be executed

    # STEP 5 - (test if certain types of species are more likely to be endangered)
    print("\nSTEP 5 - Analyze if certain stypes of species more likely to be endangered. In other words, test if the samples from each population category significantly different from each other: \n")
    # 1) add column in species dataframe - "is_protected", who's value for each row is:
    #   --->  "True" if "conservation_status" != "No Intervention", else value is "False"
    print("\nModifying species dataframe by adding a new column 'is_protected' to the end: \n")
    is_protected_value = lambda s: True if s != "No Intervention" else "False"
    species["is_protected"] = species.conservation_status.apply(is_protected_value)
    print(species.head())
    print("\n")
    
    # 2) create and save new dataframe from grouping by both 'category' and 'is_protected'
    print("category_counts dataframe - displaying species count for each UNIQUE combination of ('category', 'is_protected') value: ")
    #category_counts = species.groupby(["category", "is_protected"]).scientific_name.count().reset_index() # need to chain reset_index() method to return a dataframe object
    category_counts = species.groupby(["category", "is_protected"]).scientific_name.nunique().reset_index() # need to chain reset_index() method to return a dataframe object

    # 3) Examine the category_counts dataframe
    print(category_counts.head())
    #print(type(category_counts))
    print("\n")

    # 4) For better view of data - pivot category_counts dataframe s.t (columns - is_protected, index - category, values - scientific_name)
    print("Pivot of category_counts")
    category_pivot = category_counts.pivot(columns="is_protected", index="category", values="scientific_name").reset_index()
    print(category_pivot)
    print("\n")

    # 5) Renaming the columns to something more descriptive
    # use format - dataframe.columns = ['col1', 'col2', ..]
    category_pivot.columns = ["category", "protected", "not_protected"]
    print("category_pivot updated with renamed columns: ")
    print(category_pivot)
    print("\n")

    # 6) Add column to category_pivot, "percent_protected", who's value = protected/total speices count value for each row
    percent_protected_function = lambda row: (float(row.protected))/((float(row.not_protected) + float(row.protected)))
    category_pivot["percent_protected"] = category_pivot.apply(percent_protected_function, axis=1)
    
    # 7) Examine the updated categor_pivot dataframe
    print("category_pivot with new 'percent_protected' column: ")
    print(category_pivot)
    print("\n")

    

    # 8) Test the significance of the statement - "Species in the mammals are more likely to be endangered than birds"
    print("STATISTICAL SIGNIFICANCE TEST 1 - Test if percent protected mammals is significantly different from the percent of protected birds:")
    # since we are comparing categorical data between 2 or more populations, the best method would be to use a Chi Squared Test
    # we will create a contingency table from our bird, and mammal data (first nested list - our bird population, second nested list - our mammal population)
    contingency = [[75, 413], 
                   [30, 146]]
    # check the pvalue obtained from passing the table to the chi2_contingency() function in the following format: chi2, pval, dof, expected = chi2_contingency(contingency_table)
    bird_mammal_pval = chi2_contingency(contingency)[1]
    if bird_mammal_pval < .05:
        print("The bird_mammal_pval from performing a chi squared test on the data is {}.\nWe CAN REJECT THE NULL HYPOTHESIS, thus the percentage of protected mammals IS SIGNIFICANTLY DIFFERENT from the percentage of protected birds.\n".format(bird_mammal_pval))
    if bird_mammal_pval >= .05:
        print("The bird_mammal_pval from performing a chi squared test on the data is {}.\nWe CANNOT REJECT THE NULL HYPOTHESIS, thus the percentage of protected mammals is NOT SIGNIFICANTLY DIFFERENT from the percentage of protected birds.\n".format(bird_mammal_pval))

    # check if there is a signficant difference between the reptile and mammal populations in our data
    print("STATISTICAL SIGNIFICANCE TEST 2 - Test if percent protected mammals is significantly different from the percent of protected reptiles:")
    contingency_reptile_mammal = [[30, 146], 
                                   [5, 73]] 
    reptile_mammal_pval = chi2_contingency(contingency_reptile_mammal)[1]
    if reptile_mammal_pval < .05:
        print("The reptile_mammal_pval from performing a chi squared test on the data is {}.\nWe CAN REJECT THE NULL HYPOTHESIS, thus the percentage of protected mammals IS SIGNIFICANTLY DIFFERENT from the percentage of protected reptiles.\n".format(reptile_mammal_pval))
    if reptile_mammal_pval >= .05:
        print("The reptile_mammal_pval from performing a chi squared test on the data is {}.\nWe CANNOT REJECT THE NULL HYPOTHESIS , thus the percentage of protected mammals is NOT SIGNIFICANTLY DIFFERENT from the percentage of protected reptiles.\n".format(reptile_mammal_pval))

    print("From our significance tests, we can conclude that CERTIAIN TYPES OF SPECIES ARE MORE LIKELY TO BE ENDANGERED THAN OTHERS.\n")

    # STEP 6 - utilize observation data, and our species data to determine sample size needed to test viability of a disease reduction program
    print("\nSTEP 6 PART I - using both observation data and our species data, figure out the total number of observed sheep for each of our national parks")
    # 1) create and save data from observations.csv into dataframe for analysis
    observations = pd.read_csv("observations.csv")
    # 2) inspect the data
    print("observations data: ")
    print(observations.head())
    print("\n")
    
    # 3) To help aid scientists studying sheep sightings,  add a column to our species dataframe which indicates if the species in each row pertains to a sheep or not
    print("Adding column 'is_sheep' to dataframe, which uses a lambda function to to determine if the species is a sheep based on presence of 'Sheep' in common_names: ")
    species["is_sheep"] = species.common_names.apply(lambda s: True if "Sheep" in s else False) # NOTE -  could also have used -----> lambda s: "Sheep" in s
    print(species.head())
    # 4) Select and display all the rows where the 'is_sheep' column is True
    print("\nRows where 'is_sheep' column is True: ")
    print(species[species.is_sheep == True])
    print("\n")
    # 5) To remove any plant's, we refine and save the dataframe to only include species with a category value of "mammal"
    print("'sheep_species' - To remove any plant species, created a new filtered dataframe which only contains rows where 'category' value is mammal and 'is_sheep' value is True:")
    sheep_species = species[(species.is_sheep == True) & (species.category == "Mammal")]
    print(sheep_species)
    print("\n")
  
    # 6) Create, save, and inspect new dataframe from merging sheep_species with observations
    # use merge function to merge dataframes on commonn columns
    print("Merged dataframe, 'sheep_observations' created from merging 'sheep_species' with 'observation' dataframes:")
    #sheep_observations = sheep_species.merge(observations)
    sheep_observations = observations.merge(sheep_species)
    print(sheep_observations)
    print("\n")

    # 7) Create, save, and display dataframe that displays the sheep observations at each park
    print("Dataframe of total sheep observations per park:")
    obs_by_park = sheep_observations.groupby("park_name").observations.sum().reset_index()
    print(obs_by_park)
    print("\n")

    # 8) Create and display bar chart showing the observations per week at each park
    print("Bar chart of observations at each park:")
    observations_value_list = obs_by_park["observations"].tolist()
    park_name_value_list = obs_by_park["park_name"].tolist()
    plt.close("all")
    plt.figure(figsize=(16, 4))
    ax = plt.subplot()
    plt.bar(range(len(park_name_value_list)), observations_value_list)
    ax.set_xticks(range(len(park_name_value_list)))
    ax.set_xticklabels(park_name_value_list)
    plt.xlabel("Park Name")
    plt.ylabel("Number of Observations")
    plt.title("Observations of Sheep per Week")
    plt.savefig("parkwise_observations_of_sheep_per_week.png")
    plt.show() # NOTE!! - need to save and close image before following code can be executed

    print("\nSTEP 6 PART II- using our new dataframe of total observed sheep per park, help researchers determine the necessary sample size for testing the viability of a sheep foot and mouth disease reduction program:\n")

    # 9) Calculate sample size needed to test the effectivness of Yellowstone's sheep foot and mouth disease reduction program
    # 15% of sheep at Bryce national park have foot and mouth disease
    # For Viable program -> need to detect at least a 5% reduction (ie confident that at most, %10 percent of sheep in yellowstone have foot and mouth disease)
    # Using a significance level of 90% (At most %10 chance that our data is not significant)
    baseline_conversion_rate = .15 # current percent of infected population (based on stats from Bryce National Park)
    current_infected_val = 77.05 # .15 * 507
    goal_infected_number = 50.7 # .10 * 507
    minimum_detectable_effect = 100.0 * ((77.05 - 50.7)/ 77.05) # gives us 33.33
    # note - for minimum_detectable_effect, we could have also just done (based on the 'need to detect value' of 5%) --> 100.0 * (.05/.15) ie (100.0 * (required reduction as percent of baseline)
    statistical_significance = .90
    required_sample_size = 510
    print("\nPlugging the following values into the sample size calculator at Optimizely:\nBaseline_Conversion_Rate - 15%\nMinimum Detectable Effect - 33.33\nStatistical Significance - 90%\n\nThe required sample size for each group (baseline at Bryce and test group at Yellowstone) of {} to test the viability of our foot and mouth disease program.\n".format(required_sample_size))

    # 10) calc # weeks needed at Bryce and Yellowstone national parks to observe enough sheep in order perform our test

    num_weeks_bryce = 510.0/250.0 # 510.0/250.0 rounded to next nearest week
    num_weeks_yellowstone = 510.0/507.0 # 510.0/507.0 rounded to nearest week
    print("Based on the required sample size, we need {} weeks of observations at Bryce National Park and {} week of observations at Yellowstone National Park".format(num_weeks_bryce, num_weeks_yellowstone))
main()