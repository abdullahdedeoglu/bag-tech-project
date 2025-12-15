from fuzzy_system import fuzzy_performans_degerlendirme

print("=" * 60)
print("FUZZY LOGIC SİSTEM TEST SENARYOLARI")
print("=" * 60)
print()

test_senaryolari = [
    {
        "isim": "Mükemmel Operatör",
        "islem": 18,
        "hata": 0.05,
        "aciklama": "Çok fazla işlem, çok az hata"
    },
    {
        "isim": "Zayıf Operatör", 
        "islem": 4,
        "hata": 0.85,
        "aciklama": "Az işlem, çok hata"
    },
    {
        "isim": "Ortalama Operatör",
        "islem": 10,
        "hata": 0.40,
        "aciklama": "Orta seviye her şey"
    },
    {
        "isim": "Çalışkan Ama Hatalı",
        "islem": 17,
        "hata": 0.75,
        "aciklama": "Çok işlem ama çok hata"
    },
    {
        "isim": "Yavaş Ama Dikkatli",
        "islem": 9,
        "hata": 0.08,
        "aciklama": "Az işlem ama çok az hata"
    }
]

for i, senaryo in enumerate(test_senaryolari, 1):
    print(f"📋 Test {i}: {senaryo['isim']}")
    print(f"   Açıklama: {senaryo['aciklama']}")
    
    sonuc = fuzzy_performans_degerlendirme(
        senaryo["islem"],
        senaryo["hata"],
        f"Test-Op-{i}"
    )
    
    print(f"   → İşlem Sayısı: {sonuc['islem_sayisi']}")
    print(f"   → Hata Oranı: {sonuc['hata_orani']:.2f}")
    print(f"   → Performans: {sonuc['performans']:.2f}/100")
    print(f"   → Kategori: {sonuc['kategori']}")
    print()

print("=" * 60)
print("✅ Tüm testler tamamlandı!")
print("=" * 60)