"""
08_mini_oyunlar.py
━━━━━━━━━━━━━━━━━━
🎮 MİNİ OYUNLAR

İçerik:
  • Hazine Avı (koordinat hesaplama)
  • Engel Parkuru (rastgele üretilen)
  • Renk Eşleştirme Bulmacası
  • Simon Says (hafıza oyunu)

Çalıştırma: python 08_mini_oyunlar.py
"""

from mc_helper import *
import math, time, random

mc = baglan()


# ── 1. HAZİNE AVI ───────────────────────────────────────────────────

def hazine_avi(ipucu_sayisi=5):
    """
    Gizlenmiş altın bloğu bul!
    Her ipucu mesafeyi söyler (sıcak/soğuk sistemi).
    """
    mesaj(mc, "§6🗺️ HAZİNE AVI BAŞLIYOR!")
    px, py, pz = oyuncu_konum(mc)

    # Hazineyi gizle
    hazine_x = px + random.randint(-30, 30)
    hazine_z = pz + random.randint(-30, 30)
    hazine_y = mc.getHeight(hazine_x, hazine_z)

    # Hazineyi yere göm (bir blok altı)
    mc.setBlock(hazine_x, hazine_y - 1, hazine_z, ALTIN)
    mc.setBlock(hazine_x, hazine_y,     hazine_z, TOPRAK)  # üstünü kapat

    mesaj(mc, "§e💰 Altın blok bir yere gömüldü!")
    mesaj(mc, "§7  Yürü → her adımda sıcaklık ipucu alacaksın.")
    mesaj(mc, "§7  Hazineyi bulmak için o blokta dur.")

    bulunan = False
    son_mesafe = None

    bitis = time.time() + 180  # 3 dakika

    try:
        while time.time() < bitis and not bulunan:
            ox, oy, oz = oyuncu_konum(mc)
            mesafe = math.sqrt((ox-hazine_x)**2 + (oz-hazine_z)**2)

            # Sıcaklık ipucu
            if son_mesafe is None or abs(mesafe - son_mesafe) > 1:
                if mesafe < 5:
                    mesaj(mc, f"§c🔥🔥🔥 YANGIN SICAK! ({mesafe:.0f} blok)")
                elif mesafe < 10:
                    mesaj(mc, f"§6🔥🔥 Çok sıcak! ({mesafe:.0f} blok)")
                elif mesafe < 20:
                    mesaj(mc, f"§e🔥 Sıcak! ({mesafe:.0f} blok)")
                elif mesafe < 35:
                    mesaj(mc, f"§b❄ Soğuk... ({mesafe:.0f} blok)")
                else:
                    mesaj(mc, f"§9🧊 Donuyorsun! ({mesafe:.0f} blok)")
                son_mesafe = mesafe

            # Hazine üstünde mi?
            if abs(ox - hazine_x) <= 1 and abs(oz - hazine_z) <= 1:
                mc.setBlock(hazine_x, hazine_y - 1, hazine_z, HAVA)
                mc.setBlock(hazine_x, hazine_y,     hazine_z, ALTIN)
                mesaj(mc, "§6🏆 TEBRİKLER! Hazineyi buldun!")
                mesaj(mc, f"§7  Süre: {int(180 - (bitis - time.time()))} saniye")
                bulunan = True

            time.sleep(0.5)

    except KeyboardInterrupt:
        pass

    if not bulunan:
        mesaj(mc, f"§c⏰ Süre doldu! Hazine: X={hazine_x}, Z={hazine_z}")
        mc.setBlock(hazine_x, hazine_y - 1, hazine_z, ALTIN)
        mc.setBlock(hazine_x, hazine_y,     hazine_z, HAVA)


# ── 2. PARKUR ───────────────────────────────────────────────────────

def parkur(uzunluk=20):
    """Rastgele atlama parkuru oluşturur."""
    mesaj(mc, "§a🏃 Parkur oluşturuluyor...")
    px, py, pz = oyuncu_konum(mc)

    x, y, z = px + 3, py, pz
    platform_boyutlari = []

    for i in range(uzunluk):
        # Platform boyutu
        en = random.randint(1, 3)
        boy = random.randint(1, 3)

        blok = random.choice([COBBLE, TAŞ, AHŞAP, SANDSTONE, TUĞLA])
        for dx in range(en):
            for dz in range(boy):
                mc.setBlock(x+dx, y, z+dz, blok)

        platform_boyutlari.append((x, y, z, en, boy))

        # Sonraki platforma atlama mesafesi
        atlama_x = random.randint(2, 4)
        atlama_y = random.randint(-2, 2)
        atlama_z = random.randint(-2, 2)

        x += en + atlama_x
        y  = max(py - 5, min(py + 15, y + atlama_y))
        z += atlama_z

    # Başlangıç işareti
    sx, sy, sz = platform_boyutlari[0][:3]
    mc.setBlock(sx, sy + 1, sz, YÜN, YEŞİL)
    mc.postToChat("§a START →")

    # Bitiş işareti
    ex, ey, ez = platform_boyutlari[-1][:3]
    mc.setBlock(ex, ey + 1, ez, ALTIN)
    mc.postToChat("§6← FİNİŞ")

    mesaj(mc, f"§a✔ {uzunluk} platformlu parkur hazır! Yeşil bloktan başla!")


# ── 3. RENK BULMACASI ───────────────────────────────────────────────

