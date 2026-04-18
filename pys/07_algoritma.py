"""
07_algoritma.py
━━━━━━━━━━━━━━━
💻 ALGORİTMA GÖRSELLEŞTIRICISI

Öğrenilen kavramlar:
  • Sıralama algoritmaları (Bubble, Selection, Quick)
  • İkili arama
  • Fraktallar (Sierpinski, Koch kar tanesi)
  • Recursion (özyineleme)

Çalıştırma: python 07_algoritma.py
"""

from mc_helper import *
import math, time, random

mc = baglan()


def dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=-1, vurgula_j=-1):
    """Diziyi Minecraft'ta dikey sütunlar halinde çizer."""
    for i, deger in enumerate(dizi):
        renk = SARI
        if i == vurgula_i: renk = KIRMIZI
        if i == vurgula_j: renk = YEŞİL
        if i < vurgula_i:  renk = MAVİ   # sıralanmış kısım

        # Eski sütunu sil
        for dy in range(max(dizi) + 2):
            mc.setBlock(x0 + i*2, y0 + dy, z0, HAVA)
        # Yeni sütunu çiz
        for dy in range(deger):
            mc.setBlock(x0 + i*2, y0 + dy, z0, YÜN, renk)


def bubble_sort():
    """Kabarcık sıralama — her adım görsel olarak gösterilir."""
    mesaj(mc, "§e🔢 Bubble Sort başlıyor!")
    mesaj(mc, "§7  Kırmızı=karşılaştırılan, Mavi=sıralanmış")

    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py, pz + 5

    dizi = random.sample(range(2, 18), 12)
    mesaj(mc, f"§7  Başlangıç: {dizi}")

    n = len(dizi)
    dizi_ciz(mc, dizi, x0, y0, z0)
    time.sleep(1)

    adim = 0
    for i in range(n):
        for j in range(n - i - 1):
            adim += 1
            dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=j, vurgula_j=j+1)
            time.sleep(0.3)

            if dizi[j] > dizi[j+1]:
                dizi[j], dizi[j+1] = dizi[j+1], dizi[j]
                dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=j, vurgula_j=j+1)
                time.sleep(0.2)

    dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=n)
    mesaj(mc, f"§e✔ Bubble Sort bitti! {adim} karşılaştırma yapıldı.")
    mesaj(mc, f"§7  Sonuç: {dizi}")


def selection_sort():
    """Seçim sıralama — her geçişte en küçüğü bulur."""
    mesaj(mc, "§9🔢 Selection Sort başlıyor!")
    mesaj(mc, "§7  Kırmızı=mevcut minimum, Yeşil=incelenen")

    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py, pz + 8

    dizi = random.sample(range(2, 18), 12)
    mesaj(mc, f"§7  Başlangıç: {dizi}")
    dizi_ciz(mc, dizi, x0, y0, z0)
    time.sleep(1)

    n = len(dizi)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=min_idx, vurgula_j=j)
            time.sleep(0.2)
            if dizi[j] < dizi[min_idx]:
                min_idx = j

        dizi[i], dizi[min_idx] = dizi[min_idx], dizi[i]
        dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=i+1)
        time.sleep(0.3)

    dizi_ciz(mc, dizi, x0, y0, z0)
    mesaj(mc, f"§9✔ Selection Sort bitti! Sonuç: {dizi}")


def ikili_arama():
    """
    Binary search — aranan değeri her adımda gösteren görsel demo.
    Sıralı dizide arama.
    """
    mesaj(mc, "§d🔍 İkili Arama Demo!")
    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py, pz + 12

    dizi = sorted(random.sample(range(1, 30), 15))
    hedef = random.choice(dizi)

    mesaj(mc, f"§7  Dizi: {dizi}")
    mesaj(mc, f"§e  Aranan: {hedef}")

    dizi_ciz(mc, dizi, x0, y0, z0)
    time.sleep(1)

    sol, sag = 0, len(dizi) - 1
    adim = 0

    while sol <= sag:
        adim += 1
        orta = (sol + sag) // 2
        dizi_ciz(mc, dizi, x0, y0, z0, vurgula_i=sol, vurgula_j=orta)

        mc.setBlock(x0 + orta*2, y0 + dizi[orta] + 1, z0, PARLAYAN)
        mesaj(mc, f"§7  Adım {adim}: sol={sol}, orta={orta}, sağ={sag}, dizi[orta]={dizi[orta]}")
        time.sleep(0.8)

        if dizi[orta] == hedef:
            mesaj(mc, f"§a✔ BULUNDU! {hedef} → indeks {orta}, {adim} adımda!")
            mc.setBlock(x0 + orta*2, y0 + dizi[orta] + 1, z0, ALTIN)
            break
        elif dizi[orta] < hedef:
            sol = orta + 1
        else:
            sag = orta - 1

    mesaj(mc, f"§d  Toplam adım: {adim} (lineer arama olsaydı: {dizi.index(hedef)+1})")


