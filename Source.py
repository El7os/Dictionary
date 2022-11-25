import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
deneme = list(range(100))
aslı = []
for i in deneme:
    aslı.append(str(i))

def veriçek():
    con = sqlite3.connect("Veri.db")
    imleç = con.cursor()
    imleç.execute("CREATE TABLE IF NOT EXISTS Veri(Başlık TEXT,İçerik TEXT)")
    con.commit()
    try:
        a = imleç.execute("Select * From Veri")
        sözlük = {}
        for i,j in a:
            if i.strip(" ") == "" or j.strip(" ") == "":
                continue
            sözlük[i] = j
        con.close()
        return sözlük
    except:
        return {}



def veri_güncelle(isim,değişim,yeni):
    con = sqlite3.connect("Veri.db")
    imleç = con.cursor()
    imleç.execute("Update Veri set {} = '{}' where Başlık = '{}'".format(değişim,yeni,isim))
    con.commit()
    con.close()

def veri_sil(isim):
    con = sqlite3.connect("Veri.db")
    imleç = con.cursor()
    imleç.execute("Delete from Veri where Başlık = '{}'".format(isim))
    con.commit()
    con.close()
def veri_ekle(başlık,içerik):
    con = sqlite3.connect("Veri.db")
    imleç = con.cursor()
    imleç.execute("Insert into Veri Values(?,?)", (başlık,içerik))
    con.commit()
    con.close()

class Arama_sayfa(QWidget):
    def __init__(self):
        super().__init__()
        self.harfler = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W",
                        "X","Y","Z",""]
        self.initui()

    def initui(self):
        self.a = 0
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        for i in self.harfler:
            if i == "":
                continue
            if i == "J":
                self.a += 1
            if i == "R":
                self.a += 1
            if self.a == 0:
                self.i = QPushButton(i)
                self.i.clicked.connect(self.func)
                h1.addWidget(self.i)
            if self.a == 1:
                self.i = QPushButton(i)
                self.i.clicked.connect(self.func)
                h2.addWidget(self.i)
            if self.a == 2:
                self.i = QPushButton(i)
                self.i.clicked.connect(self.func)
                h3.addWidget(self.i)



        v_box = QVBoxLayout()

        v_box.addLayout(h1)
        v_box.addLayout(h2)

        v_box.addLayout(h3)



        self.setLayout(v_box)

    def func(self):
        self.gönderen = self.sender().text()
        lays = arama_sonuç(self.gönderen)
        Ana_sayfa.setCentralWidget(m,lays)









class Kelime_ekle(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()


    def initui(self):
        self.kelimestr = QLabel("Kelimeyi girininiz: ")
        self.kelimeiç = QLineEdit()
        self.içerikstr = QLabel("İçeriği giriniz:       ")
        self.içerikiç = QTextEdit()
        self.ekle = QPushButton("Ekle")


        self.ekle.clicked.connect(self.ekleme)


        h_1 = QHBoxLayout()

        h_1.addWidget(self.kelimestr)
        h_1.addWidget(self.kelimeiç)
        h_1.addWidget(self.ekle)

        h_2 = QHBoxLayout()
        h_2.addWidget(self.içerikstr)
        h_2.addWidget(self.içerikiç)

        v = QVBoxLayout()
        v.addLayout(h_1)
        v.addLayout(h_2)
        self.setLayout(v)


    def ekleme(self):
        self.başlık = self.kelimeiç.text()
        baş = self.başlık[0]
        baş = baş.upper()
        self.başlık = self.başlık[1:]
        self.başlık = baş + self.başlık

        self.iç = self.içerikiç.toPlainText()
        self.kelimeiç.clear()
        self.içerikiç.clear()
        veri_ekle(self.başlık,self.iç)
        a = Arama_sayfa()
        Ana_sayfa.setCentralWidget(m,a)







class arama_sonuç(QWidget):
    def __init__(self,a):
        super().__init__()
        self.initui(a)

    def initui(self,a):
        self.üstb = QLabel("--------------{}--------------".format(a))
        self.üstb.setFont(QFont("Constantia",16))
        self.aram = QScrollArea()


        b = veriçek()
        form = QFormLayout()
        for i in b.keys():
            if i.startswith(a):

                self.i = QPushButton(i)
                self.i.clicked.connect(self.k)
                form.addRow(self.i)
        g = QGroupBox()
        g.setLayout(form)
        self.aram.setWidgetResizable(True)
        self.aram.setWidget(g)
        v = QVBoxLayout()
        v.addWidget(self.üstb)
        v.addWidget(self.aram)
        self.setLayout(v)
    def k(self):
        s = self.sender().text()
        sa = SonS(s)
        Ana_sayfa.setCentralWidget(m,sa)




class SonS(QWidget):
    def __init__(self,isim):
        super().__init__()
        self.isin = isim
        self.ad(isim)

    def ad(self,isim):
        veri = veriçek()
        self.içerik1 = veri[isim]
        self.başlık = QLineEdit()
        self.başlık.setText(isim)
        self.ad = isim
        self.adış = veri[isim]

        self.içerik = QTextEdit()
        self.içerik.setText(self.içerik1)
        self.güncelle = QPushButton("Güncelle")
        self.sil = QPushButton("Sil")
        self.etiket = QLabel("LUDOS™")
        self.güncelle.clicked.connect(self.guncel)
        self.sil.clicked.connect(self.Sil)
        h1 = QHBoxLayout()
        h1.addWidget(self.başlık)
        h1.addWidget(self.güncelle)
        h1.addWidget(self.sil)

        h2 = QHBoxLayout()
        h2.addStretch()
        h2.addWidget(self.etiket)

        v = QVBoxLayout()
        v.addLayout(h1)
        v.addWidget(self.içerik)
        v.addLayout(h2)

        self.setLayout(v)
    def Sil(self):

        veri_sil(self.isin)
        a = Arama_sayfa()
        Ana_sayfa.setCentralWidget(m, a)
    def guncel(self):
        isim = self.başlık.text()
        içerik = self.içerik.toPlainText()
        veri_güncelle(self.ad,"Başlık",isim)
        veri_güncelle(isim,"İçerik",içerik)
        a = Arama_sayfa()
        Ana_sayfa.setCentralWidget(m,a)

class Ana_sayfa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arama = Arama_sayfa()

        self.ada()

    def ada(self):
        self.setGeometry(500, 200, 300, 600)
        self.setWindowIcon(QIcon("Icons/dict.jpg"))
        menü = self.menuBar()
        veri_ekle = QAction("Kelime ekle",self)
        veri_bul = QAction("Kelime bul",self)

        menü.addAction(veri_bul)
        menü.addAction(veri_ekle)

        veri_bul.triggered.connect(self.zahit)
        veri_ekle.triggered.connect(self.zahit)




        self.setMenuBar(menü)
        self.setWindowTitle("Sözlük")
        self.setCentralWidget(self.arama)
        self.show()
    def zahit(self):
        self.göndere = self.sender()
        self.gönderen = self.göndere.text()
        if self.gönderen == "Kelime ekle":
            self.kel = Kelime_ekle()
            self.setCentralWidget(self.kel)
        if self.gönderen == "Kelime bul":
            self.keli = Arama_sayfa()
            self.setCentralWidget(self.keli)


app = QApplication(sys.argv)
m = Ana_sayfa()
sys.exit(app.exec_())





