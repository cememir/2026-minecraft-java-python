"""
╔═══════════════════════════════════════════════════════════════════╗
║        MİNECRAFT PYTHON SCRİPTLERİ KOLEKSİYONU                  ║
║        Stack: Paper 1.21 + FruitJuice + pyncraft                 ║
╠═══════════════════════════════════════════════════════════════════╣
║  İÇİNDEKİLER:                                                    ║
║   1.  saat()          → Havaya dijital saat yaz                  ║
║   2.  gokkusagi()     → Altında yürüdükçe gökkuşağı oluştur      ║
║   3.  kule()          → Dev spiral kule inşa et                  ║
║   4.  piramit()       → Taş piramit yap                          ║
║   5.  sehir()         → Komple şehir inşa et                     ║
║   6.  deprem()        → Ayakların altını rastgele pat pat yap     ║
║   7.  havai_fisek()   → TNT havai fişeği patla                   ║
║   8.  labirent()      → Rastgele labirent oluştur                ║
║   9.  yazı_yaz()      → Havaya herhangi bir yazı yaz             ║
║  10.  ağaç_ormanı()   → Büyük bir orman ekle                     ║
╚═══════════════════════════════════════════════════════════════════╝

KULLANIM:
  - Bu dosyanın altına in, istediğin fonksiyonu çağır
  - Ya da terminalde: python minecraft_koleksiyon.py
"""

from pyncraft.minecraft import Minecraft
from pyncraft import block
from datetime import datetime
import time
import random
import math

# ─── BAĞLANTI ────────────────────────────────────────────────────────────────
mc = Minecraft.create("localhost", 4711)

# ─── BLOK SABİTLERİ ──────────────────────────────────────────────────────────
HAVA        = block.AIR
TAŞ         = block.STONE
TOPRAK      = block.DIRT
ÇIMEN       = block.GRASS
KUMU        = block.SAND
AHŞAP       = block.WOOD
YAPRAK      = block.LEAVES
CAM         = block.GLASS
TUĞLA       = block.BRICK_BLOCK
ALTIN       = block.GOLD_BLOCK
DEMİR       = block.IRON_BLOCK
DİAMAN     = block.DIAMOND_BLOCK
PARLAYAN    = block.GLOWSTONE_BLOCK
SU          = block.WATER_STATIONARY
LAV         = block.LAVA_STATIONARY
YÜN         = block.WOOL            # data parametresiyle renk
SANDSTONE   = block.SANDSTONE
COBBLESTONE = block.COBBLESTONE

# YÜN RENKLERİ (data değerleri)
BEYAZ=0; TURUNCU=1; EFLATUN=2; AÇIK_MAVİ=3; SARI=4
YEŞİL=5; PEMBE=6; GRİ=7; AÇIK_GRİ=8; SİYAN=9
MOR=10; MAVİ=11; KAHVE=12; KOYU_YEŞİL=13; KIRMIZI=14; SİYAH=15


# ════════════════════════════════════════════════════════════════════
# 1. DİJİTAL SAAT
# ════════════════════════════════════════════════════════════════════

RAKAMLAR = {
    "0":["XXX","X X","X X","X X","XXX"],
    "1":[" X ","XX "," X "," X ","XXX"],
    "2":["XXX","  X","XXX","X  ","XXX"],
    "3":["XXX","  X","XXX","  X","XXX"],
    "4":["X X","X X","XXX","  X","  X"],
    "5":["XXX","X  ","XXX","  X","XXX"],
    "6":["XXX","X  ","XXX","X X","XXX"],
    "7":["XXX","  X","  X","  X","  X"],
    "8":["XXX","X X","XXX","X X","XXX"],
    "9":["XXX","X X","XXX","  X","XXX"],
    ":": [" ","X"," ","X"," "],
}

def saat(sure=60):
    """Oyuncunun önünde havada dijital saat gösterir."""
    mc.postToChat("§b⏰ Saat başlatıldı!")
    px, py, pz = mc.player.getTilePos()
    x0, y0, z0 = px - 5, py + 30, pz + 3

    def temizle():
        mc.setBlocks(x0, y0, z0, x0+38, y0+7, z0, HAVA)

    def ciz(metin):
        imle = x0
        for ch in metin:
            if ch not in RAKAMLAR: imle += 2; continue
            kal = RAKAMLAR[ch]; h = len(kal)
            for ri, row in enumerate(kal):
                for ci, c in enumerate(row):
                    mc.setBlock(imle+ci, y0+(h-1-ri), z0,
                                PARLAYAN if c=="X" else HAVA)
            imle += len(kal[0]) + 1

    son = ""
    bitis = time.time() + sure
    try:
        while time.time() < bitis:
            simdi = datetime.now().strftime("%H:%M:%S")
            if simdi != son:
                temizle(); ciz(simdi)
                son = simdi
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    temizle()
    mc.postToChat("§cSaat durduruldu.")