def sierpinski_ucgeni(n=6):
    """
    Sierpinski üçgeni fraktalı — özyinelemeli çizim.
    n: iterasyon sayısı (2-7 arası önerilir)
    """
    mesaj(mc, f"§6🔺 Sierpinski Üçgeni (n={n}) çiziliyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 5

    # Sierpinski chaos oyunu yöntemi
    boyut = 2 ** n
    noktalar = set()

    # 3 köşe
    A = (0,       0)
    B = (boyut,   0)
    C = (boyut//2, boyut)

    # Rastgele başla
    x, y = boyut // 2, boyut // 2

    for _ in range(50000):
        koseler = random.choice([A, B, C])
        x = (x + koseler[0]) // 2
        y = (y + koseler[1]) // 2
        noktalar.add((x, y))

    # Minecraft'a çiz
    for (x, y) in noktalar:
        mc.setBlock(ox + x, oy + y, oz, YÜN, TURUNCU)

    mesaj(mc, f"§6✔ Sierpinski üçgeni: {len(noktalar)} benzersiz nokta")


def koh_kar_tanesi(iterasyon=4):
    """Koch kar tanesi fraktalı."""
    mesaj(mc, f"§b❄ Koch Kar Tanesi (iterasyon={iterasyon}) çiziliyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 40, py + 5, pz + 5

    def koch_noktalar(p1, p2, n):
        if n == 0:
            return [p1, p2]
        ax, ay = p1
        bx, by = p2
        # 3'e böl
        p3 = ((2*ax + bx)/3, (2*ay + by)/3)
        p5 = ((ax + 2*bx)/3, (ay + 2*by)/3)
        # Üçgen tepesi
        mx, my = (ax+bx)/2, (ay+by)/2
        aci = math.atan2(by-ay, bx-ax) - math.pi/3
        uzun = math.sqrt((bx-ax)**2 + (by-ay)**2) / 3
        p4 = (p3[0] + uzun*math.cos(aci), p3[1] + uzun*math.sin(aci))

        noktalar = (koch_noktalar(p1, p3, n-1)[:-1] +
                    koch_noktalar(p3, p4, n-1)[:-1] +
                    koch_noktalar(p4, p5, n-1)[:-1] +
                    koch_noktalar(p5, p2, n-1))
        return noktalar

    boyut = 30
    p1 = (0, 0)
    p2 = (boyut, 0)
    p3 = (boyut/2, boyut * math.sqrt(3)/2)

    import sys; sys.setrecursionlimit(20000)

    for (pa, pb) in [(p1,p2), (p2,p3), (p3,p1)]:
        noktalar = koch_noktalar(pa, pb, iterasyon)
        for i in range(len(noktalar)-1):
            x1, y1 = noktalar[i]
            x2, y2 = noktalar[i+1]
            # Lineer interpolasyon
            adimlar = max(abs(int(x2-x1)), abs(int(y2-y1)), 1)
            for t in range(adimlar+1):
                bx = ox + int(x1 + (x2-x1)*t/adimlar)
                by = oy + int(y1 + (y2-y1)*t/adimlar)
                mc.setBlock(bx, by, oz, YÜN, AÇIK_MAVİ)

    mesaj(mc, "§b✔ Koch Kar Tanesi tamamlandı! ❄")


print("""
💻 ALGORİTMA GÖRSELLEŞTİRİCİSİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 → Bubble Sort (kabarcık sıralama)
2 → Selection Sort (seçim sıralama)
3 → Binary Search (ikili arama)
4 → Sierpinski Üçgeni (fraktal)
5 → Koch Kar Tanesi (fraktal)
""")

secim = input("Seçim (1-5): ").strip()
if secim == "1":   bubble_sort()
elif secim == "2": selection_sort()
elif secim == "3": ikili_arama()
elif secim == "4": sierpinski_ucgeni()
elif secim == "5": koh_kar_tanesi()
else: print("Geçersiz seçim!")
