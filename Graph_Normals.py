import CV_Data_Analysis as cvd
from pylab import *
from scipy.stats import variation
import csv


# This function creates a 2d matrix with each column representing a different percent of ON/OFF and each row
# representing a trial (using make_percentage_total_spread function). It then normalizes and plots the data with each
# percent getting its own graph. There are a few other features to help its usability but not much.
def plot_normalized_sums(variables, percents_on_off, percents_to_ignore, sample_size, num_trials, **kwargs):
    if len(variables) != 2:
        print("Only 2 variables allowed!")
        return
    # Makes a data set
    instance = cvd.CSVAnalyzer(variables)
    totals_matrix = instance.make_percentage_total_spread(percents_on_off, sample_size, num_trials)
    # This loop will iterate through all percents the user wants
    for specific_percent in percents_on_off:
        # Makes sure to not plot what user doesn't want plotted
        if specific_percent in percents_to_ignore:
            continue
        # Setting up the plot
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_xlabel('Sums of models')
        ax1.set_ylabel('Percent of Occurences (%)')
        ax1.grid(True)
        fig.suptitle('Sums vs Percent Occurences for ' + str(specific_percent * 100) + '% of ' + str(variables[0]) +
                     ' and ' + str(variables[1]) + ' Variables')
        # Just because IDE is annoyed
        list_of_sums = []
        # This loop gets the specific list of totals for the specified percent
        for percent_index in range(len(percents_on_off)):
            if percents_on_off[percent_index] == specific_percent:
                list_of_sums = totals_matrix[percent_index]
                break
        # Sort the big list of sums
        list_of_sums.sort()
        # Get the x and y data for occurrence graph
        sums_list = []  # This will be the x data for graph
        num_occurences = []  # This will be the y data for graph
        for cur_sum in list_of_sums:
            if cur_sum in sums_list:
                num_occurences[len(num_occurences) - 1] += 1
            else:
                sums_list.append(cur_sum)
                num_occurences.append(1)
        # This is the part that will normalize the data set for easier human comparison
        for cur_total_index in range(len(num_occurences)):
            num_occurences[cur_total_index] = num_occurences[cur_total_index] / num_trials * 100
        # This part will plot the data
        cur_label = 'CV = ' + str(variation(list_of_sums) * 100) + '%'
        ax1.set_title(cur_label)
        ax1.set_autoscalex_on(False)
        ax1.set_autoscaley_on(False)
        ylim([0, np.amax(num_occurences) + 1])
        if 'xspread' in kwargs:
            xlim([sums_list[0], sums_list[0] + kwargs['xspread']])
        else:
            xlim([sums_list[0], sums_list[0] + 100])
        ax1.plot(sums_list, num_occurences, 'bo')
        if 'save' in kwargs:
            fig.savefig(str(int(specific_percent * 100)) + kwargs['save'])

    plt.show()


plot_normalized_sums([2,1], [.01,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.99], [.2,.3,.4,.5,.6,.7,.8], 1000, 1000,
                     xspread=70, save='test.png')
