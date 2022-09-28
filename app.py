import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem
)
from PyQt5 import QtCore, QtGui
from cv2 import line
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pyrsistent import s

from main_window_ui import Ui_MainWindow
from util import dms2dec
from tqdm import tqdm
import subprocess
import re 
from PIL import Image
import numpy as np
import math
input_dir = "D:/Radek/Doktorat/Badania/Termo/data/20220701_tyniec/tif/1240"
output_dir = "D:/Radek/Doktorat/Badania/Termo/data/20220701_tyniec/tif_tuned/1240"


class Window(QMainWindow, Ui_MainWindow):
    def writeCsv(self):
        with open(os.path.join(output_dir, "files.csv"), "w") as f:
            for csv_dict in self.csv_data:
                f.write(csv_dict["file"] + "," + str(csv_dict["lat"]) + "," + str(csv_dict["lon"]) + "," + str(csv_dict["offset"]) + "\n")
    def populateTable(self):
        for i, csv_dict in enumerate(self.csv_data):
            self.tableWidget_files.setItem(i, 0, QTableWidgetItem(csv_dict["file"]))
            self.tableWidget_files.setItem(i, 1, QTableWidgetItem(str(csv_dict["offset"])))
            if hasattr(self, "reference_row") and self.reference_row == i:  
                self.tableWidget_files.item(i, 0).setBackground(QtGui.QColor("pink"))
                self.tableWidget_files.item(i, 1).setBackground(QtGui.QColor("pink"))
            elif hasattr(self, "selected_row") and self.selected_row == i:
                self.tableWidget_files.item(i, 0).setBackground(QtGui.QColor("lightblue"))
                self.tableWidget_files.item(i, 1).setBackground(QtGui.QColor("lightblue"))
            elif math.isclose(csv_dict["offset"],0.0):
                self.tableWidget_files.item(i, 0).setBackground(QtGui.QColor("white"))
                self.tableWidget_files.item(i, 1).setBackground(QtGui.QColor("white"))
            else:
                self.tableWidget_files.item(i, 0).setBackground(QtGui.QColor("lightgreen"))
                self.tableWidget_files.item(i, 1).setBackground(QtGui.QColor("lightgreen"))

    def on_ApplyClicked(self):
        self.offset = self.doubleSpinBox_Offset.value()
        self.csv_data[self.selected_row]["offset"] = self.offset
        self.redraw_selected()
        self.populateTable()
        self.writeCsv()
        if hasattr(self, "marker_coords"):
            self.doubleSpinBox_Probe.setValue(self.selected_tiff[self.marker_coords[1], self.marker_coords[0]])
    def image_onclick(self, event):
        if hasattr(self, "marker_handle"):
            if len(self.marker_handle)>0:
                [h.remove() for h in self.marker_handle]
                self.marker_handle.clear()
        self.marker_coords = (int(event.xdata), int(event.ydata))
        self.marker_handle = self.mpl_selectedImage.canvas.axes.plot(self.marker_coords[0], self.marker_coords[1], "x", markersize=10, color="red")
        self.mpl_selectedImage.canvas.draw()
        #set self.doubleSpinBox_Probe value to selected pixel value
        self.doubleSpinBox_Probe.setValue(self.selected_tiff[self.marker_coords[1], self.marker_coords[0]])
    def redraw_map(self):
        colors = []
        for i, csv_dict in enumerate(self.csv_data):
            if hasattr(self, "reference_row") and self.reference_row == i:  
                colors.append("pink")
            elif hasattr(self, "selected_row") and self.selected_row == i:
                colors.append("lightblue")
            elif math.isclose(csv_dict["offset"],0.0):
                colors.append("gray")
            else:
                colors.append("lightgreen")
        self.mpl_map.canvas.axes.cla()
        self.mpl_map.canvas.axes.scatter(self.lat_list, self.lon_list, color=colors)
        self.mpl_map.canvas.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.mpl_map.canvas.draw()
    def redraw_histogram(self):
        self.mpl_histogram.canvas.axes.cla()
        #remove margins
        self.mpl_histogram.canvas.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.1)
        if hasattr(self, "hist_reference"):
            self.mpl_histogram.canvas.axes.plot(self.hist_reference[1][:-1], self.hist_reference[0], color="red")
        if hasattr(self, "hist_selected"):
            self.mpl_histogram.canvas.axes.plot(self.hist_selected[1][:-1], self.hist_selected[0], color="blue")
        self.mpl_histogram.canvas.draw()
    def redraw_selected(self):
        self.selected_tiff = np.array(Image.open(os.path.join(input_dir, self.csv_data[self.selected_row]["file"]))) + self.csv_data[self.selected_row]["offset"]
        self.mpl_selectedImage.canvas.axes.imshow(self.selected_tiff, cmap='nipy_spectral')
        self.mpl_selectedImage.canvas.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.mpl_selectedImage.canvas.draw()
        self.mpl_selectedImage.canvas.mpl_connect('button_press_event', self.image_onclick)
        if not (hasattr(self, "min_temp") and hasattr(self, "max_temp")):
            self.min_temp = self.selected_tiff.min()
            self.max_temp = self.selected_tiff.max()
        self.hist_selected = np.histogram(self.selected_tiff, bins=50, range=(self.min_temp, self.max_temp))
        self.redraw_histogram()
    def redraw_reference(self):
        self.reference_tiff = np.array(Image.open(os.path.join(input_dir, self.csv_data[self.reference_row]["file"]))) + self.csv_data[self.selected_row]["offset"]
        self.min_temp = self.reference_tiff.min()
        self.max_temp = self.reference_tiff.max()
        self.mpl_referenceImage.canvas.axes.imshow(self.reference_tiff, cmap='nipy_spectral')
        self.mpl_referenceImage.canvas.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.mpl_referenceImage.canvas.draw()
        self.hist_reference = np.histogram(self.reference_tiff, bins=50, range=(self.min_temp, self.max_temp))
        self.redraw_histogram()
    def on_tableWidget_files_clicked(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.reference_row = self.tableWidget_files.currentRow()
            self.populateTable()
            self.redraw_reference()
        else:
            self.selected_row = self.tableWidget_files.currentRow()
            self.doubleSpinBox_Offset.setValue(self.csv_data[self.selected_row]["offset"])
            self.populateTable()
            self.redraw_selected()
        self.redraw_map()
    def load_files(self):
        #check if files.csv file exists
        self.csv_data = []
        if os.path.isfile(os.path.join(output_dir, "files.csv")):
            #read files.csv
            with open(os.path.join(output_dir, "files.csv"), "r") as f:
                lines = f.readlines()
                for line in lines:
                    v = line.split(",")
                    self.csv_data.append({"file": v[0], "lat": float(v[1]), "lon": float(v[2]), "offset": float(v[3])})
        else:
            file_list = [file for file in os.listdir(input_dir) if file.endswith(".tiff")]
            for file in tqdm(file_list):
                file_path = os.path.join(input_dir, file)
                #read exiftool command output
                lat, lon = subprocess.run(['exiftool', '-GPSLatitude', '-GPSLongitude', file_path], stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()
                lat = lat.split(":",1)[1].strip()
                lon = lon.split(":",1)[1].strip()
                #lon = subprocess.run(['exiftool', '-GPSLongitude', file_path], stdout=subprocess.PIPE).stdout.decode("utf-8").split(":",1)[1].strip()
                lat = [x.strip() for x in re.split('[deg\'"]', lat) if x]
                lon = [x.strip() for x in re.split('[deg\'"]', lon) if x]
                print(f"{lat}; {lon}")
                lat = dms2dec(lat)
                lon = dms2dec(lon)
                self.csv_data.append({"file": file, "lat": lat, "lon": lon, "offset": 0.0})
            #write files.csv
            self.writeCsv()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        os.makedirs(output_dir, exist_ok=True)
        self.load_files()
        #populate self.listView_images with file_list
        self.tableWidget_files.setRowCount(len(self.csv_data))
        self.tableWidget_files.setColumnCount(2)
        self.tableWidget_files.setHorizontalHeaderLabels(["File", "Offset"])
        self.populateTable()
        self.mpl_referenceImage.canvas.axes.axis("off")
        self.mpl_referenceImage.canvas.figure.set_facecolor('pink')
        self.mpl_selectedImage.canvas.axes.axis("off")
        self.mpl_selectedImage.canvas.figure.set_facecolor('lightblue')
        self.mpl_map.canvas.axes.axis("off")
        self.lat_list = [csv_dict["lat"] for csv_dict in self.csv_data]
        self.lon_list = [csv_dict["lon"] for csv_dict in self.csv_data]
        self.redraw_map()
        #listWidget_files selection change callback
        self.tableWidget_files.clicked.connect(self.on_tableWidget_files_clicked)
        self.pushButton_Apply.clicked.connect(self.on_ApplyClicked)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())