# ════════════════════════════════════════════════════════════════════
# 2. GÖKKUŞAĞI — Oyuncu yürüdükçe altına renkli yün döşe
# ════════════════════════════════════════════════════════════════════

def gokkusagi(sure=60):
    """Oyuncu yürüdükçe gittiği yere gökkuşağı renkleri döşer."""
    renkler = [KIRMIZI, TURUNCU, SARI, YEŞİL, SİYAN, MAVİ, MOR]
    renk_i = 0
    mc.postToChat("§aGökkuşağı modu açık! Yürü!")
    son_pos = None
    bitis = time.time() + sure
    try:
        while time.time() < bitis:
            x, y, z = mc.player.getTilePos()
            if (x, z) != son_pos:
                mc.setBlock(x, y-1, z, YÜN, renkler[renk_i % len(renkler)])
                renk_i += 1
                son_pos = (x, z)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    mc.postToChat("§cGökkuşağı modu kapandı.")


# ════════════════════════════════════════════════════════════════════
# 3. SPİRAL KULE
# ════════════════════════════════════════════════════════════════════

def kule(yukseklik=60, yaricap=5):
    """Oyuncunun yanına devasa bir spiral kule inşa eder."""
    mc.postToChat("§6Kule inşa ediliyor...")
    px, py, pz = mc.player.getTilePos()
    cx, cz = px + 15, pz

    # Dış duvar
    for y in range(py, py + yukseklik):
        for aci in range(0, 360, 5):
            rad = math.radians(aci)
            x = cx + int(yaricap * math.cos(rad))
            z = cz + int(yaricap * math.sin(rad))
            mc.setBlock(x, y, z, COBBLESTONE if y % 10 != 0 else TUĞLA)

    # Spiral merdiven (içte dönen platform)
    for y in range(py, py + yukseklik):
        aci = (y - py) * 12  # Her blok 12 derece döner
        rad = math.radians(aci)
        for r in range(1, yaricap):
            x = cx + int(r * math.cos(rad))
            z = cz + int(r * math.sin(rad))
            mc.setBlock(x, y, z, AHŞAP)

    # Tepe: cam kubbe
    for y in range(py + yukseklik, py + yukseklik + 5):
        r = yaricap - (y - (py + yukseklik))
        for aci in range(0, 360, 10):
            rad = math.radians(aci)
            x = cx + int(r * math.cos(rad))
            z = cz + int(r * math.sin(rad))
            mc.setBlock(x, y, z, CAM)

    # Tepe ışığı
    mc.setBlock(cx, py + yukseklik + 5, cz, PARLAYAN)
    mc.postToChat("§6✔ Kule tamamlandı!")


# ════════════════════════════════════════════════════════════════════
# 4. PİRAMİT
# ════════════════════════════════════════════════════════════════════

def piramit(boyut=20):
    """Kumtaşı piramit inşa eder. boyut = taban kenar uzunluğu."""
    mc.postToChat("§eParamit inşa ediliyor...")
    px, py, pz = mc.player.getTilePos()
    cx, cz = px + boyut + 5, pz

    for kat in range(boyut):
        y = py + kat
        for x in range(cx - (boyut - kat), cx + (boyut - kat) + 1):
            for z in range(cz - (boyut - kat), cz + (boyut - kat) + 1):
                # Sadece dış kabuk (içi boş)
                dıs = (abs(x - cx) == boyut - kat or
                       abs(z - cz) == boyut - kat or
                       kat == 0)
                if dıs:
                    mc.setBlock(x, y, z, SANDSTONE)

    # Tepe
    mc.setBlock(cx, py + boyut, cz, ALTIN)
    mc.postToChat("§e✔ Piramit tamamlandı!")


# ════════════════════════════════════════════════════════════════════
# 5. ŞEHİR İNŞAATI
# ════════════════════════════════════════════════════════════════════

