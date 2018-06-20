from pylab import *
import csv
#import CV_Data_Analysis as cvd


# This will plot the average CVs as percentage vs value
def read_csv_to_plot(filename):
    with open(filename, 'r') as file:
        file_reader = csv.reader(file)
        labels = next(file_reader)
        data = next(file_reader)
    labels = [float(label) for label in labels]
    data = [float(dat) for dat in data]
    plt.plot(labels, data, 'bo')
    xlabel('Percentage of ONs (%)')
    ylabel('Average CV')
    grid(True)
    plt.axis([0, 100, 0, 500])
    plt.show()


read_csv_to_plot('avgCVs.csv')