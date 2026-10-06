import pyodbc
from database import baglanti_olustur


# -------------------------
# ÖĞRENCİ EKLE
# -------------------------

def ogrenci_ekle():
    numara = input("Öğrenci numarası: ")
    ad = input("Öğrenci adı: ")
    bolum = input("Bölüm: ")

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Ogrenciler (Numara, Ad, Bolum)
            VALUES (?, ?, ?)
            """,
            (numara, ad, bolum)
        )

        baglanti.commit()

        print("Öğrenci başarıyla eklendi!")

    except pyodbc.IntegrityError:
        print("Bu öğrenci numarası zaten kayıtlı.")

    finally:
        baglanti.close()

# -------------------------
# ÖĞRENCİLERİ LİSTELE
# -------------------------

def ogrencileri_listele():
    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Numara, Ad, Bolum
        FROM Ogrenciler
        """
    )

    ogrenciler = cursor.fetchall()
    baglanti.close()

    if not ogrenciler:
        print("Henüz öğrenci kaydı yok.")
        return

    print("\n--- Öğrenciler ---")

    for ogrenci in ogrenciler:
        print("Numara:", ogrenci[0])
        print("Ad:", ogrenci[1])
        print("Bölüm:", ogrenci[2])
        print("------------------")


# -------------------------
# ÖĞRENCİ ARA
# -------------------------

def ogrenci_ara():
    numara = input("Aramak istediğiniz öğrenci numarası: ")

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Numara, Ad, Bolum
        FROM Ogrenciler
        WHERE Numara = ?
        """,
        (numara,)
    )

    ogrenci = cursor.fetchone()
    baglanti.close()

    if ogrenci:
        print("\n--- Öğrenci Bilgileri ---")
        print("Numara:", ogrenci[0])
        print("Ad:", ogrenci[1])
        print("Bölüm:", ogrenci[2])
    else:
        print("Öğrenci bulunamadı.")


# -------------------------
# ÖĞRENCİ GÜNCELLE
# -------------------------

def ogrenci_guncelle():
    numara = input(
        "Bilgilerini güncellemek istediğiniz öğrencinin numarası: "
    )

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Ad, Bolum
        FROM Ogrenciler
        WHERE Numara = ?
        """,
        (numara,)
    )

    ogrenci = cursor.fetchone()

    if ogrenci is None:
        print("Bu numaraya sahip öğrenci bulunamadı.")
        baglanti.close()
        return

    print("\nMevcut bilgiler:")
    print("Ad:", ogrenci[0])
    print("Bölüm:", ogrenci[1])

    yeni_ad = input("Yeni ad: ")
    yeni_bolum = input("Yeni bölüm: ")

    cursor.execute(
        """
        UPDATE Ogrenciler
        SET Ad = ?, Bolum = ?
        WHERE Numara = ?
        """,
        (yeni_ad, yeni_bolum, numara)
    )

    baglanti.commit()
    baglanti.close()

    print("Öğrenci bilgileri başarıyla güncellendi.")


# -------------------------
# ÖĞRENCİ SİL
# -------------------------

def ogrenci_sil():
    numara = input("Silinecek öğrencinin numarası: ")

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Id, Ad
        FROM Ogrenciler
        WHERE Numara = ?
        """,
        (numara,)
    )

    ogrenci = cursor.fetchone()

    if ogrenci is None:
        print("Bu numaraya sahip öğrenci bulunamadı.")
        baglanti.close()
        return

    ogrenci_id = ogrenci[0]
    ogrenci_adi = ogrenci[1]

    cevap = input(
        f"{ogrenci_adi} adlı öğrenciyi silmek istediğinize "
        "emin misiniz? (e/h): "
    )

    if cevap.lower() != "e":
        print("Silme işlemi iptal edildi.")
        baglanti.close()
        return

    # Önce öğrencinin derslerini siliyoruz.
    cursor.execute(
        """
        DELETE FROM Dersler
        WHERE OgrenciId = ?
        """,
        (ogrenci_id,)
    )

    # Daha sonra öğrenciyi siliyoruz.
    cursor.execute(
        """
        DELETE FROM Ogrenciler
        WHERE Id = ?
        """,
        (ogrenci_id,)
    )

    baglanti.commit()
    baglanti.close()

    print("Öğrenci ve dersleri başarıyla silindi.")


# -------------------------
# DERS VE NOT EKLE
# -------------------------

def ders_ekle():
    numara = input("Ders eklenecek öğrencinin numarası: ")
    ders_adi = input("Ders adı: ")

    while True:
        try:
            vize = float(input("Vize notu: "))

            if 0 <= vize <= 100:
                break

            print("Vize notu 0 ile 100 arasında olmalıdır.")

        except ValueError:
            print("Lütfen sayısal bir değer girin.")

    while True:
        try:
            final = float(input("Final notu: "))

            if 0 <= final <= 100:
                break

            print("Final notu 0 ile 100 arasında olmalıdır.")

        except ValueError:
            print("Lütfen sayısal bir değer girin.")

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Id
        FROM Ogrenciler
        WHERE Numara = ?
        """,
        (numara,)
    )

    ogrenci = cursor.fetchone()

    if ogrenci is None:
        print("Bu numaraya sahip öğrenci bulunamadı.")
        baglanti.close()
        return

    ogrenci_id = ogrenci[0]

    cursor.execute(
        """
        INSERT INTO Dersler (OgrenciId, DersAdi, Vize, Final)
        VALUES (?, ?, ?, ?)
        """,
        (ogrenci_id, ders_adi, vize, final)
    )

    baglanti.commit()
    baglanti.close()

    print("Ders ve notlar başarıyla eklendi!")


