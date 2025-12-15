import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def fuzzy_performans_degerlendirme(islem_sayisi, hata_orani, operator_id):
    """
    Fuzzy Logic ile operatör performansını değerlendirir
    """
    
    # 1. GİRDİ DEĞİŞKENLERİ TANIMLA
    # İşlem Sayısı: 0-20 arası
    islem = ctrl.Antecedent(np.arange(0, 21, 1), 'islem_sayisi')
    islem['dusuk'] = fuzz.trimf(islem.universe, [0, 0, 8])
    islem['orta'] = fuzz.trimf(islem.universe, [5, 10, 15])
    islem['yuksek'] = fuzz.trimf(islem.universe, [12, 20, 20])
    
    # Hata Oranı: 0.0-1.0 arası
    hata = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'hata_orani')
    hata['dusuk'] = fuzz.trimf(hata.universe, [0, 0, 0.3])
    hata['orta'] = fuzz.trimf(hata.universe, [0.2, 0.5, 0.8])
    hata['yuksek'] = fuzz.trimf(hata.universe, [0.6, 1, 1])
    
    # 2. ÇIKTI DEĞİŞKENİ TANIMLA
    # Performans: 0-100 arası skor
    performans = ctrl.Consequent(np.arange(0, 101, 1), 'performans')
    performans['dusuk'] = fuzz.trimf(performans.universe, [0, 0, 40])
    performans['orta'] = fuzz.trimf(performans.universe, [30, 50, 70])
    performans['yuksek'] = fuzz.trimf(performans.universe, [60, 100, 100])
    
    # 3. KURALLARI TANIMLA (4+ kural gerekli)
    kural1 = ctrl.Rule(islem['yuksek'] & hata['dusuk'], performans['yuksek'])
    kural2 = ctrl.Rule(islem['dusuk'] | hata['yuksek'], performans['dusuk'])
    kural3 = ctrl.Rule(islem['orta'] & hata['orta'], performans['orta'])
    kural4 = ctrl.Rule(islem['yuksek'] & hata['yuksek'], performans['dusuk'])
    kural5 = ctrl.Rule(islem['orta'] & hata['dusuk'], performans['yuksek'])
    
    # 4. KONTROL SİSTEMİNİ OLUŞTUR
    performans_ctrl = ctrl.ControlSystem([kural1, kural2, kural3, kural4, kural5])
    performans_sim = ctrl.ControlSystemSimulation(performans_ctrl)
    
    # 5. GİRDİLERİ VER VE HESAPLA
    performans_sim.input['islem_sayisi'] = islem_sayisi
    performans_sim.input['hata_orani'] = hata_orani
    performans_sim.compute()
    
    # 6. SONUCU DÖNDÜR
    skor = performans_sim.output['performans']
    
    # Kategori belirle
    if skor >= 70:
        kategori = "YÜKSEK PERFORMANS"
    elif skor >= 40:
        kategori = "ORTA PERFORMANS"
    else:
        kategori = "DÜŞÜK PERFORMANS"
    
    return {
        'operator': operator_id,
        'islem_sayisi': islem_sayisi,
        'hata_orani': hata_orani,
        'performans': skor,
        'kategori': kategori
    }