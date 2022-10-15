import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox



conn = sql.connect("C:\\Users\\Batuhan\\PycharmProjects\\python\\veritabanı\\sarki.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS sarkilar (ID INTEGER PRIMARY KEY, Sarkiismi TEXT , Sanatci TEXT, Albüm TEXT, Prodüksiyon_Sirketi TEXT,Sarki_Süresi INTEGER , CikisTarih YEAR )")


# =============================================#


tiklama= False
def tümveri(satir):
    trv.delete(*trv.get_children())
    for dt in satir:
        trv.insert("", 'end', values=dt)






def temizle():

    cursor.execute("SELECT * FROM sarkilar")
    satir = cursor.fetchall()
    tümveri(satir)
    sarkientry.delete(0, 'end')
    sanactientry.delete(0, 'end')
    albümentry.delete(0, 'end')
    prodentry.delete(0, 'end')
    sarkisüreentry.delete(0, 'end')
    sarkitarihentry.delete(0, 'end')



def sarkiara():
    sarkiarama1 = arama.get()
    cursor.execute(
        "SELECT * FROM sarkilar WHERE Sarkiismi LIKE '" + sarkiarama1 + "%' OR Sanatci LIKE '" + sarkiarama1 + "%' ")
    satir = cursor.fetchall()
    tümveri(satir)
    conn.commit()


def veriekle():
    hatabul()
    if hatadurum == False:
        Sarkiismi = sarkiad.get()
        Sanatci = sanactiad.get()
        Albüm = albümad.get()
        Prodüksiyon_Sirketi = proad.get()
        Sarki_Süresi = sarkisüre.get()
        CikisTarih = sarkitarih.get()

        cursor.execute("Select Max(Id) From sarkilar")
        kimlik = cursor.fetchone()[0]
        if kimlik == None:
            cursor.execute("INSERT INTO sarkilar  VALUES({},'{}','{}','{}','{}',{},{});"
                           .format(1, Sarkiismi, Sanatci, Albüm, Prodüksiyon_Sirketi, Sarki_Süresi, CikisTarih))
            conn.commit()
        else:
            cursor.execute("INSERT INTO sarkilar VALUES({},'{}','{}','{}','{}',{},{});"
                           .format(kimlik + 1, Sarkiismi, Sanatci, Albüm, Prodüksiyon_Sirketi, Sarki_Süresi,
                                   CikisTarih))
            conn.commit()
        temizle()
    else:
        pass

def bilgial(event):

    satirbilgi = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    sarkiad.set(item['values'][1])
    sanactiad.set(item['values'][2])
    albümad.set(item['values'][3])
    proad.set(item['values'][4])
    sarkisüre.set(item['values'][5])
    sarkitarih.set(item['values'][6])



def verigüncelle():
    try:
            item = trv.item(trv.focus())
            id = (item['values'][0])
            Sarkiismi = sarkiad.get()
            Sanatci = sanactiad.get()
            Albüm = albümad.get()
            Prodüksiyon_Sirketi = proad.get()
            Sarki_Süresi = sarkisüre.get()
            CikisTarih = sarkitarih.get()
            if messagebox.askyesno("Onayla", "Veriler Değiştirilicektir Onaylıyormusun?"):
                komut = "UPDATE sarkilar SET Sarkiismi=?,Sanatci=?,Albüm=?,Prodüksiyon_Sirketi=?,Sarki_Süresi=?,CikisTarih=? WHERE id=?"
                conn.execute(komut, (Sarkiismi, Sanatci, Albüm, Prodüksiyon_Sirketi, Sarki_Süresi, CikisTarih, id,))
                conn.commit()
                temizle()
    except:
        pass

def verisil():
    item = trv.item(trv.focus())
    id = (item['values'][0])
    if messagebox.askyesno("Şarkı Listeden Silenecek", "Emin Misin?"):
        conn.execute("DELETE FROM sarkilar WHERE id=" + str(id))
        conn.commit()
        temizle()
    else:
        pass


