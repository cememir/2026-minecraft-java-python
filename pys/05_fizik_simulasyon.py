"""
05_fizik_simulasyon.py
━━━━━━━━━━━━━━━━━━━━━━
⚗️ FİZİK SİMÜLASYONLARI

Öğrenilen kavramlar:
  • Serbest düşüş: y = y0 - ½gt²
  • Mermi hareketi (projectile motion)
  • Su dalgaları
  • Yerçekimi simülasyonu

Çalıştırma: python 05_fizik_simulasyon.py
"""

from mc_helper import *
import math, time

mc = baglan()


def serbest_dusus():
    """
    Bir blok yüksekten bırakılır ve yere düşer.
    y(t) = y0 - 0.5 * g * t²  formülü canlandırılır.
    """
    mesaj(mc, "§b⬇ Serbest Düşüş Deneyi!")
    mesaj(mc, "§7  y(t) = y0 - ½ × g × t²")
    px, py, pz = oyuncu_konum(mc)

    # 3 farklı yükseklikten aynı anda bırak
    baslangic_yukseklikleri = [40, 60, 80]
    renkler = [KIRMIZI, SARI, YEŞİL]
    g = 9.8  # yerçekimi ivmesi (ölçekli)

    # Başlangıç konumları
    for i, (y0, renk) in enumerate(zip(baslangic_yukseklikleri, renkler)):
        mc.setBlock(px + 5 + i*5, py + y0, pz + 5, YÜN, renk)

    mesaj(mc, "§e3... 2... 1... BIRAKILIYOR!")
    time.sleep(2)

    t = 0
    dt = 0.1
    onceki_y = list(baslangic_yukseklikleri)

    while any(y > 0 for y in onceki_y):
        t += dt
        time.sleep(0.05)

        for i, (y0, renk) in enumerate(zip(baslangic_yukseklikleri, renkler)):
            # Serbest düşüş formülü
            yeni_y = int(y0 - 0.5 * g * t*t)
            yeni_y = max(0, yeni_y)

            # Eski konumu sil
            mc.setBlock(px + 5 + i*5, py + onceki_y[i], pz + 5, HAVA)

            # Yeni konuma koy
            if yeni_y > 0:
                mc.setBlock(px + 5 + i*5, py + yeni_y, pz + 5, YÜN, renk)
            else:
                # Yere çarptı — küçük patlama efekti
                for dx in range(-1, 2):
                    for dz in range(-1, 2):
                        mc.setBlock(px+5+i*5+dx, py, pz+5+dz, YÜN, renk)
                mc.postToChat(f"§c💥 {baslangic_yukseklikleri[i]} bloktan düştü!")

            onceki_y[i] = yeni_y

    mesaj(mc, "§b✔ Hepsi yere çarptı! Hepsi aynı anda mı?")


def mermi_hareketi():
    """
    Farklı açılarda atılan mermilerin parabolik yolunu çizer.
    x(t) = v*cos(θ)*t
    y(t) = v*sin(θ)*t - ½*g*t²
    """
    mesaj(mc, "§e🎯 Mermi Hareketi Deneyi!")
    mesaj(mc, "§7  Hangi açıda en uzağa gider?")

    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 5

    açılar = [15, 30, 45, 60, 75]  # derece
    renkler = [KIRMIZI, TURUNCU, SARI, YEŞİL, MAVİ]
    v0 = 20  # başlangıç hızı (ölçekli)
    g  = 9.8

    for aci, renk in zip(açılar, renkler):
        rad = math.radians(aci)
        vx  = v0 * math.cos(rad)
        vy  = v0 * math.sin(rad)

        t = 0
        noktalar = []
        while True:
            x = int(vx * t)
            y = int(vy * t - 0.5 * g * t*t)
            if y < 0 or x > 100:
                break
            noktalar.append((ox + x, oy + y, oz))
            t += 0.1

        for (bx, by, bz) in noktalar:
            mc.setBlock(bx, by, bz, YÜN, renk)

        mesaj(mc, f"§7  {aci}° açısı: {max(int(p[0]-ox) for p in noktalar)} blok menzil")
        time.sleep(0.3)

    mesaj(mc, "§e✔ 45° açısı en uzağa gider! (Neden?)")


