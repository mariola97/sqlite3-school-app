from tkinter import *
from sqlite3 import *
class Nastavnik: #definicija klase nastavnik s atributima iz baze
    def __init__(self, oib, ime, prezime, adresa):
        self.O = oib
        self.I = ime
        self.P = prezime
        self.A = adresa
        return
    def __repr__(self):  #__repr__ -> specijalna metoda za prikaz klase u obliku stringa
        return '{} {}'.format(self.I, self.P)
class Odjeljenje: #definicija klase odjeljenje
    def __init__(self, ID, naziv, razrednik):
        self.ID = ID
        self.N = naziv
        self.R = razrednik
        return
class Ucenik: #definira objekte učenika
    def __init__(self, oib, ime, prezime, adr, datR, odj):
        self.O = oib
        self.I = ime
        self.P = prezime
        self.D = datR
        self.A = adr
        self.R = odj
        self.IP = self.I + ' ' + self.P
        return
    def __repr__(self):
        s = 'Ime i prezime:{} OIB:({})'.format(self.IP, self.O)
        s += '\nAdresa: ' + self.A
        s += '\nRazred: {}'.format(self.R.N)
        s +='\nRazrednik:{}'.format(self.R.R)
        return s
class Trazi(Frame): #klasa u kojoj će se izvršiti inicijalizacija sučelja
    def __init__(self, root):
        self.R = root
        super().__init__(self.R)
        self.R.title('Pretraživanje učenika')
        self.grid(rows = 2, columns = 2)
        self.kreirajSucelje()
        return
    def kreirajSucelje(self): #stvara se sučelje 
        f = ('Calibri', 14, 'bold')
        self.S = Entry(self,font =f, bg ='white', fg = 'black') #polje za unos teksta
        self.S.grid(row = 0, column = 0)
        self.S.bind('<KeyPress-Return>', self.trazi)
        self.L = Listbox(self, font = f) #prikaz rezultata pretraživanja
        self.L.grid(row = 1, column = 0, rowspan = 3)
        self.L.bind('<<ListboxSelect>>', self.ucitajUcenika)
        self.T=Text(self,width=50,height=12,font=f,fg='black') #prikaz detalja o učeniku
        self.T.grid(row = 0, column = 1, rowspan = 2)
        return
    def trazi(self, e):  #metoda pokreće upit u bazu podataka pritiskom tipke enter
        conn = connect('skola.db')
        c = conn.cursor()
        upit = '''SELECT * 
                    FROM učenici, nastavnici, razredi
                    WHERE učenici.Razred = razredi.ID AND 
                    nastavnici.OIB = razredi.razrednik  
                    AND (učenici.Ime LIKE "{0}%" OR učenici.Prezime LIKE "{0}%") 
                    ORDER BY Prezime ASC'''.format(self.S.get()) #upit koji pretražuje učenike te na temeljlu unesenog teksta prikazuje rezultate
        self.U = []
        self.L.delete(0, END)
        for t in c.execute(upit): #iteracija rezultata izvršenjem sql upita
            r = Nastavnik(t[6], t[7], t[8], t[9]) #stvara se objekt r, a za svaki rezultat t uzimaju se podaci uz nastavnika na pozicijama 6,7,8,9
            o = Odjeljenje(t[10], t[11], r) #objekt o, podaci za odjeljenje se nalaze na pozicijama 10 i 11 te objekt r
            u = Ucenik(t[0], t[1], t[2], t[3], t[4], o) #objekt u, a podaci na pozicijama 01,2,3,4, te objekt o
           
            self.U.append(u) #podaci se dodaju u listu self.U
            self.L.insert(END, u.IP) #ime i prezime se doda u listbox na ispisu
        conn.close()
        return
    def ucitajUcenika(self, e): #metoda odgovorna za prikaz detalja o učeniku
        t = self.L.curselection()
        t = int(t[0])
        u = self.U[t]
        self.T.delete(0.0, END)
        self.T.insert(END, u) #podaci o odabranom učenuku se dodaju u textbox
        return
root = Tk()
app = Trazi(root)
root.mainloop()
