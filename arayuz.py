import tkinter as tk
from tkinter import ttk, messagebox
import math

try:
    from balistik_hesaplayici import BalistikHesaplayici
except ImportError:
    messagebox.showerror("Modül Bulunamadı", "Lütfen 'balistik_hesaplayici.py' dosyasının bu programla aynı klasörde olduğundan emin olun.")
    exit()

class BalistikArayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Silah Sistemi Balistik Simülatörü")
        self.root.geometry("1450x850")
        
        self.hesaplayici = BalistikHesaplayici()
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), borderwidth=0)
        style.map('TButton', background=[('active', '#3c7a3e'), ('!disabled', '#4CAF50')], foreground=[('!disabled', 'white')])
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.left_frame = ttk.Frame(main_frame, padding="15", relief="groove")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.right_frame = ttk.Frame(main_frame, padding="15", relief="groove")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1, minsize=450)
        main_frame.grid_columnconfigure(1, weight=2, minsize=700)
        self.left_frame.grid_columnconfigure(1, weight=1)

        self.create_input_fields()
        self.create_result_display()
        self.create_scope_view()
        self.create_status_bar()

        # Arayüzü ilk silahla başlat
        default_weapon = list(self.hesaplayici.SILAH_PLATFORMLARI.keys())[0]
        self.silah_combo.set(default_weapon)
        self.silah_degisti(None)

    def create_input_fields(self):
        frame = ttk.Frame(self.left_frame)
        frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        frame.columnconfigure(1, weight=1)
        
        ttk.Label(frame, text="Sistem ve Çevre Parametreleri", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        self.entries = {}
        row_index = 1

        # YENİ: Silah seçimi en üste geldi
        ttk.Label(frame, text="Silah Platformu:").grid(row=row_index, column=0, sticky="w", pady=3)
        self.silah_combo = ttk.Combobox(frame, values=list(self.hesaplayici.SILAH_PLATFORMLARI.keys()), state="readonly")
        self.silah_combo.grid(row=row_index, column=1, sticky="ew", pady=3)
        self.silah_combo.bind('<<ComboboxSelected>>', self.silah_degisti)
        row_index += 1
        
        # Mermi tipi seçimi
        ttk.Label(frame, text="Mermi Tipi:").grid(row=row_index, column=0, sticky="w", pady=3)
        self.mermi_tipi_combo = ttk.Combobox(frame, state="readonly")
        self.mermi_tipi_combo.grid(row=row_index, column=1, sticky="ew", pady=3)
        self.mermi_tipi_combo.bind('<<ComboboxSelected>>', self.mermi_tipi_degisti)
        row_index += 1

        ttk.Label(frame, text="Efektif Hız (m/s):").grid(row=row_index, column=0, sticky="w", pady=3)
        self.hiz_label = ttk.Label(frame, text="", font=('Segoe UI', 10, 'bold'))
        self.hiz_label.grid(row=row_index, column=1, sticky="w", pady=3)
        row_index += 1
        
        # Diğer girişler
        input_fields = {
            "hedef_mesafe": "Hedef Mesafesi (m):", "durbun_yuksekligi": "Dürbün Yüksekliği (cm):",
            "sifirlama_mesafesi": "Sıfırlama Mesafesi (m):", "ruzgar_hizi": "Rüzgar Hızı (m/s):",
            "ruzgar_acisi": "Rüzgar Açısı (°, 90=Sağdan):", "sicaklik": "Sıcaklık (°C):",
            "basinc": "Basınç (hPa):", "nem": "Bağıl Nem (%):", "enlem": "Atış Konumu Enlemi (°):"
        }
        defaults = {
            "hedef_mesafe": "100", "sifirlama_mesafesi": "100", "ruzgar_hizi": "4.5",
            "ruzgar_acisi": "90", "sicaklik": "15", "basinc": "1013.25", "nem": "50", "enlem": "40.82"
        }
        
        for key, label_text in input_fields.items():
            ttk.Label(frame, text=label_text).grid(row=row_index, column=0, sticky="w", pady=3)
            entry = ttk.Entry(frame)
            entry.insert(0, defaults.get(key, "0"))
            entry.grid(row=row_index, column=1, sticky="ew", pady=3)
            self.entries[key] = entry
            row_index += 1

        ttk.Button(self.left_frame, text="Balistik Hesapla", command=self.hesapla).grid(row=1, column=0, columnspan=2, pady=20, ipady=5, sticky="ew")

    def silah_degisti(self, event):
        """Silah değiştiğinde mermi listesini ve varsayılanları günceller."""
        silah_adi = self.silah_combo.get()
        if not silah_adi: return
        
        silah = self.hesaplayici.SILAH_PLATFORMLARI[silah_adi]
        uyumlu_kalibreler = silah["uyumlu_kalibreler"]
        
        # Mermi listesini filtrele
        uyumlu_mermiler = [mermi_adi for mermi_adi, mermi_detay in self.hesaplayici.MERMI_TIPLERI.items() if mermi_detay["kalibre"] in uyumlu_kalibreler]
        
        self.mermi_tipi_combo['values'] = uyumlu_mermiler
        if uyumlu_mermiler:
            self.mermi_tipi_combo.set(uyumlu_mermiler[0])
        else:
            self.mermi_tipi_combo.set("")
        
        # Dürbün yüksekliğini güncelle
        self.entries["durbun_yuksekligi"].delete(0, tk.END)
        self.entries["durbun_yuksekligi"].insert(0, str(silah["durbun_yuksekligi_cm"]))
        
        # Hız etiketini de güncelle
        self.mermi_tipi_degisti(None)

    def mermi_tipi_degisti(self, event):
        """Mermi tipi veya silah değiştiğinde efektif hızı günceller."""
        silah_adi = self.silah_combo.get()
        mermi_adi = self.mermi_tipi_combo.get()
        
        if silah_adi and mermi_adi:
            silah = self.hesaplayici.SILAH_PLATFORMLARI[silah_adi]
            mermi = self.hesaplayici.MERMI_TIPLERI[mermi_adi]
            
            efektif_hiz = mermi["hiz"] * (1 + silah["namlu_hiz_modifikatoru"])
            self.hiz_label.config(text=f"{efektif_hiz:.1f}")
        else:
            self.hiz_label.config(text="N/A")

    # create_result_display, create_scope_view, draw_reticle, update_scope_target, create_status_bar (değişiklik yok)
    def create_result_display(self):
        ttk.Label(self.left_frame, text="Hesaplama Sonuçları", style='Header.TLabel').grid(row=2, column=0, columnspan=2, pady=(10, 5), sticky="w")
        self.sonuc_text = tk.Text(self.left_frame, height=15, width=60, wrap=tk.WORD, font=('Consolas', 10), background='#2b2b2b', foreground='#a9b7c6', relief='flat', insertbackground='white')
        self.sonuc_text.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.left_frame.rowconfigure(3, weight=1)

    def create_scope_view(self):
        self.scope_canvas = tk.Canvas(self.right_frame, bg='#1e1e1e', highlightthickness=0)
        self.scope_canvas.pack(fill=tk.BOTH, expand=True)
        self.scope_canvas.bind("<Configure>", self.draw_reticle)
        self.last_scope_size = (0, 0)

    def draw_reticle(self, event=None):
        if (event and self.last_scope_size == (event.width, event.height)) or not hasattr(self, 'hesaplayici'): return
        self.scope_canvas.delete("all")
        width, height = self.scope_canvas.winfo_width(), self.scope_canvas.winfo_height()
        self.last_scope_size = (width, height)
        center_x, center_y, radius = width / 2, height / 2, min(width, height) / 2 * 0.95
        self.scope_canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline='#333333', width=20)
        MIL_TO_PIXEL_RATIO = radius / 8
        for i in range(-7, 8):
            if i == 0: continue
            x = center_x + i * MIL_TO_PIXEL_RATIO
            self.scope_canvas.create_line(x, center_y - 10, x, center_y + 10, fill='#999999')
            self.scope_canvas.create_text(x, center_y + 20, text=str(abs(i)), fill='#cccccc', font=('Segoe UI', 8))
            y = center_y + i * MIL_TO_PIXEL_RATIO
            self.scope_canvas.create_line(center_x - 10, y, center_x + 10, y, fill='#999999')
            self.scope_canvas.create_text(center_x - 20, y, text=str(abs(i)), fill='#cccccc', font=('Segoe UI', 8))
        self.scope_canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, fill='#FF4136', width=1.5)
        self.scope_canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, fill='#FF4136', width=1.5)

    def update_scope_target(self, yanal_mil, dikey_mil, uyari_mesaji):
        self.draw_reticle()
        self.scope_canvas.delete("target_marker")
        width, height = self.scope_canvas.winfo_width(), self.scope_canvas.winfo_height()
        center_x, center_y, radius = width / 2, height / 2, min(width, height) / 2 * 0.95
        MIL_TO_PIXEL_RATIO = radius / 8
        pixel_offset_x, pixel_offset_y = yanal_mil * MIL_TO_PIXEL_RATIO, -dikey_mil * MIL_TO_PIXEL_RATIO
        target_x, target_y = center_x + pixel_offset_x, center_y + pixel_offset_y
        marker_color = '#FF4136' if "UYARI" in uyari_mesaji else '#00FF7F'
        s = 10
        self.scope_canvas.create_oval(target_x - s, target_y - s, target_x + s, target_y + s, outline=marker_color, width=2, tags="target_marker")
        self.scope_canvas.create_line(target_x - s, target_y, target_x + s, target_y, fill=marker_color, tags="target_marker")
        self.scope_canvas.create_line(target_x, target_y - s, target_x, target_y + s, fill=marker_color, tags="target_marker")
        self.scope_canvas.create_text(target_x, target_y - s - 10, text=f"{dikey_mil:+.2f} UP, {yanal_mil:+.2f} R", fill=marker_color, font=('Segoe UI', 9, 'bold'), tags="target_marker")

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır. Lütfen bir silah platformu seçin.")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5).pack(side=tk.BOTTOM, fill=tk.X)

    def hesapla(self):
        try:
            self.status_var.set("Hesaplanıyor...")
            self.root.update_idletasks()

            params = {
                # YENİ: silah_tipi eklendi
                "silah_tipi": self.silah_combo.get(),
                "mermi_tipi": self.mermi_tipi_combo.get(),
                "atis_acisi": 0.0,
                "hedef_mesafe": float(self.entries["hedef_mesafe"].get()),
                "durbun_yuksekligi_m": float(self.entries["durbun_yuksekligi"].get()) / 100.0,
                "sifirlama_mesafesi": float(self.entries["sifirlama_mesafesi"].get()),
                "ruzgar_hizi": float(self.entries["ruzgar_hizi"].get()),
                "ruzgar_acisi_derece": float(self.entries["ruzgar_acisi"].get()),
                "sicaklik_c": float(self.entries["sicaklik"].get()),
                "basinc_hpa": float(self.entries["basinc"].get()),
                "nem_bagil": float(self.entries["nem"].get()),
                "enlem_derece": float(self.entries["enlem"].get()),
            }
            
            if not params["silah_tipi"] or not params["mermi_tipi"]:
                raise ValueError("Lütfen bir silah ve mermi tipi seçin.")

            sonuc = self.hesaplayici.atis_hesapla(**params)

            self.sonuc_text.delete(1.0, tk.END)
            dikey_ayar_yonu = "YUKARI (UP)" if sonuc['gerekli_yukselis_ayari_mil'] >= 0 else "AŞAĞI (DOWN)"
            yanal_ayar_yonu = "SAĞA (RIGHT)" if sonuc['gerekli_yanal_ayari_mil'] >= 0 else "SOLA (LEFT)"
            output = (
                f"--- DÜRBÜN AYAR ÖNERİLERİ (MİL) ---\n"
                f"Dikey Ayar: {abs(sonuc['gerekli_yukselis_ayari_mil']):.2f} MİL {dikey_ayar_yonu}\n"
                f"Yanal Ayar: {abs(sonuc['gerekli_yanal_ayari_mil']):.2f} MİL {yanal_ayar_yonu}\n\n"
                f"--- UÇUŞ DETAYLARI ---\n"
                f"Efektif Namlu Çıkış Hızı: {sonuc['detaylar']['efektif_hiz_mps']:.1f} m/s\n"
                f"Uçuş Süresi: {sonuc['ucus_suresi_s']:.2f} saniye\n"
                f"Hedefteki Hız: {sonuc['son_hiz_mps']:.2f} m/s\n\n"
                f"--- DURUM ---\n"
                f"{sonuc['uyari_mesaji']}"
            )
            self.sonuc_text.insert(tk.END, output)
            
            self.update_scope_target(sonuc['gerekli_yanal_ayari_mil'], sonuc['gerekli_yukselis_ayari_mil'], sonuc['uyari_mesaji'])
            self.status_var.set("Hesaplama tamamlandı.")

        except ValueError as e:
            messagebox.showerror("Giriş Hatası", str(e))
            self.status_var.set(f"Hata: {e}")
        except Exception as e:
            messagebox.showerror("Hesaplama Hatası", f"Beklenmedik bir hata oluştu: {str(e)}")
            self.status_var.set(f"Hata: {e}")

def main():
    root = tk.Tk()
    app = BalistikArayuz(root)
    root.mainloop()

if __name__ == "__main__":
    main()