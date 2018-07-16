import numpy as np
import csv


def create_model_good(variables, percents, total_size, sample_size, **kwargs):
    master_list = []
    # Creates list of tuples of each variable and their total count (to be reduced each time it's placed in model)
    for index in range(len(variables)):
        cur_number = percents[index] * float(total_size)
        master_list.append([variables[index], cur_number])
    model = []
    # Appends each variable in model for however many times it supposed to appear based on percentages
    for position in range(total_size):
        for var in master_list:
            if var[1] > 0:
                model.append(var[0])
                var[1] -= 1
                break
    # Shuffles model
    model = np.array(model)
    np.random.shuffle(model)
    # Cut head end of model off to be used as actual model
    model = model[0:sample_size]
    # If specified, write model to csv file
    if 'filename' in kwargs:
        with open(kwargs['filename'], 'w') as file:
            writer1 = csv.writer(file)
            for var in model:
                writer1.writerow([var])
    return model


def get_good_model_mean_cvs(data_filename, variables, percentages, total_size, sample_size, trials):
    big_data_header_list_variables = ["Variables"]
    big_data_header_list_percentages = ["Percentages"]
    big_data_list = []
    big_row_means = []
    big_row_stds = []
    big_row_cvs = []
    for var_set in variables:
        print("starting variable " + str(var_set))
        cur_row_means = []
        cur_row_stds = []
        cur_row_cvs = []
        for percent in percentages:
            cur_mean_list = []
            # Prepare to write a new file with current data point data
            big_data_header_list_variables.append(str(var_set))
            big_data_header_list_percentages.append(percent)
            for cur_trial in range(trials):
                cur_model = create_model_good(var_set, percent, total_size, sample_size)
                cur_mean = np.mean(cur_model)
                cur_mean_list.append(cur_mean)
            big_data_list.append(cur_mean_list)
            cur_answer_mean = np.mean(cur_mean_list)
            cur_answer_std = np.std(cur_mean_list)
            cur_answer_cv = cur_answer_std / cur_answer_mean * 100
            cur_row_means.append(cur_answer_mean)
            cur_row_stds.append(cur_answer_std)
            cur_row_cvs.append(cur_answer_cv)
        big_row_means = big_row_means + cur_row_means
        big_row_stds = big_row_stds + cur_row_stds
        big_row_cvs = big_row_cvs + cur_row_cvs
    data_file = open(data_filename, 'w')
    writer1 = csv.writer(data_file)
    writer1.writerow(big_data_header_list_variables)
    writer1.writerow(big_data_header_list_percentages)
    big_data_list = [list(i) for i in zip(*big_data_list)]
    for row_index in range(len(big_data_list)):
        writer1.writerow([row_index + 1] + big_data_list[row_index])
    writer1.writerow(["Mean"] + big_row_means)
    writer1.writerow(["Standard Deviation"] + big_row_stds)
    writer1.writerow(["%CV"] + big_row_cvs)
    data_file.close()


def main():
    variable_assignments = [[2000, 2000], [1500,2000], [1333,2000], [1000, 2000], [666, 2000], [500, 2000], [0, 2000]]
    percentage_assignments = [[.01, .99], [.05, .95], [.1, .9], [.2, .8], [.3, .7], [.4, .6], [.5, .5], [.6, .4],
                              [.7, .3], [.8, .2], [.9, .1], [.95, .05], [.99, .01]]

    get_good_model_mean_cvs('testdata2.csv', variable_assignments, percentage_assignments, 10000, 1000, 1000)
    '''
    print(create_model_good([1000, 2000], [.5, .5], 10000, 1000))
    '''


if __name__ == '__main__':
    main()
