from PyQt5.QtWidgets import *

import UI as ui
from common import PATH
import matplotlib

import tkinter.messagebox
from tkinter import *
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from randomData import getData
from PyQt5.QtWidgets import *
import json

matplotlib.use("Qt5Agg")  # Declare the use of QT5


# Create a matplotlib graphics drawing class
class MyFigure(FigureCanvas):
    # creat a Figure
    def __init__(self, width, height, dpi):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # Activate the Figure window in the parent class
        super(MyFigure, self).__init__(self.fig)
        # Create a subgraph for drawing graphics. 111 represents the subgraph number.
        self.axes = self.fig.add_subplot(111)


class MainDialogImgBW(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainDialogImgBW, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Main Window")
        self.setMinimumSize(0, 0)

        # current trail
        self.curStep = 0
        # paths data
        self.pathData = getData()
        # answer
        self.answerData = []

        # initialization
        self.lastTime = datetime.now()
        self.last_image_type = ''
        self.last_color = ''
        self.last_target_name = ''
        self.last_target_value = ''
        self.last_data = {}

        # add answer
        self.comboBox.addItems(PATH)
        # initialize Choice nothing
        self.comboBox.setCurrentIndex(-1)
        # trigger event
        self.pushButton.clicked.connect(self.nextClick)
        self.pushButton_2.clicked.connect(self.start)

        # colour
        self.color_list = ['#88CCEE', '#CC6677', '#DDCC77', '#117733', '#332288', '#AA4499', '#44AA99', '#999933',
                           '#661100', '#6699CC', '#888888']
        self.color_list2 = ['#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF',
                            '#FFFFFF', '#FFFFFF', '#FFFFFF']

    # bar chart
    def drawBar(self, x, y, color):
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of patients choosing different pathways')
        if color is None:
            plt.barh(x, y, color=color)
            plt.yticks(x, None,  fontsize=8)
        else:
            for i in range(11):
                plt.barh(x[i], y[i], color=self.color_list[i])
                plt.yticks([], None, fontsize=8)
                plt.legend(x, ncol=2, loc="best", fontsize=10, bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()

    # column chart
    def drawColumn(self, x, y, color):
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of patients choosing different pathways')
        if color is None:
            plt.bar(x, y)
            plt.xticks(x, None, rotation=45, fontsize=8)
        else:
            for i in range(11):
                plt.bar(x[i], y[i], color=self.color_list[i])
                plt.xticks([], None, rotation=45, fontsize=8)
                plt.legend(x, ncol=2, loc="best", fontsize=10, bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()

    # pie chart
    def drawPie(self, x, y):
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of a single path as a percentage of the cost of 11 paths')
        plt.pie(y, labels=None, colors=self.color_list)
        plt.legend(x, loc="best", fontsize=10, bbox_to_anchor=(0.1, 1))
        plt.show()
        plt.tight_layout()

    # pie chart
    def drawPie2(self, x, y):
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of a single path as a percentage of the cost of 11 paths')
        plt.pie(y, labels=x, colors=self.color_list2, wedgeprops={'linewidth': 3, "edgecolor": "black"})
        plt.show()
        plt.tight_layout()

    def start(self):
        if self.curStep > 0:
            tkinter.messagebox.showinfo("Remind", "The experiment has already started.")
            return

        # initialization
        self.lastTime = datetime.now()
        self.last_image_type = self.pathData[self.curStep].get("image_type")
        self.last_color = self.pathData[self.curStep].get("color")
        self.last_target_name = self.pathData[self.curStep].get("target_name")
        self.last_target_value = self.pathData[self.curStep].get("target_value")
        self.last_data = self.pathData[self.curStep]

        image_type = self.pathData[self.curStep].get("image_type")
        color = self.pathData[self.curStep].get("color")

        x = []
        y = []

        for item in self.pathData[self.curStep].get("data"):
            name = item.get("name")
            value = item.get("value")
            x.append(name)
            y.append(value)

        self.draw(image_type, color, x, y)

        self.comboBox.clear()
        self.comboBox.clearEditText()

        # Add collection of answers.
        self.comboBox.addItems(PATH)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.setCurrentText('')

        self.curStep += 1

    # Next
    def nextClick(self):

        if self.curStep == 0:
            tkinter.messagebox.showinfo("Remind", "Please click start.")
            return

        # Check if the answer is selected
        if self.comboBox.currentIndex() == -1 and len(self.comboBox.currentText()) == 0:
            tkinter.messagebox.showinfo("Remind", "Please select an answer.")
            return

        last_time = self.lastTime
        now = datetime.now()
        duration = (now - last_time).seconds

        select = self.comboBox.currentText()

        if select == self.last_target_name:
            result = 'right'
        else:
            result = 'wrong'

        if self.last_target_value == 660 and self.last_image_type == 'column' and self.last_color == 'text':
            condition = 1
        if self.last_target_value == 1200 and self.last_image_type == 'column' and self.last_color == 'text':
            condition = 2
        if self.last_target_value == 660 and self.last_image_type == 'column' and self.last_color == 'color':
            condition = 3
        if self.last_target_value == 1200 and self.last_image_type == 'column' and self.last_color == 'color':
            condition = 4
        if self.last_target_value == 660 and self.last_image_type == 'bar' and self.last_color == 'text':
            condition = 5
        if self.last_target_value == 1200 and self.last_image_type == 'bar' and self.last_color == 'text':
            condition = 6
        if self.last_target_value == 660 and self.last_image_type == 'bar' and self.last_color == 'color':
            condition = 7
        if self.last_target_value == 1200 and self.last_image_type == 'bar' and self.last_color == 'color':
            condition = 8
        if self.last_target_value == 660 and self.last_image_type == 'pie' and self.last_color == 'none':
            condition = 9
        if self.last_target_value == 1200 and self.last_image_type == 'pie' and self.last_color == 'none':
            condition = 10
        if self.last_target_value == 660 and self.last_image_type == 'pie' and self.last_color == 'color':
            condition = 11
        if self.last_target_value == 1200 and self.last_image_type == 'pie' and self.last_color == 'color':
            condition = 12

        answer = {
            'condition': condition,
            'duration': duration,
            'result': result,
            'customer_select': select,
            'last_target_name': self.last_target_name,
            'last_target_value': self.last_target_value,
            'last_image_type': self.last_image_type,
            'last_color': self.last_color,
            'last_data': self.last_data
        }
        self.answerData.append(answer)

        if self.curStep < len(self.pathData):
            self.lastTime = datetime.now()
            self.last_image_type = self.pathData[self.curStep].get("image_type")
            self.last_color = self.pathData[self.curStep].get("color")
            self.last_target_name = self.pathData[self.curStep].get("target_name")
            self.last_target_value = self.pathData[self.curStep].get("target_value")
            self.last_data = self.pathData[self.curStep]

            image_type = self.pathData[self.curStep].get("image_type")
            color = self.pathData[self.curStep].get("color")

            x = []
            y = []

            for item in self.pathData[self.curStep].get("data"):
                name = item.get("name")
                value = item.get("value")
                x.append(name)

                y.append(value)

            self.curStep += 1

            self.draw(image_type, color, x, y)

            # add answer
            self.comboBox.clear()
            self.comboBox.clearEditText()
            self.comboBox.addItems(PATH)
            self.comboBox.setCurrentIndex(-1)
            self.comboBox.setCurrentText('')
        else:
            tkinter.messagebox.askyesno("Thanks", "The experiment is complete, thanks for participating.")
            answerData = json.dumps(self.answerData)
            txt = "./answer" + str(datetime.now()) + ".txt"
            file = open(txt, 'w')
            file.write(answerData)
            file.close()

    # draw charts

    def draw(self, image_type, color, x, y):
        if image_type == "bar":
            if color == 'color':
                self.drawBar(x, y, self.color_list)
            else:
                self.drawBar(x, y, None)
        if image_type == "column":
            if color == 'color':
                self.drawColumn(x, y, self.color_list)
            else:
                self.drawColumn(x, y, None)
        if image_type == "pie":
            if color == "color":
                self.drawPie(x, y)
            else:
                self.drawPie2(x, y)


if __name__ == "__main__":

    tk = Tk()
    tk.withdraw()

    askyesno = tkinter.messagebox.askyesno("Hi", "Please make sure you have informed consent.")
    if askyesno:
        app = QApplication(sys.argv)
        main = MainDialogImgBW()
        main.show()
        sys.exit(app.exec_())
    else:
        tkinter.messagebox.showinfo("Bye", "Have a good day.")
        sys.exc_info()
