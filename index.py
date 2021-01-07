#!usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
# from main import Ui_MainWindow
import img_rc
import sys
import sqlite3
from functools import partial
import datetime
ui,_ = loadUiType('main.ui')
class createProduct(QMainWindow, ui):
    def __init__(self , parent=None):
        super(createProduct , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.heroLay = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.heroLay.setMinimumSize(QtCore.QSize(250, 250))
        self.heroLay.setMaximumSize(QtCore.QSize(250, 250))

        
        # Create the group box
        self.newCart = QtWidgets.QVBoxLayout(self.heroLay)
        self.newCart.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.newCart.setContentsMargins(10, 10, 10, 10)

        # Create the images
        self.image = QtWidgets.QLabel(self.heroLay)
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("img/download.jpeg")) ##################
        self.image.setScaledContents(True)


        # append the image to the group box
        self.newCart.addWidget(self.image)

        # Create the name 
        self.name = QtWidgets.QLabel(self.heroLay)
        self.name.setText("") ###############################
        font = QtGui.QFont()
        font.setPointSize(14)
        self.name.setFont(font)


        # append the name to th group box
        self.newCart.addWidget(self.name)

        # Create the button 
        self.btnShow = QtWidgets.QPushButton(self.heroLay)
        self.btnShow.setText("تصفح")
        self.btnShow.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(29)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnShow.sizePolicy().hasHeightForWidth())
        self.btnShow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnShow.setFont(font)
        self.btnShow.setStyleSheet("padding: 20px;")


        # append the button to the group box
        self.newCart.addWidget(self.btnShow)


