"""
10_ozel_efektler.py
━━━━━━━━━━━━━━━━━━━
✨ ÖZEL EFEKTLER & GÖSTERILER

İçerik:
  • Pro havai fişek gösterisi
  • Domino etkisi
  • Lazer ışın gösterisi
  • Matrix yağmuru (blok yağmur kodu)
  • Işık halkası animasyonu

Çalıştırma: python 10_ozel_efektler.py
"""

from mc_helper import *
import math, time, random

mc = baglan()


def pro_havai_fisek(sure=30):
    """Profesyonel havai fişek gösterisi — senkronize patlama desenleri."""
    mesaj(mc, "§e🎆 HAVAI FİŞEK GÖSTERİSİ BAŞLIYOR!")
    px, py, pz = oyuncu_konum(mc)
    bitis = time.time() + sure

    desenleri = ["küre", "yıldız", "halka", "kalp", "spiral"]

    def patlama_küre(cx, cy, cz, r, renk):
        noktalar = []
        for _ in range(60):
            u = random.uniform(0, 2*math.pi)
            v = random.uniform(0, math.pi)
            ir = random.uniform(r*0.7, r)
            x = cx + int(ir * math.sin(v) * math.cos(u))
            y = cy + int(ir * math.cos(v))
            z = cz + int(ir * math.sin(v) * math.sin(u))
            noktalar.append((x, y, z))
            mc.setBlock(x, y, z, YÜN, renk)
        return noktalar

    def patlama_yıldız(cx, cy, cz, r, renk):
        noktalar = []
        for kol in range(6):
            aci = math.radians(kol * 60)
            for ir in range(1, r+1):
                x = cx + int(ir * math.cos(aci))
                y = cy + random.randint(-1, 1)
                z = cz + int(ir * math.sin(aci))
                noktalar.append((x, y, z))
                mc.setBlock(x, y, z, YÜN, renk)
        return noktalar

    def patlama_halka(cx, cy, cz, r, renk):
        noktalar = []
        for aci in range(0, 360, 5):
            rad = math.radians(aci)
            x = cx + int(r * math.cos(rad))
            y = cy
            z = cz + int(r * math.sin(rad))
            noktalar.append((x, y, z))
            mc.setBlock(x, y, z, YÜN, renk)
        return noktalar

    def patlama_kalp(cx, cy, cz, ölçek, renk):
        noktalar = []
        for t_deg in range(0, 360, 5):
            t = math.radians(t_deg)
            # Kalp parametrik denklemi
            hx = int(ölçek * 16 * math.sin(t)**3)
            hy = int(ölçek * (13*math.cos(t) - 5*math.cos(2*t) -
                              2*math.cos(3*t) - math.cos(4*t)))
            noktalar.append((cx+hx, cy+hy, cz))
            mc.setBlock(cx+hx, cy+hy, cz, YÜN, renk)
        return noktalar

    patlama_fonksiyonları = [patlama_küre, patlama_yıldız, patlama_halka, patlama_kalp]
    tüm_renkler = list(range(16))

    try:
        while time.time() < bitis:
            # Rastgele patlama noktası
            fx = px + random.randint(-15, 15)
            fy = py + random.randint(20, 40)
            fz = pz + random.randint(-15, 15)
            r  = random.randint(4, 9)
            renk = random.choice(tüm_renkler)
            fonk = random.choice(patlama_fonksiyonları)

            noktalar = fonk(fx, fy, fz, r, renk)
            time.sleep(0.6)

            # Sön
            for (x, y, z) in noktalar:
                mc.setBlock(x, y, z, HAVA)

            time.sleep(0.2)

    except KeyboardInterrupt:
        pass

    mesaj(mc, "§e🎆 Gösteri bitti!")


