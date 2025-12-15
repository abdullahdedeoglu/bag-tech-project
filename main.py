import pandas as pd
import random

def veri_oku(dosya_yolu):
    """CSV dosyasını okur"""
    try:
        df = pd.read_csv(dosya_yolu)
        print(f"✓ {len(df)} satır veri yüklendi\n")
        return df
    except FileNotFoundError:
        print(f"HATA: {dosya_yolu} bulunamadı!")
        return None

def gunluk_ozet(df):
    """Toplam ÇIKIŞ miktarlarını hesaplar"""
    cikis_df = df[df['Hareket_Turu'] == 'CIKIS']
    
    kg_toplam = cikis_df[cikis_df['Birim'] == 'KG']['Miktar'].sum()
    adet_toplam = cikis_df[cikis_df['Birim'] == 'ADET']['Miktar'].sum()
    
    return kg_toplam, adet_toplam

def verimlilik_raporu(df):
    """En çok hareket yapan 3 operatörü bulur"""
    operator_sayilari = df.groupby('Operator_ID').size().sort_values(ascending=False)
    return operator_sayilari.head(3)

def rapor_olustur(df, fuzzy_sonuc=None):
    """Tüm sonuçları ekrana ve dosyaya yazar"""
    rapor = []
    rapor.append("=" * 60)
    rapor.append("BAG TECH DEPO ANALİZ RAPORU")
    rapor.append("=" * 60)
    rapor.append("")
    
    # Günlük Özet
    kg, adet = gunluk_ozet(df)
    rapor.append("📊 GÜNLÜK ÖZET (Toplam ÇIKIŞ Miktarları)")
    rapor.append(f"   KG Birimi    : {kg} KG")
    rapor.append(f"   ADET Birimi  : {adet} ADET")
    rapor.append("")
    
    # Verimlilik
    top3 = verimlilik_raporu(df)
    rapor.append("🏆 VERİMLİLİK RAPORU (En Çok Hareket Yapan Operatörler)")
    for i, (op_id, sayi) in enumerate(top3.items(), 1):
        rapor.append(f"   {i}. {op_id}: {sayi} işlem")
    rapor.append("")
    
    # Fuzzy Logic Sonucu
    if fuzzy_sonuc:
        rapor.append("🤖 FUZZY LOGIC PERFORMANS DEĞERLENDİRMESİ")
        rapor.append(f"   Operatör      : {fuzzy_sonuc['operator']}")
        rapor.append(f"   İşlem Sayısı  : {fuzzy_sonuc['islem_sayisi']}")
        rapor.append(f"   Hata Oranı    : {fuzzy_sonuc['hata_orani']:.2f}")
        rapor.append(f"   Performans    : {fuzzy_sonuc['performans']:.2f}/100")
        rapor.append(f"   Kategori      : {fuzzy_sonuc['kategori']}")
    
    rapor.append("=" * 60)
    
    # Ekrana yazdır
    rapor_metni = "\n".join(rapor)
    print(rapor_metni)
    
    # Dosyaya kaydet
    with open('analiz_raporu.txt', 'w', encoding='utf-8') as f:
        f.write(rapor_metni)
    print("\n✓ Rapor 'analiz_raporu.txt' dosyasına kaydedildi")

# Ana program
if __name__ == "__main__":
    # Veriyi yükle
    df = veri_oku('depo_verileri.csv')
    
    if df is not None:
        # Fuzzy Logic için simüle veri
        operator_id = 'Op-101'
        islem_sayisi = len(df[df['Operator_ID'] == operator_id])
        hata_orani = random.uniform(0.05, 0.25)  # Simüle edilmiş
        
        # Fuzzy sistemi çalıştır (aşağıda yazacağız)
        from fuzzy_system import fuzzy_performans_degerlendirme
        fuzzy_sonuc = fuzzy_performans_degerlendirme(
            islem_sayisi, 
            hata_orani, 
            operator_id
        )
        
        # Raporu oluştur
        rapor_olustur(df, fuzzy_sonuc)