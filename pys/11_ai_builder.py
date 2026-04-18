"""
11_ai_builder.py
━━━━━━━━━━━━━━━━
🤖 AI BUILDER (Text-to-Build)
Bu script, Minecraft üzerindeki chat mesajlarını dinler ve 
basit komutları algılayarak yapılar inşa eder.

Gelecekte LLM (Large Language Model) API entegrasyonu ile 
çok daha karmaşık yapıları "anlayarak" yapabilecektir.
"""

from mc_helper import *
import time
import sys
import io

# Terminal çıktılarını zorunlu olarak UTF-8 yap (Parametre eklemeden çalışması için)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

mc = baglan()

def ai_interpretation(text):
    """
    Metni analiz eder; komutu, 3 farklı boyut (val1, val2, val3) ve malzemeyi döndürür.
    val1: Genişlik (X), val2: Uzunluk (Z), val3: Yükseklik (Y)
    """
    text = text.lower()
    
    # Sayıları bul (Cümledeki tüm sayıları listele)
    sayilar = [int(s) for s in text.split() if s.isdigit()]
    val1 = sayilar[0] if len(sayilar) > 0 else 10 # Varsayılan X
    val2 = sayilar[1] if len(sayilar) > 1 else val1 # Varsayılan Z
    val3 = sayilar[2] if len(sayilar) > 2 else val2 # Varsayılan Y
    
    # Malzeme Belirleme
    malzeme = None
    if "altın" in text or "altin" in text: malzeme = ALTIN
    elif "demir" in text: malzeme = DEMİR
    elif "elmas" in text or "dia" in text: malzeme = DİAMAN
    elif "taş" in text or "tas" in text: malzeme = TAŞ
    elif "tuğla" in text or "tugla" in text: malzeme = TUĞLA
    elif "obsidyen" in text or "obsidiyen" in text: malzeme = OBSIDYEN
    elif "cam" in text: malzeme = CAM
    elif "yün" in text or "yun" in text: malzeme = YÜN

    # Komut Belirleme (X, Z, Y parametreli)
    if "kule" in text or "tower" in text or "kÃ¼le" in text:
        # Kule: val1=en, val2=boy, val3=yükseklik
        return "KULE", val1, val2, val3, (malzeme if malzeme else DEMİR)
            
    elif "havuz" in text or "pool" in text or "havu" in text:
        return "HAVUZ", val1, val2, val3, SU

    elif "küre" in text or "sphere" in text or "kÃ¼re" in text or "kure" in text:
        return "KÜRE", val1, 0, 0, (malzeme if malzeme else ALTIN)
        
    elif "pira" in text:
        return "PİRAMİT", val1, 0, 0, (malzeme if malzeme else SANDSTONE)

    elif "ağaç" in text or "aç" in text or "agac" in text or "tree" in text or "aäÿaã§" in text or "ağa" in text:
        return "AĞAÇ", 0, 0, 0, AHŞAP

    elif "yol" in text or "road" in text:
        return "YOL", val1, val2, 0, (malzeme if malzeme else TAŞ)

    elif "duvar" in text or "wall" in text:
        return "DUVAR", val1, val2, val3, (malzeme if malzeme else TUĞLA)
        
    # Komut 8: Temizle (Temizle, clean, sil)
    elif "temiz" in text or "clean" in text or "sil" in text:
        return "TEMİZLE", val1 if val1 != 10 else 20, 0, 0, HAVA

    return None, 0, 0, 0, None

