from ogrenci import (
    ogrenci_ekle,
    ogrencileri_listele,
    ogrenci_ara,
    ders_ekle,
    notlari_goster,
    ogrenci_sil,
    ogrenci_guncelle,
    ders_sil,
    not_guncelle
)


while True:
    print("\n===== ÖĞRENCİ TAKİP SİSTEMİ =====")
    print("1 - Öğrenci Ekle")
    print("2 - Öğrencileri Listele")
    print("3 - Öğrenci Ara")
    print("4 - Ders ve Not Ekle")
    print("5 - Notları Görüntüle")
    print("6 - Öğrenci Sil")
    print("7 - Öğrenci Güncelle")
    print("8 - Ders Sil")
    print("9 - Not Güncelle")
    print("0 - Çıkış")

    secim = input("Seçiminiz: ")

    if secim == "1":
        ogrenci_ekle()

    elif secim == "2":
        ogrencileri_listele()

    elif secim == "3":
        ogrenci_ara()

    elif secim == "4":
        ders_ekle()

    elif secim == "5":
        notlari_goster()

    elif secim == "6":
        ogrenci_sil()

    elif secim == "7":
        ogrenci_guncelle()

    elif secim == "8":
        ders_sil()

    elif secim == "9":
        not_guncelle()

    elif secim == "0":
        print("Program kapatılıyor...")
        break

    else:
        print("Geçersiz seçim!")