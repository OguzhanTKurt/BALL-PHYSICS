import tkinter as tk
from tkinter import font as tkfont
import random
import time
import math

# --- Yapılandırma ---
TOP_BOYUTLARI = [15, 30, 45]  # Küçük, Orta, Büyük boyutlar
TOP_RENKLERI = ["#FF3B30", "#007AFF", "#FFCC00"]  # Modern renkler
MAX_TOP_SAYISI = 50  # Maksimum top sayısı
GRID_ARALIK = 40  # Grid çizgileri arasındaki mesafe

# Hız kontrolü için temel gecikme
TEMEL_GECIKME_MS = 30 

class Ball:
    """Tek bir topun özelliklerini (konum, hız, renk, boyut) tutar."""
    def __init__(self, canvas, size, color, x=None, y=None):
        self.canvas = canvas
        self.size = size
        self.color = color
        
        # Canvas boyutunu güvenli şekilde al
        canvas.update_idletasks()
        canvas_width = max(canvas.winfo_width(), 100)
        canvas_height = max(canvas.winfo_height(), 100)
        
        # Konum belirtilmişse kullan, yoksa random konum
        if x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            # Random konum ve hız başlatma
            self.x = random.randint(size + 20, canvas_width - size - 20)
            self.y = random.randint(size + 20, canvas_height - size - 20)
        
        # Kütle (hacim ile orantılı - boyut^3)
        self.mass = size ** 3
        
        # Hız boyuta göre ayarlanır (büyük toplar daha yavaş, küçük toplar daha hızlı)
        # Temel hız çarpanı: küçük toplar için daha yüksek, büyük toplar için daha düşük
        # En küçük top (15) için hız çarpanı ~1.0, en büyük (45) için ~0.33
        base_speed_multiplier = (TOP_BOYUTLARI[0] / size)  # Küçük toplar için daha yüksek çarpan
        
        # Random hız yönü ve büyüklüğü
        # Hızlar saniye başına piksel cinsinden (60 FPS referansı için 60 ile çarpıyoruz)
        speed_magnitude = random.choice([2, 2.5, 3, 3.5]) * base_speed_multiplier * 60
        direction = random.choice([-1, 1])
        self.dx = direction * speed_magnitude * random.choice([0.8, 1.0, 1.2])
        self.dy = direction * speed_magnitude * random.choice([0.8, 1.0, 1.2])
        
        # Gölge efekti için ikinci bir oval
        self.shadow_id = canvas.create_oval(
            self.x - self.size + 3, 
            self.y - self.size + 3, 
            self.x + self.size + 3, 
            self.y + self.size + 3, 
            fill="#2a2a2a", outline="")
        
        self.id = canvas.create_oval(
            self.x - self.size, 
            self.y - self.size, 
            self.x + self.size, 
            self.y + self.size, 
            fill=self.color,
            outline="white",
            width=2)

    def move(self, delta_time, speed_multiplier):
        """Topun hareketini hesaplar ve günceller. Delta time ile stabil hız."""
        # Delta time ile çarpılarak FPS'ten bağımsız stabil hareket sağlanır
        # delta_time saniye cinsinden, speed_multiplier hız çarpanı
        # 60 FPS için delta_time ≈ 0.0167, bu yüzden hızları buna göre ayarlıyoruz
        self.x += self.dx * delta_time * speed_multiplier
        self.y += self.dy * delta_time * speed_multiplier
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if self.x + self.size > canvas_width or self.x - self.size < 0:
            self.dx *= -1
            self.x = min(max(self.x, self.size), canvas_width - self.size)
            
        if self.y + self.size > canvas_height or self.y - self.size < 0:
            self.dy *= -1
            self.y = min(max(self.y, self.size), canvas_height - self.size)

        # Gölge güncelleme
        self.canvas.coords(self.shadow_id,
                          self.x - self.size + 3,
                          self.y - self.size + 3,
                          self.x + self.size + 3,
                          self.y + self.size + 3)
        
        # Top güncelleme
        self.canvas.coords(self.id, 
                           self.x - self.size, 
                           self.y - self.size, 
                           self.x + self.size, 
                           self.y + self.size)
    
    def check_collision(self, other):
        """İki top arasındaki çarpışmayı kontrol eder ve momentum korunumlu çarpışma hesaplar."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx * dx + dy * dy)
        min_distance = self.size + other.size
        
        if distance < min_distance and distance > 0:
            # Çarpışma tespit edildi - momentum korunumlu çarpışma
            # Normalize edilmiş çarpışma vektörü
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
            else:
                nx = 1
                ny = 0
            
            # Göreceli hız
            dvx = self.dx - other.dx
            dvy = self.dy - other.dy
            
            # Çarpışma yönündeki göreceli hız
            dvn = dvx * nx + dvy * ny
            
            # Çarpışma gerçekleşiyorsa (birbirine yaklaşıyorlar)
            if dvn < 0:
                # Esneklik katsayısı (1.0 = tamamen esnek, enerji korunur)
                restitution = 1.0
                
                # Momentum korunumlu çarpışma
                # İmpuls büyüklüğü
                impulse = -(1 + restitution) * dvn / (1/self.mass + 1/other.mass)
                
                # Hızları güncelle (momentum korunumu)
                self.dx += impulse * nx / self.mass
                self.dy += impulse * ny / self.mass
                
                other.dx -= impulse * nx / other.mass
                other.dy -= impulse * ny / other.mass
            
            # Topları ayır (çakışmayı önle)
            overlap = min_distance - distance
            if overlap > 0:
                # Kütleye göre ayrılma (ağır top daha az hareket eder)
                total_mass = self.mass + other.mass
                self.x += math.cos(math.atan2(dy, dx)) * overlap * (other.mass / total_mass)
                self.y += math.sin(math.atan2(dy, dx)) * overlap * (other.mass / total_mass)
                other.x -= math.cos(math.atan2(dy, dx)) * overlap * (self.mass / total_mass)
                other.y -= math.sin(math.atan2(dy, dx)) * overlap * (self.mass / total_mass)
            
            return True
        return False

class BallAnimationApp:
    def __init__(self, master):
        self.master = master
        master.title("Ball Physics Simulator")
        master.configure(bg="#1a1a1a")
        
        # Modern font - responsive boyutlar için başlangıç değerleri
        self.base_font_size = 9
        self.title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.button_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.label_font = tkfont.Font(family="Segoe UI", size=9)
        
        # Pencere boyutu değişikliği için callback
        master.bind("<Configure>", self.on_window_resize)
        self.last_width = master.winfo_width()

        # --- Durum Değişkenleri ---
        self.is_running = False
        self.balls = []
        self.speed_multiplier = 1.0
        self.animation_job = None
        self.current_color = None
        self.current_size = None
        self.grid_lines = []  # Grid çizgilerini saklamak için
        self.last_fps_time = time.time()
        self.fps = 0
        self.frame_count = 0
        self.last_frame_time = time.time()  # Delta time için
        self.collision_enabled = True  # Çarpışma özelliği açık/kapalı

        # --- Header ---
        header_frame = tk.Frame(master, bg="#1a1a1a", height=60)
        header_frame.pack(fill=tk.X, pady=(10, 0))
        
        title_label = tk.Label(header_frame, text="⚫ BALL PHYSICS", 
                              font=self.title_font, fg="#ffffff", bg="#1a1a1a")
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Birleştirilmiş stats+speed label
        stats_label = tk.Label(header_frame, text="Active Objects: 0 | Speed: 1.0x", 
                              font=self.label_font, fg="#888888", bg="#1a1a1a")
        stats_label.pack(side=tk.RIGHT, padx=20)
        self.stats_label = stats_label
        # FPS etiketi ve self.fps_label kaldırıldı

        # --- Canvas (Modern Dark Theme) ---
        canvas_frame = tk.Frame(master, bg="#1a1a1a")
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#0a0a0a", highlightthickness=2,
                          highlightbackground="#333333", width=800, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Canvas boyutu değiştiğinde grid'i yeniden çiz
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # İlk grid çizimi
        self.master.after_idle(self.draw_grid)

        # --- Control Panel ---
        self.control_panel = tk.Frame(master, bg="#1a1a1a", height=120)
        self.control_panel.pack(fill=tk.X, padx=20, pady=(0, 20))

        # SIZE CONTROL
        size_section = tk.Frame(self.control_panel, bg="#1a1a1a")
        size_section.pack(side=tk.LEFT, padx=15)
        
        tk.Label(size_section, text="SIZE", font=self.label_font, 
                fg="#888888", bg="#1a1a1a").pack(anchor=tk.W, pady=(0, 5))
        
        size_container = tk.Frame(size_section, bg="#1a1a1a")
        size_container.pack()
        
        self.size_canvases = {}
        for idx, size in enumerate(TOP_BOYUTLARI):
            size_frame = tk.Frame(size_container, bg="#252525", 
                                 highlightthickness=2, highlightbackground="#333333")
            size_frame.pack(side=tk.LEFT, padx=5)
            
            canvas_size = 70
            draw_size = size - 10  # Hepsi için ciddi bir küçültme
            extra_glow_margin = 5  # biraz daha belirgin glow

            size_btn = tk.Canvas(size_frame, width=canvas_size, height=canvas_size,
                               bg="#252525", highlightthickness=0, cursor="hand2")
            center = canvas_size // 2
            # Glow efekti
            size_btn.create_oval(center - draw_size - extra_glow_margin, center - draw_size - extra_glow_margin,
                               center + draw_size + extra_glow_margin, center + draw_size + extra_glow_margin,
                               fill="#444444", outline="")
            size_btn.create_oval(center - draw_size, center - draw_size,
                               center + draw_size, center + draw_size,
                               fill="#666666", outline="#999999", width=2)
            size_btn.bind("<Button-1>", lambda e, s=size, f=size_frame: self.set_size(s, f))
            size_btn.bind("<Enter>", lambda e, c=size_btn: c.configure(bg="#2a2a2a"))
            size_btn.bind("<Leave>", lambda e, c=size_btn: c.configure(bg="#252525"))
            size_btn.pack(padx=8, pady=8)
            self.size_canvases[size] = size_frame

        # COLOR CONTROL
        color_section = tk.Frame(self.control_panel, bg="#1a1a1a")
        color_section.pack(side=tk.LEFT, padx=15)
        
        tk.Label(color_section, text="COLOR", font=self.label_font,
                fg="#888888", bg="#1a1a1a").pack(anchor=tk.W, pady=(0, 5))
        
        color_container = tk.Frame(color_section, bg="#1a1a1a")
        color_container.pack()
        
        self.color_buttons = {}
        color_names = ["RED", "BLUE", "YELLOW"]
        for idx, (color, name) in enumerate(zip(TOP_RENKLERI, color_names)):
            btn_frame = tk.Frame(color_container, bg="#252525",
                               highlightthickness=2, highlightbackground="#333333")
            btn_frame.pack(side=tk.LEFT, padx=5)
            
            color_btn = tk.Canvas(btn_frame, width=70, height=70, bg=color,
                                highlightthickness=0, cursor="hand2")
            color_btn.bind("<Button-1>", lambda e, c=color, f=btn_frame: self.set_color(c, f))
            color_btn.bind("<Enter>", lambda e, c=color_btn, col=color: c.configure(bg=self.lighten_color(col)))
            color_btn.bind("<Leave>", lambda e, c=color_btn, col=color: c.configure(bg=col))
            color_btn.pack(padx=8, pady=8)
            
            self.color_buttons[color] = btn_frame

        # Separator
        self.sep = tk.Frame(self.control_panel, bg="#333333", width=2)
        self.sep.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

        # ACTIONS
        action_section = tk.Frame(self.control_panel, bg="#1a1a1a")
        action_section.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        tk.Label(action_section, text="CONTROLS", font=self.label_font,
                fg="#888888", bg="#1a1a1a").pack(anchor=tk.W, pady=(0, 5))
        
        buttons_frame = tk.Frame(action_section, bg="#1a1a1a")
        buttons_frame.pack()
        
        # Butonları saklamak için referanslar
        self.buttons_frame = buttons_frame
        self.buttons = {}
        
        # START
        self.buttons['start'] = tk.Button(buttons_frame, text="▶ START", bg="#00C853", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#00E676", cursor="hand2",
                             command=self.start_animation)
        self.buttons['start'].grid(row=0, column=0, padx=5, pady=3, sticky="ew")
        
        # STOP
        self.buttons['stop'] = tk.Button(buttons_frame, text="⏸ STOP", bg="#FF3B30", fg="white",
                            font=self.button_font, bd=0,
                            activebackground="#FF6961", cursor="hand2",
                            command=self.stop_animation)
        self.buttons['stop'].grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        
        # RESET
        self.buttons['reset'] = tk.Button(buttons_frame, text="⟳ RESET", bg="#FF9500", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#FFB340", cursor="hand2",
                             command=self.reset_animation)
        self.buttons['reset'].grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        
        # SPEED UP
        self.buttons['speed_up'] = tk.Button(buttons_frame, text="⚡ BOOST", bg="#5E5CE6", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#7D7AFF", cursor="hand2",
                             command=self.speed_up)
        self.buttons['speed_up'].grid(row=1, column=1, padx=5, pady=3, sticky="ew")
        
        # SPEED DOWN
        self.buttons['speed_down'] = tk.Button(buttons_frame, text="⏪ SLOW", bg="#5856D6", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#7876FF", cursor="hand2",
                             command=self.speed_down)
        self.buttons['speed_down'].grid(row=2, column=0, padx=5, pady=3, sticky="ew")
        
        # DELETE LAST BALL
        self.buttons['delete'] = tk.Button(buttons_frame, text="🗑 DELETE", bg="#AF52DE", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#BF62EE", cursor="hand2",
                             command=self.delete_last_ball)
        self.buttons['delete'].grid(row=2, column=1, padx=5, pady=3, sticky="ew")
        
        # COLLISION TOGGLE
        self.buttons['collision'] = tk.Button(buttons_frame, text="💥 ÇARPIŞMA: AÇIK", bg="#4CAF50", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#66BB6A", cursor="hand2",
                             command=self.toggle_collision)
        self.buttons['collision'].grid(row=3, column=0, columnspan=2, padx=5, pady=3, sticky="ew")

        # --- YENİ: RANDOM 10 BALL BUTONU ---
        self.buttons['random10'] = tk.Button(buttons_frame, text="🎲 10x RANDOM", bg="#00B8D9", fg="white",
                             font=self.button_font, bd=0,
                             activebackground="#33DAFF", cursor="hand2",
                             command=self.random_10_balls)
        self.buttons['random10'].grid(row=4, column=0, columnspan=2, padx=5, pady=9, sticky="ew")
        
        # Grid column ayarları - responsive için
        buttons_frame.grid_columnconfigure(0, weight=1, uniform="btn_col")
        buttons_frame.grid_columnconfigure(1, weight=1, uniform="btn_col")

        # Speed indicator
        self.speed_label = tk.Label(action_section, text="Speed: 1.0x",
                                   font=self.label_font, fg="#888888", bg="#1a1a1a")
        self.speed_label.pack(pady=(5, 0))
        
        # Canvas'a sağ tık ile top silme
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        
        # İlk responsive ayarlama
        self.master.after_idle(self.update_responsive_layout)

    def on_window_resize(self, event):
        """Pencere boyutu değiştiğinde çağrılır."""
        # Sadece ana pencere boyutu değişikliğini kontrol et
        if event.widget == self.master:
            current_width = self.master.winfo_width()
            # Önemli bir değişiklik varsa güncelle (5 piksel tolerans)
            if abs(current_width - self.last_width) > 5:
                self.last_width = current_width
                self.update_responsive_layout()

    def update_responsive_layout(self):
        """Butonları ve fontları ekran boyutuna göre günceller."""
        try:
            window_width = self.master.winfo_width()
            if window_width < 100:  # Henüz render edilmemiş
                return
            
            # Font boyutunu pencere genişliğine göre ayarla
            if window_width < 700:
                font_size = 7
                button_font_size = 8
                button_char_width = 8
            elif window_width < 900:
                font_size = 8
                button_font_size = 9
                button_char_width = 9
            elif window_width < 1200:
                font_size = 9
                button_font_size = 10
                button_char_width = 10
            else:
                font_size = 10
                button_font_size = 11
                button_char_width = 12
            
            # Fontları güncelle
            self.button_font.configure(size=button_font_size)
            self.label_font.configure(size=font_size)
            
            # Buton genişliklerini güncelle (Tkinter'de width karakter cinsinden)
            if hasattr(self, 'buttons') and self.buttons:
                for btn in self.buttons.values():
                    btn.configure(width=button_char_width)
                    
        except Exception as e:
            # Hata durumunda sessizce devam et
            pass

    def lighten_color(self, color):
        """Rengi açıklaştırır (hover efekti için)."""
        # Hex rengi RGB'ye çevir
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # %20 açıklaştır
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_grid(self):
        """Grid çizgilerini dinamik olarak çizer."""
        # Eski grid çizgilerini sil
        for line_id in self.grid_lines:
            self.canvas.delete(line_id)
        self.grid_lines.clear()
        
        # Canvas boyutunu al
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        # Dikey çizgiler
        for i in range(0, canvas_width, GRID_ARALIK):
            line_id = self.canvas.create_line(i, 0, i, canvas_height, 
                                             fill="#151515", width=1, tags="grid")
            self.grid_lines.append(line_id)
        
        # Yatay çizgiler
        for i in range(0, canvas_height, GRID_ARALIK):
            line_id = self.canvas.create_line(0, i, canvas_width, i, 
                                             fill="#151515", width=1, tags="grid")
            self.grid_lines.append(line_id)
        
        # Grid çizgilerini en alta gönder
        self.canvas.tag_lower("grid")

    def on_canvas_configure(self, event):
        """Canvas boyutu değiştiğinde çağrılır."""
        self.draw_grid()
        # Grid çizgilerini her zaman en alta gönder (topların üstünde kalmaması için)
        self.canvas.tag_lower("grid")

    def on_canvas_right_click(self, event):
        """Canvas'a sağ tıklandığında en yakın topu siler."""
        if not self.balls:
            return
        
        # En yakın topu bul
        min_distance = float('inf')
        closest_ball = None
        
        for ball in self.balls:
            dx = event.x - ball.x
            dy = event.y - ball.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < min_distance and distance < ball.size + 20:
                min_distance = distance
                closest_ball = ball
        
        if closest_ball:
            self.delete_ball(closest_ball)

    def set_color(self, color, frame):
        """Seçilen top rengini ayarlar."""
        # Tüm renk frame'lerini normal hale getir
        for f in self.color_buttons.values():
            f.configure(highlightbackground="#333333", highlightthickness=2)
        
        # Seçili frame'i vurgula
        frame.configure(highlightbackground=color, highlightthickness=3)
        
        self.current_color = color
        print(f"Seçilen Renk: {color}")
        
        if self.current_size is not None:
            self.add_ball()
            self.reset_selection()

    def set_size(self, size, frame):
        """Seçilen top boyutunu ayarlar."""
        # Tüm boyut frame'lerini normal hale getir
        for f in self.size_canvases.values():
            f.configure(highlightbackground="#333333", highlightthickness=2)
        
        # Seçili frame'i vurgula
        frame.configure(highlightbackground="#00C853", highlightthickness=3)
        
        self.current_size = size
        print(f"Seçilen Boyut: {size}")
        
        if self.current_color is not None:
            self.add_ball()
            self.reset_selection()

    def find_safe_position(self, size, max_attempts=100):
        """Mevcut toplarla çakışmayacak güvenli bir konum bulur."""
        self.canvas.update_idletasks()
        canvas_width = max(self.canvas.winfo_width(), 100)
        canvas_height = max(self.canvas.winfo_height(), 100)
        
        for attempt in range(max_attempts):
            # Random konum dene
            x = random.randint(size + 20, canvas_width - size - 20)
            y = random.randint(size + 20, canvas_height - size - 20)
            
            # Mevcut toplarla çakışma kontrolü
            collision = False
            for ball in self.balls:
                dx = x - ball.x
                dy = y - ball.y
                distance = math.sqrt(dx * dx + dy * dy)
                min_distance = size + ball.size + 10  # 10 piksel ekstra boşluk
                
                if distance < min_distance:
                    collision = True
                    break
            
            # Çakışma yoksa bu konumu kullan
            if not collision:
                return x, y
        
        # Tüm denemeler başarısız olduysa, merkeze yakın bir yere yerleştir
        return canvas_width // 2, canvas_height // 2
    
    def add_ball(self):
        """Seçili renk ve boyutta yeni bir top ekler."""
        if len(self.balls) >= MAX_TOP_SAYISI:
            print(f"[UYARI] Maksimum top sayısına ulaşıldı ({MAX_TOP_SAYISI})")
            return
            
        if self.current_color and self.current_size:
            # Güvenli bir konum bul
            safe_x, safe_y = self.find_safe_position(self.current_size)
            
            # Topu güvenli konumda oluştur
            new_ball = Ball(self.canvas, self.current_size, self.current_color, safe_x, safe_y)
            self.balls.append(new_ball)
            # Grid çizgilerini her zaman en alta gönder
            self.canvas.tag_lower("grid")
            self.update_stats()
            print(f"Top eklendi: Boyut={self.current_size}, Renk={self.current_color}")

    def delete_ball(self, ball):
        """Belirtilen topu siler."""
        if ball in self.balls:
            self.canvas.delete(ball.shadow_id)
            self.canvas.delete(ball.id)
            self.balls.remove(ball)
            self.update_stats()
            print("Top silindi")

    def delete_last_ball(self):
        """Son eklenen topu siler."""
        if self.balls:
            last_ball = self.balls[-1]
            self.delete_ball(last_ball)

    def reset_selection(self):
        """Seçimleri sıfırlar."""
        self.current_color = None
        self.current_size = None
        
        # Frame vurgularını kaldır
        for f in self.color_buttons.values():
            f.configure(highlightbackground="#333333", highlightthickness=2)
        for f in self.size_canvases.values():
            f.configure(highlightbackground="#333333", highlightthickness=2)

    def update_stats(self):
        """İstatistikleri ve hızı birlikte günceller."""
        self.stats_label.config(text=f"Active Objects: {len(self.balls)}/{MAX_TOP_SAYISI} | Speed: {self.speed_multiplier:.1f}x")
        
    def update_fps(self):
        """FPS'i hesaplar ve günceller."""
        current_time = time.time()
        self.frame_count += 1
        
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_fps_time = current_time
            # self.fps_label.config(text=f"FPS: {self.fps}") # Bu satır kaldırıldı
        
    def start_animation(self):
        """Topların hareketini başlatır."""
        if not self.is_running:
            self.is_running = True
            self.last_frame_time = time.time()  # Delta time için başlangıç zamanı
            print("[OK] Animasyon BAŞLATILDI.")
            self.animate()
    
    def stop_animation(self):
        """Topların hareketini durdurur."""
        if self.is_running:
            self.is_running = False
            if self.animation_job:
                self.master.after_cancel(self.animation_job)
            print("[DURDUR] Animasyon DURDURULDU.")
            
    def reset_animation(self):
        """Ekrandaki tüm topları siler ve varsayılan duruma döner."""
        self.stop_animation()
        for ball in self.balls:
            self.canvas.delete(ball.shadow_id)
            self.canvas.delete(ball.id)
        self.balls = []
        self.speed_multiplier = 1.0
        self.reset_selection()
        self.update_stats()
        self.speed_label.config(text="Speed: 1.0x")
        print("[RESET] Ekran SIFIRLANDI.")

    def speed_up(self):
        """Hızı artırır."""
        self.speed_multiplier *= 1.3
        if self.speed_multiplier > 5: 
             self.speed_multiplier = 5
        self.update_stats()
        self.speed_label.config(text=f"Speed: {self.speed_multiplier:.1f}x")
        print(f"[HIZ+] Hız ARTTIRILDI. Çarpan: {self.speed_multiplier:.2f}")

    def speed_down(self):
        """Hızı azaltır."""
        self.speed_multiplier /= 1.3
        if self.speed_multiplier < 0.1:
            self.speed_multiplier = 0.1
        self.update_stats()
        self.speed_label.config(text=f"Speed: {self.speed_multiplier:.1f}x")
        print(f"[HIZ-] Hız AZALTILDI. Çarpan: {self.speed_multiplier:.2f}")
    
    def toggle_collision(self):
        """Çarpışma özelliğini açar/kapatır."""
        self.collision_enabled = not self.collision_enabled
        if self.collision_enabled:
            self.buttons['collision'].config(text="💥 ÇARPIŞMA: AÇIK", bg="#4CAF50", activebackground="#66BB6A")
            print("[ÇARPIŞMA] Çarpışma özelliği AÇILDI.")
        else:
            self.buttons['collision'].config(text="💥 ÇARPIŞMA: KAPALI", bg="#757575", activebackground="#9E9E9E")
            print("[ÇARPIŞMA] Çarpışma özelliği KAPANDI.")

    def animate(self):
        """Animasyon döngüsünü yürütür. Delta time ile stabil hız."""
        if self.is_running:
            # Delta time hesapla (geçen süre - saniye cinsinden)
            current_time = time.time()
            delta_time = current_time - self.last_frame_time
            self.last_frame_time = current_time
            
            # Delta time çok büyükse (örneğin pencere minimize edildi), sınırla
            # Bu, animasyonun donmasını önler
            if delta_time > 0.1:
                delta_time = 0.1
            
            # Yüksek hızlarda tunneling'i önlemek için hareketi küçük adımlara böl
            # Hız çarpanına göre adım sayısını ayarla
            steps = max(1, int(self.speed_multiplier))
            step_delta = delta_time / steps
            
            for step in range(steps):
                # Topları küçük adımlarla hareket ettir
                for ball in self.balls:
                    ball.move(step_delta, self.speed_multiplier)
                
                # Her adımda çarpışma kontrolü (yüksek hızlarda tunneling'i önler)
                # Çarpışma özelliği açıksa kontrol et
                if self.collision_enabled:
                    processed_collisions = set()
                    for i in range(len(self.balls)):
                        for j in range(i + 1, len(self.balls)):
                            # Aynı çarpışmayı birden fazla işlememek için kontrol
                            collision_key = (min(i, j), max(i, j))
                            if collision_key not in processed_collisions:
                                if self.balls[i].check_collision(self.balls[j]):
                                    processed_collisions.add(collision_key)
            
            # FPS güncelle
            # self.update_fps() # Bu satır kaldırıldı

            # Sabit frame rate için delay (hız çarpanı delay'i etkilemez, sadece hareket hızını)
            delay = int(TEMEL_GECIKME_MS)
            self.animation_job = self.master.after(delay, self.animate)

    def random_10_balls(self):
        """Canvas'a rastgele renk ve boyutta 10 top ekler."""
        from random import choice
        for _ in range(10):
            if len(self.balls) >= MAX_TOP_SAYISI:
                break
            size = choice(TOP_BOYUTLARI)
            color = choice(TOP_RENKLERI)
            self.current_size = size
            self.current_color = color
            self.add_ball()
        self.reset_selection()

# --- Uygulamayı Çalıştırma ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.resizable(False, False)
    root.configure(bg="#1a1a1a")
    app = BallAnimationApp(root)
    root.mainloop()
