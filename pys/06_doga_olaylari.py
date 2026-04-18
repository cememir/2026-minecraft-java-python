"""
06_doga_olaylari.py
━━━━━━━━━━━━━━━━━━━
🌋 DOĞA OLAYLARI SİMÜLASYONU

İçerik:
  • Aktif volkan (lav akışı)
  • Kar fırtınası (kar yağışı simülasyonu)
  • Göl oluşturma
  • Doğal mağara sistemi

Çalıştırma: python 06_doga_olaylari.py
"""

from mc_helper import *
import math, time, random

mc = baglan()


def volkan(yukseklik=25):
    """Aktif volkan inşa eder ve lav akıtır."""
    mesaj(mc, "§c🌋 Volkan oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 30, py, pz + 30

    # Volkan gövdesi (koni şekli)
    for y in range(yukseklik):
        yaricap = int((yukseklik - y) * 0.7) + 1
        for x in range(-yaricap - 1, yaricap + 2):
            for z in range(-yaricap - 1, yaricap + 2):
                uzaklik = math.sqrt(x*x + z*z)
                # Dış katman
                if uzaklik <= yaricap + 1:
                    blok = COBBLE if y < yukseklik - 3 else OBSIDYEN
                    mc.setBlock(cx+x, cy+y, cz+z, blok)

    # Krater (üst kısım boş)
    for dy in range(-3, 1):
        for x in range(-3, 4):
            for z in range(-3, 4):
                if x*x + z*z <= 9:
                    mc.setBlock(cx+x, cy+yukseklik+dy, cz+z, HAVA)

    # Krater tabanına lav
    for x in range(-2, 3):
        for z in range(-2, 3):
            if x*x + z*z <= 4:
                mc.setBlock(cx+x, cy+yukseklik-4, cz+z, LAV)

    mesaj(mc, "§c✔ Volkan hazır! Lav akışı başlıyor...")
    time.sleep(2)

    # Lav akışı animasyonu
    for dalga in range(5):
        mesaj(mc, f"§c🌋 Lav dalgası {dalga+1}!")

        # Rastgele yönlerde lav ak
        for _ in range(8):
            aci = random.uniform(0, 2 * math.pi)
            uzaklik = random.randint(2, 5)
            lx = cx + int(uzaklik * math.cos(aci))
            lz = cz + int(uzaklik * math.sin(aci))
            yüzey_y = cy + yukseklik - 3

            # Lav yavaşça aşağı iner
            for dy in range(yukseklik - 3):
                mc.setBlock(lx, yüzey_y - dy, lz, LAV)
                time.sleep(0.05)
                # Lav soğur (obsidyen olur)
                if dy > 3:
                    mc.setBlock(lx, yüzey_y - dy + 3, lz, OBSIDYEN)

        time.sleep(1)

    mesaj(mc, "§7✔ Volkan aktif! Yaklaşma!")


def kar_firtinasi(sure=20):
    """Oyuncunun etrafına kar yağdırır."""
    mesaj(mc, "§b❄ Kar Fırtınası Başlıyor!")
    bitis = time.time() + sure
    kar_konumlari = []

    try:
        while time.time() < bitis:
            px, py, pz = oyuncu_konum(mc)

            # Yeni kar taneleri oluştur
            for _ in range(15):
                kx = px + random.randint(-20, 20)
                kz = pz + random.randint(-20, 20)
                ky = py + random.randint(15, 30)
                mc.setBlock(kx, ky, kz, KAR)
                kar_konumlari.append((kx, ky, kz))

            # Kar taneleri aşağı düşsün
            yeni_konumlar = []
            for (kx, ky, kz) in kar_konumlari:
                mc.setBlock(kx, ky, kz, HAVA)
                yeni_ky = ky - 2
                if yeni_ky > py - 1:
                    mc.setBlock(kx, yeni_ky, kz, KAR)
                    yeni_konumlar.append((kx, yeni_ky, kz))
                else:
                    # Yere düştü → birikir
                    mc.setBlock(kx, py - 1, kz, KAR)

            kar_konumlari = yeni_konumlar
            time.sleep(0.15)

    except KeyboardInterrupt:
        pass

    # Kar tanelerini temizle (yerdekiler kalır)
    for (kx, ky, kz) in kar_konumlari:
        mc.setBlock(kx, ky, kz, HAVA)

    mesaj(mc, "§b✔ Kar fırtınası geçti!")


def göl_oluştur(yaricap=15):
    """Oyuncunun yakınına doğal görünümlü bir göl oluşturur."""
    mesaj(mc, "§9🏞️ Göl oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 25, py, pz + 25

    # Göl çukuru kaz
    for x in range(-yaricap, yaricap + 1):
        for z in range(-yaricap, yaricap + 1):
            uzaklik = math.sqrt(x*x + z*z)
            if uzaklik > yaricap:
                continue
            # Derinlik merkeze göre artar
            derinlik = int(4 * (1 - uzaklik / yaricap)) + 2
            for dy in range(derinlik):
                mc.setBlock(cx+x, cy-dy, cz+z, HAVA)

    # Su doldur
    for x in range(-yaricap, yaricap + 1):
        for z in range(-yaricap, yaricap + 1):
            if math.sqrt(x*x + z*z) <= yaricap:
                mc.setBlock(cx+x, cy-1, cz+z, SU)
                mc.setBlock(cx+x, cy,   cz+z, SU)

    # Kıyı: kum
    for x in range(-yaricap-2, yaricap+3):
        for z in range(-yaricap-2, yaricap+3):
            uzaklik = math.sqrt(x*x + z*z)
            if yaricap <= uzaklik <= yaricap + 2:
                mc.setBlock(cx+x, cy-1, cz+z, KUM)

    # Kıyı ağaçları
    for _ in range(8):
        aci = random.uniform(0, 2*math.pi)
        r   = yaricap + random.randint(3, 6)
        ax  = cx + int(r * math.cos(aci))
        az  = cz + int(r * math.sin(aci))
        for dy in range(random.randint(4, 7)):
            mc.setBlock(ax, cy + dy, az, AHŞAP)
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(3):
                    if abs(dx)+abs(dz)+abs(dy) <= 3:
                        mc.setBlock(ax+dx, cy+6+dy, az+dz, YAPRAK)

    mesaj(mc, "§9✔ Göl tamamlandı! Yüzebilirsin 🏊")


def mağara_sistemi(uzunluk=50):
    """Oyuncunun altında doğal görünümlü tünel mağarası oluşturur."""
    mesaj(mc, "§8🦇 Mağara sistemi oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)

    # Ana tünel (sallanarak ilerle)
    x, y, z = px + 10, py - 5, pz
    for adim in range(uzunluk):
        # Rastgele sapma
        x += random.randint(-1, 2)
        y += random.randint(-1, 1)
        z += random.randint(-1, 1)
        y = max(py - 20, min(py - 2, y))

        # Tünel (oval kesit)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx*dx + dy*dy*1.5 <= 6:
                    mc.setBlock(x+dx, y+dy, z, HAVA)

        # Ara sıra taş + ışık
        if adim % 10 == 0:
            mc.setBlock(x, y - 2, z, TAŞ)
            mc.setBlock(x, y + 2, z, PARLAYAN)

    # Giriş
    for dy in range(5):
        for dx in range(-2, 3):
            mc.setBlock(px + 10 + dx, py + dy - 3, pz, HAVA)
    mc.setBlock(px + 10, py - 5, pz, PARLAYAN)

    mesaj(mc, "§8✔ Mağara hazır! Gir ve keşfet! 🦇")


print("""
🌋 DOĞA OLAYLARI
━━━━━━━━━━━━━━━━
1 → Aktif Volkan (lav akışı)
2 → Kar Fırtınası (20 saniye)
3 → Göl Oluşturma
4 → Mağara Sistemi
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   volkan()
elif secim == "2": kar_firtinasi()
elif secim == "3": göl_oluştur()
elif secim == "4": mağara_sistemi()
else: print("Geçersiz seçim!")
