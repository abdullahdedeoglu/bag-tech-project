# BAG Tech Depo Analiz ve Fuzzy Logic Karar Sistemi

## 📖 Proje Hakkında

Bu proje, depo operasyonlarını analiz eden ve **sıfırdan yazılmış Fuzzy Logic algoritması** ile operatör performansını değerlendiren bir Python uygulamasıdır.

**Geliştirici:** [Adın Soyadın]  
**Geliştirme Süresi:** [X] gün  
**Teknolojiler:** Python, Pandas, NumPy

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip paket yöneticisi

### Kurulum Adımları
```bash
# Projeyi klonlayın
git clone [repo-url]
cd bag_tech_project

# Sanal ortam oluşturun (opsiyonel)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Bağımlılıkları yükleyin
pip install pandas numpy
```

## 💻 Kullanım
```bash
python main.py
```

Program çalıştırıldığında:
1. `depo_verileri.csv` dosyasını okur
2. Veri analizleri yapar
3. Fuzzy Logic ile operatör performansını değerlendirir
4. Sonuçları ekrana yazdırır ve `analiz_raporu.txt` dosyasına kaydeder

## 📊 Özellikler

### Veri Analizi
- ✅ CSV dosyasından veri okuma
- ✅ Toplam ÇIKIŞ miktarlarını hesaplama (KG ve ADET ayrı)
- ✅ En verimli 3 operatörü listeleme
- ✅ Otomatik rapor oluşturma

### Fuzzy Logic Karar Sistemi
**Önemli Not:** Bu proje, harici kütüphane kullanmadan **sıfırdan yazılmış** bir Fuzzy Logic sistemi içermektedir.

**Girdi Değişkenleri:**
- **İşlem Sayısı**: Operatörün toplam GİRİŞ + ÇIKIŞ sayısı
  - Düşük: 0-8 işlem
  - Orta: 5-15 işlem
  - Yüksek: 12-20 işlem

- **Hata Oranı**: Simüle edilmiş hata oranı (0.0-1.0)
  - Düşük: 0.0-0.3
  - Orta: 0.2-0.8
  - Yüksek: 0.6-1.0

**Çıktı Değişkeni:**
- **Performans Skoru**: 0-100 arası değerlendirme
  - Düşük Performans: 0-40
  - Orta Performans: 40-70
  - Yüksek Performans: 70-100

**Fuzzy Kurallar (5 adet):**
1. **Kural 1:** EĞER (İşlem Sayısı Yüksek) VE (Hata Oranı Düşük) İSE (Performans Yüksek)
2. **Kural 2:** EĞER (İşlem Sayısı Düşük) VEYA (Hata Oranı Yüksek) İSE (Performans Düşük)
3. **Kural 3:** EĞER (İşlem Sayısı Orta) VE (Hata Oranı Orta) İSE (Performans Orta)
4. **Kural 4:** EĞER (İşlem Sayısı Yüksek) VE (Hata Oranı Yüksek) İSE (Performans Düşük)
5. **Kural 5:** EĞER (İşlem Sayısı Orta) VE (Hata Oranı Düşük) İSE (Performans Yüksek)

**Durulaştırma Yöntemi:** Ağırlık Merkezi (Centroid) Yöntemi

## 📁 Proje Yapısı
```
bag_tech_project/
├── depo_verileri.csv          # Depo hareketleri veri seti (22 satır)
├── main.py                     # Ana program (veri analizi)
├── fuzzy_system.py            # Fuzzy Logic algoritması
├── analiz_raporu.txt          # Çıktı raporu (otomatik oluşur)
├── README.md                   # Bu dosya
└── requirements.txt           # Python bağımlılıkları
```

