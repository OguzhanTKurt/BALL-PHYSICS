import game
import tkinter as tk
import random

root = tk.Tk()
root.geometry("1200x800")
root.resizable(False, False)
root.configure(bg="#1a1a1a")
app = game.BallAnimationApp(root)

DELAY = 1800   # milisaniye, adımlar için bekleme
LONG = 3500    # izleme için uzun bekleme

# Rastgele top ekle fonksiyonu
def random_ball():
    size = random.choice(game.TOP_BOYUTLARI)
    color = random.choice(game.TOP_RENKLERI)
    app.set_size(size, app.size_canvases[size])
    app.set_color(color, app.color_buttons[color])

# Buton animasyonlu tıklama efekti (200ms highlight ile)
def click_with_effect(btn_key, after_fn=None):
    btn = app.buttons[btn_key]
    orig_bg = btn.cget('bg')
    active_bg = btn.cget('activebackground')
    btn.config(bg=active_bg)
    root.after(200, lambda: (btn.config(bg=orig_bg), after_fn() if after_fn else None))
    btn.invoke()

# n kez butona efektli tıkla
def click_button(btn_key, n, delay, next_fn=None):
    if n <= 0:
        if next_fn:
            next_fn()
        return
    click_with_effect(btn_key, lambda: root.after(delay, lambda: click_button(btn_key, n-1, delay, next_fn)))

# --- ADIM ADIM TESTLER ---
def test_1_add_balls(count=6, next_fn=None):
    print("\n[TEST] 6 Rastgele Top Ekle")
    for i in range(count):
        root.after(i * 300, random_ball)
    root.after(count * 350, lambda: (print("Top sayısı:", len(app.balls)), next_fn and next_fn()))

def test_2_start_anim():
    print("\n[TEST] Animasyon Başlat (Çarpışmalar izlenecek)")
    click_with_effect('start', lambda: root.after(LONG, test_3_hiz_yavas))

def test_3_hiz_yavas():
    print("\n[TEST] 3x SLOW butonu - hız net azalsın")
    click_button('speed_down', 3, 700, lambda: root.after(LONG, test_4_hiz_artir))

def test_4_hiz_artir():
    print("\n[TEST] 5x BOOST butonu - hız net artsın")
    click_button('speed_up', 5, 550, lambda: root.after(LONG, test_5_disable_collision))

def test_5_disable_collision():
    print("\n[TEST] Çarpışma KAPATILDI (butondan)")
    if not app.collision_enabled:
        click_with_effect('collision', lambda: None)
    click_with_effect('collision', lambda: root.after(DELAY, test_6_delete_some_balls))

def test_6_delete_some_balls():
    print("\n[TEST] 2x DELETE butonu ile top SİL (hareketli ve çarpışmasız)")
    click_button('delete', 2, 600, lambda: root.after(DELAY, test_7_reset))

def test_7_reset():
    print("\n[TEST] RESET butonu - Tüm toplar ve ayarlar sıfırlanır")
    def after_reset():
        # resetten sonra çarpışma kapalıysa açmak için gösterişli buton tıklaması
        if not app.collision_enabled:
            print("[TEST] Reset sonrası Çarpışma tekrar AÇILIYOR!")
            click_with_effect('collision', lambda: root.after(350, testler_bitti))
        else:
            root.after(DELAY, testler_bitti)
    click_with_effect('reset', after_reset)

def testler_bitti():
    print("\n[TÜM GÖRSEL FUN TESTLERİ TAMAMLANDI]")
    print("--- GUI açık, elle veya butonlarla istediğin gibi devam edebilirsin! ---")

root.after(600, lambda: test_1_add_balls(6, test_2_start_anim))
root.mainloop()
