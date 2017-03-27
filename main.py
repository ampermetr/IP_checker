#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright 2016 Ampermetr <user@localhost>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import sys
import os
import time
import socket
from PyQt4 import QtGui, QtCore

from simple_thread import SimpleThread

server_sock = socket.socket()
server_sock.bind(('', 9090))
server_sock.listen(60)

class FormLayout(QtGui.QWidget):
    def load_file(self):
        
        self.lock = 1
        
        file = QtGui.QFileDialog().getOpenFileName(self, caption="Select file", directory="/home/user")
        current_file = open(file, "r")
        content_table = current_file.readlines()
        self.model.setRowCount(len(content_table))
        current_file.close()
        
        self.content = []
        x = 0
        
        for item in content_table:
            self.content.append(item.split("~", maxsplit=3))
        
        for item in self.content:
            name = QtGui.QStandardItem(item[0])
            ip = QtGui.QStandardItem(item[1])
            date = QtGui.QStandardItem(item[2])
            condition = QtGui.QStandardItem(item[3])
            
            self.model.setItem(x, 0, name)
            name.setEditable(False)
            self.model.setItem(x, 1, ip)
            ip.setEditable(False)
            self.model.setItem(x, 2, date)
            date.setEditable(False)
            self.model.setItem(x, 3, condition)
            condition.setEditable(False)
            
            x += 1
            
        self.crutch_1 = item[3].split("d")[1]
        
        self.lock = 0
            
    
    def save_file(self):
        
        self.lock = 1

        table = ""
        for x in range(0, self.model.rowCount()):
            for y in range(0, self.model.columnCount()):
                if y == 0:
                    table += self.model.data(self.model.index(x, y))
                else:
                    table += ("~" + self.model.data(self.model.index(x, y)))

        save_file = QtGui.QFileDialog.getSaveFileName(self, caption="Select file", directory="/home/user")
        file = open(save_file, "w")
        file.write(table)
        file.close()

        self.lock = 0
    
    def new(self):
        
        self.lock = 1
        
        ip, ok = QtGui.QInputDialog.getText(self, "Enter IP", "Введите IP пользователя")
        lock = 0
        
        if ok:
            for item in range(0, self.model.rowCount()):
                if ip == self.model.data(self.model.index(item, 1)):
                    lock = 1
                    result = QtGui.QMessageBox.question(self, "IP already exist", "Указанный IP уже существует, перезаписать?", \
                                                        buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
                    if result == 16384:
                        for x in range(0, self.model.columnCount()):
                            self.model.takeItem(item, x)
                        new_ip = QtGui.QStandardItem(ip)
                        self.model.setItem(item, 1, new_ip)
                        new_ip.setEditable(False) 
                        self.get_info(item, ip)
                
            if lock == 0:
                new_ip = QtGui.QStandardItem(ip)
                self.model.setItem(item, 1, new_ip)
                new_ip.setEditable(False)
                self.get_info(item, ip)
                
        self.lock = 0
                        
    
    def ping(self):
        
        self.lock = 1
        
        for item in range(0, self.model.rowCount()):
            ip = self.model.data(self.model.index(item, 1))
            try:
                self.get_info(item, ip)
            except Exception as trouble:
                condition = QtGui.QStandardItem("Disconnected" + self.crutch_1)
                self.model.takeItem(item, 3)
                self.model.setItem(item, 3, condition)
                condition.setEditable(False)
                print (str(trouble))
                
        self.lock = 0
    
    
    def get_info(self, length, ip):
        
        self.lock = 1
        
        addr = ip
        port = int(9091)

        sock = socket.socket()
        sock.connect((addr, port))
        sock.send(b"get info")
        while True:
            
            info = sock.recv(512)
            if not info:
                break
            sock.close()
                
            if info:
                name = QtGui.QStandardItem(info.decode('utf-8').split(" ", maxsplit=1)[0])
                date = QtGui.QStandardItem(info.decode('utf-8').split(" ", maxsplit=1)[1])
                condition = QtGui.QStandardItem("Connected" + self.crutch_1)
                
                self.model.takeItem(length, 0)
                self.model.setItem(length, 0, name)
                name.setEditable(False)
                self.model.takeItem(length, 2)
                self.model.setItem(length, 2, date)
                date.setEditable(False)
                self.model.takeItem(length, 3)
                self.model.setItem(length, 3, condition)
                condition.setEditable(False)
                break
            else:
                condition = QtGui.QStandardItem("Disconnected" + self.crutch_1)
                self.model.takeItem(length, 3)
                self.model.setItem(length, 3, condition)
                condition.setEditable(False)
        self.lock = 0
        
        return port
                
        
    @SimpleThread
    def bar(self):
        while True:
            self.setText(thr_method=None)


    def setText(self):
        temp = ""
        last_connect = ""

        while True:
            conn, addr = server_sock.accept()
    
            while True:
                data = conn.recv(2048)
                if not data:
                    break
        
                last_connect = data.decode("utf-8")
                if last_connect != temp:
                    if self.lock != 1:
                        self.lock = 1
                        for item in range(0, self.model.rowCount()):
                            if last_connect.split("~")[0] == self.model.data(self.model.index(item, 0)):
                                
                                    self.model.takeItem(item, 1)
                                    new_ip = QtGui.QStandardItem(last_connect.split("~")[1])
                                    self.model.setItem(item, 1, new_ip)
                                    self.model.takeItem(item, 2)
                                    date = QtGui.QStandardItem(last_connect.split("~")[2])
                                    self.model.setItem(item, 2, date)
                                    self.model.takeItem(item, 3)
                                    condition = QtGui.QStandardItem("Connected" + self.crutch_1)
                                    self.model.setItem(item, 3, condition)
                        temp = last_connect
                        self.time_label.setText("Last update at: " + time.ctime(time.time()))
                        self.lock = 0
                    else:
                        time.sleep(1)
                else:
                    time.sleep(1)
            conn.close()
            break
                                
        
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('grid layout')
        self.resize(445, 280)
        window = QtGui.QWidget()

        

        self.model = QtGui.QStandardItemModel(4,4)
        self.model.setHorizontalHeaderLabels(["Name", "IP", "Time", "Condition"])
        self.textEdit = QtGui.QTableView()
        self.textEdit.setModel(self.model)
        
        button1 = QtGui.QPushButton("&Oбновить")
        self.connect(button1, QtCore.SIGNAL('pressed()'), lambda: self.ping())
        button2 = QtGui.QPushButton("&Добавить")
        self.connect(button2, QtCore.SIGNAL('pressed()'), lambda: self.new())
        button3 = QtGui.QPushButton("&Сохранить в файл")
        self.connect(button3, QtCore.SIGNAL('pressed()'), lambda: self.save_file())
        button4 = QtGui.QPushButton("&Загрузить из файла")
        self.connect(button4, QtCore.SIGNAL('pressed()'), lambda: self.load_file())


        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(button1)
        hbox.addWidget(button2)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(button3)
        hbox1.addWidget(button4)
        hbox2 = QtGui.QHBoxLayout()
        self.time_label = QtGui.QLabel()
        hbox2.addWidget(self.time_label)
        
        self.form = QtGui.QFormLayout()
        self.form.addRow(self.textEdit)
        self.form.addRow(hbox)
        self.form.addRow(hbox1)
        self.form.addRow(hbox2)

        self.setLayout(self.form)
        
        self.lock = 0


        
app = QtGui.QApplication(sys.argv)
qb = FormLayout()
qb.show()
qb.bar(thr_start=True)
sys.exit(app.exec_())
