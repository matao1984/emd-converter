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
import os
import numpy as np
from skimage import exposure, img_as_ubyte
from PIL import Image, ImageDraw, ImageFont

ver = '0.3'
rdate = 'Jul-19-2021'

class Ui_EMD_converter(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_EMD_converter,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        



    def setupUi(self, EMD_converter):
        EMD_converter.setObjectName("EMD_converter")
        EMD_converter.resize(456, 340)
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
        self.comboBox.setGeometry(QtCore.QRect(130, 100, 95, 22))
        self.comboBox.addItems(['tif + png','tif', 'png', 'jpg','bmp'])

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
        self.label_2.setGeometry(QtCore.QRect(30, 315, 351, 16))
        self.label_2.setObjectName("label_2")
        
        self.pushButton_4 = QtWidgets.QPushButton(EMD_converter)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 280, 90, 30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(EMD_converter)
        self.pushButton_5.setGeometry(QtCore.QRect(150, 280, 90, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(EMD_converter)
        self.pushButton_6.setGeometry(QtCore.QRect(270, 280, 130, 30))
        self.pushButton_6.setObjectName("pushButton_4")

        self.retranslateUi(EMD_converter)
        QtCore.QMetaObject.connectSlotsByName(EMD_converter)
        
#====================================================================
# Connect all functions
        self.pushButton.clicked.connect(self.openfile)
        self.pushButton_2.clicked.connect(self.set_dir)
        self.pushButton_3.clicked.connect(self.convert_emd)
        self.pushButton_4.clicked.connect(self.show_about)
        self.pushButton_5.clicked.connect(self.show_contact)
        self.pushButton_6.clicked.connect(self.donate)
        

    def retranslateUi(self, EMD_converter):
        _translate = QtCore.QCoreApplication.translate
        EMD_converter.setWindowTitle(_translate("EMD_converter", "EMD converter Ver {}".format(ver)))
        self.pushButton.setText(_translate("EMD_converter", "Open files"))
        self.label.setText(_translate("EMD_converter", "Covnert to"))
        self.pushButton_2.setText(_translate("EMD_converter", "Output \n"
"directory"))
        self.checkBox.setText(_translate("EMD_converter", "Scale bar"))
        self.pushButton_3.setText(_translate("EMD_converter", "Let\'s go!"))
        self.label_2.setText(_translate("EMD_converter", "EMD converter by Dr. Tao Ma   {}".format(rdate)))
        
        self.pushButton_4.setText(_translate("EMD_converter", "About"))
        self.pushButton_5.setText(_translate("EMD_converter", "Contact"))
        self.pushButton_6.setText(_translate("EMD_converter", "Buy me a LUNCH!"))
#===================================================================
# Open file button connected to pushButton

    def openfile(self):
        global files, output_dir
        files, _ = QFileDialog.getOpenFileNames(self,"Select files to be converted:", "","Velox emd Files (*.emd);;TIA ser Files (*.ser);;DigitalMicrograph Files (*.dm3 *.dm4);;All Files (*)")
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
        output_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory") + '/')
        if output_dir:
            self.textEdit_2.setText(output_dir)
            
#===================================================================
# Let's go button connected to pushButton_3

    def convert_emd(self):
        global f_type, scale_bar
        f_type = self.comboBox.currentText()
        
        if self.checkBox.isChecked():
            scale_bar = True
        else:
            scale_bar = False
        self.textEdit_3.append('Converting, please wait...') 
        QtWidgets.QApplication.processEvents()
        for file in files:        
            try:
                convert_emd_with_hs(file,output_dir,f_type)
                msg = "'{}.{}' has been converted".format(getFileName(file),getFileType(file))
            except:
                msg = "'{}.{}' has been skipped".format(getFileName(file),getFileType(file))
            self.textEdit_3.append(msg)
            QtWidgets.QApplication.processEvents()
        self.textEdit_3.append('Conversion finished!')        
        
#=====================================================================        
    def show_about(self):
        msg = QMessageBox()
#        msg.setIcon(QMessageBox.Information)
        msg.setText("EMD converter: a tool to convert Velox emd files and more to tiff, png, bmp, and jpg."\
                    "<br>"\
                    "This app was designed by Dr. Tao Ma"\
                    "<br>"\
                    "Version: {}  Released: {}"\
                    "<br>"\
                    "Hope you get good results and publications from it!"\
                    "<br>"\
                    "Get more information and source code from <a href=\"https://github.com/matao1984/emd-converter\">here</a>.".format(ver, rdate))
        msg.setWindowTitle(ver + ": About")

        returnValue = msg.exec()

#=====================================================================        
    def show_contact(self):
        msg = QMessageBox()
        msg.setText("Ask questions and report bugs to:"\
                    "<br>"
                    "<a href=\"mailto:matao1984@gmail.com\">matao1984@gmail.com</a>")
        msg.setWindowTitle(ver + ": Contact")

        returnValue = msg.exec()
        
#====================================================================
        
    def donate(self):
        msg = QMessageBox()
        msg.setText("I will make this app freely available for the society.<br>"\
                    "If you like this app, show your appreciation and <a href=\"https://www.paypal.com/donate/?business=ZCSWE88TR2YHY&no_recurring=0&currency_code=USD\">buy me a lunch!</a>"\
                    "<br>"\
                    "Your support is my motivation!")
        msg.setWindowTitle(ver + ": Buy me a LUNCH!")

        returnValue = msg.exec()

                  

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

def getFileType(file):
    full_name = getDirectory(file)
    file_type = file[len(full_name):]
    return file_type

def save_emd_as(emd_file, f_name, output_dir, f_type):
    #Save images
    #Reset the scale and origin for the intensity
    try:
        emd_file.metadata.Signal.Noise_properties.Variance_linear_model.gain_factor = 1
        emd_file.metadata.Signal.Noise_properties.Variance_linear_model.gain_offset = 0
    except:
        pass
    #Check if the output_dir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if f_type == 'tif':
        # For tif format, save directly as 16-bit with calibration, no scalebar
        # No manipulation of data
        emd_file.save(output_dir + f_name + '.' + f_type, overwrite=True)
        
    elif f_type == 'tif + png' or 'jpg' or f_type == 'bmp' or f_type == 'png':
        #Rescale and convert the data to uint8
        data = img_as_ubyte(exposure.rescale_intensity(emd_file.data))
        im = Image.fromarray(data)
        if scale_bar == True:
            #Add a scale bar
            im_x, im_y = im.size
            scale = emd_file.axes_manager[0].scale
            unit = emd_file.axes_manager[0].units
            fov_x = im_x * scale
            # Find a good integer length for the scalebar 
            sb_len_float = fov_x / 6 #Scalebar length is about 1/6 of FOV
            # A list of allowed lengths for the scalebar
            sb_lst = [0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000]
            # Find the closest value in the list
            sb_len = sorted(sb_lst, key=lambda a: abs(a - sb_len_float))[0]
            sb_len_px = sb_len / scale
            sb_start_x, sb_start_y = (im_x / 12, im_y *11 / 12) #Bottom left corner from 1/12 of FOV
            draw = ImageDraw.Draw(im)
            sb = (sb_start_x, sb_start_y, sb_start_x + sb_len_px, sb_start_y + im_y/ 100)
            outline_width = round(im_y/500)
            if outline_width == 0:
                outline_width = 1
            draw.rectangle(sb, fill = 'white', outline = 'black', width = outline_width)
            # Add text
            text = str(sb_len) + ' ' + unit
            fontsize = int(im_x / 20)
            try: 
                font = ImageFont.truetype("arial.ttf", fontsize)
            except:
                try: 
                    font = ImageFont.truetype("Helvetica.ttc", fontsize)
                except:
                    font = ImageFont.load_default()
            txt_x, txt_y = (sb_start_x * 1.2, sb_start_y - fontsize * 1.2 - im_y/100)
            # Add outline to the text
            draw.text((txt_x-1, txt_y-1), text, font=font, fill='black')
            draw.text((txt_x+1, txt_y-1), text, font=font, fill='black')
            draw.text((txt_x-1, txt_y+1), text, font=font, fill='black')
            draw.text((txt_x+1, txt_y+1), text, font=font, fill='black')
            draw.text((txt_x, txt_y), text, fill='white', font=font, anchor=None)
        if f_type == 'tif + png':
            emd_file.save(output_dir + f_name + '.tif', overwrite=True)
            f_type = 'png'
            
        im.save(output_dir + f_name + '.' + f_type)
        
        
def convert_emd_with_hs(file, output_dir, f_type):
    #f_type: The file type to be saved. e.g., '.tif', '.png', '.jpg' 
    #
    f_emd = load(file,lazy=True)
    f_name = getFileName(file)
    if len(f_emd) == 1: #Single file, the simplest dataset
        if f_emd.axes_manager.signal_dimension == 2:
            save_emd_as(f_emd, f_name, output_dir, f_type=f_type)
    else:
        for idx in range(len(f_emd)):
            if len(f_emd[idx]) != 1:
                DCFI = 1
                break
            else:
                DCFI = 0
        if DCFI == 0:#EMD file contains multiple images, e.g., HAADF, BF, DF2,...
            for idx in range(len(f_emd)):
                if f_emd[idx].axes_manager.signal_dimension == 2:#This is a 2D image
                    title = f_emd[idx].metadata.General.title
                    new_name = f_name + '_' + title
                    save_emd_as(f_emd[idx], new_name, output_dir, f_type=f_type)

        if DCFI == 1:#Make a folder for DCFI type images
            new_dir = output_dir + f_name + '/'
            for idx in range(len(f_emd)):
#                print('idx={}'.format(idx))
                if f_emd[idx].axes_manager.signal_dimension == 2:#This is a 2D image
                    title = f_emd[idx].metadata.General.title
                    s_lst = list(f_emd[idx])
                    for i_idx in range(len(s_lst)):
#                        print('i_idx={}'.format(i_idx))
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
