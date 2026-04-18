"""
09_cografya.py
━━━━━━━━━━━━━━
🌍 COĞRAFYA DERSİ

Öğrenilen kavramlar:
  • Koordinat sistemi
  • Renk kodlaması (yükseklik haritası)
  • Coğrafi yapılar (dağ, vadi, delta)
  • Ülke bayrakları

Çalıştırma: python 09_cografya.py
"""

from mc_helper import *
import math, random

mc = baglan()


def yukseklik_haritasi(boyut=40):
    """
    Gerçekçi arazi yükseklik haritası.
    Renk → yükseklik ilişkisini gösterir:
      Mavi = deniz, Sarı = kıyı, Yeşil = ova, Kahve = dağ, Beyaz = zirve
    """
    mesaj(mc, "§2🗺️ Yükseklik haritası oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 5

    # Perlin benzeri rastgele arazi (basit octave noise)
    def gürültü(x, z, ölçek=0.08):
        val = (math.sin(x*ölçek*1.3 + 0.7) *
               math.cos(z*ölçek*1.1 + 0.3) +
               math.sin(x*ölçek*2.5 + 1.2) *
               math.cos(z*ölçek*2.3 + 0.8) * 0.5 +
               math.sin(x*ölçek*5.0 + 2.1) *
               math.cos(z*ölçek*4.8 + 1.5) * 0.25)
        return (val + 1.75) / 3.5  # 0-1 arasına normalize

    for x in range(boyut):
        for z in range(boyut):
            h = gürültü(x, z)

            # Renk ve yükseklik eşlemesi
            if h < 0.3:
                renk, y_offset = MAVİ,       0     # Derin deniz
            elif h < 0.38:
                renk, y_offset = SİYAN,      0     # Sığ deniz
            elif h < 0.45:
                renk, y_offset = SARI,       1     # Kıyı/Plaj
            elif h < 0.6:
                renk, y_offset = YEŞİL,      2     # Ova
            elif h < 0.72:
                renk, y_offset = KOYU_YEŞİL, 4     # Orman
            elif h < 0.85:
                renk, y_offset = KAHVE,      7     # Dağ
            elif h < 0.93:
                renk, y_offset = GRİ,        10    # Yüksek dağ
            else:
                renk, y_offset = BEYAZ,      14    # Kar örtüsü

            mc.setBlock(ox+x, oy + y_offset, oz+z, YÜN, renk)

    mesaj(mc, "§2✔ Arazi haritası tamamlandı!")
    mesaj(mc, "§7  Mavi=Deniz Sarı=Kıyı Yeşil=Ova Kahve=Dağ Beyaz=Zirve")


def türk_bayragi():
    """Türk bayrağını blokla çizer."""
    mesaj(mc, "🇹🇷 Türk bayrağı çiziliyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 3

    EN, BOY = 30, 20

    # Kırmızı zemin
    for x in range(EN):
        for y in range(BOY):
            mc.setBlock(ox+x, oy+y, oz, YÜN, KIRMIZI)

    # Beyaz ay (yarım daire) — merkezden hesapla
    ay_cx, ay_cy = 10, BOY // 2
    ay_r_dis = 6
    ay_r_ic  = 5
    ic_offset = 2  # İç daire ofset (hilal için)

    for x in range(EN):
        for y in range(BOY):
            dx, dy = x - ay_cx, y - ay_cy
            dış = dx*dx + dy*dy <= ay_r_dis**2
            iç  = (dx - ic_offset)**2 + dy*dy <= ay_r_ic**2
            if dış and not iç:
                mc.setBlock(ox+x, oy+y, oz, YÜN, BEYAZ)

    # Beyaz yıldız (5 köşeli)
    yıldız_cx, yıldız_cy = 18, BOY // 2
    for aci in range(0, 360, 1):
        rad = math.radians(aci)
        # 5 köşeli yıldız: iç ve dış yarıçap
        köşe_no = int(aci / 36) % 2
        r = 3 if köşe_no == 0 else 1.5
        x = yıldız_cx + int(r * math.cos(rad - math.pi/2))
        y = yıldız_cy + int(r * math.sin(rad - math.pi/2))
        if 0 <= x < EN and 0 <= y < BOY:
            mc.setBlock(ox+x, oy+y, oz, YÜN, BEYAZ)

    mesaj(mc, "🇹🇷 Türk bayrağı tamamlandı!")


def dağ_silsilesi(uzunluk=60):
    """
    Gerçekçi dağ silsilesi profili çizer.
    Oyuncu yanından bakınca sılüet görebilir.
    """
    mesaj(mc, "⛰️ Dağ silsilesi oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 10

    # Çoklu frekans ile dağ profili
    for x in range(uzunluk):
        h = (
            20 * math.sin(x * 0.05 + 0.5) +      # Ana dağ
            10 * math.sin(x * 0.13 + 1.2) +       # Orta tepe
             5 * math.sin(x * 0.27 + 2.3) +       # Küçük çıkıntılar
             2 * math.sin(x * 0.55 + 0.8)         # Pürüzlülük
        )
        h = max(0, int(h) + 22)  # Minimum 0, pozitife kaydır

        for y in range(h):
            # Yüksekliğe göre renk
            if y < h // 3:
                blok, data = TAŞ, 0        # Kaya tabanı
            elif y < int(h * 0.75):
                blok, data = YÜN, KOYU_YEŞİL   # Yamaç
            elif y < h - 3:
                blok, data = YÜN, GRİ      # Kayalık
            else:
                blok, data = YÜN, BEYAZ    # Kar
            mc.setBlock(ox+x, oy+y, oz, blok, data)

    mesaj(mc, "⛰️ Dağ silsilesi tamamlandı!")


def nehir_delta():
    """
    Nil deltasına benzer nehir ağzı oluşturur.
    Kıyısında tarım arazileri.
    """
    mesaj(mc, "🌊 Nehir deltası oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py - 1, pz + 5

    boyut = 35

    # Zemin: çimen
    for x in range(-5, boyut + 10):
        for z in range(-5, boyut + 10):
            mc.setBlock(ox+x, oy, oz+z, ÇIMEN)

    # Ana nehir gövdesi (z ekseninde)
    for z in range(boyut):
        genislik = 3 + z // 10
        for x in range(-genislik, genislik+1):
            mc.setBlock(ox + boyut//2 + x, oy, oz+z, SU)

    # Delta kolları (denize açılır)
    delta_baslangic = boyut - 15
    for kol, aci_fark in [(0, -20), (1, 0), (2, 20)]:
        for adim in range(20):
            aci = math.radians(90 + aci_fark)
            kol_x = ox + boyut//2 + int(adim * math.cos(aci))
            kol_z = oz + delta_baslangic + int(adim * math.sin(aci))
            genislik = 1 + adim // 5
            for dx in range(-genislik, genislik+1):
                mc.setBlock(kol_x+dx, oy, kol_z, SU)

    # Tarım arazileri (nehir kenarı)
    tarla_renkleri = [KOYU_YEŞİL, YEŞİL, SARI, KAHVE]
    for i in range(6):
        tx = ox + 3 + i * 5
        for z in range(10, 30):
            mc.setBlock(tx, oy, oz+z, YÜN, tarla_renkleri[i%4])
        tx2 = ox + boyut - 3 - i * 5
        for z in range(10, 30):
            mc.setBlock(tx2, oy, oz+z, YÜN, tarla_renkleri[(i+2)%4])

    mesaj(mc, "🌊 Nehir deltası tamamlandı! Üstten bak!")


print("""
🌍 COĞRAFYA DERSİ
━━━━━━━━━━━━━━━━━
1 → Yükseklik Haritası (arazi + renk kodlaması)
2 → Türk Bayrağı
3 → Dağ Silsilesi
4 → Nehir Deltası
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   yukseklik_haritasi()
elif secim == "2": türk_bayragi()
elif secim == "3": dağ_silsilesi()
elif secim == "4": nehir_delta()
else: print("Geçersiz seçim!")
