import sys
import csv
from itertools import islice
import random
from scipy.stats import variation
import numpy as np
#import threading  -> Hope to add multithreading for faster completion


class CSVAnalyzer:

    def __init__(self, in_file, out_file, vars):
        self.in_file = in_file
        self.out_file = out_file
        self.vars = vars

    def create_csv(self, percents, total):
        master_list = []
        total_percent = 0.0

        for index in range(len(self.vars)):
            cur_number = percents[index] * total
            total_percent += float(percents[index])
            master_list.append([self.vars[index], total_percent, cur_number])

        with open(self.in_file, 'w') as data:
            writer1 = csv.writer(data)
            model = []

            for position in range(total):
                for var in master_list:
                    if var[2] > 0:
                        model.append(str(var[0]))
                        var[2] -= 1
                        break

            # Might be stupid but I don't trust this shuffle function
            random.shuffle(model)
            random.shuffle(model)
            random.shuffle(model)

            for item in model:
                writer1.writerow(item)

    def analyze_csv(self, total, batch_size):

        batches = int(total / batch_size)

        with open(self.in_file, 'r') as data_csv:
            data = csv.reader(data_csv)

            batch_data = open(self.out_file, 'w')
            writer1 = csv.writer(batch_data)

            writer1.writerow(self.vars)  # header for out_file

            for batch in range(batches):
                print("Starting batch number " + str(batch) + " of " + str(batches - 1) + ':')
                batch_list = []
                batch_data_dict = {}  # Creating the dictionary of occurences of each variable
                for var in self.vars:
                    batch_data_dict[var] = 0

                for cur_item in islice(data, 0, batch_size):
                    cur_item_value = int(cur_item[0])
                    batch_list.append(cur_item)
                    batch_data_dict[cur_item_value] += 1
                print(batch_data_dict)

                batch_data_list = []
                for key in batch_data_dict:
                    batch_data_list.append(batch_data_dict[key] / batch_size)
                writer1.writerow(batch_data_list)
                print(batch_data_list)
                print('\n')

    # This function creates a big dataset with a specified amount of each variable
    # This is a closer model to a genome, because it mimicks getting a small sample of genes out of a certain cell
    # culture. Unfortunately, it is slower than he next function, do to the extra scrambling step it has to take
    def create_model(self, percents, total):
        master_list = []
        total_percent = 0.0

        for index in range(len(self.vars)):
            cur_number = percents[index] * total
            total_percent += float(percents[index])
            master_list.append([self.vars[index], total_percent, cur_number])

        model = []

        for position in range(total):
            for var in master_list:
                if var[2] > 0:
                    model.append(int(var[0]))
                    var[2] -= 1
                    break

        print("Shuffling Data...")
        random.shuffle(model)
        print("Data Shuffled\n")

        return model

    # This function creates a smaller model, but still succeeds at what is necessary.
    # It creates a model of the specified variables ONLY the length of the batch size, and randomly which variable
    # based on a randomnly generated percentage. It is much faster than the previous model function due to no scrambling
    def create_model2(self, percents, total):
        percents_list = []
        total_percent = 0
        for index in range(len(self.vars)):
            total_percent += float(percents[index])
            percents_list.append(total_percent)

        model = []

        print("Creating random dataset...")
        for position in range(total):
            randm_float = random.random()
            for index in range(len(self.vars)):
                if randm_float < percents_list[index]:
                    model.append(int(self.vars[index]))
                    break
        print("Done")

        return model

    # Creates model of random data, and anaylzes the COEFFICIENTS OF VARIATION for each trial of the results of a bunch
    # of batches of the random data, returns list of average CV for each variable
    def analyze_CVs(self, percents, total, batch_size, num_trials):

        list_of_means = []
        big_list_of_cvs_per_var = []

        batches = int(total / batch_size)

        batch_data = open(self.out_file, 'w')
        writer1 = csv.writer(batch_data)
        writer1.writerow(self.vars)

        for trial in range(num_trials):
            print("\nStarting trial number " + str(trial) + " of " + str(num_trials - 1) + ':\n')
            model = self.create_model(percents, total)
            list_of_cvs = []

            # Ew
            for var in range(len(self.vars)):
                list_occurences_per_batch = []  # This will end up having the length of total number of batches

                for batch in range(batches):
                    print("Starting batch number " + str(batch) + " of " + str(batches - 1) + ':')
                    occurences_this_batch = 0
                    for cur_item in model[batch_size * batch: batch_size * (batch + 1)]:
                        if int(cur_item) == self.vars[var]:
                            occurences_this_batch += 1
                    list_occurences_per_batch.append(occurences_this_batch)

                list_of_cvs.append(variation(list_occurences_per_batch))  # Makes a list of CVs per variable

            print(list_of_cvs)
            writer1.writerow(list_of_cvs)

            big_list_of_cvs_per_var.append(list_of_cvs)

        big_list_of_cvs_per_var = [list(x) for x in zip(*big_list_of_cvs_per_var)]  # Flips the double list
        for var in range(len(self.vars)):
            list_of_means.append(np.mean(big_list_of_cvs_per_var[var]))

        return list_of_means


