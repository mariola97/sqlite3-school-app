# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 00:25:36 2023

@author: Korisnik
"""
from tkinter import *
from tkinter.messagebox import *
from sqlite3 import *
class Program(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.R = root
        self.R.title('Novi učenik')
        self.grid(row = 5, column = 4)
        self.kreirajSucelje()
        return
    def kreirajSucelje(self): 
        f = ('Calibri', 16, 'bold') 
        Label(self, text = 'OIB', font = f, fg = 'black').grid(row = 0, column = 0)
        self.O = Entry(self, font = f, bg = 'white', fg = 'black')
        self.O.grid(row = 0, column = 1)
        Label(self, text='Datum rođenja', font = f,fg = 'black').grid(row = 0,column = 2)
        self.D = Entry(self, font = f, bg = 'white', fg = 'black')
        self.D.grid(row = 0, column = 3)
        Label(self, text = 'Ime', font = f, fg = 'black').grid(row = 1, column = 0)
        self.I = Entry(self, font = f, bg = 'white', fg = 'black')
        self.I.grid(row = 1, column = 1)
        Label(self, text = 'Prezime', font = f, fg = 'black').grid(row = 1, column = 2)
        self.P = Entry(self, font = f, bg = 'white', fg = 'black')
        self.P.grid(row = 1, column = 3)
        Label(self, text = 'Adresa', font = f, fg = 'black').grid(row = 2, column = 0)
        self.A = Text(self, width = 30, height = 10, font = f, bg = 'white', fg = 'black')
        self.A.grid(row = 3, column = 0, columnspan = 3)
        Label(self, text = 'Razred', font = f, fg = 'black').grid(row = 2, column = 3)
        self.L = Listbox(self, font = f, bg = 'white', fg = 'black')
        self.RA=self.ucitajRazrede()
        for t in self.RA:
            self.L.insert(END, t[1])
        self.L.grid(row = 3, column = 3)
        Button(self, text = 'Spremi', command=self.spremi, font = f, bg = 'white', fg = 'black').grid(row = 4, column = 0, columnspan = 4)
        return
    def ucitajRazrede(self):
        conn = connect('skola.db')
        c = conn.cursor()
        upit = 'SELECT * FROM razredi ORDER BY NAZIV ASC'
        r = []
        for t in c.execute(upit):
            r.append((t[0], t[1]))
        conn.close()
        return r
    def spremi(self):
        conn = connect('skola.db')
        c = conn.cursor()
        t = self.L.curselection()
        if len(t) > 0:
            upit = 'INSERT INTO učenici (OIB, Ime, Prezime, Adresa, Datum_rodjenja, Razred) VALUES (?, ?, ?, ?, ?, ?)'
            values = (self.O.get(), self.I.get(), self.P.get(), self.A.get(0.0, END), self.D.get(), self.RA[t[0]][0])
            c.execute(upit, values)
            conn.commit()
            showinfo('Novi učenik', 'Učenik je dodan')
            conn.close()
        else:
            showinfo('Novi učenik', 'Niste odabrali razredno odjeljenje')
        return

root = Tk()
app = Program(root)
root.mainloop()


