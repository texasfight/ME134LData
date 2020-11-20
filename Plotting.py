import pandas
import math
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filename = filedialog.askopenfilename()
print(filename)


class Specimen:
    area = None

    def __init__(self, filepath):
        # Create Dataframe for the excel file for all of the tension testing data
        self.data = pandas.read_excel(filepath, header=8, usecols="B:C")
        self.constants = pandas.read_excel(filepath, header=None, nrows=8, usecols="A:B").transpose()
        self.constants.columns = self.constants.iloc[0]
        self.constants = self.constants.iloc[1]
        self.diameter = self.constants["Initial Diameter (calipers)"]
        self.area = self.diameter ** 2 / 4 * math.pi
        self.name = self.constants["Specimen Name"]
        self.gaugeLength = self.constants["Gauge Length (extensometer)"]
        self.eng_stress = self.data["Load N"].apply(lambda x, a: x / a, args=(self.area,))
        self.eng_stress = self.eng_stress.rename({"Load N": "Eng. Stress"})
        self.eng_strain = self.data["Extension(extensometer) mm"].apply(lambda x, e: x / e, args=(self.gaugeLength,))
        self.eng_strain = self.eng_strain.rename({"Extension(extensometer) mm": "Eng. Strain"})
        self.eng_data = pandas.DataFrame(self.eng_strain, self.eng_stress)
        print(self.eng_data)

    def gen_graphs(self):
        output_file("Stress_Strain_{}.html".format(self.name))
        source = ColumnDataSource(self.eng_data)
        xlabel = 'Engineering Strain'
        ylabel = 'Engineering Stress'
        TOOLS = 'pan, wheel_zoom, box_select, reset, save'
        plot = figure(title="Ln(stress) vs. Ln(strain)", x_axis_label=xlabel, y_axis_label=ylabel,
                      tools=TOOLS, toolbar_location="below")
        plot.circle(x="Eng. Strain", y="Eng. Stress", source=source, fill_color="white", radius=.05)
        show(plot)

    # Create Engineering Stress and Strain data sets
    # eng_stress = [force / area for force in load]
    # eng_strain = [length / diameter for length in extension]
    #
    # # Create True Stress and Strain Data Sets
    # true_stress = [stress * (1 + strain) for stress, strain in zip(eng_stress, eng_strain)]
    # true_strain = [math.log(1 + strain) for strain in eng_strain]
    # plt.figure(1)
    # plt.plot(true_strain, true_stress)
    # plt.ylabel("True Stress (MPa)")
    # plt.xlabel("True Strain")
    # plt.savefig("true_plots.png")
    #
    # ln_true_stress = []
    # ln_true_strain = []
    # for strain, stress in zip(true_strain, true_stress):
    #     if strain > 0:
    #         ln_true_strain.append(math.log(strain))
    #         ln_true_stress.append(math.log(stress))
    # output_file("Logarithmic_true{}.html".format(""))
    #
    # xlabel = 'Natural Logarithm of True Strain'
    # ylabel = 'Natural Logarithm of True Stress'
    # TOOLS = 'pan, wheel_zoom, box_select, reset, save'
    # lnplot = figure(title="Ln(stress) vs. Ln(strain)", x_axis_label=xlabel, y_axis_label=ylabel,
    #                 tools=TOOLS, toolbar_location="below")
    # lnplot.circle(ln_true_strain, ln_true_stress, fill_color="white", radius=.05)


spec = Specimen(filename)
spec.gen_graphs()
