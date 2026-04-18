"""
03_renk_lab.py
━━━━━━━━━━━━━━
🎨 RENK KARIŞTIRMA LABORATUVARI

Öğrenilen kavramlar:
  • RGB renk modeli
  • Ana renkler ve tamamlayıcı renkler
  • Renk gradyanları
  • Simetri ve desen oluşturma

Çalıştırma: python 03_renk_lab.py
"""

from mc_helper import *
import math

mc = baglan()

def renk_paleti():
    """16 yün rengini yan yana dizer, her rengin adını sohbete yazar."""
    mesaj(mc, "§d🎨 Renk paleti oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)

    renk_isimleri = [
        "Beyaz","Turuncu","Eflatun","Açık Mavi","Sarı",
        "Yeşil","Pembe","Gri","Açık Gri","Siyan",
        "Mor","Mavi","Kahve","Koyu Yeşil","Kırmızı","Siyah"
    ]

    for i in range(16):
        # 4x4 kare her renk için
        for dx in range(4):
            for dy in range(4):
                mc.setBlock(px + 5 + i*5 + dx, py + dy, pz + 3,
                            YÜN, i)
        # Üstüne yükseklik göstergesi
        mc.setBlock(px + 5 + i*5 + 2, py + 5, pz + 3, PARLAYAN)
        mesaj(mc, f"§7Renk {i}: {renk_isimleri[i]}")
        import time; time.sleep(0.1)

    mesaj(mc, "§d✔ 16 renk paleti tamamlandı!")


def gradyan_duvar(genislik=32, yukseklik=10):
    """Mavi→Kırmızı gradyan duvarı oluşturur."""
    mesaj(mc, "§b🌈 Gradyan duvarı çiziliyor...")
    px, py, pz = oyuncu_konum(mc)

    renk_sirasi = [MAVİ, SİYAN, YEŞİL, AÇIK_MAVİ, SARI, TURUNCU, KIRMIZI]
    dilim = genislik // len(renk_sirasi)

    for i, renk in enumerate(renk_sirasi):
        for dx in range(dilim):
            for dy in range(yukseklik):
                mc.setBlock(px + 5 + i*dilim + dx, py + dy, pz + 5,
                            YÜN, renk)

    mesaj(mc, "§b✔ Gradyan duvarı hazır! Renk skalasını incele.")


def mozaik_sanat():
    """Matematiksel desen: simetrik mozaik oluşturur."""
    mesaj(mc, "§e✨ Mozaik sanat oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)

    boyut = 20
    cx, cz = px + 5 + boyut, pz + boyut

    for x in range(boyut * 2):
        for z in range(boyut * 2):
            # Merkeze uzaklık
            dx, dz = x - boyut, z - boyut
            uzaklik = math.sqrt(dx*dx + dz*dz)
            aci = math.atan2(dz, dx)

            # Renk: uzaklık + açıya göre
            desen = int(uzaklik + aci * 3) % 16
            mc.setBlock(cx + dx, py, cz + dz, YÜN, desen)

    mesaj(mc, "§e✔ Mozaik tamamlandı! Üstten bak (F5 → yukarı bak).")


def gökkuşağı_kubesi():
    """Renk küpü: her yüzü farklı renkten dolgu."""
    mesaj(mc, "§6🌈 Gökkuşağı küpü inşa ediliyor...")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 10, py, pz + 10
    boyut = 10

    yüzler = [
        # (eksen, sabit_değer, renk)
        ("x_min", KIRMIZI),
        ("x_max", TURUNCU),
        ("y_min", SARI),
        ("y_max", YEŞİL),
        ("z_min", MAVİ),
        ("z_max", MOR),
    ]

    for x in range(boyut):
        for y in range(boyut):
            for z in range(boyut):
                kenar_x = (x == 0 or x == boyut-1)
                kenar_y = (y == 0 or y == boyut-1)
                kenar_z = (z == 0 or z == boyut-1)

                if not (kenar_x or kenar_y or kenar_z):
                    continue

                if x == 0:          renk = KIRMIZI
                elif x == boyut-1:  renk = TURUNCU
                elif y == 0:        renk = SARI
                elif y == boyut-1:  renk = YEŞİL
                elif z == 0:        renk = MAVİ
                else:               renk = MOR

                mc.setBlock(cx+x, cy+y, cz+z, YÜN, renk)

    mesaj(mc, "§6✔ 6 yüzü 6 farklı renkte küp tamamlandı!")


print("""
🎨 RENK KARIŞTIRMA LABORATUVARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 → 16 Renk Paleti
2 → Gradyan Duvar
3 → Mozaik Sanat (matematiksel desen)
4 → Gökkuşağı Küpü (6 yüz, 6 renk)
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   renk_paleti()
elif secim == "2": gradyan_duvar()
elif secim == "3": mozaik_sanat()
elif secim == "4": gökkuşağı_kubesi()
else: print("Geçersiz seçim!")
