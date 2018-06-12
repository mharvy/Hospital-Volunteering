import sys
import csv
from itertools import islice
import random
from scipy.stats import variation
import numpy as np
import CV_Analysis_Helpers


class CSVAnalyzer:

    # Only static variable should be the actual variables
    def __init__(self, variables):
        self.variables = variables

    # Creates a random model perfectly based on percents. Writes model to csv. Returns model as list.
    # It works by generating a huge list of ordered variables based exactly on percentages. Then scrambles makes model
    # only the head end of the list of size sample_size
    def create_model_good(self, percents, total_size, sample_size, **keyword_parameters):
        master_list = []
        # Creates list of tuples of each variable and their total count (to be reduced each time it's placed in model)
        for index in range(len(self.variables)):
            cur_number = percents[index] * total_size
            master_list.append([self.variables[index], cur_number])
        model = []
        # Appends each variable in model for however many times it supposed to appear based on percentages
        for position in range(total_size):
            for var in master_list:
                if var[2] > 0:
                    model.append(int(var[0]))
                    var[2] -= 1
                    break
        # Shuffles model
        print("Shuffling Data...")
        random.shuffle(model)
        print("Data Shuffled\n")
        # Cut head end of model off to be used as actual model
        model = model[0:sample_size]
        # If specified, write model to csv file
        if 'filename' in keyword_parameters:
            with open(keyword_parameters['filename']) as file:
                writer1 = csv.writer(file)
                for var in model:
                    writer1.writerow(var)
        return model

    # Creates a random model quickly based on percents. Writes model to csv. Returns model as list.
    # It works by appending elements to model one at a time, generating a random percentage and comparing it to
    # specified percentages. This requires no scrambling and is very random, but isn't a great representation of
    # analyzing a cell culture. It's good for quickly testing algorithms
    def create_model_fast(self, percents, sample_size, **keyword_parameters):
        # Format percents list better
        percents = CV_Analysis_Helpers.percent_corrector(percents)
        model = []
        print("Creating random dataset...")
        # Appends data to model one at a time randomly, but also based on percentages
        for position in range(sample_size):
            random_float = random.random()
            for index in range(len(self.variables)):
                if random_float < percents[index]:
                    model.append(int(self.variables[index]))
                    break
        print("Done")
        # If specified, write model to csv file
        if 'filename' in keyword_parameters:
            with open(keyword_parameters['filename']) as file:
                writer1 = csv.writer(file)
                for var in model:
                    writer1.writerow(var)
        return model

    # Makes a csv table of average coefficients of variation of artificially randomized data based on percentages
    # First it uses create_model_good or create_model+fast to generate a model, then it calculates the CV, and adds it
    # to a list. Then, it repeats those two steps for however many trials are specified, and then repeats all of that
    # for each percentage specified. This is the more accurate version of this function
    def make_percentage_spread(self, percents_on_off, sample_size, num_trials, **keyword_parameters):
        if len(self.variables) != 2:
            print("Only is useful for two variables!")
            return []

        list_of_cv_means = []
        list_list_of_cvs = []

        for percent in percents_on_off:
            print("\nWorking on percent = ", str(percent), "%...\n")
            cur_list_of_cvs = []
            for trial in range(num_trials):
                print("Working on trial " + str(trial) + " of " + str(num_trials) + "... " + "(percentage_on = " +
                      str(percent * 100) + ")")
                if 'mode' in keyword_parameters and keyword_parameters['mode'] == 'good':
                    cur_model = self.create_model_good([percent, 1 - percent], keyword_parameters['total_size'],
                                                       sample_size)
                else:
                    cur_model = self.create_model_fast([percent, 1 - percent], sample_size)
                cur_cv = variation(cur_model) * 100
                cur_list_of_cvs.append(cur_cv)
            list_list_of_cvs.append(cur_list_of_cvs)
            list_of_cv_means.append(np.mean(cur_list_of_cvs))
        print(cur_model)
        print("\nDone analyzing\n")

        if 'avg_file' in keyword_parameters:
            print("Writing average CVs to ", keyword_parameters['avg_file'], "\n")
            avg_file = open(keyword_parameters['avg_file'], 'w')
            avg_writer = csv.writer(avg_file)
            avg_writer.writerow([percent * 100 for percent in percents_on_off])
            avg_writer.writerow(list_of_cv_means)
        if 'CV_file' in keyword_parameters:
            print("Writing all CVs to ", keyword_parameters['CV_file'], "\n")
            CV_file = open(keyword_parameters['CV_file'], 'w')
            CV_writer = csv.writer(CV_file)
            CV_writer.writerow([percent * 100 for percent in percents_on_off])
            for trial in range(num_trials):
                cur_row = []
                for percent in range(len(percents_on_off)):
                    cur_row.append(list_list_of_cvs[percent][trial])
                CV_writer.writerow(cur_row)
        return list_of_cv_means


def main():
    instance = CSVAnalyzer([1, 0])
    #instance.make_percentage_spread([.1, .2, .3, .4, .5, .6, .7, .8, .9], 1000, 1000, avg_file='newAvgCVs.csv',
    #                                CV_file='newAllCVs.csv')
    if len(sys.argv) != 4:
        print("Include percents, batch_size, num_trials")
    else:
        instance = CSVAnalyzer([1, 0])
        percentages = [float(x) for x in sys.argv[1].strip('[]').split(',')]
        instance.make_percentage_spread(percentages, int(sys.argv[2]), int(sys.argv[3]), avg_file='avgCVs.csv',
                                        CV_file='allCVs.csv')


if __name__ == '__main__':
    main()

