"""
04_mimari.py
━━━━━━━━━━━━
🏛️ MİMARİ YAPILAR

Öğrenilen kavramlar:
  • Mimari oran ve simetri
  • Döngülerle yapı inşası
  • Katmanlı (layer-by-layer) inşaat
  • Gerçek yapı tasarımı

Yapılar: Kale, Gotik Katedral, Roma Tapınağı, Japon Pagodası
Çalıştırma: python 04_mimari.py
"""

from mc_helper import *
import math

mc = baglan()

# ── Kale ────────────────────────────────────────────────────────────

def kale():
    """4 kuleli surlu kale inşa eder."""
    mesaj(mc, "§7🏰 Kale inşa ediliyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 5

    EN, BOY = 30, 30
    SUR_Y   = 12
    KULEr   = 6

    def sur_bloğu(x, y, z):
        # Mazgal (üst kısımda her 2 blokta bir boşluk)
        if y >= SUR_Y - 2 and (x + z) % 2 == 0:
            return HAVA
        return COBBLE

    # Sur duvarları (setBlocks ile optimize edildi)
    mc.setBlocks(ox, oy, oz, ox + EN, oy + SUR_Y - 1, oz, COBBLE)           # Ön duvar
    mc.setBlocks(ox, oy, oz + BOY, ox + EN, oy + SUR_Y - 1, oz + BOY, COBBLE) # Arka duvar
    mc.setBlocks(ox, oy, oz, ox, oy + SUR_Y - 1, oz + BOY, COBBLE)           # Sol duvar
    mc.setBlocks(ox + EN, oy, oz, ox + EN, oy + SUR_Y - 1, oz + BOY, COBBLE) # Sağ duvar

    # Mazgal (mazgal kısımlarında hava boşlukları)
    for x in range(0, EN + 1, 2):
        mc.setBlock(ox + x, oy + SUR_Y - 1, oz, HAVA)
        mc.setBlock(ox + x, oy + SUR_Y - 1, oz + BOY, HAVA)
    for z in range(0, BOY + 1, 2):
        mc.setBlock(ox, oy + SUR_Y - 1, oz + z, HAVA)
        mc.setBlock(ox + EN, oy + SUR_Y - 1, oz + z, HAVA)

    # Köşe kuleler (daha yüksek)
    for (kx, kz) in [(ox, oz), (ox+EN, oz), (ox, oz+BOY), (ox+EN, oz+BOY)]:
        for y in range(SUR_Y + KULEr):
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    kenar = abs(dx) == 2 or abs(dz) == 2
                    if not kenar:
                        continue
                    mazgal = (y >= SUR_Y + KULEr - 2 and (dx + dz) % 2 == 0)
                    mc.setBlock(kx+dx, oy+y, kz+dz,
                                HAVA if mazgal else COBBLE)
        # Kule bayrağı
        for dy in range(4):
            mc.setBlock(kx, oy + SUR_Y + KULEr + dy, kz, AHŞAP)
        mc.setBlock(kx + 1, oy + SUR_Y + KULEr + 3, kz, YÜN, KIRMIZI)

    # Ana kapı
    kapı_x = ox + EN // 2
    for dy in range(4):
        for dz in range(-1, 2):
            mc.setBlock(kapı_x, oy + dy, oz + dz, HAVA)
    # Kapı kemeri
    for dz in range(-2, 3):
        mc.setBlock(kapı_x - 1, oy + 4, oz + dz, COBBLE)
        mc.setBlock(kapı_x + 1, oy + 4, oz + dz, COBBLE)
    mc.setBlock(kapı_x, oy + 5, oz, COBBLE)

    # İç zemin
    mc.setBlocks(ox + 1, oy - 1, oz + 1, ox + EN - 1, oy - 1, oz + BOY - 1, TAŞ)

    # Şato binası (iç yapı)
    for x in range(8, 22):
        for z in range(8, 22):
            for y in range(10):
                kenar = (x == 8 or x == 21 or z == 8 or z == 21)
                if kenar:
                    mc.setBlock(ox + x, oy + y, oz + z, TUĞLA)
    # Şato çatısı
    for x in range(8, 22):
        for z in range(8, 22):
            mc.setBlock(ox + x, oy + 10, oz + z, AHŞAP)

    mesaj(mc, "§7✔ Kale tamamlandı! Kapıdan içeri gir.")


# ── Roma Tapınağı ────────────────────────────────────────────────────

def roma_tapinagi():
    """Sütunlu Roma tapınağı inşa eder."""
    mesaj(mc, "§e🏛️ Roma Tapınağı inşa ediliyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz + 5

    EN, BOY, YUK = 20, 30, 15

    # Merdivenler (3 basamak)
    for basamak in range(3):
        mc.setBlocks(ox - basamak, oy + basamak - 1, oz - basamak, 
                     ox + EN + basamak, oy + basamak - 1, oz + BOY + basamak, SANDSTONE)

    # Zemin platform
    mc.setBlocks(ox, oy + 2, oz, ox + EN, oy + 2, oz + BOY, SANDSTONE)

    # Sütunlar (ön ve arka sıra)
    sutun_aralik = 4
    for ix in range(0, EN + 1, sutun_aralik):
        for iz in [0, BOY]:
            for dy in range(YUK):
                mc.setBlock(ox + ix, oy + 3 + dy, oz + iz, SANDSTONE)
            # Sütun başlığı
            for dx in range(-1, 2):
                for dz in range(-1, 2):
                    mc.setBlock(ox+ix+dx, oy+3+YUK,   oz+iz+dz, SANDSTONE)
                    mc.setBlock(ox+ix+dx, oy+3+YUK+1, oz+iz+dz, SANDSTONE)

    # Yan sütunlar
    for iz in range(sutun_aralik, BOY, sutun_aralik):
        for ix in [0, EN]:
            for dy in range(YUK):
                mc.setBlock(ox + ix, oy + 3 + dy, oz + iz, SANDSTONE)

    # Üst kiriş (entablatür)
    for x in range(-1, EN + 2):
        for z in range(-1, BOY + 2):
            mc.setBlock(ox + x, oy + 3 + YUK + 2, oz + z, SANDSTONE)
            mc.setBlock(ox + x, oy + 3 + YUK + 3, oz + z, SANDSTONE)

    # Üçgen alın (pediment)
    ped_yuk = 6
    for dy in range(ped_yuk):
        sol = dy
        sag = EN - dy
        for x in range(sol, sag + 1):
            mc.setBlock(ox + x, oy + 3 + YUK + 4 + dy, oz,    SANDSTONE)
            mc.setBlock(ox + x, oy + 3 + YUK + 4 + dy, oz+BOY, SANDSTONE)

    # İç Cella (tapınak odası)
    for x in range(3, EN - 2):
        for z in range(3, BOY - 2):
            for y in range(YUK - 2):
                kenar = (x == 3 or x == EN-3 or z == 3 or z == BOY-3)
                if kenar:
                    mc.setBlock(ox+x, oy+3+y, oz+z, TAŞ)

    # Sunak / altar
    dolu_kure(mc, ox + EN//2, oy + 5, oz + BOY//2, 2, ALTIN)

    mesaj(mc, "§e✔ Roma Tapınağı tamamlandı! Kültürel miras!")


# ── Japon Pagodası ───────────────────────────────────────────────────

def pagoda(kat_sayisi=5):
    """Geleneksel Japon pagodası inşa eder."""
    mesaj(mc, "§c⛩️ Japon Pagodası inşa ediliyor...")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 10, py, pz + 10

    for kat in range(kat_sayisi):
        boyut  = (kat_sayisi - kat) * 3 + 2
        y_baz  = cy + kat * 6

        # Duvarlar
        for x in range(-boyut, boyut + 1):
            for z in range(-boyut, boyut + 1):
                kenar = abs(x) == boyut or abs(z) == boyut
                if not kenar: continue
                for dy in range(5):
                    mc.setBlock(cx+x, y_baz+dy, cz+z, AHŞAP)

        # Çıkıntılı çatı (eave)
        cati_boyut = boyut + 2
        for x in range(-cati_boyut, cati_boyut + 1):
            for z in range(-cati_boyut, cati_boyut + 1):
                # Çatı eğimi: köşeler daha alçak
                uzaklik = max(abs(x), abs(z))
                dy_cati = cati_boyut - uzaklik
                if dy_cati >= 0:
                    mc.setBlock(cx+x, y_baz+5+dy_cati, cz+z, YÜN, KIRMIZI)

        # Zemin
        for x in range(-boyut, boyut + 1):
            for z in range(-boyut, boyut + 1):
                mc.setBlock(cx+x, y_baz-1, cz+z, AHŞAP)

    # Tepe süsü
    tepe_y = cy + kat_sayisi * 6 + 3
    for dy in range(5):
        mc.setBlock(cx, tepe_y + dy, cz, ALTIN)
    mc.setBlock(cx, tepe_y + 5, cz, PARLAYAN)

    mesaj(mc, f"§c✔ {kat_sayisi} katlı Pagoda tamamlandı!")


# ── Köprü ────────────────────────────────────────────────────────────

def askili_kopru(uzunluk=40):
    """Kablo askılı modern köprü inşa eder."""
    mesaj(mc, "§9🌉 Askılı köprü inşa ediliyor...")
    px, py, pz = oyuncu_konum(mc)
    ox, oy, oz = px + 5, py, pz

    # Kule yüksekliği
    KULEr_Y = 18

    # Köprü tabliyesi (yol)
    for x in range(uzunluk + 1):
        for z in range(-2, 3):
            mc.setBlock(ox + x, oy, oz + z, COBBLE)
        # Korkuluklar
        mc.setBlock(ox + x, oy + 1, oz - 2, DEMİR)
        mc.setBlock(ox + x, oy + 1, oz + 2, DEMİR)

    # Ana kuleler (başlangıç ve bitiş)
    for kx in [ox + 8, ox + uzunluk - 8]:
        for dy in range(KULEr_Y):
            for z in range(-1, 2):
                mc.setBlock(kx,     oy + dy, oz + z, DEMİR)
                mc.setBlock(kx + 1, oy + dy, oz + z, DEMİR)
        # Kule köprüsü
        for z in range(-1, 2):
            mc.setBlock(kx, oy + KULEr_Y, oz + z, DEMİR)
            mc.setBlock(kx+1, oy + KULEr_Y, oz + z, DEMİR)

    # Ana kablo (parabolik eğri)
    for x in range(uzunluk + 1):
        # Parabolik kablo y konumu
        t = (x - uzunluk/2) / (uzunluk/2)
        kablo_y = int(KULEr_Y * (t*t * 0.8 + 0.2))
        mc.setBlock(ox + x, oy + kablo_y, oz - 2, ALTIN)
        mc.setBlock(ox + x, oy + kablo_y, oz + 2, ALTIN)

        # Askı kabloları (düşey)
        if x % 3 == 0:
            t2 = (x - uzunluk/2) / (uzunluk/2)
            kablo_y2 = int(KULEr_Y * (t2*t2 * 0.8 + 0.2))
            for dy in range(kablo_y2):
                mc.setBlock(ox + x, oy + dy, oz - 2, ALTIN)
                mc.setBlock(ox + x, oy + dy, oz + 2, ALTIN)

    mesaj(mc, "§9✔ Köprü tamamlandı! Karşıya geç.")


print("""
🏛️ MİMARİ YAPILAR
━━━━━━━━━━━━━━━━━━
1 → Ortaçağ Kalesi (surlar + kuleler + şato)
2 → Roma Tapınağı (sütunlar + pediment)
3 → Japon Pagodası (5 katlı)
4 → Askılı Köprü (parabolik kablo)
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   kale()
elif secim == "2": roma_tapinagi()
elif secim == "3": pagoda()
elif secim == "4": askili_kopru()
else: print("Geçersiz seçim!")
