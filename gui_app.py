import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
import random
from fuzzy_system import fuzzy_performans_degerlendirme

class DepoAnalızGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BAG Tech - Depo Analiz ve Fuzzy Logic Sistemi")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Tema renkleri
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'bg': '#ECF0F1',
            'white': '#FFFFFF'
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.df = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Ana UI bileşenlerini oluşturur"""

        # Tema menüsü
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tema", menu=theme_menu)
        theme_menu.add_command(label="🌙 Koyu Tema", command=self.apply_dark_theme)
        theme_menu.add_command(label="☀️ Açık Tema", command=self.apply_light_theme)
        
        # Başlık
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🏭 BAG Tech Depo Yönetim Sistemi",
            font=("Arial", 20, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=20)
        
        # Ana container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Kontroller
        left_panel = tk.Frame(main_container, bg=self.colors['white'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        self.create_control_panel(left_panel)
        
        # Sağ panel - Sonuçlar
        right_panel = tk.Frame(main_container, bg=self.colors['white'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_results_panel(right_panel)
    
    def create_control_panel(self, parent):
        """Sol kontrol paneli"""
        
        # Başlık
        control_title = tk.Label(
            parent,
            text="📁 Veri İşlemleri",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        control_title.pack(pady=15)
        
        # Dosya yükleme butonu
        load_btn = tk.Button(
            parent,
            text="📂 CSV Dosyası Yükle",
            command=self.load_csv,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        load_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Varsayılan dosya butonu
        default_btn = tk.Button(
            parent,
            text="📄 Varsayılan Veriyi Kullan",
            command=self.load_default_data,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        default_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Ayırıcı
        ttk.Separator(parent, orient='horizontal').pack(fill=tk.X, padx=20, pady=20)
        
        # Analiz başlık
        analysis_title = tk.Label(
            parent,
            text="📊 Analiz Seçenekleri",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        analysis_title.pack(pady=15)
        
        # Analiz butonları
        analyze_btn = tk.Button(
            parent,
            text="🔍 Veri Analizini Çalıştır",
            command=self.run_analysis,
            bg=self.colors['warning'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        analyze_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Fuzzy Logic butonu
        fuzzy_btn = tk.Button(
            parent,
            text="🤖 Fuzzy Logic Değerlendirmesi",
            command=self.run_fuzzy_logic,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        fuzzy_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Operatör seçimi
        operator_frame = tk.Frame(parent, bg=self.colors['white'])
        operator_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(
            operator_frame,
            text="Operatör Seçin:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).pack(anchor=tk.W)
        
        self.operator_combo = ttk.Combobox(
            operator_frame,
            state="readonly",
            font=("Arial", 10)
        )
        self.operator_combo.pack(fill=tk.X, pady=5)
        
        # Rapor kaydetme
        ttk.Separator(parent, orient='horizontal').pack(fill=tk.X, padx=20, pady=20)
        
        save_btn = tk.Button(
            parent,
            text="💾 Raporu Kaydet",
            command=self.save_report,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        save_btn.pack(pady=10, padx=20, fill=tk.X)
    
    def create_results_panel(self, parent):
        """Sağ sonuçlar paneli"""
        
        # Başlık
        results_title = tk.Label(
            parent,
            text="📈 Analiz Sonuçları",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        results_title.pack(pady=15)
        
        # Sonuç text alanı
        text_frame = tk.Frame(parent, bg=self.colors['white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg='#F8F9FA',
            fg=self.colors['primary'],
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)
        
        # Başlangıç mesajı
        welcome_message = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        BAG Tech Depo Analiz Sistemine Hoş Geldiniz!       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

🚀 Başlamak için:

1. Sol panelden "CSV Dosyası Yükle" butonuna tıklayın
   VEYA
   "Varsayılan Veriyi Kullan" seçeneğini kullanın

2. Veri yüklendikten sonra analiz butonlarını kullanın

3. Sonuçları bu alanda göreceksiniz

💡 İpucu: Fuzzy Logic değerlendirmesi için önce bir 
   operatör seçmeyi unutmayın!

"""
        self.results_text.insert('1.0', welcome_message)
        self.results_text.config(state=tk.DISABLED)
    
    def load_csv(self):
        """CSV dosyası yükler"""
        file_path = filedialog.askopenfilename(
            title="CSV Dosyası Seçin",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.update_operator_list()
                self.show_message(
                    f"✅ Başarılı!\n\n{len(self.df)} satır veri yüklendi.",
                    "success"
                )
                self.display_data_preview()
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya yüklenemedi:\n{str(e)}")
    
    def load_default_data(self):
        """Varsayılan depo_verileri.csv dosyasını yükler"""
        try:
            self.df = pd.read_csv('depo_verileri.csv')
            self.update_operator_list()
            self.show_message(
                f"✅ Başarılı!\n\nVarsayılan veri yüklendi ({len(self.df)} satır)",
                "success"
            )
            self.display_data_preview()
        except FileNotFoundError:
            messagebox.showerror(
                "Hata", 
                "depo_verileri.csv dosyası bulunamadı!\n\n"
                "Lütfen dosyanın proje klasöründe olduğundan emin olun."
            )
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yüklenemedi:\n{str(e)}")
    
    def update_operator_list(self):
        """Operatör listesini günceller"""
        if self.df is not None:
            operators = sorted(self.df['Operator_ID'].unique())
            self.operator_combo['values'] = operators
            if operators:
                self.operator_combo.current(0)
    
    def display_data_preview(self):
        """Yüklenen verinin önizlemesini gösterir"""
        if self.df is None:
            return
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        
        preview = f"""
╔════════════════════════════════════════════════════════════╗
║                    VERİ ÖNİZLEMESİ                         ║
╚════════════════════════════════════════════════════════════╝

📊 Toplam Kayıt Sayısı: {len(self.df)}
📅 Tarih Aralığı: {self.df['Tarih'].min()} - {self.df['Tarih'].max()}
👥 Operatör Sayısı: {self.df['Operator_ID'].nunique()}
📦 Ürün Çeşidi: {self.df['Urun_Kodu'].nunique()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

İlk 5 Kayıt:

{self.df.head().to_string()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Veri başarıyla yüklendi! Analiz butonlarını kullanabilirsiniz.
"""
        self.results_text.insert('1.0', preview)
        self.results_text.config(state=tk.DISABLED)
    
    def run_analysis(self):
        """Veri analizini çalıştırır"""
        if self.df is None:
            messagebox.showwarning("Uyarı", "Önce veri yüklemelisiniz!")
            return
        
        try:
            # Günlük özet
            cikis_df = self.df[self.df['Hareket_Turu'] == 'CIKIS']
            kg_toplam = cikis_df[cikis_df['Birim'] == 'KG']['Miktar'].sum()
            adet_toplam = cikis_df[cikis_df['Birim'] == 'ADET']['Miktar'].sum()
            
            # Verimlilik
            operator_counts = self.df.groupby('Operator_ID').size().sort_values(ascending=False)
            top3 = operator_counts.head(3)
            
            # Ürün bazlı analiz
            product_summary = self.df.groupby('Urun_Kodu').agg({
                'Miktar': 'sum',
                'Hareket_Turu': 'count'
            }).sort_values('Miktar', ascending=False)
            
            # Sonuçları göster
            result = f"""
╔════════════════════════════════════════════════════════════╗
║                  VERİ ANALİZ RAPORU                        ║
╚════════════════════════════════════════════════════════════╝

📊 GÜNLÜK ÖZET (Toplam ÇIKIŞ Miktarları)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • KG Birimi     : {kg_toplam:>8} KG
   • ADET Birimi   : {adet_toplam:>8} ADET

🏆 VERİMLİLİK RAPORU (En Çok Hareket Yapan Operatörler)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for i, (op_id, count) in enumerate(top3.items(), 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                result += f"   {medal} {i}. {op_id:<10} : {count:>3} işlem\n"
            
            result += f"""
📦 ÜRÜN BAZLI ÖZET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for product, row in product_summary.iterrows():
                result += f"   • {product:<12} : {int(row['Miktar']):>6} birim, {int(row['Hareket_Turu']):>3} işlem\n"
            
            result += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Analiz başarıyla tamamlandı!
⏰ Analiz Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert('1.0', result)
            self.results_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Analiz yapılırken hata oluştu:\n{str(e)}")
    
    def run_fuzzy_logic(self):
        """Fuzzy Logic değerlendirmesini çalıştırır"""
        if self.df is None:
            messagebox.showwarning("Uyarı", "Önce veri yüklemelisiniz!")
            return
        
        operator_id = self.operator_combo.get()
        if not operator_id:
            messagebox.showwarning("Uyarı", "Lütfen bir operatör seçin!")
            return
        
        try:
            # Operatör verilerini hesapla
            op_data = self.df[self.df['Operator_ID'] == operator_id]
            islem_sayisi = len(op_data)
            hata_orani = random.uniform(0.05, 0.35)  # Simüle edilmiş
            
            # Fuzzy Logic değerlendirmesi
            fuzzy_result = fuzzy_performans_degerlendirme(
                islem_sayisi,
                hata_orani,
                operator_id
            )
            
            # Performans çubuğu
            bar_length = 30
            filled = int((fuzzy_result['performans'] / 100) * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Sonucu göster
            result = f"""
╔════════════════════════════════════════════════════════════╗
║            FUZZY LOGIC PERFORMANS DEĞERLENDİRMESİ         ║
╚════════════════════════════════════════════════════════════╝

🤖 Operatör Bilgileri
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Operatör ID      : {fuzzy_result['operator']}
   • Toplam İşlem     : {fuzzy_result['islem_sayisi']} adet
   • Hata Oranı       : %{fuzzy_result['hata_orani']*100:.1f}

📊 Fuzzy Logic Analizi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   İşlem Sayısı Üyelikleri:
   • Düşük   : {fuzzy_result['debug']['islem_uyelikleri']['dusuk']:.2f}
   • Orta    : {fuzzy_result['debug']['islem_uyelikleri']['orta']:.2f}
   • Yüksek  : {fuzzy_result['debug']['islem_uyelikleri']['yuksek']:.2f}

   Hata Oranı Üyelikleri:
   • Düşük   : {fuzzy_result['debug']['hata_uyelikleri']['dusuk']:.2f}
   • Orta    : {fuzzy_result['debug']['hata_uyelikleri']['orta']:.2f}
   • Yüksek  : {fuzzy_result['debug']['hata_uyelikleri']['yuksek']:.2f}

   Aktif Kurallar:
   • Kural 1 : {fuzzy_result['debug']['kural_aktivasyonlari']['kural1']:.2f}
   • Kural 2 : {fuzzy_result['debug']['kural_aktivasyonlari']['kural2']:.2f}
   • Kural 3 : {fuzzy_result['debug']['kural_aktivasyonlari']['kural3']:.2f}
   • Kural 4 : {fuzzy_result['debug']['kural_aktivasyonlari']['kural4']:.2f}
   • Kural 5 : {fuzzy_result['debug']['kural_aktivasyonlari']['kural5']:.2f}

🎯 Performans Sonucu
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   
   Skor: {fuzzy_result['performans']:.2f} / 100
   
   [{bar}] %{fuzzy_result['performans']:.1f}
   
   Kategori: {fuzzy_result['kategori']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Fuzzy Logic değerlendirmesi tamamlandı!
⏰ Değerlendirme Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert('1.0', result)
            self.results_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Fuzzy Logic çalıştırılırken hata oluştu:\n{str(e)}")
    
    def save_report(self):
        """Raporu dosyaya kaydeder"""
        if self.results_text.get('1.0', tk.END).strip() == "":
            messagebox.showwarning("Uyarı", "Kaydedilecek rapor bulunamadı!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"bag_tech_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get('1.0', tk.END))
                messagebox.showinfo("Başarılı", f"Rapor kaydedildi:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Hata", f"Rapor kaydedilemedi:\n{str(e)}")
    
    def show_message(self, message, msg_type="info"):
        """Bilgi mesajı gösterir"""
        if msg_type == "success":
            messagebox.showinfo("Başarılı", message)
        elif msg_type == "warning":
            messagebox.showwarning("Uyarı", message)
        else:
            messagebox.showerror("Hata", message)

# --- BU KISMI show_message FONKSİYONUNUN ALTINA YAPIŞTIR ---

    def apply_dark_theme(self):
        """Koyu temayı uygular"""
        self.colors.update({
            'bg': '#2C3E50',        # Koyu arka plan
            'white': '#34495E',     # Paneller için daha açık gri (Koyu modda beyaz yerine gri)
            'primary': '#1ABC9C',   # Başlıklar için turkuaz
            'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C'
        })
        self.refresh_theme()
        messagebox.showinfo("Tema", "Koyu tema uygulandı! 🌙")

    def apply_light_theme(self):
        """Açık temayı uygular (Varsayılan)"""
        self.colors.update({
            'bg': '#ECF0F1',
            'white': '#FFFFFF',
            'primary': '#2C3E50',
             'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C'
        })
        self.refresh_theme()
        messagebox.showinfo("Tema", "Açık tema uygulandı! ☀️")

    def refresh_theme(self):
        """Arayüzü yeni renklerle günceller"""
        # Ana Arka Plan
        self.root.configure(bg=self.colors['bg'])
        
        # Basit bir döngüyle renkleri güncellemeye çalışalım
        # Not: Tkinter'da dinamik tema zordur, en iyi yöntem yeniden başlatmaktır
        # ama bu kod arka planları düzeltir.
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.colors['primary'] if widget.winfo_height() == 80 else self.colors['bg'])
                
                # Alt widgetlar
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=self.colors['white'])
                        
                        # Label ve Butonlar
                        for item in child.winfo_children():
                            # Eğer widget bir Label ise
                            if isinstance(item, tk.Label):
                                # Başlık ise
                                if "Veri İşlemleri" in str(item.cget("text")) or "Analiz" in str(item.cget("text")):
                                    item.configure(bg=self.colors['white'], fg=self.colors['primary'])
                                else:
                                    item.configure(bg=self.colors['white'])

def main():
    root = tk.Tk()
    app = DepoAnalızGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()