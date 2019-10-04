import psutil
from shutil import copyfile
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QTableWidget,
    QPushButton, QTableWidgetItem)

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.hex_file_path = "/home/marek/Desktop/heart.hex"
        self.microbit_list = []
        self.initUI()

    def search_microbits(self):
        self.microbit_list = []
        version_number = None
        self.status_table.setRowCount(0)
        all_partitions = psutil.disk_partitions()
        for partition in all_partitions:
            if "MICROBIT" in partition.mountpoint:
                self.microbit_list.append(partition)
        print(self.microbit_list)
        
        for i, microbit in enumerate(self.microbit_list):
            self.status_table.setRowCount(i+1)
            self.status_table.setItem(0,0, QTableWidgetItem(microbit.device))
            self.status_table.setItem(0,1, QTableWidgetItem(microbit.mountpoint))
            with open(microbit.mountpoint + "/DETAILS.TXT", "r") as file:
                for line in file.readlines():
                    if "Interface Version" in line:
                        version_number = line.strip().split(" ")[-1]
            if version_number:
                self.status_table.setItem(0,2, QTableWidgetItem(version_number))
        self.status_table.resizeColumnsToContents()
        self.status_table.resizeRowsToContents()


    def flash_microbits(self):
        if self.hex_file_path == None:
            print("No Hex File Chosen!")
            return

        if len(self.microbit_list) == 0:
            print("No micro:bit found")
            return

        for microbit in self.microbit_list:
            copyfile(self.hex_file_path, microbit.mountpoint + "/hex.hex")        
        
    def initUI(self):
        
        hex_file_label = QLabel('Hex File')
        status_table_label = QLabel('micro:bits')

        hex_file_edit = QLineEdit()
        self.status_table = QTableWidget()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(hex_file_label, 1, 0)
        grid.addWidget(hex_file_edit, 1, 1)
        
        hex_file_edit.setText("/home/marek/Desktop/heart.hex")

        grid.addWidget(status_table_label, 2, 0)
        grid.addWidget(self.status_table, 2, 1)

        self.status_table.setRowCount(0)
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(['Device', 'Mountpoint', 'Version'])
        self.status_table.resizeColumnsToContents()

        search_btn = QPushButton("Search for micro:bits")
        search_btn.clicked.connect(self.search_microbits)
        flash_btn = QPushButton("Flash Hex to micro:bits")
        flash_btn.clicked.connect(self.flash_microbits)
        
        grid.addWidget(search_btn, 3, 1)
        grid.addWidget(flash_btn, 4, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle('Flash:bit - flash multiple micro:bits with ease')    
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# import psutil
# from shutil import copyfile


# x = psutil.disk_partitions()

# for i in x:
#     if "MICROBIT" in i.mountpoint:
#         print(i)
#         copyfile("/home/marek/Desktop/heart.hex", i.mountpoint + "/heart.hex")
