import csv
from csv import DictReader
import  sys
import subprocess
import os
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as ms
import prettytable
from prettytable import from_csv

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pdfkit

class inventory:
    def __init__(self, master):
        self.master=master
        self.username=StringVar()
        self.password=StringVar()
        self.s=StringVar()
        self.widgets()

    def widgets(self):

        self.head = Label(self.master, text='INVENTORY SYSTEM LOGIN', font=('Times New Roman', 35, 'bold'), pady=10, bg='powder blue', padx=50, bd=3, relief='ridge')
        self.head.pack(pady=100)
        self.logf = LabelFrame(self.master, width=1350, height=600, font=('Arial',20,'bold'), relief='ridge', bg='cadet blue', bd=20)

        Label(self.logf, text='Username: ', font=('Times New Roman', 15, 'bold'), pady=5, padx=5, bg='cadet blue', bd=5, relief='ridge', fg='Cornsilk').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.logf, textvariable=self.username, bd=5, font=('Times New Roman', 15), bg='#fdeaab').grid( row=0, column=1)

        Label(self.logf, text='Password: ', font=('Times New Roman', 15, 'bold'), pady=5, padx=5, bg='cadet blue', bd=5, relief='ridge', fg='Cornsilk').grid(sticky=W + E, pady=15, padx=10)
        Entry(self.logf, textvariable=self.password, bd=5, font=('Times New Roman', 15), show='*', bg='#fdeaab').grid(row=1, column=1)

        Button(self.logf, text=' Login ', bd=5, font=('Times New Roman', 15, 'bold'), padx=2, pady=5, bg='cadet blue', fg='Cornsilk', relief='raised' ,command=self.login).grid(pady=30)
        Button(self.logf, text=' Reset ', bd=5, font=('Times New Roman', 15, 'bold'), padx=2, pady=5, bg='cadet blue', fg='Cornsilk', command=self.resetting).grid(row=2, column=1, pady=30)

        self.logf.pack(pady=50)

        self.logf.pack(padx=100,pady=50)

    def login(self):

        logon=pd.read_csv('logdetails.csv')
        df = pd.DataFrame(logon, columns= ['Username','Password'])
        s1=self.username.get()
        s2=self.password.get()
        if(s1=="" and s2==""):
            ms.showerror('Try Again.......', 'Empty fields')
        ulist=logon['Username'].tolist()
        plist=logon['Password'].tolist()
        l=len(ulist)
        u="Invalid"
        p="Invalid"
        for i in range(l):
            if(s1==ulist[i] and s2==plist[i]):
                u=ulist[i]
                p=plist[i]
                break
            else:
                continue
        if(u==s1 and p==s2):
            self.logf.pack_forget()
            self.head.forget()
            self.logf.forget()
            self.openhome()
        elif(u=='Invalid' and p=='Invalid' and s1!='' and s2!=''):
            ms.showerror('Try Again.....', 'Invalid Credentials')

    def log(self):
        self.username.set('')
        self.password.set('')
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def resetting(self):
        self.username.set("")
        self.password.set("")

    def openhome(self):
        fields = []
        rows = []
        with open('items.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)

        self.canv=Canvas(self.master, borderwidth=0, bg='powder blue')
        self.v=Frame(self.canv, bg='powder blue')
        self.vsb=tk.Scrollbar(self.master, orient="vertical", command=self.canv.yview)
        self.canv.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canv.create_window((4,4), window=self.v, anchor="nw", tags="self.v")
        self.v.pack(side="top", fill="both", expand=True)
        self.canv.pack(side="left", fill="both", expand=True)
        self.v.bind("<Configure>", self.onFrameConfigure)


        Label(self.v, text=fields[0][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=0).grid(row=0, column=0, sticky=E + W)
        Label(self.v, text=fields[0][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=1, sticky=E + W)
        Label(self.v, text=fields[0][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=2, sticky=E + W)
        Label(self.v, text=fields[0][3], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=3, sticky=E + W)
        Label(self.v, text=fields[0][4], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=4, sticky=E + W)

        for i in range(len(rows)):
            Label(self.v, text=rows[i][0], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=0, sticky=E + W)
            Label(self.v, text=rows[i][1], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=1, sticky=E + W)
            Label(self.v, text=rows[i][2], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=2, sticky=E + W)
            Label(self.v, text=rows[i][3], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=3, sticky=E + W)
            Label(self.v, text=rows[i][4], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=4, sticky=E + W)

        # self.canv.create_window(0,0,window=self.v)
        # self.canv.config(self.master, yscrollcommand=scrollbar.set)
        # self.canv.pack()
        # photo1 = PhotoImage(file=r"splus.png")
        # photoimage=photo1.subsample(3,3)
        p1but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition1).place(x=1400, y=65)
        p2but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition2).place(x=1400, y=130)
        p3but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition3).place(x=1400, y=195)
        p4but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition4).place(x=1400, y=255)
        p5but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition5).place(x=1400, y=320)
        p6but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition6).place(x=1400, y=380)
        p7but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition7).place(x=1400, y=445)
        p8but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition8).place(x=1400, y=505)
        p9but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition9).place(x=1400, y=565)
        p10but = Button(self.v, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition10).place(x=1400, y=630)

        s1but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub1).place(x=1460, y=65)
        s2but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub2).place(x=1460, y=130)
        s3but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub3).place(x=1460, y=195)
        s4but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub4).place(x=1460, y=255)
        s5but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub5).place(x=1460, y=320)
        s6but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub6).place(x=1460, y=380)
        s7but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub7).place(x=1460, y=445)
        s8but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub8).place(x=1460, y=505)
        s9but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub9).place(x=1460, y=565)
        s10but = Button(self.v, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.sub10).place(x=1460, y=630)

        gen = Button(self.v, text=' Generate Report ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.generating).place(x=600, y=700)

        Entry(self.v, textvariable=self.s, bd=5, font=('Times New Roman', 15), bg='#fdeaab').place(x=1270, y=700)
        search = Button(self.v, text=' Search ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised', command=self.searching).place(x=1330, y=750)
        self.s.set('')

# fields = []
    # rows = []
    # with open('items.csv', 'r') as csvfile:
    #     csvreader = csv.reader(csvfile)
    #     for row in csvreader:
    #         fields.append(row)
    #         break
    #     for row in csvreader:
    #         rows.append(row)
    #
    # for i in range(len(rows)):
    #     def additioni(self):
    #         data = pd.read_csv("items.csv")
    #
    #         pi = data.iloc[i,3]
    #         pi=pi+1
    #         data.iloc[i,3]=pi
    #
    #         t1=data.iloc[i,4]
    #         c1=data.iloc[i,2]
    #         t1=c1*pi
    #         data.iloc[i,4]=t1
    #
    #         data["Sr. No."]=data["Sr. No."].astype(int)
    #         data["Cost"]=data["Cost"].astype(int)
    #         data["Quantity"]=data["Quantity"].astype(int)
    #         data["Total"]=data["Total"].astype(int)
    #         data.to_csv("items.csv", index=0)
    #         self.vsb.pack_forget()
    #         self.vsb.forget()
    #         self.v.pack_forget()
    #         self.canv.pack_forget()
    #         self.v.forget()
    #         self.canv.forget()
    #         self.openhome()
    #
    #     def subi(self):
    #         data = pd.read_csv("items.csv")
    #
    #         pi = data.iloc[i,3]
    #         pi=pi-1
    #         data.iloc[i,3]=pi
    #
    #         t1=data.iloc[i,4]
    #         c1=data.iloc[i,2]
    #         t1=c1*pi
    #         data.iloc[i,4]=t1
    #
    #         data["Sr. No."]=data["Sr. No."].astype(int)
    #         data["Cost"]=data["Cost"].astype(int)
    #         data["Quantity"]=data["Quantity"].astype(int)
    #         data["Total"]=data["Total"].astype(int)
    #         data.to_csv("items.csv", index=0)
    #         self.vsb.pack_forget()
    #         self.vsb.forget()
    #         self.v.pack_forget()
    #         self.canv.pack_forget()
    #         self.v.forget()
    #         self.canv.forget()
    #         self.openhome()

    def onFrameConfigure(self,event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))
    def addition1(self):
        data = pd.read_csv("items.csv")

        p1 = data.iloc[0,3]
        p1=p1+1
        data.iloc[0,3]=p1

        t1=data.iloc[0,4]
        c1=data.iloc[0,2]
        t1=c1*p1
        data.iloc[0,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition2(self):
        data = pd.read_csv("items.csv")

        p2 = data.iloc[1,3]
        p2=p2+1
        data.iloc[1,3]=p2

        t1=data.iloc[1,4]
        c1=data.iloc[1,2]
        t1=c1*p2
        data.iloc[1,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()


    def addition3(self):
        data = pd.read_csv("items.csv")

        p3 = data.iloc[2,3]
        p3=p3+1
        data.iloc[2,3]=p3

        t1=data.iloc[2,4]
        c1=data.iloc[2,2]
        t1=c1*p3
        data.iloc[2,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()


    def addition4(self):
        data = pd.read_csv("items.csv")

        p4 = data.iloc[3,3]
        p4=p4+1
        data.iloc[3,3]=p4

        t1=data.iloc[3,4]
        c1=data.iloc[3,2]
        t1=c1*p4
        data.iloc[3,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition5(self):
        data = pd.read_csv("items.csv")

        p5 = data.iloc[4,3]
        p5=p5+1
        data.iloc[4,3]=p5

        t1=data.iloc[4,4]
        c1=data.iloc[4,2]
        t1=c1*p5
        data.iloc[4,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition6(self):
        data = pd.read_csv("items.csv")

        p6 = data.iloc[5,3]
        p6=p6+1
        data.iloc[5,3]=p6

        t1=data.iloc[5,4]
        c1=data.iloc[5,2]
        t1=c1*p6
        data.iloc[5,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition7(self):
        data = pd.read_csv("items.csv")

        p7 = data.iloc[6,3]
        p7=p7+1
        data.iloc[6,3]=p7

        t1=data.iloc[6,4]
        c1=data.iloc[6,2]
        t1=c1*p7
        data.iloc[6,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition8(self):
        data = pd.read_csv("items.csv")

        p8 = data.iloc[7,3]
        p8=p8+1
        data.iloc[7,3]=p8

        t1=data.iloc[7,4]
        c1=data.iloc[7,2]
        t1=c1*p8
        data.iloc[7,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition9(self):
        data = pd.read_csv("items.csv")

        p9 = data.iloc[8,3]
        p9=p9+1
        data.iloc[8,3]=p9

        t1=data.iloc[8,4]
        c1=data.iloc[8,2]
        t1=c1*p9
        data.iloc[8,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def addition10(self):
        data = pd.read_csv("items.csv")

        p10 = data.iloc[9,3]
        p10=p10+1
        data.iloc[9,3]=p10

        t1=data.iloc[9,4]
        c1=data.iloc[9,2]
        t1=c1*p10
        data.iloc[9,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub1(self):
        data = pd.read_csv("items.csv")

        p1 = data.iloc[0,3]
        p1=p1-1
        data.iloc[0,3]=p1

        t1=data.iloc[0,4]
        c1=data.iloc[0,2]
        t1=c1*p1
        data.iloc[0,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub2(self):
        data = pd.read_csv("items.csv")

        p2 = data.iloc[1,3]
        p2=p2-1
        data.iloc[1,3]=p2

        t1=data.iloc[1,4]
        c1=data.iloc[1,2]
        t1=c1*p2
        data.iloc[1,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub3(self):
        data = pd.read_csv("items.csv")

        p3 = data.iloc[2,3]
        p3=p3-1
        data.iloc[2,3]=p3

        t1=data.iloc[2,4]
        c1=data.iloc[2,2]
        t1=c1*p3
        data.iloc[2,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub4(self):
        data = pd.read_csv("items.csv")

        p4 = data.iloc[3,3]
        p4=p4-1
        data.iloc[3,3]=p4

        t1=data.iloc[3,4]
        c1=data.iloc[3,2]
        t1=c1*p4
        data.iloc[3,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub5(self):
        data = pd.read_csv("items.csv")

        p5 = data.iloc[4,3]
        p5=p5-1
        data.iloc[4,3]=p5

        t1=data.iloc[4,4]
        c1=data.iloc[4,2]
        t1=c1*p5
        data.iloc[4,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub6(self):
        data = pd.read_csv("items.csv")

        p6 = data.iloc[5,3]
        p6=p6-1
        data.iloc[5,3]=p6

        t1=data.iloc[5,4]
        c1=data.iloc[5,2]
        t1=c1*p6
        data.iloc[5,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub7(self):
        data = pd.read_csv("items.csv")

        p7 = data.iloc[6,3]
        p7=p7-1
        data.iloc[6,3]=p7

        t1=data.iloc[6,4]
        c1=data.iloc[6,2]
        t1=c1*p7
        data.iloc[6,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub8(self):
        data = pd.read_csv("items.csv")

        p8 = data.iloc[7,3]
        p8=p8-1
        data.iloc[7,3]=p8

        t1=data.iloc[7,4]
        c1=data.iloc[7,2]
        t1=c1*p8
        data.iloc[7,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub9(self):
        data= pd.read_csv("items.csv")

        p9 = data.iloc[8,3]
        p9=p9-1
        data.iloc[8,3]=p9

        t1=data.iloc[8,4]
        c1=data.iloc[8,2]
        t1=c1*p9
        data.iloc[8,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def sub10(self):
        data = pd.read_csv("items.csv")

        p10 = data.iloc[9,3]
        p10=p10-1
        data.iloc[9,3]=p10

        t1=data.iloc[9,4]
        c1=data.iloc[9,2]
        t1=c1*p10
        data.iloc[9,4]=t1

        data["Sr. No."]=data["Sr. No."].astype(int)
        data["Cost"]=data["Cost"].astype(int)
        data["Quantity"]=data["Quantity"].astype(int)
        data["Total"]=data["Total"].astype(int)
        data.to_csv("items.csv", index=0)
        self.vsb.pack_forget()
        self.vsb.forget()
        self.v.pack_forget()
        self.canv.pack_forget()
        self.v.forget()
        self.canv.forget()
        self.openhome()

    def generating(self):

        elements = []
        path = 'C:/Users/hites/Documents'
        nm = "Inventory Report - " + ".pdf"
        x = os.path.join(path, nm)
        doc = SimpleDocTemplate(x, pagesize=letter)
        fields = []
        rows = []
        data = []
        with open('items.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
                break
            for row in csvreader:
                data.append(row)

        t = Table(data)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (4, 0), colors.blue),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ]))

        elements.append(t)
        doc.build(elements)
        os.startfile(x)

    def searching(self):
        st=(self.s.get())
        if(st==''):
            ms.showerror('Empty Search Field....', 'Please enter the item to be searched')

        st=st.lower()
        reading=pd.read_csv("items.csv")
        fields = []
        rows = []
        data = []
        s1=''
        s2=''
        with open('items.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)
        for i in range(len(rows)):
            reading=pd.read_csv("items.csv")
            s1=reading.iloc[i,1]
            s1=s1.lower()
            if(s1==st):
                s2=s1
                break
            else:
                continue
        if(s2==st and s2!=''):
            self.vsb.pack_forget()
            self.vsb.forget()
            self.v.pack_forget()
            self.canv.pack_forget()
            self.v.forget()
            self.canv.forget()
            self.v1=Frame(self.master, bg='powder blue')
            self.v1.pack(side="left", fill="both", expand=True)
            Label(self.v1, text=fields[0][0], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=0).grid(row=0, column=0, sticky=E + W)
            Label(self.v1, text=fields[0][1], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=1, sticky=E + W)
            Label(self.v1, text=fields[0][2], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=2, sticky=E + W)
            Label(self.v1, text=fields[0][3], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=3, sticky=E + W)
            Label(self.v1, text=fields[0][4], borderwidth=2, relief="raised", font=('Times New Roman', 15, 'bold'), bg='cadet blue', bd=5, pady=15, padx=20).grid(row=0, column=4, sticky=E + W)

            Label(self.v1, text=rows[i][0], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=0, sticky=E + W)
            Label(self.v1, text=rows[i][1], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=1, sticky=E + W)
            Label(self.v1, text=rows[i][2], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=2, sticky=E + W)
            Label(self.v1, text=rows[i][3], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=3, sticky=E + W)
            Label(self.v1, text=rows[i][4], borderwidth=2, relief="raised", font=('Times New Roman', 15), bg='cadet blue', bd=5, pady=15, padx=100).grid(row=i+1, column=4, sticky=E + W)

            back = Button(self.v1, text=' Back ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised', command=self.backing).place(x=700, y=150)
            a = Button(self.v1, text=' + ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.addition).place(x=1250, y=70)
            s = Button(self.v1, text=' - ', bd=5, font=('Times New Roman', 15, 'bold'), height=0, width=0, bg='sky blue', relief='raised' ,command=self.subtraction).place(x=1320, y=70)

        elif(s2!=st and st!=''):
            ms.showerror('Try Again.....', 'No Entry Found')

    def backing(self):
        self.v1.pack_forget()
        self.v1.forget()
        self.openhome()

    def addition(self):
        st=(self.s.get())
        st=st.lower()
        s1=''
        fields = []
        rows = []
        data = []
        with open('items.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)

        for i in range(len(rows)):
            reading=pd.read_csv("items.csv")
            s1=reading.iloc[i,1]
            s1=s1.lower()
            if(st==s1):
                j=i
                break
            else:
                continue
        reading=pd.read_csv("items.csv")

        p1 = reading.iloc[j,3]
        p1=p1+1
        reading.iloc[j,3]=p1

        t1=reading.iloc[j,4]
        c1=reading.iloc[j,2]
        t1=c1*p1
        reading.iloc[j,4]=t1

        reading["Sr. No."]=reading["Sr. No."].astype(int)
        reading["Cost"]=reading["Cost"].astype(int)
        reading["Quantity"]=reading["Quantity"].astype(int)
        reading["Total"]=reading["Total"].astype(int)
        reading.to_csv("items.csv", index=0)
        self.v1.pack_forget()
        self.v1.forget()
        self.searching()

    def subtraction(self):
        st=(self.s.get())
        st=st.lower()
        s1=''
        fields = []
        rows = []
        data = []
        with open('items.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fields.append(row)
                break
            for row in csvreader:
                rows.append(row)

        for i in range(len(rows)):
            reading=pd.read_csv("items.csv")
            s1=reading.iloc[i,1]
            s1=s1.lower()
            if(st==s1):
                j=i
                break
            else:
                continue
        reading=pd.read_csv("items.csv")

        p1 = reading.iloc[j,3]
        p1=p1-1
        reading.iloc[j,3]=p1

        t1=reading.iloc[j,4]
        c1=reading.iloc[j,2]
        t1=c1*p1
        reading.iloc[j,4]=t1

        reading["Sr. No."]=reading["Sr. No."].astype(int)
        reading["Cost"]=reading["Cost"].astype(int)
        reading["Quantity"]=reading["Quantity"].astype(int)
        reading["Total"]=reading["Total"].astype(int)
        reading.to_csv("items.csv", index=0)
        self.v1.pack_forget()
        self.v1.forget()
        self.searching()


root=tk.Tk()
root.config(bg='cadet blue')
root.attributes('-fullscreen', True)
root.bind("<Escape>", exit)
inventory(root)
root.mainloop()