def sarkiSuresiToplam():
    cursor.execute("SELECT SUM(Sarki_Süresi) From sarkilar")
    sureTop = cursor.fetchall()[0][0]
    messagebox.showinfo("Toplam Şarkı Süresi", "Süre Toplamı: {} saniyedir.".format(sureTop))
    conn.commit()


def sarkiAdet():
    cursor.execute("SELECT COUNT(Sarki_Süresi) From sarkilar")
    sarkiAdet = cursor.fetchall()[0][0]
    messagebox.showinfo("Toplam Şarkı", "Toplam Şarkı: {} adet.".format(sarkiAdet))
    conn.commit()

def hatabul():
    global hatadurum
    hatadurum = False
    if len(sarkientry.get()) == 0 or len(albümentry.get()) == 0 or len(prodentry.get()) == 0 or len(
            sarkisüreentry.get()) == 0 or len(sarkitarihentry.get()) == 0 or len(sanactientry.get()) == 0:
        messagebox.showinfo("Hata", "Lütfen Boş Alan Bırakmayınız")
        hatadurum = True
    else:
        try:
            sarkisüre = int(sarkisüreentry.get())

        except:
            messagebox.showinfo("Hata", "Lütfen Şarkı Süresi Kısmına Sadece Rakam Giriniz")
            hatadurum = True
        try:
            sarkitarih = int(sarkitarihentry.get())
        except:
            messagebox.showinfo("Hata", "Lütfen Sadece Tarih Alanına Geçerli Bir Tarih Giriniz")
            hatadurum = True


# =============================================#

# =============================================#
pencere = tk.Tk()
pencere.title("Nesne Tabanlı Sql")

baslık = tk.Label(text="ZIMBA PYTHON TAKIMI \nSQLLITE3  ", font="Arial 20 bold")
baslık.place(x=140, y=35)
# =============================================#
# =============================================#
ayrim1 = LabelFrame(pencere, text="Şarkı Listesi", height=100, font="Arial 12 bold")
ayrim1.pack(fill="both", expand="no", side=RIGHT)
ayrim4 = LabelFrame(pencere, text="Ek İşlemler", height=100, font="Arial 10 bold")
ayrim4.pack(fill="both", expand="no", side=BOTTOM)
ayrim3 = LabelFrame(pencere, text="İşlemler", height=100, font="Arial 10 bold")
ayrim3.pack(fill="both", expand="no", side=BOTTOM)
ayrim2 = LabelFrame(pencere)
ayrim2.pack(fill="both", expand="no", side=BOTTOM)

# =============================================#
trv = ttk.Treeview(ayrim1, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=15)
trv.pack()
# =============================================#
trv.column(1, width=100, minwidth=100)
trv.column(2, width=120, minwidth=120)
trv.column(3, width=120, minwidth=120)
trv.column(4, width=120, minwidth=120)
trv.column(5, width=120, minwidth=120)
trv.column(6, width=120, minwidth=120)
trv.column(7, width=120, minwidth=120)
# =============================================#
trv.heading(1, text="ID")
trv.heading(2, text="Şarkı İsmi")
trv.heading(3, text="Sanatçı")
trv.heading(4, text="Albüm")
trv.heading(5, text="Prodüksiyon Şirketi")
trv.heading(6, text="Şarkı Süresi")
trv.heading(7, text="Çıkış Tarihi")

trv.bind('<Double 1>', bilgial)



# =============================================#
arama = StringVar()

aramalabel = tk.Label(ayrim2, text="Şarkı Ara", font="Arial 12 bold")
aramalabel.grid(row=1, column=0, padx=5, pady=3)
aramaentry = tk.Entry(ayrim2, textvariable=arama, width=30)
aramaentry.grid(row=1, column=1, padx=5, pady=3)
aramabuton = tk.Button(ayrim2, text="Şarkıyı Bul", command=sarkiara, width=20, bg="green3", fg="white")
aramabuton.grid(row=1, column=2, padx=5, pady=3)
temizlebuton = tk.Button(ayrim2, text="Aramayı Temizle", command=temizle, width=20, bg="red2", fg="white")
temizlebuton.grid(row=1, column=3, padx=5, pady=3)
# =============================================#
sarkiad = StringVar()
sanactiad = StringVar()
albümad = StringVar()
proad = StringVar()
sarkisüre = IntVar()
sarkitarih = IntVar()

