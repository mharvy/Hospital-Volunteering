from pylab import *
import csv
from numpy import std
import CV_Data_Analysis as cvd
#from scipy.stats import variation  Don't need this because will compute it manually for faster performance


# This function will create a CSV file full of juicy coefficient of variation data for a bunch of variables for a bunch
# of trials for a bunch of percent_on_off. The reason this is not a part of the the graph function is that this will
# take a long time and we don't want to have to compute a lot each time we want to show a graph
# Also note, variables double list must only have 2 variable per set of variables or bad stuff will happen
def write_to_csv(filename, variables, percents_on_off, sample_size, num_trials, recurse_flag=False):
    if len(variables) == 0:
        return
    cur_instance = cvd.CSVAnalyzer(variables[0])
    cur_instance.make_percentage_spread(percents_on_off, sample_size, num_trials, avg_file=filename,
                                        recurse=recurse_flag)
    variables.pop(0)
    write_to_csv(filename, variables, percents_on_off, sample_size, num_trials, True)


# This function will plot the data from a csv file with the format used in the previous function
def plot_csv(filename, num_variables, num_trials, **kwargs):
    fig = plt.figure()
    fig.suptitle('Percent Distribution vs Coeficient of Variation for Different Variable Sets')
    plt.xlabel('Percent Distribution of 1st Variable (%)')
    plt.ylabel('Average Coefficient of Variation: ' + str(num_trials) + ' Trials')
    if 'height' in kwargs:
        ylim([0, kwargs['height']])
    with open(filename, 'r') as file:
        reader1 = csv.reader(file)
        xaxis = next(reader1)
        xaxis.pop(0)
        xaxis = [float(value) for value in xaxis]
        vars_list = []
        for variable_index in range(num_variables):
            yaxis = next(reader1)
            vars_list.append(yaxis.pop(0))
            yaxis = [float(value) for value in yaxis]
            cur_ax = fig.add_subplot(1,1,1)  # I don't know what these arguments do but this thing works
            cur_ax.grid(True)
            cur_ax.plot(xaxis, yaxis)
    legend(vars_list)
    if 'save' in kwargs:
        fig.savefig(kwargs['save'])
    plt.show()


# This function generates a random model of the n variables specified (either fast or good), then gets the sum of every
# element of the model. It does this num_trials amount of times, and then gets a mean and CV of all the trials. It then
# repeats that for all the percentages
# NOTE that unlike many other functions I've made recently, this one allows more than two variables, meaning the
# percents_on_off must be passed as a list of lists. Small sacrifice for some really good functionality, because there
# will never be a case where a cell culture only has two scenarios. Instead there will be more than 4. Analyzing that
# aspect will be very important I think
#
# 061818 - I was told to edit this to provide all of the following analysis: mean, %cv, s, and mean + 2s
# Should be ezpz
def analyze_write_many_trials(file_name, variables, percents_on_off, sample_size, num_trials, **kwargs):
    # Double list of all sums of each trial of each percent, columns are percents, rows are trials
    print("Working on variables = " + str(variables))
    cur_sums_list_list = []
    for percent_set in percents_on_off:
        cur_sums_list = []
        for trial in range(num_trials):
            # Create a new model of given variables with given percents
            cur_instance = cvd.CSVAnalyzer(variables)
            if 'mode' in kwargs and kwargs['mode'] == 'good' and 'total' in kwargs:
                cur_model = cur_instance.create_model_good(percent_set, kwargs['total'], sample_size)
            else:
                cur_model = cur_instance.create_model_fast(percent_set, sample_size)
            cur_sum = np.sum(cur_model)
            cur_sums_list.append(cur_sum)
        cur_sums_list_list.append(cur_sums_list)

    with open(file_name, 'w') as file:
        writer1 = csv.writer(file)
        # Write heading for each column, probably won't work as it is right now
        writer1.writerow([' '] + percents_on_off)

        for trial in range(num_trials):
            cur_row = [trial]
            for percent_set_index in range(len(percents_on_off)):
                cur_row.append(cur_sums_list_list[percent_set_index][trial])
            writer1.writerow(cur_row)
        all_means = ['mean (x)'] + [np.mean(cur_col) for cur_col in cur_sums_list_list]
        writer1.writerow(all_means)
        all_stds = ['std (s)'] + [std(cur_col) for cur_col in cur_sums_list_list]
        all_cvs = ['% CV'] + [all_stds[index] / all_means[index] * 100 for index in range(1, len(all_means))]
        writer1.writerow(all_cvs)
        writer1.writerow(all_stds)
        final_row = ['x + 2s'] + [all_means[index] + 2 * all_stds[index] for index in range(1, len(all_means))]
        writer1.writerow(final_row)
        all_means.pop(0)
        all_cvs.pop(0)
        return all_means, all_cvs


# This function will plot the data in a csv with a format given by the analyze_write_many_trials function
def plot_many_trials(file_name, variables, percents_on_off, sample_size, num_trials):
    all_means, all_cvs = analyze_write_many_trials(file_name, variables, percents_on_off, sample_size, num_trials)
    print(all_cvs)
    percents_on = [percent[0] * 100 for percent in percents_on_off]
    fig = plt.figure()
    fig.suptitle('Percent Occurrence in Dataset (of first var) vs CV of sums')
    plt.xlabel('Percent Occurrence of ' + str(variables[0]))
    plt.ylabel('CV of sums of ' + str(num_trials) + ' trials')
    ax2 = fig.add_subplot(1, 1, 1)  # I don't know what these arguments do but this thing works
    ax2.grid(True)
    ax2.plot(percents_on, all_cvs)
    plt.show()


# Data sets to create on 061818
variable_assignments = [[0,2], [.5,2], [.66, 2], [1,2], [1.33, 2], [1.5, 2]]
for variable_set in variable_assignments:
    cur_file = 'test-' + str(variable_set[0]) + ':' + str(variable_set[1]) + '.csv'
    analyze_write_many_trials(cur_file, variable_set, [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],
                                                           [.6,.4],[.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000, mode='good', total=10000)


'''
### These are all the datasets I was assigned to create and analyze in the past. All that are not labelled with dates
### were created before or on 061518

#write_to_csv('big_cv_file.csv', [[1,0],[4,1],[4,2],[4,3],[4,5],[4,6],[4,7],[4,8]], [.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95], 1000, 1000)
#plot_csv('big_cv_file.csv', 8, 1000, height=300, save='graph_tall.png')
#plot_csv('big_cv_file.csv', 8, 1000, height=100, save='graph_short.png')
###
analyze_write_many_trials('wack.csv', [1,2,3,4], [[.1,.1,.2,.7],[.2,.2,.3,.3]], 1000, 1000)
analyze_write_many_trials('test01.csv', [0,1], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test02.csv', [0,2], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test12.csv', [1,2], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test04.csv', [0,4], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test14.csv', [1,4], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test24.csv', [2,4], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test34.csv', [3,4], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test03.csv', [0,3], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test13.csv', [1,3], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
analyze_write_many_trials('test23.csv', [2,3], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)

plot_many_trials('test01.csv', [1,2], [[.01,.99],[.05,.95],[.1,.9],[.2,.8],[.3,.7],[.4,.6],[.5,.5],[.6,.4],
                                                [.7,.3],[.8,.2],[.9,.1],[.95,.05], [.99,.01]], 1000, 1000)
'''