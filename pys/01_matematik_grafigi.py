"""
01_matematik_grafigi.py
━━━━━━━━━━━━━━━━━━━━━━━
📐 MATEMATİK GRAFİKLERİ — Minecraft'ta canlı grafik çizici

Öğrenilen kavramlar:
  • Sinüs / Kosinüs dalgaları
  • Paraboller (y = x²)
  • 3D yüzey grafikleri
  • Koordinat sistemi

Çalıştırma: python 01_matematik_grafigi.py
"""

from mc_helper import *
import math

mc = baglan()

def sinüs_dalgası(genlik=8, frekans=0.3, uzunluk=60):
    """y = A * sin(f * x) grafiğini havaya çizer."""
    mesaj(mc, "§b📈 Sinüs dalgası çiziliyor...", "")
    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py + 20, pz

    # Eski grafiği sil
    temizle_alan(mc, x0, y0-genlik-2, z0, x0+uzunluk+2, y0+genlik+2, z0)

    # Eksenleri çiz
    for x in range(uzunluk + 5):
        mc.setBlock(x0 + x, y0, z0, DEMİR)        # X ekseni
    for y in range(-genlik-2, genlik+3):
        mc.setBlock(x0, y0 + y, z0, ALTIN)         # Y ekseni

    # Grafik noktalarını çiz
    for i in range(uzunluk):
        y_deger = int(genlik * math.sin(frekans * i))
        mc.setBlock(x0 + i, y0 + y_deger, z0, YÜN, MAVİ)
        # Altını doldur (alan gösterimi)
        if y_deger > 0:
            for dy in range(y_deger):
                mc.setBlock(x0 + i, y0 + dy, z0, YÜN, SİYAN)
        elif y_deger < 0:
            for dy in range(y_deger, 0):
                mc.setBlock(x0 + i, y0 + dy, z0, YÜN, KIRMIZI)

    mesaj(mc, "§b✔ Sinüs dalgası: y = 8 × sin(0.3x)")


def paraboller():
    """y = x², y = -x² + 20, y = 0.5x² parabollerini çizer."""
    mesaj(mc, "§e📈 Paraboller çiziliyor...", "")
    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py + 5, pz + 5

    temizle_alan(mc, x0-20, y0-2, z0-3, x0+20, y0+22, z0+3)

    for i in range(-15, 16):
        # y = x² / 8 (ölçeklendi)
        y1 = int(i*i / 8)
        mc.setBlock(x0 + i, y0 + y1, z0,     YÜN, SARI)

        # y = -x²/8 + 20
        y2 = int(-i*i / 8) + 20
        mc.setBlock(x0 + i, y0 + y2, z0 + 1, YÜN, YEŞİL)

        # y = 0.3 * x²
        y3 = int(0.3 * i*i)
        if 0 <= y3 <= 25:
            mc.setBlock(x0 + i, y0 + y3, z0 + 2, YÜN, EFLATUN)

    # Etiketler
    mc.setBlock(x0 + 16, y0 + 2,  z0,     ALTIN)
    mc.setBlock(x0 + 16, y0 + 18, z0 + 1, DEMİR)
    mc.setBlock(x0 + 16, y0 + 8,  z0 + 2, PARLAYAN)

    mesaj(mc, "§e✔ 3 parabol çizildi! Sarı: x², Yeşil: -x²+20, Mor: 0.3x²")


def üç_boyutlu_yüzey():
    """z = sin(x)*cos(y) 3D yüzey grafiği çizer."""
    mesaj(mc, "§d📈 3D Yüzey çiziliyor... (biraz sürebilir)", "")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 20, py + 15, pz + 20

    boyut = 20
    ölçek = 5

    for xi in range(-boyut, boyut, 2):
        for zi in range(-boyut, boyut, 2):
            x_rad = xi * 0.3
            z_rad = zi * 0.3
            y_deger = int(ölçek * math.sin(x_rad) * math.cos(z_rad))
            renk_i = (y_deger + ölçek) % len(GÖKKUŞAĞI)
            mc.setBlock(cx + xi, cy + y_deger, cz + zi,
                        YÜN, GÖKKUŞAĞI[renk_i])

    mesaj(mc, "§d✔ 3D yüzey: z = sin(x) × cos(y)")


def fibonacci_sarmalı():
    """Altın oran sarmalını blok olarak çizer."""
    mesaj(mc, "§6🐚 Fibonacci sarmalı çiziliyor...", "")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 5, py + 1, pz + 5

    # Fibonacci kareleri
    a, b = 1, 1
    x_offset, z_offset = 0, 0
    yön = 0  # 0=sağ, 1=yukarı, 2=sol, 3=aşağı
    blok_listesi = [YÜN, TUĞLA, AHŞAP, SANDSTONE, DEMİR, ALTIN]

    for i in range(8):
        boyut = a
        blok = blok_listesi[i % len(blok_listesi)]

        # Kareyi çiz
        for x in range(boyut):
            for z in range(boyut):
                bx = cx + x_offset + x
                bz = cz + z_offset + z
                mc.setBlock(bx, cy, bz, blok)
                # Kenar çizgisi
                kenar = (x == 0 or x == boyut-1 or z == 0 or z == boyut-1)
                mc.setBlock(bx, cy + 1, bz, OBSIDYEN if kenar else HAVA)

        # Sonraki kareye geç
        if yön == 0:   x_offset += boyut
        elif yön == 1: z_offset += boyut
        elif yön == 2: x_offset -= boyut
        elif yön == 3: z_offset -= boyut
        yön = (yön + 1) % 4

        a, b = b, a + b

    mesaj(mc, "§6✔ Fibonacci sarmalı tamamlandı! 1,1,2,3,5,8,13,21...")


print("""
📐 MATEMATİK GRAFİKLERİ
━━━━━━━━━━━━━━━━━━━━━━━
1 → Sinüs Dalgası
2 → Paraboller (3 farklı)
3 → 3D Yüzey Grafiği
4 → Fibonacci Sarmalı
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   sinüs_dalgası()
elif secim == "2": paraboller()
elif secim == "3": üç_boyutlu_yüzey()
elif secim == "4": fibonacci_sarmalı()
else: print("Geçersiz seçim!")
