import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def fuzzy_performans_degerlendirme(islem_sayisi_val, hata_orani_val, operator_id):
    """
    GUI için detaylı debug verisi üreten güncellenmiş fonksiyon.
    """
    
    # 1. Değişkenleri Tanımla
    ops = ctrl.Antecedent(np.arange(0, 51, 1), 'islem_sayisi')
    error = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'hata_orani')
    performance = ctrl.Consequent(np.arange(0, 101, 1), 'performans')

    # 2. Üyelik Fonksiyonları (Membership Functions)
    # İşlem Sayısı
    ops['dusuk'] = fuzz.trimf(ops.universe, [0, 0, 20])
    ops['orta'] = fuzz.trimf(ops.universe, [10, 25, 40])
    ops['yuksek'] = fuzz.trimf(ops.universe, [30, 50, 50])

    # Hata Oranı
    error['dusuk'] = fuzz.trimf(error.universe, [0, 0, 0.2])
    error['orta'] = fuzz.trimf(error.universe, [0.1, 0.3, 0.5])
    error['yuksek'] = fuzz.trapmf(error.universe, [0.4, 0.6, 1.0, 1.0])

    # Performans
    performance['dusuk'] = fuzz.trimf(performance.universe, [0, 0, 40])
    performance['orta'] = fuzz.trimf(performance.universe, [30, 50, 70])
    performance['yuksek'] = fuzz.trimf(performance.universe, [60, 100, 100])

    # 3. Kurallar
    rule1 = ctrl.Rule(ops['dusuk'] | error['yuksek'], performance['dusuk'])
    rule2 = ctrl.Rule(ops['orta'] & error['orta'], performance['orta'])
    rule3 = ctrl.Rule(ops['yuksek'] & error['dusuk'], performance['yuksek'])
    rule4 = ctrl.Rule(error['dusuk'], performance['yuksek']) # Ekstra teşvik

    # 4. Simülasyon
    perf_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    perf_sim = ctrl.ControlSystemSimulation(perf_ctrl)

    perf_sim.input['islem_sayisi'] = islem_sayisi_val
    perf_sim.input['hata_orani'] = hata_orani_val

    try:
        perf_sim.compute()
        score = perf_sim.output['performans']
    except:
        score = 0

    # 5. Performans Kategorisi Belirleme
    kategori = "BELİRSİZ"
    if score >= 70: kategori = "YÜKSEK PERFORMANS 🚀"
    elif score >= 40: kategori = "ORTA PERFORMANS ⚠️"
    else: kategori = "DÜŞÜK PERFORMANS 🔻"

    # --- KRİTİK KISIM: GUI İÇİN DEBUG VERİLERİNİ HESAPLAMA ---
    # Scikit-fuzzy'nin arkaplanındaki matematiksel değerleri (üyelik derecelerini)
    # manuel olarak çekiyoruz ki GUI hata vermesin.
    
    # İşlem Sayısı Üyelikleri (0.0 - 1.0 arası)
    ops_memb = {
        'dusuk': fuzz.interp_membership(ops.universe, ops['dusuk'].mf, islem_sayisi_val),
        'orta': fuzz.interp_membership(ops.universe, ops['orta'].mf, islem_sayisi_val),
        'yuksek': fuzz.interp_membership(ops.universe, ops['yuksek'].mf, islem_sayisi_val),
    }

    # Hata Oranı Üyelikleri
    err_memb = {
        'dusuk': fuzz.interp_membership(error.universe, error['dusuk'].mf, hata_orani_val),
        'orta': fuzz.interp_membership(error.universe, error['orta'].mf, hata_orani_val),
        'yuksek': fuzz.interp_membership(error.universe, error['yuksek'].mf, hata_orani_val),
    }

    # Kural Aktivasyonları (Basit Mantık: AND=min, OR=max)
    # Kural 1: (Ops Düşük OR Hata Yüksek)
    r1_act = max(ops_memb['dusuk'], err_memb['yuksek'])
    # Kural 2: (Ops Orta AND Hata Orta)
    r2_act = min(ops_memb['orta'], err_memb['orta'])
    # Kural 3: (Ops Yüksek AND Hata Düşük)
    r3_act = min(ops_memb['yuksek'], err_memb['dusuk'])
    # Kural 4: (Hata Düşük)
    r4_act = err_memb['dusuk']

    # 6. Sonuç Sözlüğü (GUI'nin beklediği format)
    return {
        'performans': score,
        'operator': operator_id,
        'islem_sayisi': islem_sayisi_val,
        'hata_orani': hata_orani_val,
        'kategori': kategori,
        'debug': {
            'islem_uyelikleri': ops_memb,
            'hata_uyelikleri': err_memb,
            'kural_aktivasyonlari': {
                'kural1': r1_act,
                'kural2': r2_act,
                'kural3': r3_act,
                'kural4': r4_act,
                'kural5': 0.0 # GUI 5 kural bekliyor olabilir, boş gönderelim
            }
        }
    }