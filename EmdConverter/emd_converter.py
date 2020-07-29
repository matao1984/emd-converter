# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'emd_converter_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import numpy as np
from skimage import exposure, img_as_ubyte

class Ui_EMD_converter(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_EMD_converter,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        



    def setupUi(self, EMD_converter):
        EMD_converter.setObjectName("EMD_converter")
        EMD_converter.resize(456, 300)
        self.pushButton = QtWidgets.QPushButton(EMD_converter)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 91, 61))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(EMD_converter,readOnly=True)
        self.textEdit.setGeometry(QtCore.QRect(130, 20, 301, 61))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(EMD_converter)
        self.label.setGeometry(QtCore.QRect(40, 100, 91, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(EMD_converter)
        self.comboBox.setGeometry(QtCore.QRect(130, 100, 73, 22))
        self.comboBox.addItems(['.tif', '.png', '.jpg','.bmp'])

        self.comboBox.setObjectName("comboBox")
        self.pushButton_2 = QtWidgets.QPushButton(EMD_converter)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 130, 91, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit_2 = QtWidgets.QTextEdit(EMD_converter)
        self.textEdit_2.setGeometry(QtCore.QRect(130, 130, 301, 61))
        self.textEdit_2.setObjectName("textEdit_2")
        self.checkBox = QtWidgets.QCheckBox(EMD_converter)
        self.checkBox.setGeometry(QtCore.QRect(250, 100, 81, 20))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.pushButton_3 = QtWidgets.QPushButton(EMD_converter)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 210, 91, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textEdit_3 = QtWidgets.QTextEdit(EMD_converter)
        self.textEdit_3.setGeometry(QtCore.QRect(130, 210, 301, 61))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_2 = QtWidgets.QLabel(EMD_converter)
        self.label_2.setGeometry(QtCore.QRect(30, 280, 351, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(EMD_converter)
        QtCore.QMetaObject.connectSlotsByName(EMD_converter)
        
#====================================================================
# Connect all functions
        self.pushButton.clicked.connect(self.openfile)
        self.pushButton_2.clicked.connect(self.set_dir)
        self.pushButton_3.clicked.connect(self.convert_emd)
        

    def retranslateUi(self, EMD_converter):
        _translate = QtCore.QCoreApplication.translate
        EMD_converter.setWindowTitle(_translate("EMD_converter", "EMD_converter v0.1"))
        self.pushButton.setText(_translate("EMD_converter", "Open files"))
        self.label.setText(_translate("EMD_converter", "Covnert to"))
        self.pushButton_2.setText(_translate("EMD_converter", "Output \n"
"directory"))
        self.checkBox.setText(_translate("EMD_converter", "Overwrite"))
        self.pushButton_3.setText(_translate("EMD_converter", "Let\'s go!"))
        self.label_2.setText(_translate("EMD_converter", "EMD converter v0.1 by Dr. Tao Ma    taoma@umich.edu"))
        
#===================================================================
# Open file button connected to pushButton

    def openfile(self):
        global files, output_dir
        files, _ = QFileDialog.getOpenFileNames(self,"Select emd files to be converted:", "","Velox emd Files (*.emd);;All Files (*)")
        if files:
#            print(files)
            output_dir = getDirectory(files[0],s='/')
            self.textEdit_2.setText(output_dir)
            self.textEdit.setText('')
            for file in files:
                self.textEdit.append(file)
                


#===================================================================
# Output directory button connected to pushButton_2

    def set_dir(self):
        global output_dir
        output_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if output_dir:
            self.textEdit_2.setText(output_dir)
            
#===================================================================
# Let's go button connected to pushButton_3

    def convert_emd(self):
        global f_type, ow
        f_type = self.comboBox.currentText()
        
        if self.checkBox.isChecked():
            ow = True
        else:
            ow = False
        self.textEdit_3.append('Converting, please wait...') 
        QtWidgets.QApplication.processEvents()
        for file in files:
            convert_emd_with_hs(file,output_dir,f_type)
            msg = "'{}.emd' has been converted".format(getFileName(file))
            self.textEdit_3.append(msg)
            QtWidgets.QApplication.processEvents()
        self.textEdit_3.append('Conversion finished!')        

                  

#==================================================================
# Helper functions
from hyperspy.io import load

def getDirectory(file, s='.'):
    #Make the working directory and return the path.
    for idx in range(-1, -len(file), -1): 
        if file[idx] == s: #find the file extension and remove it. '/' for parent path
            path = file[:idx] + '/'
            return path
        
def getFileName(file):
    full_name = getDirectory(file)
    full_path = getDirectory(file, s='/')
    f_name = full_name[len(full_path):-1]
    return f_name

def save_emd_as(emd_file, f_name, output_dir, f_type):
    data = np.array(emd_file.data)
    if f_type == '.jpg' or f_type == '.bmp':
        #Rescale and convert the data to uint8 for jpg and bmp
        emd_file.data = img_as_ubyte(exposure.rescale_intensity(data))
    if f_type == '.png':
        emd_file.data = exposure.rescale_intensity(data)
    #Reset the scale and origin for the intensity
    try:
        emd_file.metadata.Signal.Noise_properties.Variance_linear_model.gain_factor = 1
        emd_file.metadata.Signal.Noise_properties.Variance_linear_model.gain_offset = 0
    except:
        pass
    emd_file.save(output_dir + f_name + f_type, overwrite=ow)
    

        
        
def convert_emd_with_hs(file, output_dir, f_type):
    #f_type: The file type to be saved. e.g., '.tif', '.png', '.jpg' 
    #
    f_emd = load(file,lazy=True)
    f_name = getFileName(file)
    if len(f_emd) == 1: #Single file, the simplest dataset
        if f_emd.metadata.Signal.signal_type == 'image':
            save_emd_as(f_emd, f_name, output_dir, f_type=f_type)
    else:
        new_dir = output_dir + f_name + '/'
        for idx in range(len(f_emd)):
            if f_emd[idx].metadata.Signal.signal_type == 'image':
                title = f_emd[idx].metadata.General.title
                s_lst = list(f_emd[idx])
                for i_idx in range(len(s_lst)):
                    new_name = '{}_{}_{}'.format(title, idx, i_idx) 
                    save_emd_as(s_lst[i_idx], new_name, new_dir, f_type=f_type)


#====Application entry==================================
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EMD_converter = QtWidgets.QWidget()
    ui = Ui_EMD_converter()
    ui.setupUi(EMD_converter)
    EMD_converter.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()