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

mc = baglan()

def ai_interpretation(text):
    """
    Basit bir 'Yapay Zeka' mantığı: Metni analiz eder ve komuta dönüştürür.
    Gerçek bir LLM (GPT, Gemini vb.) bağlandığında burası API çağrısı yapacaktır.
    """
    text = text.lower()
    
    # Komut 1: Kule İnşası
    if "kule" in text or "tower" in text:
        try:
            # Sayı bulma mantığı
            yukseklik = 10
            kelimeler = text.split()
            for k in kelimeler:
                if k.isdigit():
                    yukseklik = int(k)
            return "KULE", yukseklik
        except:
            return "KULE", 10
            
    # Komut 2: Havuz / Çukur
    elif "havuz" in text or "pool" in text:
        return "HAVUZ", 5

    # Komut 3: Altın Küre
    elif "küre" in text or "sphere" in text:
        return "KÜRE", 3
        
    return None, None

def build_tower(h):
    mesaj(mc, f"§bAI: {h} blok yüksekliğinde bir kule yapıyorum...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    # setBlocks ile ultra hızlı inşa
    mc.setBlocks(px+2, py, pz+2, px+4, py+h, pz+4, DEMİR)
    mc.setBlocks(px+3, py, pz+3, px+3, py+h, pz+3, HAVA) # İçini boşalt
    mc.setBlock(px+3, py+h+1, pz+3, PARLAYAN) # Tepe ışığı

def build_pool(r):
    mesaj(mc, f"§bAI: {r}x{r} boyutunda bir havuz yapıyorum...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    mc.setBlocks(px+2, py-1, pz+2, px+2+r, py-3, pz+2+r, TAŞ) # Çerçeve
    mc.setBlocks(px+3, py-1, pz+3, px+1+r, py-2, pz+1+r, SU)   # Su

def build_sphere(r):
    mesaj(mc, f"§bAI: {r} yarıçaplı altın bir küre oluşturuyorum...", "§6[AI Builder] ")
    px, py, pz = oyuncu_konum(mc)
    dolu_kure(mc, px+r+5, py+r+2, pz, r, ALTIN)

def main():
    mesaj(mc, "§6🤖 AI Builder Aktif! Chat'e komut yazın (Örn: '20 blok kule yap', 'küre yap')")
    mesaj(mc, "§7Durdurmak için terminalden Ctrl+C yapın.")
    
    # Son mesajı takip et ki sürekli aynı şeyi yapmasın
    last_msg = ""
    
    try:
        while True:
            # Minecraft chat'ini oku (FruitJuice/Pyncraft desteğiyle)
            chats = mc.events.pollChatPosts()
            for chat in chats:
                msg = chat.message
                if msg != last_msg:
                    print(f"Oyuncu Mesajı: {msg}")
                    cmd, val = ai_interpretation(msg)
                    
                    if cmd == "KULE":
                        build_tower(val)
                    elif cmd == "HAVUZ":
                        build_pool(val)
                    elif cmd == "KÜRE":
                        build_sphere(val)
                        
                    last_msg = msg
            
            time.sleep(0.5) # İşlemciyi yormamak için kısa bekleme
    except KeyboardInterrupt:
        print("\nAI Builder durduruldu.")

if __name__ == "__main__":
    main()
