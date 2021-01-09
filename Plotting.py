import pandas
import math
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename()


class Specimen:

    def __init__(self, filepath):
        # Create Dataframe for the excel file for all of the tension testing data
        self.data = pandas.read_excel(filepath, header=8, usecols="B:C")
        # Create pandas series for the constants data at the top of the file
        self.constants = pandas.read_excel(filepath, header=None, nrows=8, usecols="A:B").transpose()
        self.constants.columns = self.constants.iloc[0]
        self.constants = self.constants.iloc[1]
        # Create some important variables for processing the graphical data and labelling the sample
        self.area = self.constants.at["Initial Diameter (calipers)"] ** 2 / 4 * math.pi
        self.name = self.constants.at["Specimen Name"]
        self.gaugeLength = self.constants.at["Gauge Length (extensometer)"]
        self.eng_stress = self.data["Load N"].apply(lambda x, a: x / a, args=(self.area,))
        self.eng_stress = self.eng_stress.rename("Eng. Stress")
        self.eng_strain = self.data["Extension(extensometer) mm"].apply(lambda x, e: x / e, args=(self.gaugeLength,))
        self.eng_strain = self.eng_strain.rename("Eng. Strain")
        self.eng_data = pandas.concat((self.eng_strain, self.eng_stress), axis=1)

    def gen_graphs(self):
        save_location = filedialog.askdirectory()
        output_file(save_location + r"\Stress_Strain_{}.html".format(self.name))
        source = ColumnDataSource(self.eng_data)
        xlabel = 'Engineering Strain'
        ylabel = 'Engineering Stress'
        tools = 'pan, wheel_zoom, box_select, reset, save'
        eng_plot = figure(title='Engineering \u03C3 vs. \u03B5', x_axis_label=xlabel, y_axis_label=ylabel,
                          tools=tools, toolbar_location="below")
        eng_plot.circle(x="Eng. Strain", y="Eng. Stress", source=source)
        show(eng_plot)


spec = Specimen(filename)
spec.gen_graphs()