def domino_etkisi(uzunluk=30):
    """Dominolar sırayla devrilir animasyonu."""
    mesaj(mc, "§6🁣 Domino sırası kuruluyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 5

    # Dominoları dik olarak yerleştir
    for i in range(uzunluk):
        for dy in range(4):
            mc.setBlock(ox + i*3, oy + dy, oz, YÜN, BEYAZ)
        # Siyah benekler
        mc.setBlock(ox + i*3, oy + 1, oz, YÜN, SİYAH)
        mc.setBlock(ox + i*3, oy + 3, oz, YÜN, SİYAH)

    mesaj(mc, "§e3... 2... 1... İLK DOMİNO İTİLİYOR!")
    time.sleep(2)

    # Devrilme animasyonu
    for i in range(uzunluk):
        # Dikey dominoyu sil
        for dy in range(4):
            mc.setBlock(ox + i*3, oy + dy, oz, HAVA)

        # Yatay yat (devrildi)
        for dx in range(4):
            mc.setBlock(ox + i*3 + dx, oy, oz, YÜN, BEYAZ)
        mc.setBlock(ox + i*3 + 1, oy, oz, YÜN, SİYAH)
        mc.setBlock(ox + i*3 + 3, oy, oz, YÜN, SİYAH)

        mc.postToChat(f"§6💥 Domino {i+1}!")
        time.sleep(0.25)

    mesaj(mc, "§6✔ Tüm dominolar devrildi!")


def lazer_gosterisi(sure=20):
    """Dönen lazer ışınları gösterisi."""
    mesaj(mc, "§b💫 Lazer Gösterisi!")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 15, py + 5, pz + 15

    uzunluk = 20
    ışın_renkleri = [KIRMIZI, YEŞİL, MAVİ, SARI, MOR]
    ışın_sayisi = len(ışın_renkleri)

    onceki_ışınlar = [[] for _ in range(ışın_sayisi)]
    t = 0
    bitis = time.time() + sure

    try:
        while time.time() < bitis:
            for i, renk in enumerate(ışın_renkleri):
                # Eski ışını sil
                for (x, y, z) in onceki_ışınlar[i]:
                    mc.setBlock(x, y, z, HAVA)
                onceki_ışınlar[i].clear()

                # Yeni ışın çiz
                aci = t + (i * 2 * math.pi / ışın_sayisi)
                yeni_noktalar = []
                for r in range(uzunluk):
                    x = cx + int(r * math.cos(aci))
                    z = cz + int(r * math.sin(aci))
                    y = cy + int(3 * math.sin(t + r * 0.3))
                    mc.setBlock(x, y, z, YÜN, renk)
                    yeni_noktalar.append((x, y, z))

                onceki_ışınlar[i] = yeni_noktalar

            t += 0.15
            time.sleep(0.08)

    except KeyboardInterrupt:
        pass

    # Temizle
    for ışın in onceki_ışınlar:
        for (x, y, z) in ışın:
            mc.setBlock(x, y, z, HAVA)

    mesaj(mc, "§b✔ Lazer gösterisi bitti!")


def matris_yagmuru(sure=15):
    """
    Matrix filminden ilham — düşen yeşil bloklar.
    Dijital yağmur efekti.
    """
    mesaj(mc, "§2💻 Matrix Yağmuru!")
    px, py, pz = oyuncu_konum(mc)

    sütun_sayisi = 20
    sütunlar = []

    # Sütun başlangıç konumları
    for i in range(sütun_sayisi):
        sx = px + random.randint(-15, 15)
        sz = pz + random.randint(-5, 20)
        sy = py + random.randint(5, 40)
        hiz = random.choice([1, 1, 2])
        renk = random.choice([YEŞİL, KOYU_YEŞİL, AÇIK_MAVİ])
        sütunlar.append({
            "x": sx, "y": sy, "z": sz,
            "hiz": hiz, "renk": renk,
            "uzunluk": random.randint(3, 8),
            "yagmur": []
        })

    bitis = time.time() + sure

    try:
        while time.time() < bitis:
            for sut in sütunlar:
                # Eski blokları sil (kuyruğun sonunu)
                if len(sut["yagmur"]) >= sut["uzunluk"]:
                    eski = sut["yagmur"].pop(0)
                    mc.setBlock(eski[0], eski[1], eski[2], HAVA)

                # Yeni baş blok
                mc.setBlock(sut["x"], sut["y"], sut["z"], YÜN, sut["renk"])
                sut["yagmur"].append((sut["x"], sut["y"], sut["z"]))

                # Aşağı in
                sut["y"] -= sut["hiz"]

                # Yere ulaştıysa yukarıdan yeniden başla
                if sut["y"] < py - 5:
                    sut["y"]  = py + random.randint(20, 45)
                    sut["x"]  = px + random.randint(-15, 15)
                    sut["z"]  = pz + random.randint(-5, 20)
                    sut["renk"] = random.choice([YEŞİL, KOYU_YEŞİL, AÇIK_MAVİ])

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    # Temizle
    for sut in sütunlar:
        for (x, y, z) in sut["yagmur"]:
            mc.setBlock(x, y, z, HAVA)

    mesaj(mc, "§2✔ Kırmızı mı mavi mi seçerdin? 🔴🔵")


def işık_halkası(sure=15):
    """Oyuncunun etrafında dönen ışık halkaları."""
    mesaj(mc, "§e✨ Işık Halkası!")
    onceki = []
    t = 0
    bitis = time.time() + sure
    renkler = GÖKKUŞAĞI

    try:
        while time.time() < bitis:
            px, py, pz = oyuncu_konum(mc)

            # Eski halkaları sil
            for (x, y, z) in onceki:
                mc.setBlock(x, y, z, HAVA)
            onceki.clear()

            # 3 halka farklı düzlemlerde
            for halka_no in range(3):
                r       = 5 + halka_no * 2
                y_ofset = halka_no * 3
                aci_ofset = t + halka_no * math.pi / 3

                for aci_deg in range(0, 360, 10):
                    aci = math.radians(aci_deg) + aci_ofset
                    renk = renkler[int(aci_deg / (360/len(renkler)))]

                    if halka_no == 0:    # Yatay halka
                        x = px + int(r * math.cos(aci))
                        y = py + 3
                        z = pz + int(r * math.sin(aci))
                    elif halka_no == 1:  # Dikey halka (XY)
                        x = px + int(r * math.cos(aci))
                        y = py + 4 + int(r * math.sin(aci))
                        z = pz + y_ofset
                    else:               # Eğik halka (YZ)
                        x = px + y_ofset
                        y = py + 4 + int(r * math.sin(aci))
                        z = pz + int(r * math.cos(aci))

                    mc.setBlock(x, y, z, YÜN, renk)
                    onceki.append((x, y, z))

            t += 0.2
            time.sleep(0.08)

    except KeyboardInterrupt:
        pass

    for (x, y, z) in onceki:
        mc.setBlock(x, y, z, HAVA)

    mesaj(mc, "§e✔ Işık gösterisi bitti!")


print("""
✨ ÖZEL EFEKTLER
━━━━━━━━━━━━━━━━
1 → Pro Havai Fişek Gösterisi (30 sn)
2 → Domino Etkisi
3 → Lazer Gösterisi (20 sn)
4 → Matrix Yağmuru (15 sn)
5 → Işık Halkası (15 sn)
""")

secim = input("Seçim (1-5): ").strip()
if secim == "1":   pro_havai_fisek()
elif secim == "2": domino_etkisi()
elif secim == "3": lazer_gosterisi()
elif secim == "4": matris_yagmuru()
elif secim == "5": işık_halkası()
else: print("Geçersiz seçim!")