## 🧪 Örnek Çıktı
```
============================================================
BAG TECH DEPO ANALİZ RAPORU
============================================================

📊 GÜNLÜK ÖZET (Toplam ÇIKIŞ Miktarları)
   KG Birimi    : 370 KG
   ADET Birimi  : 185 ADET

🏆 VERİMLİLİK RAPORU (En Çok Hareket Yapan Operatörler)
   1. Op-101: 8 işlem
   2. Op-102: 8 işlem
   3. Op-103: 6 işlem

🤖 FUZZY LOGIC PERFORMANS DEĞERLENDİRMESİ
   Operatör      : Op-101
   İşlem Sayısı  : 8
   Hata Oranı    : 0.24
   Performans    : 67.85/100
   Kategori      : ORTA PERFORMANS
============================================================
```

## 🧠 Fuzzy Logic Algoritması Detayları

Bu projede kullanılan Fuzzy Logic sistemi 4 aşamadan oluşur:

### 1. Bulanıklaştırma (Fuzzification)
Girdi değerleri (işlem sayısı, hata oranı) üçgen üyelik fonksiyonları kullanılarak bulanık kümelere dönüştürülür.

### 2. Kural Değerlendirme
5 adet IF-THEN kuralı Mamdani çıkarım yöntemiyle değerlendirilir. Her kural için:
- **AND** operatörü: Minimum fonksiyonu
- **OR** operatörü: Maksimum fonksiyonu

### 3. Birleştirme (Aggregation)
Tüm kuralların çıktıları birleştirilir ve bulanık çıktı kümesi oluşturulur.

### 4. Durulaştırma (Defuzzification)
Ağırlık merkezi yöntemi kullanılarak bulanık çıktı, kesin bir performans skoruna (0-100) dönüştürülür.

## 🎓 Teknik Detaylar

- **Programlama Dili:** Python 3.12
- **Veri İşleme:** Pandas
- **Matematik Hesaplamalar:** NumPy
- **Fuzzy Logic:** Sıfırdan yazılmış algoritma (harici kütüphane kullanılmamıştır)
- **Kod Stili:** PEP 8 uyumlu, type hints ile

## 📝 Geliştirme Notları

- Fuzzy Logic sistemi, scikit-fuzzy gibi harici kütüphaneler yerine sıfırdan yazılmıştır
- Üçgen üyelik fonksiyonları (trimf) kullanılmıştır
- Mamdani çıkarım yöntemi uygulanmıştır
- Centroid (ağırlık merkezi) durulaştırma yöntemi kullanılmıştır

## 🖥️ Grafik Arayüz (GUI)

Proje artık kullanıcı dostu bir grafik arayüze sahiptir!

### GUI Kullanımı
```bash
python gui_app.py
```

### Özellikler

- ✅ **Sürükle-Bırak CSV Yükleme**: Kolay veri yükleme
- ✅ **Gerçek Zamanlı Analiz**: Anlık sonuçlar
- ✅ **Fuzzy Logic Görselleştirme**: Detaylı performans raporu
- ✅ **Rapor Kaydetme**: Sonuçları dosyaya kaydet
- ✅ **Modern Arayüz**: Profesyonel ve temiz tasarım

### Ekran Görüntüsü

<img width="999" height="747" alt="image" src="https://github.com/user-attachments/assets/b6f8c7f0-f45e-4546-ad5b-eb94c88ff505" />


## 🔮 Gelecek Geliştirmeler

- [ ] Görselleştirme: Matplotlib ile üyelik fonksiyonları grafikleri
- [ ] Daha fazla operatör analizi
- [ ] Tarih bazlı trend analizleri
- [ ] Web arayüzü (Flask/Django)
- [ ] Gerçek zamanlı veri entegrasyonu

## 👨‍💻 Geliştirici

**Abdullah Dedeoğlu**  
Bilgisayar Mühendisi  
abdullahdedeoglu919@gmail.com | https://www.linkedin.com/in/abdullah-dedeoğlu-87973a239/

## 📄 Lisans

Bu proje BAG Tech işe alım görevi kapsamında geliştirilmiştir.

---

⭐ Eğer bu projeyi beğendiyseniz, yıldız vermeyi unutmayın!