sarkiadlabel = tk.Label(ayrim3, text="Şarkı Adı", font="Arial 10 bold")
sarkiadlabel.grid(row=1, column=0, padx=5, pady=3)
sarkientry = tk.Entry(ayrim3, textvariable=sarkiad)
sarkientry.grid(row=1, column=1, padx=5, pady=3)

sanatciadlabel = tk.Label(ayrim3, text="Sanatçı Adı", font="Arial 10 bold")
sanatciadlabel.grid(row=1, column=2, padx=5, pady=3)
sanactientry = tk.Entry(ayrim3, textvariable=sanactiad)
sanactientry.grid(row=1, column=3, padx=5, pady=3)

albümlabel = tk.Label(ayrim3, text="Albüm Adı", font="Arial 10 bold")
albümlabel.grid(row=2, column=0, padx=5, pady=3)
albümentry = tk.Entry(ayrim3, textvariable=albümad)
albümentry.grid(row=2, column=1, padx=5, pady=3)

prodlabel = tk.Label(ayrim3, text="Prodüksiyon Adı", font="Arial 10 bold")
prodlabel.grid(row=2, column=2, padx=5, pady=3)
prodentry = tk.Entry(ayrim3, textvariable=proad)
prodentry.grid(row=2, column=3, padx=5, pady=3)

sarkisürelabel = tk.Label(ayrim3, text="Şarkı Süresi (Saniye) ", font="Arial 10 bold")
sarkisürelabel.grid(row=3, column=0, padx=5, pady=3)
sarkisüreentry = tk.Entry(ayrim3, textvariable=sarkisüre)
sarkisüreentry.grid(row=3, column=1, padx=5, pady=3)

sarkitarihlabel = tk.Label(ayrim3, text="Şarkı Çıkış Tarihi ", font="Arial 10 bold")
sarkitarihlabel.grid(row=3, column=2, padx=5, pady=3)
sarkitarihentry = tk.Entry(ayrim3, textvariable=sarkitarih)
sarkitarihentry.grid(row=3, column=3, padx=5, pady=3)

güncellebuton = tk.Button(ayrim3, text="Güncelle", command=verigüncelle, width=20, bg="green3", fg="white")
tümveributon = tk.Button(ayrim3, text="Tüm Veriyi Getir", command=temizle, width=20, bg="green3", fg="white")
eklebuton = tk.Button(ayrim3, text="Şarkı Ekle", command=veriekle, width=20, bg="green3", fg="white")
silbuton = tk.Button(ayrim3, text="Şarkı Sil", command=verisil, width=20, bg="red2", fg="white")

sarkiTopbuton = tk.Button(ayrim4, text="Toplam Şarkı Süresi ", command=sarkiSuresiToplam, width=20, bg="green3",
                          fg="white")
sarkiAdet = tk.Button(ayrim4, text="Toplam Şarkı Adet", command=sarkiAdet, width=20, bg="green3", fg="white")



eklebuton.grid(row=5, column=0, padx=5, pady=3)
güncellebuton.grid(row=5, column=2, padx=5, pady=3)
silbuton.grid(row=5, column=1, padx=5, pady=3)
tümveributon.grid(row=5, column=3, padx=5, pady=3)
sarkiAdet.grid(row=6, column=1, padx=5, pady=3)
sarkiTopbuton.grid(row=6, column=0, padx=5, pady=3)

# =============================================#


cursor.execute('SELECT * FROM sarkilar')
satir = cursor.fetchall()
tümveri(satir)

pencere.mainloop()
conn.close()