class MainApp(QMainWindow, ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handelUi()
        self.openMainScreen()
        self.DB_connection()
        today = datetime.date.today()
        self.dateEdit.setDate(today)
        self.dateEdit_2.setDate(today)
        self.handelProductPage()
        self.handelButtons()
        self.displayProduct()
        self.displayDailyWork(self.tableWidget)
        self.displayDailyWork(self.tableWidget_3, 2)
        
        self.dayEnd()

    def handelUi(self):

        self.label_8.setVisible(False)
        self.tabWidget.tabBar().setVisible(False)
        self.setWindowTitle('Elburinsesa')
        self.handelTable(self.tableWidget, 6)
        self.handelTable(self.tableWidget_3, 6)
    
    def handelTable(self, table, colNum):
        header = table.horizontalHeader()
        header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.ResizeToContents) 

    def handelButtons(self):
        self.pushButton.clicked.connect(self.dailyWork)
        self.pushButton_2.clicked.connect(self.openMainScreen)
        self.pushButton_3.clicked.connect(self.openProductScreen)
        self.pushButton_4.clicked.connect(self.openDayEnd)
        self.pushButton_6.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.openEditProduct)
        self.pushButton_8.clicked.connect(self.openBaymentScreen)
        self.pushButton_11.clicked.connect(self.getDataFromAdd)
        self.pushButton_12.clicked.connect(self.editProduct)
        self.pushButton_13.clicked.connect(self.deleteProduct)
        self.pushButton_15.clicked.connect(self.openEditProduct)
        self.pushButton_16.clicked.connect(partial(self.openImg, self.label_5))
        self.pushButton_17.clicked.connect(self.searchOnProduct)
        self.pushButton_18.clicked.connect(partial(self.openImg, self.label_7))
        self.pushButton_19.clicked.connect(self.showAllAgain)
        self.pushButton_5.clicked.connect(self.openDital)
        self.pushButton_28.clicked.connect(self.baymentProduct)
        self.pushButton_9.clicked.connect(self.tableDetails)
        


    def DB_connection(self):
        self.db = sqlite3.connect('Elburinsisa.db')
        self.cr = self.db.cursor()

    def searchOnProduct(self):
        pro = self.lineEdit_7.text()
        self.clearScreen()
        self.cr.execute('''
            SELECT * FROM Product WHERE name="{}"
        '''.format(pro))
        data = self.cr.fetchall()
        
        for i in data:
            newProUi = createProduct()
            newProUi.name.setText(i[1])
            newProUi.image.setPixmap(QtGui.QPixmap(str(i[6])))
            newProUi.btnShow.clicked.connect(partial(self.getData, i[0]))
            self.addProductUi(newProUi, 0)

        
        
    def showAllAgain(self):

    
        self.cr.execute('''
            DELETE FROM ProductDimen WHERE remo=0
            ''')
        self.db.commit()
        self.clearScreen()
        self.handelProductPage()


        
    def openImg(self, obj):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        obj.setText(str(filename[0]))

    def rightDime(self, remo):
        
        dimens = self.cr.execute('''
            SELECT * FROM ProductDimen ORDER BY id DESC LIMIT 1;
        ''').fetchall()  

        if len(dimens) == 0:
            self.cr.execute('''
                INSERT INTO ProductDimen (one, two, three, four, remo)  VALUES({}, {}, {}, {}, {})
            '''.format(0, 2, 1, 1, remo))
            self.db.commit()
            return [0, 2, 1, 1, remo]


        else:
            arr = []
            for i in dimens[0][1:]:
                arr.append(i)
            if arr[1] == 0:
                arr[0] += 1
                arr[1]  = 2
            else:
                arr[1] -= 1

            self.cr.execute('''
                INSERT INTO ProductDimen (one, two, three, four, remo)  VALUES({}, {}, {}, {}, {})
            '''.format(arr[0], arr[1], arr[2], arr[3], remo))
            self.db.commit()
            
            return arr
            

    def getData(self, var):
        fromData = self.cr.execute('''
                SELECT * FROM Product WHERE id={}
        '''.format(var)).fetchall()
        
        self.lineEdit_12.setText(fromData[0][1])
        self.lineEdit_13.setText(str(fromData[0][4]))
        self.lineEdit_9.setText(str(fromData[0][3]))
        self.lineEdit_10.setText(str(fromData[0][2]))
        self.lineEdit_11.setText(fromData[0][5])
        self.label_8.setText(str(fromData[0][0]))
        self.label_3.setPixmap(QtGui.QPixmap(str(fromData[0][6])))
        self.tabWidget.setCurrentIndex(4)

    
    def handelProductPage(self):

        allProductData = self.cr.execute('SELECT * FROM Product').fetchall()
        allLayoutData  = self.cr.execute('SELECT * FROM ProductDimen').fetchall()
    
        for i in range(len(allProductData)):
            newProUi = createProduct()
            newProUi.name.setText(allProductData[i][1])
            newProUi.image.setPixmap(QtGui.QPixmap(str(allProductData[i][6])))
            newProUi.btnShow.clicked.connect(partial(self.getData, allProductData[i][0]))
            self.gridLayout_2.addWidget(
                newProUi.heroLay, 
                allLayoutData[i][1], 
                allLayoutData[i][2], 
                allLayoutData[i][3], 
                allLayoutData[i][4])
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        

    def getDataFromAdd(self):
        name = self.lineEdit.text()
        goldType = self.comboBox_5.currentText()
        qty = self.lineEdit_4.text()
        size = self.lineEdit_5.text()
        hala = self.comboBox_6.currentText()
        img  = self.label_5.text()
        self.addProduct(name, size, qty, goldType, hala, img)


    def addProduct(self, *args):

        # Get Data From Ui 
        

        # Insert Data Into DataBase
        self.cr.execute('''
            INSERT INTO Product(name, size, number, goldType, hala, img)
            VALUES("{}", {}, {}, {}, "{}", "{}")
        '''.format(args[0], args[1], args[2], args[3], args[4], args[5]))


        self.cr.execute('''
        
            INSERT INTO daily(grams) VALUES({})
        '''.format(args[1]))

        data = self.cr.execute('''
            SELECT name, id FROM Product ORDER BY id DESC LIMIT 1;
            
        ''').fetchone()


        self.lineEdit.setText("")
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.comboBox_6.setCurrentIndex(0)
        


        ######################################3
        
        newProUi = createProduct()
        newProUi.name.setText(data[0][0])
        newProUi.image.setPixmap(QtGui.QPixmap(str(args[5])))

        self.db.commit()
        
        newProUi.btnShow.clicked.connect(partial(self.getData, data[0][1]))
        self.displayProduct()
        self.addProductUi(newProUi, 1)
        self.label_5.setText("")

        self.dayEnd()


    def addProductUi(self, createdProduct, remo):
        pos = self.rightDime(remo)
        self.gridLayout_2.addWidget(createdProduct.heroLay, pos[0], pos[1], pos[2], pos[3])
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def editProduct(self):
        name = self.lineEdit_12.text()
        size = self.lineEdit_10.text()
        goldType = self.lineEdit_13.text()
        qty = self.lineEdit_9.text()
        hala = self.lineEdit_11.text()
        img = self.label_7.text()
        id_ = self.label_8.text()
        if img == '':
            query = self.cr.execute('''
                UPDATE Product SET name="{}", size={}, number={}, 
                goldType={}, hala="{}" WHERE id={};
            '''.format(name, size, goldType, qty, hala, id_))
        else:
            query = self.cr.execute('''
                UPDATE Product SET name="{}", size={}, number={}, 
                goldType={}, hala="{}", img="{}" WHERE id={};
            '''.format(name, size, goldType, qty, hala, img, id_))
        self.db.commit()
        self.deleteFromUi()
        self.openEditProduct()

    def deleteProduct(self, altId=0):
        tmp = ''
        if altId == 0:
           tmp = self.label_8.text()

        else:
            tmp = altId

        sqlQuery = '''DELETE FROM Product WHERE id={}'''.format(tmp)
        sqlQuery2= '''DELETE FROM ProductDimen WHERE id={}'''.format(tmp)
        
        self.cr.execute(sqlQuery)
        self.cr.execute(sqlQuery2)

        
            
        self.db.commit()
        self.displayProduct()
        self.deleteFromUi()
        
        if altId == 0:
            self.openEditProduct()

    def deleteFromUi(self):
        self.clearScreen()
        self.handelProductPage()



    def clearScreen(self):
        for i in self.findChildren(QtWidgets.QGroupBox):
            i.setParent(None)

    def dayEnd(self):
        
        self.cr.execute('SELECT cost FROM mape WHERE typeofwork="بيع"')
        win = self.cr.fetchall() #  self.label_68
        
        self.cr.execute('SELECT cost FROM mape WHERE typeofwork="شراء"')
        buy = self.cr.fetchall() #  self.label_72
        

        self.cr.execute('SELECT grams FROM daily;')
        grams = self.cr.fetchall() #  self.label_14
        

        self.cr.execute('SELECT size FROM dameged')
        damGrams = self.cr.fetchall() #  self.label_32
        
         
        self.handelDayEnd(win, self.label_68)
        self.handelDayEnd(buy, self.label_72)
        self.handelDayEnd(grams, self.label_14)
        self.handelDayEnd(damGrams, self.label_32)
       

    def handelDayEnd(self, fildItr, dist):
        if fildItr == []:
            return
        else:
            sumOfItr = 0.0
            for i in fildItr:
                sumOfItr += i[0]
        
            if str(sumOfItr).split('.')[1] == '0':
                dist.setText(str(int(sumOfItr)))
            else:
                dist.setText(str(sumOfItr))


    
        

    def displayProduct(self):
        self.comboBox_4.clear()
        self.comboBox_4.addItem('--------------')
        self.cr.execute('''SELECT name FROM Product;''')
        data = self.cr.fetchall()
        
        for one in data:
            self.comboBox_4.addItem("         "+one[0])


    def dailyWork(self):
        time = datetime.datetime.now()
        pro = self.comboBox_4.currentIndex()
        size = self.lineEdit_2.text()
        qty = self.lineEdit_3.text()
        price = self.lineEdit_8.text()

        if size == '' or qty == '' or price == '' or pro == 0:
            QMessageBox.information(self,'خطأ', 'لقد نسيت احد المعلومات برجاء التأكد من اكمال عملية ادخال المعلومات')
            return

        size = float(size)
        qty = int(qty)

        

        self.cr.execute('''
            SELECT * FROM Product WHERE id={};
        '''.format(pro))

        data = self.cr.fetchall()


        if size > data[0][2] or qty > data[0][3]:
            QMessageBox.information(self, 'خطأ', 'الكمية الحالية لا تكفي رجاء المحاولة مره اخري مع  التأكد من صحة البيانات ')
            return
    

        if data[0][2] - size == 0.0:
            #QMessageBox.information('خطأ', '')
            self.deleteProduct(data[0][0])
            
        fGrams = data[0][2] - size

        self.cr.execute('''
            INSERT INTO Mape(name, size, goldType, qty, hala, cost, date, typeofwork) 
            VALUES          ("{}", {}, {}, {}, "{}", {}, "{}", "بيع")
        '''.format(
                data[0][1],
                size,
                data[0][4],
                qty,
                data[0][5],
                float(price)*int(qty),
                "{}:{}:{}".format(datetime.date.today(), time.hour, time.minute)))

        self.cr.execute('''
            UPDATE product SET size={}, number={} WHERE id={}; 
        '''.format( fGrams, data[0][3] - qty, pro))

        self.cr.execute('''
            UPDATE daily SET grams={} WHERE id={}
        '''.format(fGrams, pro)) 

        self.comboBox_4.setCurrentIndex(0)
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_8.setText("")

        self.db.commit()
        self.displayDailyWork(self.tableWidget)
        self.dayEnd()


    def tableDetails(self):
        self.displayDailyWork(self.tableWidget_3, 2, self.comboBox_3.currentIndex())


    def handelDate(self, date):
        data = str(date).split('/')
        return '-'.join([str(datetime.datetime.now().year), data[0], data[1]])



    def handelQuery(self, select, q1="", q2="", q3="", q4=""):

        sqlCaseOne   = "SELECT name, size, goldType, qty, hala, cost, date FROM Mape {}".format(q1)

        sqlCaseTwo   = "SELECT name, size, goldType, qty, hala, cost, date FROM Mape WHERE typeofwork='بيع' {}".format(q2)

        sqlCaseThree = "SELECT name, size, goldType, qty, hala, cost, date FROM Mape WHERE typeofwork='شراء' {}".format(q3)

        sqlCaseFour  = "SELECT name, size, goldType, qty, hala, price, date FROM dameged {}".format(q4)


        if select == 0:
            self.cr.execute(sqlCaseOne)
        elif select == 1:
            self.cr.execute(sqlCaseTwo)
        elif select == 2:
            self.cr.execute(sqlCaseThree)
        elif select == 3:
            self.cr.execute(sqlCaseFour)

      

    def displayDailyWork(self, table, any_=1, select=0):
        time = datetime.datetime.now()

        today = datetime.date.today()

        nextDate = today + datetime.timedelta(days=1)
        
        today = str(today)

        date1 = self.dateEdit.text()
        date2 = self.dateEdit_2.text()


        table.setRowCount(0)
        table.insertRow(0)

        ff = "date BETWEEN '{}' AND '{}' ".format(self.handelDate(date1), self.handelDate(date2))
        
        if any_ == 2:
            if self.handelDate(date1) == today and self.handelDate(date2) == today: 
                self.handelQuery(select)
            else:
                # self.handelQuery(select)
                self.handelQuery(select,"WHERE "+ff, "AND "+ff, "AND "+ff, "WHERE "+ff)

        else:
            # self.handelQuery(select)
            self.cr.execute('''
                SELECT name, size, goldType, qty, hala, cost, typeofwork, date FROM Mape WHERE date BETWEEN '{}' AND '{}'
            '''.format(today, nextDate))

        proData = self.cr.fetchall()
        if proData == []:
            pass
        else: 
            for row, form in enumerate(proData):
                for col, item in enumerate(form):
                    table.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                rowLoc = table.rowCount()
                table.insertRow(rowLoc)
            table.removeRow(rowLoc)
            # if proData[0][6] == 2:
            #     table.setItem(0, 6, QTableWidgetItem('"شراء"'))
            # else:
            #     table.setItem(0, 6, QTableWidgetItem('"بيع"'))


    def baymentProduct(self):
        time = datetime.datetime.now()
        name = self.lineEdit_25.text()
        goldType = self.comboBox_13.currentText()
        qty = self.lineEdit_27.text()
        size = self.lineEdit_26.text()
        price = self.lineEdit_28.text()
        hala = self.comboBox_15.currentText()
        whereToGo = self.comboBox_14.currentIndex()

        self.cr.execute('''
            INSERT INTO Mape(name, size, goldType, qty, hala, cost, date, typeofwork) 
            VALUES("{}", {}, {}, {}, "{}", {}, "{}", "شراء")
        '''.format(
                name,
                size,
                goldType, 
                qty, 
                hala, 
                float(price)*int(qty),  
                "{}:{}:{}".format(datetime.date.today(),time.hour, time.minute)))

        if whereToGo == 1:
            self.addProduct(name, size, qty, goldType, hala,'img/download.png')
        else:
            self.cr.execute('''
            
                INSERT INTO dameged(name, size, qty, price, hala, wheretogo, goldtype, date)
                VALUES("{}", {}, {}, {}, "{}", {}, "{}", "{}")

            '''.format(name, size, qty, price, hala, whereToGo, goldType,"{}:{}:{}".format(datetime.date.today(),time.hour, time.minute)))

            self.label_32.setText(size) #####################################################

        self.db.commit()

        self.displayDailyWork(self.tableWidget)

        self.lineEdit_25.setText("")
        self.comboBox_13.setCurrentIndex(0)
        self.lineEdit_27.setText("")
        self.lineEdit_26.setText("")
        self.lineEdit_28.setText("")
        self.comboBox_15.setCurrentIndex(0)
        self.comboBox_14.setCurrentIndex(0)



    # Open System Screens   

    def openEditProduct(self):
        self.tabWidget.setCurrentIndex(3)

    def openProductScreen(self):
        self.tabWidget.setCurrentIndex(1)

    def openMainScreen(self):
        self.tabWidget.setCurrentIndex(0)

    def openBaymentScreen(self):
        self.tabWidget.setCurrentIndex(2)

    def openDayEnd(self):
        self.tabWidget.setCurrentIndex(5)

    def openDital(self):
        self.tabWidget.setCurrentIndex(6)
    

    
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
	main()