def bina(cx, cy, cz, en, boy, yukseklik, dis_blok, cam_blok):
    """Tek bir bina inşa eder (içi boş, pencereli)."""
    # Zemin
    for x in range(cx, cx + en):
        for z in range(cz, cz + boy):
            mc.setBlock(x, cy - 1, z, COBBLESTONE)

    # Duvarlar
    for y in range(cy, cy + yukseklik):
        for x in range(cx, cx + en):
            for z in range(cz, cz + boy):
                kenar = (x == cx or x == cx+en-1 or
                         z == cz or z == cz+boy-1)
                if not kenar:
                    continue
                # Pencere: 2'de bir katda, köşe değilse cam
                kose = ((x == cx or x == cx+en-1) and
                        (z == cz or z == cz+boy-1))
                pencere = (y % 3 == 1 and not kose and
                           x != cx and x != cx+en-1)
                mc.setBlock(x, y, z, cam_blok if pencere else dis_blok)

    # Çatı
    for x in range(cx, cx + en):
        for z in range(cz, cz + boy):
            mc.setBlock(x, cy + yukseklik, z, dis_blok)

    # Çatı lambası
    mc.setBlock(cx + en//2, cy + yukseklik + 1, cz + boy//2, PARLAYAN)


def sehir(bina_sayisi=12):
    """
    Oyuncunun yanına komple bir mini şehir inşa eder.
    Yollar, binalar, park alanı ve ışıklandırma içerir.
    """
    mc.postToChat("§d🏙️ Şehir inşa ediliyor... (biraz zaman alabilir)")
    px, py, pz = mc.player.getTilePos()

    # Şehir merkezi — oyuncudan 10 blok uzakta başlasın
    baslangic_x = px + 10
    baslangic_z = pz - 30

    blok_tipleri = [
        (COBBLESTONE, CAM),
        (TUĞLA,       CAM),
        (TAŞ,         CAM),
        (DEMİR,       CAM),
        (SANDSTONE,   CAM),
    ]

    bina_konumlari = []

    # Izgara düzeninde bina yerleşimi
    satir_sayisi = 3
    sutun_sayisi = 4
    aralik = 18       # Binalar arası mesafe (yol genişliği dahil)

    for satir in range(satir_sayisi):
        for sutun in range(sutun_sayisi):
            if len(bina_konumlari) >= bina_sayisi:
                break

            bx = baslangic_x + sutun * aralik
            bz = baslangic_z + satir * aralik

            en       = random.randint(6, 10)
            boy      = random.randint(6, 10)
            yuksek   = random.randint(8, 20)
            dis, cam = random.choice(blok_tipleri)

            bina(bx, py, bz, en, boy, yuksek, dis, cam)
            bina_konumlari.append((bx, bz, en, boy))
            mc.postToChat(f"§7  Bina {len(bina_konumlari)}/{bina_sayisi} tamamlandı.")

    # ── YOLLAR ──────────────────────────────────────────────────────
    mc.postToChat("§7  Yollar döşeniyor...")
    şehir_genislik = sutun_sayisi * aralik + 12
    şehir_uzunluk  = satir_sayisi  * aralik + 12

    # Yatay ana yollar
    for satir in range(satir_sayisi + 1):
        z = baslangic_z - 3 + satir * aralik
        for x in range(baslangic_x - 3, baslangic_x + şehir_genislik):
            mc.setBlock(x, py - 1, z,     COBBLESTONE)  # yol
            mc.setBlock(x, py - 1, z + 1, COBBLESTONE)
            mc.setBlock(x, py - 1, z + 2, COBBLESTONE)

    # Dikey ana yollar
    for sutun in range(sutun_sayisi + 1):
        x = baslangic_x - 3 + sutun * aralik
        for z in range(baslangic_z - 3, baslangic_z + şehir_uzunluk):
            mc.setBlock(x,     py - 1, z, COBBLESTONE)
            mc.setBlock(x + 1, py - 1, z, COBBLESTONE)
            mc.setBlock(x + 2, py - 1, z, COBBLESTONE)

    # ── YOL LAMBASI ──────────────────────────────────────────────────
    mc.postToChat("§7  Sokak lambaları yerleştiriliyor...")
    for satir in range(satir_sayisi + 1):
        for sutun in range(sutun_sayisi + 1):
            lx = baslangic_x - 3 + sutun * aralik + 1
            lz = baslangic_z - 3 + satir * aralik + 1
            for dy in range(4):
                mc.setBlock(lx, py + dy, lz, DEMİR)
            mc.setBlock(lx,     py + 4, lz,     PARLAYAN)
            mc.setBlock(lx + 1, py + 4, lz,     PARLAYAN)
            mc.setBlock(lx,     py + 4, lz + 1, PARLAYAN)

    # ── PARK ALANI ───────────────────────────────────────────────────
    mc.postToChat("§7  Park oluşturuluyor...")
    park_x = baslangic_x + sutun_sayisi * aralik // 2 - 4
    park_z = baslangic_z + satir_sayisi  * aralik // 2 - 4
    park_boyut = 8

    for x in range(park_x, park_x + park_boyut):
        for z in range(park_z, park_z + park_boyut):
            mc.setBlock(x, py - 1, z, ÇIMEN)

    # Park ağaçları (4 köşe)
    for (tx, tz) in [
        (park_x + 1,              park_z + 1),
        (park_x + park_boyut - 2, park_z + 1),
        (park_x + 1,              park_z + park_boyut - 2),
        (park_x + park_boyut - 2, park_z + park_boyut - 2),
    ]:
        # Gövde
        for dy in range(5):
            mc.setBlock(tx, py + dy, tz, AHŞAP)
        # Yaprak topu
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(3):
                    if abs(dx) + abs(dz) + abs(dy) <= 3:
                        mc.setBlock(tx+dx, py+5+dy, tz+dz, YAPRAK)

    # Park havuzu
    hv_x, hv_z = park_x + 3, park_z + 3
    for x in range(hv_x, hv_x + 3):
        for z in range(hv_z, hv_z + 3):
            mc.setBlock(x, py - 2, z, SU)
            mc.setBlock(x, py - 1, z, SU)

    mc.postToChat("§d✔ Şehir tamamlandı! 🏙️ Keşfetmeye hazır!")


# ════════════════════════════════════════════════════════════════════
# 6. DEPREM
# ════════════════════════════════════════════════════════════════════

def deprem(sure=10, siddet=3):
    """
    Oyuncunun etrafındaki zemini rastgele kaldırıp indirerek
    deprem efekti yapar. (Güvenli — hava bloğu kullanır)
    """
    mc.postToChat("§c⚠ DEPREM BAŞLIYOR! ⚠")
    time.sleep(1)
    bitis = time.time() + sure
    dalgalanma = []

    try:
        while time.time() < bitis:
            px, py, pz = mc.player.getTilePos()
            # Eski dalgalanmaları geri al
            for (x, y, z, eski) in dalgalanma:
                mc.setBlock(x, y, z, eski)
            dalgalanma.clear()

            # Yeni dalgalanma uygula
            for _ in range(30):
                dx = random.randint(-siddet * 3, siddet * 3)
                dz = random.randint(-siddet * 3, siddet * 3)
                dy = random.randint(-1, 1)
                x, y, z = px + dx, py - 1 + dy, pz + dz
                mevcut = mc.getBlock(x, y, z)
                mc.setBlock(x, y, z, HAVA if mevcut != 0 else COBBLESTONE)
                dalgalanma.append((x, y, z, mevcut))
            time.sleep(0.15)

    except KeyboardInterrupt:
        pass

    # Temizle
    for (x, y, z, eski) in dalgalanma:
        mc.setBlock(x, y, z, eski)
    mc.postToChat("§aDeprem durdu!")


# ════════════════════════════════════════════════════════════════════
# 7. HAVAİ FİŞEK (TNT Patlaması Simulasyonu)
# ════════════════════════════════════════════════════════════════════

def havai_fisek(adet=5):
    """
    Oyuncunun üzerinde havada parlayan blok kümeleri patlatır.
    (Gerçek TNT değil — bloklar önce oluşur, sonra silinir.)
    """
    mc.postToChat("§e🎆 Havai Fişek!")
    px, py, pz = mc.player.getTilePos()
    renkler = [KIRMIZI, TURUNCU, SARI, YEŞİL, SİYAN, MAVİ, MOR, BEYAZ]

    for _ in range(adet):
        # Rastgele merkez noktası
        mx = px + random.randint(-10, 10)
        my = py + random.randint(20, 35)
        mz = pz + random.randint(-10, 10)
        renk = random.choice(renkler)

        # Patlama: küresel dağılım
        noktalar = []
        for _ in range(400):
            aci1 = random.uniform(0, 2 * math.pi)
            aci2 = random.uniform(0, math.pi)
            r    = random.randint(3, 6)
            dx = int(r * math.sin(aci2) * math.cos(aci1))
            dy = int(r * math.cos(aci2))
            dz = int(r * math.sin(aci2) * math.sin(aci1))
            noktalar.append((mx+dx, my+dy, mz+dz))

        # Yak
        for (x, y, z) in noktalar:
            mc.setBlock(x, y, z, YÜN, renk)
        mc.postToChat(f"§e✨ Patlama {_+1}!")
        time.sleep(0.8)

        # Söndür
        for (x, y, z) in noktalar:
            mc.setBlock(x, y, z, HAVA)
        time.sleep(0.2)

    mc.postToChat("§eHavai fişek bitti!")


# ════════════════════════════════════════════════════════════════════
# 8. LABİRENT
# ════════════════════════════════════════════════════════════════════

def labirent(boyut=21):
    """
    Recursive backtracking algoritmasıyla rastgele labirent oluşturur.
    boyut tek sayı olmalı (örn. 21, 31, 41).
    """
    if boyut % 2 == 0:
        boyut += 1

    mc.postToChat(f"§b🌀 {boyut}x{boyut} labirent oluşturuluyor...")
    px, py, pz = mc.player.getTilePos()
    ox, oz = px + 5, pz - boyut // 2

    # Izgara: True = duvar, False = yol
    grid = [[True] * boyut for _ in range(boyut)]

    def carve(cx, cz):
        grid[cz][cx] = False
        yonler = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(yonler)
        for dx, dz in yonler:
            nx, nz = cx + dx, cz + dz
            if 0 <= nx < boyut and 0 <= nz < boyut and grid[nz][nx]:
                grid[cz + dz//2][cx + dx//2] = False
                carve(nx, nz)

    # Başlangıç: (1,1)
    import sys
    sys.setrecursionlimit(10000)
    carve(1, 1)

    # Giriş ve çıkış
    grid[0][1]        = False
    grid[boyut-1][boyut-2] = False

    # Minecraft'a çiz
    for z in range(boyut):
        for x in range(boyut):
            bx, bz = ox + x, oz + z
            if grid[z][x]:
                # Duvar: 3 blok yüksekliğinde
                for dy in range(3):
                    mc.setBlock(bx, py + dy, bz, COBBLESTONE)
            else:
                # Yol: zemin taşı, üstü hava
                mc.setBlock(bx, py - 1, bz, TAŞ)
                mc.setBlock(bx, py,     bz, HAVA)
                mc.setBlock(bx, py + 1, bz, HAVA)
                mc.setBlock(bx, py + 2, bz, HAVA)

    # Oyuncuyu girişe ışınla
    mc.player.setPos(ox + 1, py + 1, oz - 1)
    mc.postToChat("§b✔ Labirent hazır! Çıkışı bul! 🌀")


# ════════════════════════════════════════════════════════════════════
# 9. HAVAYA YAZI YAZ
# ════════════════════════════════════════════════════════════════════

HARF_LISTESI = {
    "A": ["XXX","X X","XXX","X X","X X"],
    "B": ["XX ","X X","XX ","X X","XX "],
    "C": ["XXX","X  ","X  ","X  ","XXX"],
    "D": ["XX ","X X","X X","X X","XX "],
    "E": ["XXX","X  ","XXX","X  ","XXX"],
    "F": ["XXX","X  ","XXX","X  ","X  "],
    "G": ["XXX","X  ","X X","X X","XXX"],
    "H": ["X X","X X","XXX","X X","X X"],
    "I": ["XXX"," X "," X "," X ","XXX"],
    "J": ["XXX","  X","  X","X X","XXX"],
    "K": ["X X","XX ","X  ","XX ","X X"],
    "L": ["X  ","X  ","X  ","X  ","XXX"],
    "M": ["X X","XXX","X X","X X","X X"],
    "N": ["X X","XXX","XXX","X X","X X"],
    "O": ["XXX","X X","X X","X X","XXX"],
    "P": ["XXX","X X","XXX","X  ","X  "],
    "R": ["XXX","X X","XXX","XX ","X X"],
    "S": ["XXX","X  ","XXX","  X","XXX"],
    "T": ["XXX"," X "," X "," X "," X "],
    "U": ["X X","X X","X X","X X","XXX"],
    "V": ["X X","X X","X X","X X"," X "],
    "Y": ["X X","X X"," X "," X "," X "],
    "Z": ["XXX","  X","XXX","X  ","XXX"],
    " ": ["   ","   ","   ","   ","   "],
    "!": [" X "," X "," X ","   "," X "],
    "?": ["XXX","  X"," X ","   "," X "],
}

def yazi_yaz(metin="MERHABA", yukseklik=25, blok_tipi=None):
    """Havaya büyük harflerle yazı yazar."""
    if blok_tipi is None:
        blok_tipi = PARLAYAN

    metin = metin.upper()
    mc.postToChat(f"§a'{metin}' yazılıyor...")
    px, py, pz = mc.player.getTilePos()
    x0, y0, z0 = px - 2, py + yukseklik, pz + 3

    imle = x0
    for ch in metin:
        kalip = HARF_LISTESI.get(ch, HARF_LISTESI[" "])
        h = len(kalip)
        for ri, satir in enumerate(kalip):
            y = y0 + (h - 1 - ri)
            for ci, c in enumerate(satir):
                mc.setBlock(imle + ci, y, z0, blok_tipi if c == "X" else HAVA)
        imle += len(kalip[0]) + 1

    mc.postToChat(f"§a✔ '{metin}' yazısı tamamlandı!")


# ════════════════════════════════════════════════════════════════════
# 10. AĞAÇ ORMANI
# ════════════════════════════════════════════════════════════════════

def agac(kx, ky, kz, yukseklik=6):
    """Tek bir ağaç inşa eder."""
    # Gövde
    for dy in range(yukseklik):
        mc.setBlock(kx, ky + dy, kz, AHŞAP)
    # Yaprak küre
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            for dy in range(-2, 3):
                if dx*dx + dz*dz + dy*dy <= 10:
                    mc.setBlock(kx+dx, ky+yukseklik+dy, kz+dz, YAPRAK)


def agac_ormani(agac_sayisi=30, alan=40):
    """Oyuncunun yakınına büyük bir orman ekler."""
    mc.postToChat(f"§2🌲 {agac_sayisi} ağaçlık orman oluşturuluyor...")
    px, py, pz = mc.player.getTilePos()

    yerlesimler = []
    deneme = 0

    while len(yerlesimler) < agac_sayisi and deneme < agac_sayisi * 10:
        deneme += 1
        ax = px + random.randint(-alan, alan)
        az = pz + random.randint(-alan, alan)

        # Diğer ağaçlara çok yakın mı?
        cok_yakin = any(abs(ax-ex) < 6 and abs(az-ez) < 6
                        for (ex, ez) in yerlesimler)
        if cok_yakin:
            continue

        # Zemin yüksekliğini bul
        ay = mc.getHeight(ax, az)
        yuksek = random.randint(5, 9)
        agac(ax, ay, az, yuksek)
        yerlesimler.append((ax, az))

    mc.postToChat(f"§2✔ {len(yerlesimler)} ağaç dikildi! 🌲")


# ════════════════════════════════════════════════════════════════════
# ANA MENÜ — İstediğin fonksiyonu aşağıdan çağır!
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("""
╔══════════════════════════════════════════════╗
║   MİNECRAFT PYTHON KOLEKSİYONU              ║
╠══════════════════════════════════════════════╣
║  1  → Dijital Saat (60 sn)                  ║
║  2  → Gökkuşağı (yürüyerek)                 ║
║  3  → Spiral Kule                           ║
║  4  → Piramit                               ║
║  5  → Şehir İnşaatı                         ║
║  6  → Deprem Efekti                         ║
║  7  → Havai Fişek                           ║
║  8  → Labirent                              ║
║  9  → Havaya Yazı Yaz                       ║
║  10 → Ağaç Ormanı                           ║
╚══════════════════════════════════════════════╝
    """)

    secim = input("Seçim (1-10): ").strip()

    if secim == "1":
        saat()
    elif secim == "2":
        gokkusagi()
    elif secim == "3":
        kule()
    elif secim == "4":
        piramit()
    elif secim == "5":
        sehir()
    elif secim == "6":
        deprem()
    elif secim == "7":
        havai_fisek()
    elif secim == "8":
        labirent()
    elif secim == "9":
        metin = input("Yazılacak metin: ").strip() or "MERHABA"
        yazi_yaz(metin)
    elif secim == "10":
        agac_ormani()
    else:
        print("Geçersiz seçim!")