# Tuns out this function is mathematically wrong. Not deleting however because it has some good qualities
# It wasn't truly random because it was analyzing multiple batches from each model, and taking a bunch of batches from
# same model is not random enough
def make_big_CV_spread(in_file, out_file, final_file, total, batch_size, num_trials):
    list_of_means = []

    final_CV_data = open(final_file, 'w')
    writer1 = csv.writer(final_CV_data)

    writer1.writerow([90, 80, 70, 60, 50, 40, 30, 20, 10])

    instance = CSVAnalyzer(in_file, out_file, [1, 0])

    print("Analyzing all constants of variation:")
    for i in range(9):
        percent = round(i * .1 + .1, 1)
        cur_on_percentage = round(1 - percent, 1)
        print("\nTesting for percentage on  = " + str((cur_on_percentage) * 100))
        instance.out_file = 'percent_on=' + str(cur_on_percentage) + '.csv'
        cur_mean = instance.analyze_CVs([cur_on_percentage, percent], total, batch_size, num_trials)[0]
        list_of_means.append(cur_mean)

    writer1.writerow(list_of_means)


# This function creates the csv table that was requested of me. It shows the average coefficient of variation of models
# ranging from 10:90 on:off to 90:10 on:off. This uses the create_model function which makes this function, although
# quite accurate, very very slow, which is not great since it deals with very big datasets.
def make_big_CV_spread2(in_file, out_file, final_file, final_avg_file, total, batch_size, num_trials):
    list_of_cv_means = []
    # Gene is on when value is 1, off when value is zero. After some experimenting, it was found that the on value
    # has no effect on the resulting CV of a list as long as off remains 0
    instance = CSVAnalyzer(in_file, out_file, [1, 0])
    list_list_of_cvs = []
    for i in range(9):
        percent = round(i * .1 + .1, 1)
        print("Working on list for " + str(percent * 100) + "%...")
        cur_list_of_cvs = []
        for trial in range(num_trials):
            print("Working on trial " + str(trial) + " of " + str(num_trials) + "..." + "( percentage_on = " +
                  str(percent * 100) + ")")
            cur_model = instance.create_model([percent, 1 - percent], total)
            cur_cv = variation(cur_model[:batch_size]) * 100  # Gets coefficient of variation as percentage
            cur_list_of_cvs.append(cur_cv)
        list_list_of_cvs.append(cur_list_of_cvs)
        list_of_cv_means.append(np.mean(cur_list_of_cvs))
    print(cur_model)

    print("\nDone with analyzing, writing to files...\n")
    final_CV_big_file = open(final_file, 'w')
    writer1 = csv.writer(final_CV_big_file)
    writer1.writerow([i * 10 for i in range(1, 10)])
    for i in range(num_trials):
        cur_row = []
        for n in range(9):
            cur_row.append(list_list_of_cvs[n][i])
        writer1.writerow(cur_row)

    print("\nDone with big csv file, starting average cv file...\n")
    final_CV_avg_file = open(final_avg_file, 'w')
    writer2 = csv.writer(final_CV_avg_file)
    writer2.writerow([i * 10 for i in range(1, 10)])
    writer2.writerow(list_of_cv_means)
    print("Done :^)")