def su_dalgası():
    """
    Dairesel su dalgası animasyonu.
    y = A * sin(kr - ωt)
    """
    mesaj(mc, "§9🌊 Su Dalgası Animasyonu!")
    mesaj(mc, "§7  y = A × sin(k×r - ω×t)")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 20, py, pz + 20

    A = 4    # genlik
    k = 0.5  # dalga sayısı
    omega = 2  # açısal frekans
    boyut = 20

    bitis = time.time() + 15
    t = 0

    try:
        while time.time() < bitis:
            for x in range(-boyut, boyut + 1, 2):
                for z in range(-boyut, boyut + 1, 2):
                    r = math.sqrt(x*x + z*z)
                    y_dalga = int(A * math.sin(k * r - omega * t))
                    mc.setBlock(cx+x, cy + y_dalga, cz+z, SU)
                    # Alt bölümü temizle
                    for dy in range(-A-1, A+2):
                        if dy != y_dalga:
                            mc.setBlock(cx+x, cy+dy, cz+z, HAVA)

            t += 0.2
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    # Temizle
    temizle_alan(mc, cx-boyut-1, cy-A-2, cz-boyut-1,
                     cx+boyut+1, cy+A+2, cz+boyut+1)
    mesaj(mc, "§9✔ Dalga animasyonu bitti!")


def sarkaç():
    """Sarkaç hareketi: x = A*cos(ωt), periyot = 2π√(L/g)"""
    mesaj(mc, "§d⏱️ Sarkaç Deneyi!")
    mesaj(mc, "§7  Periyot T = 2π × √(L/g)")
    px, py, pz = oyuncu_konum(mc)

    # Sarkaç parametreleri
    oy_ust = py + 25  # üst bağlantı noktası
    L      = 20       # ip uzunluğu (blok)
    g      = 9.8
    A      = 15       # başlangıç açısı (derece)
    omega  = math.sqrt(g / L)
    T      = 2 * math.pi / omega

    mesaj(mc, f"§7  Periyot ≈ {T:.1f} saniye")

    # Destek yapısı
    for dy in range(5):
        mc.setBlock(px + 5, oy_ust + dy, pz + 5, AHŞAP)
    mc.setBlock(px + 5 - 3, oy_ust + 4, pz + 5, AHŞAP)
    mc.setBlock(px + 5 + 3, oy_ust + 4, pz + 5, AHŞAP)
    for dx in range(-3, 4):
        mc.setBlock(px + 5 + dx, oy_ust + 4, pz + 5, AHŞAP)

    onceki = None
    bitis = time.time() + T * 5  # 5 periyot göster

    try:
        t = 0
        while time.time() < bitis:
            # Küçük açı yaklaşımı: x(t) = A*cos(ωt)
            aci_rad = math.radians(A) * math.cos(omega * t)
            top_x   = int(L * math.sin(aci_rad))
            top_y   = int(-L * math.cos(aci_rad))

            bx = px + 5 + top_x
            by = oy_ust + top_y
            bz = pz + 5

            if onceki:
                ox2, oy2, oz2 = onceki
                # İp çiz (eski ipi sil)
                for dy in range(-L-2, 2):
                    mc.setBlock(px+5, oy_ust+dy, pz+5, HAVA)
                mc.setBlock(ox2, oy2, oz2, HAVA)

            # Yeni ip ve top
            for dy in range(min(by, oy_ust+4) - oy_ust + 1, 0):
                mc.setBlock(px+5, oy_ust+dy, pz+5, COBBLE)
            mc.setBlock(bx, by, bz, YÜN, KIRMIZI)

            onceki = (bx, by, bz)
            t += 0.1
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    mesaj(mc, "§d✔ Sarkaç deneyi bitti!")


print("""
⚗️ FİZİK SİMÜLASYONLARI
━━━━━━━━━━━━━━━━━━━━━━━━
1 → Serbest Düşüş (3 yükseklik, aynı anda)
2 → Mermi Hareketi (5 farklı açı)
3 → Su Dalgası Animasyonu
4 → Sarkaç Hareketi
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   serbest_dusus()
elif secim == "2": mermi_hareketi()
elif secim == "3": su_dalgası()
elif secim == "4": sarkaç()
else: print("Geçersiz seçim!")
