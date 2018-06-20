from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QInputDialog)
import sys


class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    variables_str = ""
    percentages_str = ""
    trials = 0

    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Marc Harvey")


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Input Information")
        layout = QFormLayout()
        variables = QLineEdit()
        variables.textChanged.connect(self.get_variables)
        layout.addRow(QLabel("All Variable Sets (eg. '[0, 2], [1, 2], [1.5, 2]'):"), variables)
        percentages = QLineEdit()
        layout.addRow(QLabel("All Percentage Distributions (eg. '[5, 95], [10, 90], [40, 60], [99, 1]'):"), percentages)
        trials = QSpinBox()
        layout.addRow(QLabel("Trials:"), trials)
        #trials, okPressed = QInputDialog.getInt(self, "Get integer", "Trials:", 1000, 0, 10000, 100)
        #if okPressed:
            #print(self.formGroupBox)
        print(variables.text())
        self.formGroupBox.setLayout(layout)
        print(variables)


    def get_variables(self, text):
        self.variables_str = text


    def get_percentages(self, text):
        self.percentages_str = text


    # This is where I'm leaving off at 062018
    def make_variables(self, text):
        cur_list = text.split(" ")
        for vars in cur_list:
            if vars[0] != "[" or vars[-1] != "]":
                print("error with imput")
                return False
            try:
                vars.strip("[]".split(","))
                int(vars)
            except ValueError:
                return False
            self.variables.append(cur_list)
        print(self.variables)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
sys.exit(dialog.exec_())
