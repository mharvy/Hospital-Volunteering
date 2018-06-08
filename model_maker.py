import csv
from itertools import islice
import random
from scipy.stats import variation
import numpy as np


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

    def create_model2(self, percents, total):
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
                    model.append(str(var[0]))
                    var[2] -= 1
                    break

        # Might be stupid but I don't trust this shuffle function
        random.shuffle(model)
        random.shuffle(model)
        random.shuffle(model)

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
            model = self.create_model2(percents, total)
            list_of_cvs = []

            # Create ugly data structure
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


def make_big_CV_spread(in_file, out_file, final_file, total, batch_size, num_trials):
    list_of_means = []

    final_CV_data = open(final_file, 'w')
    writer1 = csv.writer(final_CV_data)

    writer1.writerow([90, 80, 70, 60, 50, 40, 30, 20, 10])

    instance = CSVAnalyzer(in_file, out_file, [1, 0])

    print("Analyzing all constants of variation:")
    for i in range(9):
        percent = round(i * .1 + .1, 1)
        print("Testing for percentage = " + str(percent * 100))
        instance.out_file = 'percent=' + str(percent) + '.csv'
        cur_mean = instance.analyze_CVs([1 - percent, percent], total, batch_size, num_trials)[0]
        list_of_means.append(cur_mean)

    writer1.writerow(list_of_means)


def main():
    make_big_CV_spread('test.csv', 'result3.csv', 'averageCVs.csv', 10000, 100, 10)
    '''
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