# This function is mathematically sound and quite quick, as it uses the create_model2 function. Other than that it is
# the same as the above functions
def make_big_CV_spread3(in_file, out_file, final_file, final_avg_file, data_size, num_trials):
    list_of_cv_means = []
    # Gene is on when value is 1, off when value is zero. After some experimenting, it was found that the on value
    # has no effect on the resulting CV of a list as long as off remains 0
    instance = CSVAnalyzer(in_file, out_file, [1, 0])
    list_list_of_cvs = []
    for i in range(9):
        percent = round(i * .1 + .1, 1)
        print("Working on list for " + str(percent * 100) + "%...")
        cur_list_of_cvs = []
        for trial in range(num_trials):
            print("Working on trial " + str(trial) + " of " + str(num_trials) + "..." + "( percentage_on = " +
                  str(percent * 100) + ")")
            cur_model = instance.create_model2([percent, 1 - percent], data_size)
            cur_cv = variation(cur_model) * 100  # Gets coefficient of variation as percentage
            cur_list_of_cvs.append(cur_cv)
        list_list_of_cvs.append(cur_list_of_cvs)
        list_of_cv_means.append(np.mean(cur_list_of_cvs))
    print(cur_model)
    print(len(cur_model))

    print("\nDone with analyzing, writing to files...\n")
    final_CV_big_file = open(final_file, 'w')
    writer1 = csv.writer(final_CV_big_file)
    writer1.writerow([i * 10 for i in range(1, 10)])
    for i in range(num_trials):
        cur_row = []
        for n in range(9):
            cur_row.append(list_list_of_cvs[n][i])
        writer1.writerow(cur_row)

    print("\nDone with big csv file, starting average cv file...\n")
    final_CV_avg_file = open(final_avg_file, 'w')
    writer2 = csv.writer(final_CV_avg_file)
    writer2.writerow([i * 10 for i in range(1, 10)])
    writer2.writerow(list_of_cv_means)
    print("Done :^)")


def main():
    if len(sys.argv) != 3:
        print("Include batch_size and num_trials")
    else:
        args = [int(x) for x in sys.argv[1:]]
        make_big_CV_spread3('na.csv', 'na.csv', 'allCVs.csv', 'averageCVs.csv', args[0], args[1])
    '''
    if len(sys.argv) != 4:
        print("Include total_data, batch_size, and num_trials")
    else:
        args = [int(x) for x in sys.argv[1:]]
        make_big_CV_spread2('test.csv', 'result.csv', 'allCVs.csv', 'averageCVs.csv', args[0], args[1], args[2])
    '''
    '''
    # This is for a command that creates scrambled data and then finds a bunch of coefficients of variation
    if len(sys.argv) != 7:
        instance = CSVAnalyzer('test.csv', 'result2.csv', [1,0])
        instance.analyze_CVs([.1,.9], 10000, 1000, 10)
        print("Arguments should be: in_file out_file variables(list) percentages(list) total_number batch_size")
    else:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
        vars = sys.argv[3].strip('[]').split(',')
        vars = [int(i) for i in vars]
        percent = sys.argv[4].strip('[]').split(',')
        percent = [float(i) for i in percent]
        total = int(sys.argv[5])
        batch_size = int(sys.argv[6])
        print(total)
        instance = CSVAnalyzer(in_file, out_file, vars)
        instance.create_csv(percent, total)
        instance.analyze_csv(total, batch_size)
    '''


if __name__ == "__main__":
    main()