# -------------------------
# HARF NOTU HESAPLA
# -------------------------

def harf_notu_hesapla(ortalama):
    if ortalama >= 90:
        return "AA"
    elif ortalama >= 85:
        return "BA"
    elif ortalama >= 80:
        return "BB"
    elif ortalama >= 75:
        return "CB"
    elif ortalama >= 70:
        return "CC"
    elif ortalama >= 65:
        return "DC"
    elif ortalama >= 60:
        return "DD"
    elif ortalama >= 50:
        return "FD"
    else:
        return "FF"


# -------------------------
# NOTLARI GÖSTER
# -------------------------

def notlari_goster():
    numara = input(
        "Notlarını görmek istediğiniz öğrencinin numarası: "
    )

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT
            Ogrenciler.Ad,
            Dersler.DersAdi,
            Dersler.Vize,
            Dersler.Final
        FROM Ogrenciler
        INNER JOIN Dersler
            ON Ogrenciler.Id = Dersler.OgrenciId
        WHERE Ogrenciler.Numara = ?
        """,
        (numara,)
    )

    dersler = cursor.fetchall()
    baglanti.close()

    if not dersler:
        print("Bu öğrenciye ait ders bulunamadı.")
        return

    print("\n--- Öğrenci Notları ---")
    print("Öğrenci:", dersler[0][0])

    toplam = 0

    for ders in dersler:
        ders_adi = ders[1]
        vize = ders[2]
        final = ders[3]

        ortalama = float(vize) * 0.4 + float(final) * 0.6

        toplam += ortalama

        harf = harf_notu_hesapla(ortalama)

        if ortalama >= 50:
            durum = "Geçti"
        else:
            durum = "Kaldı"

        print("\nDers:", ders_adi)
        print("Vize:", vize)
        print("Final:", final)
        print("Ortalama:", round(ortalama, 2))
        print("Harf Notu:", harf)
        print("Durum:", durum)

    genel_ortalama = toplam / len(dersler)

    print("\n----------------------")
    print("Genel Ortalama:", round(genel_ortalama, 2))


# -------------------------
# DERS SİL
# -------------------------

def ders_sil():
    numara = input("Dersi silinecek öğrencinin numarası: ")
    ders_adi = input("Silinecek dersin adı: ")

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Dersler.Id
        FROM Dersler
        INNER JOIN Ogrenciler
            ON Ogrenciler.Id = Dersler.OgrenciId
        WHERE Ogrenciler.Numara = ?
        AND Dersler.DersAdi = ?
        """,
        (numara, ders_adi)
    )

    ders = cursor.fetchone()

    if ders is None:
        print("Bu öğrenciye ait böyle bir ders bulunamadı.")
        baglanti.close()
        return

    ders_id = ders[0]

    cursor.execute(
        """
        DELETE FROM Dersler
        WHERE Id = ?
        """,
        (ders_id,)
    )

    baglanti.commit()
    baglanti.close()

    print("Ders başarıyla silindi.")


# -------------------------
# NOT GÜNCELLE
# -------------------------

def not_guncelle():
    numara = input(
        "Notu güncellenecek öğrencinin numarası: "
    )

    ders_adi = input(
        "Notu güncellenecek dersin adı: "
    )

    baglanti = baglanti_olustur()
    cursor = baglanti.cursor()

    cursor.execute(
        """
        SELECT Dersler.Id, Dersler.Vize, Dersler.Final
        FROM Dersler
        INNER JOIN Ogrenciler
            ON Ogrenciler.Id = Dersler.OgrenciId
        WHERE Ogrenciler.Numara = ?
        AND Dersler.DersAdi = ?
        """,
        (numara, ders_adi)
    )

    ders = cursor.fetchone()

    if ders is None:
        print("Bu öğrenciye ait böyle bir ders bulunamadı.")
        baglanti.close()
        return

    ders_id = ders[0]

    print("\nMevcut notlar:")
    print("Vize:", ders[1])
    print("Final:", ders[2])

    while True:
        try:
            yeni_vize = float(input("Yeni vize notu: "))

            if 0 <= yeni_vize <= 100:
                break

            print("Not 0 ile 100 arasında olmalıdır.")

        except ValueError:
            print("Lütfen sayısal bir değer girin.")

    while True:
        try:
            yeni_final = float(input("Yeni final notu: "))

            if 0 <= yeni_final <= 100:
                break

            print("Not 0 ile 100 arasında olmalıdır.")

        except ValueError:
            print("Lütfen sayısal bir değer girin.")

    cursor.execute(
        """
        UPDATE Dersler
        SET Vize = ?, Final = ?
        WHERE Id = ?
        """,
        (yeni_vize, yeni_final, ders_id)
    )

    baglanti.commit()
    baglanti.close()

    print("Notlar başarıyla güncellendi.")