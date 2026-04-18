"""
02_gunes_sistemi.py
━━━━━━━━━━━━━━━━━━━
🪐 GÜNEŞ SİSTEMİ SİMÜLASYONU

Öğrenilen kavramlar:
  • Dairesel hareket: x = r*cos(t), z = r*sin(t)
  • Trigonometri (açı → koordinat)
  • Ölçek ve hız kavramı
  • Döngüsel animasyon

Çalıştırma: python 02_gunes_sistemi.py
"""

from mc_helper import *
import math, time

mc = baglan()

# Gezegen tanımları: (isim, yörünge_yarıçapı, hız_çarpanı, blok, data, boyut)
GEZEGENLER = [
    ("Merkür",  15, 4.0,  YÜN,     GRİ,          1),
    ("Venüs",   22, 1.6,  YÜN,     TURUNCU,       2),
    ("Dünya",   30, 1.0,  YÜN,     MAVİ,          2),
    ("Mars",    40, 0.5,  YÜN,     KIRMIZI,       2),
    ("Jüpiter", 55, 0.08, YÜN,     KAHVE,         4),
    ("Satürn",  68, 0.03, YÜN,     SARI,          3),
    ("Uranüs",  80, 0.01, YÜN,     AÇIK_MAVİ,     2),
    ("Neptün",  92, 0.006,YÜN,     MAVİ,          2),
]

def gunes_sistemi(sure=120):
    """
    Gezegenleri güneşin etrafında döndürür.
    sure: kaç saniye çalışsın
    """
    mesaj(mc, "§e☀ Güneş Sistemi başlatıldı!")
    px, py, pz = oyuncu_konum(mc)
    gx, gy, gz = px + 110, py + 40, pz + 110  # Güneş merkezi

    # Güneşi inşa et (büyük parlayan küre)
    mesaj(mc, "§7  Güneş inşa ediliyor...")
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            for dz in range(-5, 6):
                if dx*dx + dy*dy + dz*dz <= 25:
                    mc.setBlock(gx+dx, gy+dy, gz+dz, PARLAYAN)

    # Yörünge halkalarını çiz (dekoratif)
    mesaj(mc, "§7  Yörüngeler çiziliyor...")
    for (_, r, _, _, _, _) in GEZEGENLER:
        for aci in range(0, 360, 3):
            rad = math.radians(aci)
            ox = gx + int(r * math.cos(rad))
            oz = gz + int(r * math.sin(rad))
            mc.setBlock(ox, gy, oz, CAM)

    mesaj(mc, "§e✔ Hazır! Gezegenler dönüyor... (Ctrl+C ile durdur)")

    # Önceki gezegen konumları
    onceki = {isim: None for (isim, *_) in GEZEGENLER}
    t = 0
    bitis = time.time() + sure

    try:
        while time.time() < bitis:
            t += 0.05

            for (isim, r, hiz, blk, data, boyut) in GEZEGENLER:
                aci = t * hiz
                rad = math.radians(aci * 57.29578)  # radyan → derece → radyan
                rad = t * hiz  # direkt radyan kullan

                yeni_x = gx + int(r * math.cos(rad))
                yeni_z = gz + int(r * math.sin(rad))
                yeni_y = gy

                # Eski konumu sil
                if onceki[isim]:
                    ox, oy, oz = onceki[isim]
                    for dx in range(-boyut+1, boyut):
                        for dy in range(-boyut+1, boyut):
                            for dz in range(-boyut+1, boyut):
                                mc.setBlock(ox+dx, oy+dy, oz+dz, HAVA)

                # Yeni konuma çiz
                for dx in range(-boyut+1, boyut):
                    for dy in range(-boyut+1, boyut):
                        for dz in range(-boyut+1, boyut):
                            if dx*dx+dy*dy+dz*dz <= boyut*boyut:
                                mc.setBlock(yeni_x+dx, yeni_y+dy, yeni_z+dz,
                                            blk, data)

                # Dünya'ya Ay ekle
                if isim == "Dünya":
                    ay_r = 5
                    ay_rad = t * 3
                    ax = yeni_x + int(ay_r * math.cos(ay_rad))
                    az = yeni_z + int(ay_r * math.sin(ay_rad))
                    mc.setBlock(ax, yeni_y + 2, az, YÜN, BEYAZ)

                onceki[isim] = (yeni_x, yeni_y, yeni_z)

            time.sleep(0.08)

    except KeyboardInterrupt:
        pass

    mesaj(mc, "§cGüneş Sistemi durduruldu.")


def gezegen_bilgileri():
    """Gezegenleri sırayla havaya yazar (eğitici mod)."""
    mesaj(mc, "§6📚 Gezegen bilgileri yükleniyor...")
    px, py, pz = oyuncu_konum(mc)

    bilgiler = [
        ("MERKÜR", "En küçük gezegen!", YÜN, GRİ),
        ("VENÜS",  "En sıcak gezegen!", YÜN, TURUNCU),
        ("DÜNYA",  "Bizim evimiz!",      YÜN, MAVİ),
        ("MARS",   "Kırmızı Gezegen!",   YÜN, KIRMIZI),
    ]

    for i, (isim, bilgi, blk, renk) in enumerate(bilgiler):
        mesaj(mc, f"§e{isim}: §f{bilgi}")
        # Her gezegeni farklı yüksekliğe yaz
        dolu_kure(mc, px+15, py+10+i*15, pz+5, 3, blk, renk)
        time.sleep(1.5)

    mesaj(mc, "§6✔ Tüm gezegenler gösterildi!")


print("""
🪐 GÜNEŞ SİSTEMİ SİMÜLASYONU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 → Canlı Güneş Sistemi Animasyonu (2 dakika)
2 → Gezegen Bilgileri (eğitici mod)
""")

secim = input("Seçim (1-2): ").strip()
if secim == "1":   gunes_sistemi()
elif secim == "2": gezegen_bilgileri()
else: print("Geçersiz seçim!")