def renk_bulmacasi(soru_sayisi=5):
    """
    Minecraft'ta renk sırası bulmacası.
    Sırayı gösterir, siler, oyuncu yeniden sıralamayı tamamlar.
    (Oyuncu blokları komut satırından sırayla girer)
    """
    mesaj(mc, "§d🎨 RENK BULMACASI!")
    mesaj(mc, "§7  Renk sırasını ezberle ve yeniden yaz!")

    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py + 5, pz + 5

    renk_isimleri = {
        KIRMIZI:"Kırmızı", SARI:"Sarı", YEŞİL:"Yeşil",
        MAVİ:"Mavi", MOR:"Mor", TURUNCU:"Turuncu",
        BEYAZ:"Beyaz", SİYAH:"Siyah"
    }
    tüm_renkler = list(renk_isimleri.keys())

    skor = 0

    for tur in range(soru_sayisi):
        uzunluk = 3 + tur  # Her turda bir renk daha
        sıra = random.sample(tüm_renkler, uzunluk)

        # Sırayı göster
        mesaj(mc, f"§e--- Tur {tur+1}/{soru_sayisi} | {uzunluk} renk ---")
        for i, renk in enumerate(sıra):
            mc.setBlock(x0 + i*2, y0, z0, YÜN, renk)
            mesaj(mc, f"§7  {i+1}. {renk_isimleri[renk]}")
        time.sleep(2 + uzunluk * 0.5)

        # Sil
        for i in range(uzunluk):
            mc.setBlock(x0 + i*2, y0, z0, HAVA)

        mesaj(mc, "§c❓ Sıra silindi! Terminale sırayla gir:")
        for i, renk in enumerate(sıra):
            mesaj(mc, f"§7  Pozisyon {i+1}: ?")

        # Cevap al
        doğru = 0
        for i, doğru_renk in enumerate(sıra):
            cevap_adi = input(f"  {i+1}. renk neydi? ").strip().lower()
            doğru_isim = renk_isimleri[doğru_renk].lower()
            if cevap_adi in doğru_isim or doğru_isim in cevap_adi:
                mc.setBlock(x0 + i*2, y0, z0, YÜN, doğru_renk)
                mesaj(mc, f"§a✔ Doğru! {renk_isimleri[doğru_renk]}")
                doğru += 1
            else:
                mc.setBlock(x0 + i*2, y0, z0, YÜN, KIRMIZI)
                mesaj(mc, f"§c✗ Yanlış! Doğrusu: {renk_isimleri[doğru_renk]}")

        skor += doğru
        mesaj(mc, f"§e  Bu turda {doğru}/{uzunluk} doğru!")
        time.sleep(2)

        # Temizle
        for i in range(uzunluk):
            mc.setBlock(x0 + i*2, y0, z0, HAVA)

    toplam = sum(3 + i for i in range(soru_sayisi))
    mesaj(mc, f"§6🏆 OYUN BİTTİ! Skor: {skor}/{toplam}")


# ── 4. SIMON SAYS ───────────────────────────────────────────────────

def simon_says(tur=6):
    """
    Simon says: renk dizisi her turda uzar.
    Oyuncu doğru rengi terminale girerek onar.
    """
    mesaj(mc, "§b🎮 SİMON SAYS BAŞLIYOR!")
    mesaj(mc, "§7  Her turda bir renk daha! Kaç tur dayanabileceksin?")

    px, py, pz = oyuncu_konum(mc)
    x0, y0, z0 = px + 5, py + 3, pz + 5

    RENKLER = [
        (KIRMIZI, "K"), (SARI, "S"), (YEŞİL, "Y"),
        (MAVİ, "M"), (MOR, "L"), (TURUNCU, "T"),
    ]

    sıra = []
    mesaj(mc, "§7  Kısaltmalar: K=Kırmızı S=Sarı Y=Yeşil M=Mavi L=Mor T=Turuncu")

    for tur_no in range(1, tur + 1):
        # Yeni renk ekle
        yeni = random.choice(RENKLER)
        sıra.append(yeni)

        mesaj(mc, f"§b=== Tur {tur_no} — {tur_no} renk ===")

        # Sırayı göster
        for (renk_val, _) in sıra:
            mc.setBlock(x0, y0, z0, YÜN, renk_val)
            time.sleep(0.8)
            mc.setBlock(x0, y0, z0, HAVA)
            time.sleep(0.4)

        # Oyuncudan cevap al
        cevap = input(f"Sırayı gir ({tur_no} harf, boşluksuz): ").strip().upper()

        doğru_cevap = "".join(k for (_, k) in sıra)

        if cevap == doğru_cevap:
            mesaj(mc, f"§a✔ DOĞRU! {tur_no}. turu geçtin!")
            dolu_kure(mc, x0, y0, z0, 2, YÜN, YEŞİL)
            time.sleep(0.5)
            dolu_kure(mc, x0, y0, z0, 2, HAVA)
        else:
            mesaj(mc, f"§c✗ YANLIŞ! Doğru sıra: {doğru_cevap}")
            mesaj(mc, f"§c  Sen yazdın: {cevap}")
            dolu_kure(mc, x0, y0, z0, 2, YÜN, KIRMIZI)
            time.sleep(1)
            dolu_kure(mc, x0, y0, z0, 2, HAVA)
            mesaj(mc, f"§6Oyun bitti! {tur_no-1}. turda elendin.")
            return

    mesaj(mc, f"§6🏆 TEBRİKLER! Tüm {tur} turu tamamladın!")


print("""
🎮 MİNİ OYUNLAR
━━━━━━━━━━━━━━━
1 → Hazine Avı (sıcak/soğuk)
2 → Engel Parkuru
3 → Renk Bulmacası
4 → Simon Says
""")

secim = input("Seçim (1-4): ").strip()
if secim == "1":   hazine_avi()
elif secim == "2": parkur()
elif secim == "3": renk_bulmacasi()
elif secim == "4": simon_says()
else: print("Geçersiz seçim!")