def build_tower(w, l, h, blok):
    mesaj(mc, f"§bAI: {w}x{l} tabanlı, {h} yüksekliğinde kule inşa ediliyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    hw = w // 2
    hl = l // 2
    mc.setBlocks(px+5-hw, py, pz-hl, px+5+hw, py+h, pz+hl, blok)
    mc.setBlocks(px+5-hw+1, py, pz-hl+1, px+5+hw-1, py+h, pz+hl-1, HAVA) # İçini boşalt
    mc.setBlock(px+5, py+h+1, pz, PARLAYAN)

def build_pool(w, l, h, blok):
    mesaj(mc, f"§bAI: {w}x{l} boyutunda, {h} derinliğinde havuz kazaılıyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    hw = w // 2
    hl = l // 2
    mc.setBlocks(px+5-hw-1, py-1, pz-hl-1, px+5+hw+1, py-h-1, pz+hl+1, TAŞ) # Kenar
    mc.setBlocks(px+5-hw, py-1, pz-hl, px+5+hw, py-h, pz+hl, blok) # Su/Malzeme

def build_sphere(r, blok):
    mesaj(mc, f"§bAI: {r} yarıçaplı dairesel yapı oluşturuluyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    dolu_kure(mc, px+r+5, py+r+2, pz, r, blok)

def build_pyramid(h, blok):
    mesaj(mc, f"§bAI: {h} katlı dev bir piramit inşa ediliyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    cx, cy, cz = px + 15, py, pz
    for i in range(h):
        y = cy + i
        r = h - i
        mc.setBlocks(cx - r, y, cz - r, cx + r, y, cz + r, blok)

def build_tree():
    mesaj(mc, "§bAI: Bir ağaç dikiyorum...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    tx, ty, tz = px + 10, py, pz + 10
    mc.setBlocks(tx, ty, tz, tx, ty + 4, tz, AHŞAP)
    mc.setBlocks(tx - 2, ty + 3, tz - 2, tx + 2, ty + 3, tz + 2, YAPRAK)
    mc.setBlocks(tx - 1, ty + 4, tz - 1, tx + 1, ty + 5, tz + 1, YAPRAK)

def build_road(w, l, blok):
    mesaj(mc, f"§bAI: {w} genişliğinde, {l} uzunluğunda yol döşeniyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    hl = w // 2
    mc.setBlocks(px + 2, py - 1, pz - hl, px + 2 + l, py - 1, pz + hl, blok)

def build_wall(l, h, w, blok):
    # w burada duvarın kalınlığı olsun
    mesaj(mc, f"§bAI: {l} uzunluğunda, {h} yüksekliğinde duvar çekiliyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    tk = w // 2 if w > 1 else 0
    mc.setBlocks(px + 2, py, pz + 5 - tk, px + 2 + l, py + h, pz + 5 + tk, blok)

def build_clear(r):
    mesaj(mc, f"§cAI: {r} yarıçapındaki alan temizleniyor...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    mc.setBlocks(px-r, py, pz-r, px+r, py+60, pz+r, HAVA)

def main():
    print("""
🤖 AI BUILDER - KULLANIM REHBERİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 Chat üzerinden komut vererek inşaat yapabilirsiniz.
🏗️ Yapılar: kule, küre, piramit, havuz, duvar, yol, ağaç, temizle
💎 Malzemeler: altın, demir, elmas, taş, tuğla, obsidyen, cam, yün
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    # Oyundaki kişiye detaylı bilgi ver
    mesaj(mc, "§6╔════════ AI BUILDER REHBERİ ════════╗")
    mesaj(mc, "§b🤖 Sistem Aktif! §fKullanım: §e[En] [Boy] [Yükseklik] [Yapı] [Malzeme]")
    mesaj(mc, "§7---------------------------------------")
    mesaj(mc, "§6🏗️ YAPILAR: §fkule, küre, piramit, havuz, duvar, yol, ağaç, temizle")
    mesaj(mc, "§6💎 MALZEMELER: §faltın, demir, elmas, taş, tuğla, obsidyen, cam, yün")
    mesaj(mc, "§7---------------------------------------")
    mesaj(mc, "§6📋 ÖRNEK KOMUTLAR (10 Adet):")
    mesaj(mc, "§e1. §f'obsidyen kule' §7(Standart kule)")
    mesaj(mc, "§e2. §f'7 7 40 kule' §7(7x7 genişlik, 40 yükseklik)")
    mesaj(mc, "§e3. §f'25 katlı elmas piramit'")
    mesaj(mc, "§e4. §f'15 15 5 havuz' §7(15x15 boyut, 5 derinlik)")
    mesaj(mc, "§e5. §f'100 15 2 duvar' §7(Uzunluk=100, Yük=15, Kalınlık=2)")
    mesaj(mc, "§e6. §f'altın küre yap' §7(Altın top)")
    mesaj(mc, "§e7. §f'ağaç dik' §7(Ağaç oluşturur)")
    mesaj(mc, "§e8. §f'5 100 yol' §7(Genişlik=5, Uzunluk=100)")
    mesaj(mc, "§e9. §f'50 temizle' §7(50 blokluk alanı siler)")
    mesaj(mc, "§e10. §f'cam kule' §7(Şeffaf kule)")
    mesaj(mc, "§6╚══════════════════════════════════╝")
    
    last_msg = ""
    
    try:
        while True:
            chats = mc.events.pollChatPosts()
            for chat in chats:
                msg = chat.message
                try:
                    if isinstance(msg, bytes): msg = msg.decode('utf-8')
                    else: msg = msg.encode('latin-1').decode('utf-8')
                except: pass

                if msg != last_msg:
                    print(f"Oyuncu Mesajı: {msg}")
                    cmd, v1, v2, v3, mat = ai_interpretation(msg)
                    
                    if cmd == "KULE":
                        build_tower(v1, v2, v3, mat)
                    elif cmd == "HAVUZ":
                        build_pool(v1, v2, v3, mat)
                    elif cmd == "KÜRE":
                        build_sphere(v1, mat)
                    elif cmd == "PİRAMİT":
                        build_pyramid(v1, mat)
                    elif cmd == "AĞAÇ":
                        build_tree()
                    elif cmd == "YOL":
                        build_road(v1, v2, mat)
                    elif cmd == "DUVAR":
                        build_wall(v1, v2, v3, mat)
                    elif cmd == "TEMİZLE":
                        build_clear(v1)
                        
                    last_msg = msg
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nAI Builder durduruldu.")

if __name__ == "__main__":
    main()
