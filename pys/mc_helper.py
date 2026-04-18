"""
mc_helper.py — Ortak bağlantı ve yardımcı fonksiyonlar
Tüm scriptler bu dosyayı import eder. Aynı klasörde olmalı!
"""

from pyncraft.minecraft import Minecraft
from pyncraft import block
import time, math, random

# ── Bağlan ────────────────────────────────────────────────────────
def baglan(ip="localhost", port=4711):
    try:
        mc = Minecraft.create(ip, port)
        mc.postToChat("§a✔ Bağlantı kuruldu!")
        return mc
    except Exception as e:
        print(f"[HATA] Sunucuya bağlanılamadı: {e}")
        print("Paper sunucunun çalıştığından ve FruitJuice eklentisinin kurulu olduğundan emin ol.")
        raise

# ── Blok sabitleri ────────────────────────────────────────────────
HAVA        = block.AIR
TAŞ         = block.STONE
TOPRAK      = block.DIRT
ÇIMEN       = block.GRASS
KUM         = block.SAND
AHŞAP       = block.WOOD
YAPRAK      = block.LEAVES
CAM         = block.GLASS
TUĞLA       = block.BRICK_BLOCK
ALTIN       = block.GOLD_BLOCK
DEMİR       = block.IRON_BLOCK
DİAMAN      = block.DIAMOND_BLOCK
PARLAYAN    = block.GLOWSTONE_BLOCK
SU          = block.WATER_STATIONARY
LAV         = block.LAVA_STATIONARY
YÜN         = block.WOOL
SANDSTONE   = block.SANDSTONE
COBBLE      = block.COBBLESTONE
OBSIDYEN    = block.OBSIDIAN
BUZ         = block.ICE
KAR         = block.SNOW_BLOCK
KABAK       = block.MELON  # Pyncraft'ta PUMPKIN yerine MELON mevcut

# Yün renk sabitleri
BEYAZ=0; TURUNCU=1; EFLATUN=2; AÇIK_MAVİ=3; SARI=4
YEŞİL=5; PEMBE=6; GRİ=7; AÇIK_GRİ=8; SİYAN=9
MOR=10; MAVİ=11; KAHVE=12; KOYU_YEŞİL=13; KIRMIZI=14; SİYAH=15

GÖKKUŞAĞI = [KIRMIZI, TURUNCU, SARI, YEŞİL, SİYAN, MAVİ, MOR]

# ── Yardımcı fonksiyonlar ─────────────────────────────────────────
def oyuncu_konum(mc):
    p = mc.player.getTilePos()
    return p.x, p.y, p.z

def mesaj(mc, metin, renk="§f"):
    mc.postToChat(renk + metin)

def temizle_alan(mc, x1, y1, z1, x2, y2, z2):
    mc.setBlocks(x1, y1, z1, x2, y2, z2, HAVA)

def kure_noktalar(cx, cy, cz, r):
    """Bir küre üzerindeki blok koordinatlarını döndürür."""
    for x in range(cx-r, cx+r+1):
        for y in range(cy-r, cy+r+1):
            for z in range(cz-r, cz+r+1):
                if (x-cx)**2 + (y-cy)**2 + (z-cz)**2 <= r*r:
                    yield x, y, z

def dolu_kure(mc, cx, cy, cz, r, blok, data=0):
    for x, y, z in kure_noktalar(cx, cy, cz, r):
        mc.setBlock(x, y, z, blok, data)
