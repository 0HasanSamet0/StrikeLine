import math

class BalistikHesaplayici:
    # YENİ: Silah platformları veritabanı
    # Her silahın kendine özgü namlu hızı modifikatörü, yiv seti, dürbün yüksekliği ve uyumlu mühimmatı var.
   # Silah Platformları ve Mermi Tanımları

    SILAH_PLATFORMLARI = {
    "M4A1 Karabina": {
        "uyumlu_kalibreler": ["5.56x45mm"],
        "namlu_hiz_modifikatoru": -0.03,  # %3 daha yavaş (kısa namlu)
        "yiv_seti": 7,
        "durbun_yuksekligi_cm": 6.5
    },
    "M110 SASS Keskin Nişancı Tüfeği": {
        "uyumlu_kalibreler": ["7.62x51mm"],
        "namlu_hiz_modifikatoru": +0.02,  # %2 daha hızlı (uzun namlu)
        "yiv_seti": 11,
        "durbun_yuksekligi_cm": 7.0
    },
    "AK-47 (Modifiye)": {
        "uyumlu_kalibreler": ["7.62x39mm"],
        "namlu_hiz_modifikatoru": 0.0,
        "yiv_seti": 9.45,
        "durbun_yuksekligi_cm": 7.5
    },
    "Accuracy International Arctic Warfare": {
        "uyumlu_kalibreler": ["7.62x51mm",],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 12,    # 305 mm = 1 in/12"
        "durbun_yuksekligi_cm": 6.0
    },
    "Sako TRG-22": {
        "uyumlu_kalibreler": ["7.62x51mm", "6.5 Creedmoor"],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 11,    # 280 mm = 1 in/11"
        "durbun_yuksekligi_cm": 7.0
    },
    "McMillan TAC-50C": {
        "uyumlu_kalibreler": [".50 BMG"],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 15,    # 381 mm = 1 in/15"
        "durbun_yuksekligi_cm": 8.5
    },
    "Accuracy International AWM (.338 Lapua)": {
        "uyumlu_kalibreler": [".338 Lapua Mag"],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 10,
        "durbun_yuksekligi_cm": 5.5
    },
    "Barrett MRAD (.300 Win Mag)": {
        "uyumlu_kalibreler": [".300 Win Mag"],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 11,
        "durbun_yuksekligi_cm": 6.0
    },
    "Desert Tech SRS (.338/.300/6.5)": {
        "uyumlu_kalibreler": [".338 Lapua Mag", ".300 Win Mag", "6.5 Creedmoor"],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 10,
        "durbun_yuksekligi_cm": 6.5
    },
    "Ruger Precision Rifle": {
        "uyumlu_kalibreler": [".308 Winchester", "6.5 Creedmoor"],
        "namlu_hiz_modifikatoru": 0.00,
        "yiv_seti": 10,
        "durbun_yuksekligi_cm": 7.0
    }
}

    MERMI_TIPLERI = {
    "5.56x45mm NATO (M855A1)": {
        "kalibre": "5.56x45mm",
        "kutle": 0.004,
        "cap": 0.00569,
        "bc": 0.370,
        "bc_tipi": "G1",
        "hiz": 948
    },
    "7.62x51mm NATO (M118LR)": {
        "kalibre": "7.62x51mm",
        "kutle": 0.0113,
        "cap": 0.00782,
        "bc": 0.505,
        "bc_tipi": "G1",
        "hiz": 790
    },
    "7.62x51mm NATO (M80)": {
        "kalibre": "7.62x51mm",
        "kutle": 0.0097,
        "cap": 0.00782,
        "bc": 0.395,
        "bc_tipi": "G1",
        "hiz": 850
    },
    ".300 Winchester Magnum (Mk248 Mod 1)": {
        "kalibre": ".300 Win Mag",
        "kutle": 0.0125,
        "cap": 0.00782,
        "bc": 0.670,
        "bc_tipi": "G1",
        "hiz": 884
    },
    ".338 Lapua Magnum (Scenar)": {
        "kalibre": ".338 Lapua Mag",
        "kutle": 0.0194,
        "cap": 0.0086,
        "bc": 0.778,
        "bc_tipi": "G1",
        "hiz": 820
    },
    ".50 BMG (M33 Ball)": {
        "kalibre": ".50 BMG",
        "kutle": 0.0430,
        "cap": 0.0128,
        "bc": 0.670,
        "bc_tipi": "G1",
        "hiz": 887
    },
    "7.62x39mm (123gr FMJ)": {
        "kalibre": "7.62x39mm",
        "kutle": 0.008,
        "cap": 0.00792,
        "bc": 0.280,
        "bc_tipi": "G1",
        "hiz": 730
    },
    # Yeni Eklenen Mermiler
    ".300 Winchester Magnum (220gr SMK)": {
        "kalibre": ".300 Win Mag",
        "kutle": 0.01426,
        "cap": 0.00782,
        "bc": 0.555,
        "bc_tipi": "G1",
        "hiz": 823
    },
    ".338 Lapua Magnum (300gr Scenar)": {
        "kalibre": ".338 Lapua Mag",
        "kutle": 0.01944,
        "cap": 0.0086,
        "bc": 0.707,
        "bc_tipi": "G1",
        "hiz": 915
    },
    "6.5 Creedmoor (140gr Hornady ELD-M)": {
        "kalibre": "6.5 Creedmoor",
        "kutle": 0.00907,
        "cap": 0.0067,
        "bc": 0.661,
        "bc_tipi": "G1",
        "hiz": 820
    }
}


    # G1 Sürükleme Tablosu (değişiklik yok)
    G1_DRAG_TABLE = {
        0: 0.268, 50: 0.258, 100: 0.248, 150: 0.238, 200: 0.23, 250: 0.231, 300: 0.245, 
        320: 0.265, 340: 0.315, 343: 0.322, 350: 0.34, 360: 0.37, 370: 0.395, 380: 0.42, 
        400: 0.44, 450: 0.43, 500: 0.41, 550: 0.39, 600: 0.37, 650: 0.355, 700: 0.34, 
        750: 0.325, 800: 0.31, 850: 0.3, 900: 0.29, 950: 0.28, 1000: 0.27, 1100: 0.25, 
        1200: 0.235, 1300: 0.22, 1400: 0.21
    }

    def __init__(self):
        self.g = 9.80665
        self.R_dry_air = 287.05
        self.R_water_vapor = 461.495
        self.max_dikey_ayar_mil = 25.0
        self.max_yanal_ayar_mil = 12.0

    # get_drag_coefficient_g1, saturated_vapor_pressure, hava_yogunlugu_hesapla (değişiklik yok)
    def get_drag_coefficient_g1(self, velocity):
        velocities = sorted(self.G1_DRAG_TABLE.keys())
        if velocity <= velocities[0]: return self.G1_DRAG_TABLE[velocities[0]]
        if velocity >= velocities[-1]: return self.G1_DRAG_TABLE[velocities[-1]]
        for i in range(len(velocities) - 1):
            v1, v2 = velocities[i], velocities[i+1]
            if v1 <= velocity <= v2:
                c1, c2 = self.G1_DRAG_TABLE[v1], self.G1_DRAG_TABLE[v2]
                return c1 + (c2 - c1) * (velocity - v1) / (v2 - v1)
        return 0.0

    def saturated_vapor_pressure(self, temp_c):
        return 610.94 * math.exp((17.625 * temp_c) / (243.04 + temp_c))

    def hava_yogunlugu_hesapla(self, sicaklik_c, basinc_hpa, nem_bagil):
        T_K = sicaklik_c + 273.15
        P_Pa = basinc_hpa * 100
        Es = self.saturated_vapor_pressure(sicaklik_c)
        E = (nem_bagil / 100) * Es
        Pd = P_Pa - E
        rho_d = Pd / (self.R_dry_air * T_K)
        rho_v = E / (self.R_water_vapor * T_K)
        return rho_d + rho_v

    # _get_forces ve _rk4_step (değişiklik yok)
    def _get_forces(self, pos, vel, params):
        m, d, bc = params['kutle'], params['cap'], params['bc']
        hava_yogunlugu, ruzgar_hizi = params['hava_yogunlugu'], params['ruzgar_hizi']
        ruzgar_acisi_rad = math.radians(params['ruzgar_acisi'])
        enlem_rad = math.radians(params['enlem'])
        mermi_spin_hizi = params['mermi_spin_hizi']
        
        wind_vel_x = ruzgar_hizi * math.cos(ruzgar_acisi_rad)
        wind_vel_y = ruzgar_hizi * math.sin(ruzgar_acisi_rad)
        relative_vel_x, relative_vel_y, relative_vel_z = vel[0] - wind_vel_x, vel[1] - wind_vel_y, vel[2]
        v_magn_relative = math.sqrt(relative_vel_x**2 + relative_vel_y**2 + relative_vel_z**2)
        
        F_grav_z = -m * self.g
        F_drag_x, F_drag_y, F_drag_z = 0, 0, 0
        if v_magn_relative > 0:
            alan = math.pi * (d / 2)**2
            sd_imperial = (m / alan) * 0.0014223
            form_factor_i = sd_imperial / bc if bc > 0 else float('inf')
            Cd_ref_G1 = self.get_drag_coefficient_g1(v_magn_relative)
            Cd_bullet = form_factor_i * Cd_ref_G1
            drag_force_magnitude = 0.5 * hava_yogunlugu * v_magn_relative**2 * alan * Cd_bullet
            F_drag_x = -drag_force_magnitude * (relative_vel_x / v_magn_relative)
            F_drag_y = -drag_force_magnitude * (relative_vel_y / v_magn_relative)
            F_drag_z = -drag_force_magnitude * (relative_vel_z / v_magn_relative)
        
        omega = 7.292115e-5
        f_coriolis_y = 2 * m * omega * vel[0] * math.sin(enlem_rad)
        f_coriolis_z = -2 * m * omega * vel[1] * math.sin(enlem_rad)
        
        f_spin_drift_y = 0.0
        if mermi_spin_hizi > 0 and v_magn_relative > 0:
            Sg = (0.00000002 * mermi_spin_hizi**2 * (params.get('mermi_uzunlugu_mm', d*4.5) / d)**2) / (hava_yogunlugu / 1.225)
            if Sg != 0:
                alan = math.pi * (d / 2)**2
                magnus_accel_y = (0.5 * hava_yogunlugu * v_magn_relative * alan * d * mermi_spin_hizi) / (2.0 * m * Sg)
                f_spin_drift_y = m * magnus_accel_y * 0.1
        
        return (F_drag_x, F_drag_y + f_coriolis_y + f_spin_drift_y, F_drag_z + F_grav_z + f_coriolis_z)

    def _rk4_step(self, current_pos, current_vel, params, dt):
        m = params['kutle']
        def derivatives(pos, vel):
            Fx, Fy, Fz = self._get_forces(pos, vel, params)
            return vel[0], vel[1], vel[2], Fx / m, Fy / m, Fz / m

        k1_vx, k1_vy, k1_vz, k1_ax, k1_ay, k1_az = derivatives(current_pos, current_vel)
        pos2 = (current_pos[0] + 0.5*dt*k1_vx, current_pos[1] + 0.5*dt*k1_vy, current_pos[2] + 0.5*dt*k1_vz)
        vel2 = (current_vel[0] + 0.5*dt*k1_ax, current_vel[1] + 0.5*dt*k1_ay, current_vel[2] + 0.5*dt*k1_az)
        k2_vx, k2_vy, k2_vz, k2_ax, k2_ay, k2_az = derivatives(pos2, vel2)
        pos3 = (current_pos[0] + 0.5*dt*k2_vx, current_pos[1] + 0.5*dt*k2_vy, current_pos[2] + 0.5*dt*k2_vz)
        vel3 = (current_vel[0] + 0.5*dt*k2_ax, current_vel[1] + 0.5*dt*k2_ay, current_vel[2] + 0.5*dt*k2_az)
        k3_vx, k3_vy, k3_vz, k3_ax, k3_ay, k3_az = derivatives(pos3, vel3)
        pos4 = (current_pos[0] + dt*k3_vx, current_pos[1] + dt*k3_vy, current_pos[2] + dt*k3_vz)
        vel4 = (current_vel[0] + dt*k3_ax, current_vel[1] + dt*k3_ay, current_vel[2] + dt*k3_az)
        k4_vx, k4_vy, k4_vz, k4_ax, k4_ay, k4_az = derivatives(pos4, vel4)

        new_pos = (current_pos[0] + (dt/6.0) * (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx),
                   current_pos[1] + (dt/6.0) * (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy),
                   current_pos[2] + (dt/6.0) * (k1_vz + 2*k2_vz + 2*k3_vz + k4_vz))
        new_vel = (current_vel[0] + (dt/6.0) * (k1_ax + 2*k2_ax + 2*k3_ax + k4_ax),
                   current_vel[1] + (dt/6.0) * (k1_ay + 2*k2_ay + 2*k3_ay + k4_ay),
                   current_vel[2] + (dt/6.0) * (k1_az + 2*k2_az + 2*k3_az + k4_az))
        return new_pos, new_vel


    # GÜNCELLENDİ: Fonksiyon artık 'silah_tipi' alıyor.
    def atis_hesapla(self, silah_tipi, mermi_tipi, atis_acisi, hedef_mesafe, 
                       ruzgar_hizi, ruzgar_acisi_derece, sicaklik_c, basinc_hpa, nem_bagil,
                       enlem_derece=41, durbun_yuksekligi_m=0.05, sifirlama_mesafesi=100, dt=0.002):

        if silah_tipi not in self.SILAH_PLATFORMLARI:
            raise ValueError(f"Bilinmeyen silah tipi: {silah_tipi}")
        if mermi_tipi not in self.MERMI_TIPLERI:
            raise ValueError(f"Bilinmeyen mermi tipi: {mermi_tipi}")

        silah = self.SILAH_PLATFORMLARI[silah_tipi]
        mermi = self.MERMI_TIPLERI[mermi_tipi]

        # YENİ: UYUMLULUK KONTROLÜ
        if mermi['kalibre'] not in silah['uyumlu_kalibreler']:
            raise ValueError(f"'{mermi_tipi}' mermisi, '{silah_tipi}' silahı ile uyumlu değil.")

        # YENİ: Silaha göre namlu çıkış hızı ve yiv seti ayarlanıyor
        efektif_hiz = mermi["hiz"] * (1 + silah["namlu_hiz_modifikatoru"])
        yiv_seti_m = silah["yiv_seti"] * 0.0254
        mermi_spin_hizi = (efektif_hiz * 2 * math.pi) / yiv_seti_m
        
        mermi_uzunlugu_mm = mermi["cap"] * 1000 * 4.5

        # --- Başlangıç Koşulları (Değişiklik yok) ---
        current_pos = [0.0, 0.0, -durbun_yuksekligi_m]
        atis_acisi_rad = math.radians(atis_acisi)
        current_vel = [efektif_hiz * math.cos(atis_acisi_rad), 0.0, efektif_hiz * math.sin(atis_acisi_rad)]
        
        hava_yogunlugu = self.hava_yogunlugu_hesapla(sicaklik_c, basinc_hpa, nem_bagil)
        
        params = {
            'kutle': mermi["kutle"], 'cap': mermi["cap"], 'bc': mermi["bc"],
            'hava_yogunlugu': hava_yogunlugu, 'ruzgar_hizi': ruzgar_hizi,
            'ruzgar_acisi': ruzgar_acisi_derece, 'enlem': enlem_derece,
            'mermi_spin_hizi': mermi_spin_hizi, 'mermi_uzunlugu_mm': mermi_uzunlugu_mm,
        }

        # Simülasyonun geri kalanı aynı mantıkla çalışır...
        zero_params = params.copy()
        zero_params.update({'ruzgar_hizi': 0.0, 'enlem': 0.0, 'mermi_spin_hizi': 0.0})
        pos_z, vel_z = [0.0, 0.0, -durbun_yuksekligi_m], list(current_vel)
        traj_points_z = []
        while pos_z[0] <= sifirlama_mesafesi and pos_z[2] > -20:
            traj_points_z.append(tuple(pos_z))
            pos_z, vel_z = self._rk4_step(pos_z, vel_z, zero_params, dt)
        
        zero_z_at_distance = -durbun_yuksekligi_m
        if len(traj_points_z) >= 2:
            p1_x, _, p1_z = traj_points_z[-2]; p2_x, _, p2_z = traj_points_z[-1]
            if p2_x > p1_x:
                zero_z_at_distance = p1_z + (p2_z - p1_z) * (sifirlama_mesafesi - p1_x) / (p2_x - p1_x)
        
        ucus_suresi, max_yukseklik = 0.0, -durbun_yuksekligi_m
        trajectory_points = []
        while current_pos[0] <= hedef_mesafe * 1.2 and current_pos[2] > -50:
            trajectory_points.append(tuple(current_pos))
            current_pos, current_vel = self._rk4_step(current_pos, current_vel, params, dt)
            ucus_suresi += dt
            if current_pos[2] > max_yukseklik: max_yukseklik = current_pos[2]
            if current_pos[0] >= hedef_mesafe:
                trajectory_points.append(tuple(current_pos))
                break
        
        final_y_sapma, final_z_sapma = 0.0, 0.0
        if len(trajectory_points) >= 2 and trajectory_points[-1][0] >= hedef_mesafe:
            p1_x, p1_y, p1_z = trajectory_points[-2]; p2_x, p2_y, p2_z = trajectory_points[-1]
            if p2_x > p1_x:
                ratio = (hedef_mesafe - p1_x) / (p2_x - p1_x)
                final_y_sapma = p1_y + (p2_y - p1_y) * ratio
                final_z_sapma = p1_z + (p2_z - p1_z) * ratio
        else: final_y_sapma, final_z_sapma = current_pos[1], current_pos[2]
        
        net_dikey_sapma_durbun_hattina_gore = final_z_sapma - zero_z_at_distance
        gerekli_yukselis_ayari_mil = -net_dikey_sapma_durbun_hattina_gore / (hedef_mesafe / 1000.0) if hedef_mesafe > 0 else 0
        gerekli_yanal_ayari_mil = -final_y_sapma / (hedef_mesafe / 1000.0) if hedef_mesafe > 0 else 0

        uyari_mesaji = ""
        if abs(gerekli_yukselis_ayari_mil) > self.max_dikey_ayar_mil / 2.0:
            uyari_mesaji += f"UYARI: Gerekli dikey ayar ({gerekli_yukselis_ayari_mil:.2f} Mil) dürbün limitini (±{self.max_dikey_ayar_mil / 2.0:.1f} Mil) aşıyor.\n"
        if abs(gerekli_yanal_ayari_mil) > self.max_yanal_ayar_mil / 2.0:
            uyari_mesaji += f"UYARI: Gerekli yanal ayar ({gerekli_yanal_ayari_mil:.2f} Mil) dürbün limitini (±{self.max_yanal_ayar_mil / 2.0:.1f} Mil) aşıyor.\n"
        if not (len(trajectory_points) > 0 and trajectory_points[-1][0] >= hedef_mesafe):
            uyari_mesaji += "UYARI: Mermi hedefe ulaşmadan yere çarptı.\n"

        return {
            "ucus_suresi_s": ucus_suresi,
            "max_yukseklik_m": max_yukseklik,
            "son_hiz_mps": math.sqrt(current_vel[0]**2 + current_vel[1]**2 + current_vel[2]**2),
            "hedef_mesafedeki_yanal_sapma_m": final_y_sapma, 
            "hedef_mesafedeki_dikey_sapma_durbun_hattina_gore_m": net_dikey_sapma_durbun_hattina_gore, 
            "gerekli_yukselis_ayari_mil": gerekli_yukselis_ayari_mil, 
            "gerekli_yanal_ayari_mil": gerekli_yanal_ayari_mil, 
            "uyari_mesaji": uyari_mesaji or "Hesaplama başarılı.",
            "detaylar": {
                "efektif_hiz_mps": efektif_hiz
            }
        }