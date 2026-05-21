import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os, math

# ======================================================
#  KONFIGURASI IDOL  (sudah diisi otomatis)
# ======================================================
IDOL_NAME      = "Mingyu"
IDOL_FULLNAME  = "Kim Mingyu (김민규)"
IDOL_GROUP     = "SEVENTEEN (SVT)"
IDOL_BIRTHDATE = "6 April 1997"
IDOL_POSITION  = "Rapper · Vocalist · Visual"
IDOL_HEIGHT    = "187 cm"

# ======================================================
#  WARNA TEMA  — biru muda & emas
# ======================================================
BG          = "#C9DFF0"   # biru muda background utama
DARK_NAVY   = "#0D2137"   # navy gelap
MID_BLUE    = "#2E6DA4"   # biru sedang aksen
LIGHT_BLUE  = "#E8F4FD"   # putih kebiruan kartu
GOLD        = "#C9A84C"   # emas utama
LIGHT_GOLD  = "#F2D785"   # emas muda highlight
TEXT_DARK   = "#0D2137"
TEXT_MID    = "#2E5F88"
WHITE       = "#FFFFFF"

# ======================================================
#  NAMA FILE GAMBAR  (harus 1 folder dengan script ini)
# ======================================================
PORTRAIT_IMGS  = [
    "mingyu_walpapper.jpeg",
    "Mingyu.jpeg",
    "580119995791993812.jpeg",
]
LANDSCAPE_IMGS = [
    "754071531396493649.jpeg",
    "758786237258048067.jpeg",
    "__Mingyu_Scrapbook__.jpeg",
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ─────────────────────────────────────────────────────
#  HELPER: buat canvas background dekoratif
# ─────────────────────────────────────────────────────
def make_bg_image(w, h):
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    # Lingkaran dekoratif transparan
    circles = [
        (50,  50,  160, "#B0D0EA"),
        (w-80, 80, 200, "#A8C8E8"),
        (w//2, h-60, 240, "#BDDAF0"),
        (30,  h-100, 120, "#C5D8EC"),
        (w-30, h//2, 100, "#B5CEEA"),
    ]
    for cx, cy, r, col in circles:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col, outline=None)

    # Titik-titik emas kecil
    import random; random.seed(42)
    for _ in range(60):
        x, y = random.randint(0, w), random.randint(0, h)
        r = random.randint(2, 5)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=GOLD)

    return img.filter(ImageFilter.GaussianBlur(6))


# ─────────────────────────────────────────────────────
#  HELPER: rounded border frame (gold border)
# ─────────────────────────────────────────────────────
def gold_frame(parent, **kw):
    outer = tk.Frame(parent, bg=GOLD, padx=3, pady=3, **kw)
    inner = tk.Frame(outer, bg=LIGHT_BLUE)
    inner.pack(fill="both", expand=True)
    return outer, inner


# ======================================================
#  APLIKASI UTAMA
# ======================================================
class MingYuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💙 MINGYU SVT — Fan Card")
        self.root.resizable(True, True)
        self.refs = []        # simpan ImageTk agar tidak di-GC
        self.name_var = tk.StringVar()
        self._show_input()

    # ──────────────────────────────────────────────
    #  LAYAR 1: INPUT NAMA
    # ──────────────────────────────────────────────
    def _show_input(self):
        self.root.geometry("600x500")
        self._clear()
        self.refs.clear()

        # Background canvas
        bg_img = make_bg_image(600, 500)
        bg_tk  = ImageTk.PhotoImage(bg_img)
        self.refs.append(bg_tk)

        canvas = tk.Canvas(self.root, width=600, height=500,
                           highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=bg_tk)

        # ── judul ──
        canvas.create_text(300, 55,
            text="✨ SEVENTEEN · MINGYU FAN CARD ✨",
            font=("Georgia", 16, "bold"), fill=DARK_NAVY)
        canvas.create_text(300, 85,
            text="Hello Semua! 💙  Masukkan nama kamu ya~",
            font=("Arial", 11), fill=MID_BLUE)

        # ── kartu tengah ──
        card = tk.Frame(canvas, bg=LIGHT_BLUE, padx=35, pady=30)
        card_border = tk.Frame(canvas, bg=GOLD, padx=3, pady=3)
        card_border_inner = tk.Frame(card_border, bg=LIGHT_BLUE,
                                     padx=35, pady=30)
        card_border_inner.pack()
        canvas.create_window(300, 270, window=card_border, anchor="center")

        tk.Label(card_border_inner,
                 text="Siapa nama kamu?",
                 font=("Arial", 14, "bold"),
                 fg=DARK_NAVY, bg=LIGHT_BLUE).pack(pady=(0, 8))

        entry = tk.Entry(card_border_inner, textvariable=self.name_var,
                         font=("Arial", 15), width=22,
                         relief="flat", bd=0,
                         highlightthickness=2,
                         highlightbackground=MID_BLUE,
                         highlightcolor=GOLD,
                         fg=DARK_NAVY, justify="center")
        entry.pack(ipady=6)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self._goto_fancard())

        tk.Label(card_border_inner, text="", bg=LIGHT_BLUE).pack()

        btn = tk.Button(card_border_inner,
                        text="  ✨  Lihat Fan Card  ✨  ",
                        command=self._goto_fancard,
                        font=("Arial", 12, "bold"),
                        bg=GOLD, fg=DARK_NAVY,
                        activebackground=LIGHT_GOLD,
                        relief="flat", cursor="hand2",
                        padx=18, pady=9)
        btn.pack()

        # ── info idol bawah ──
        canvas.create_text(300, 430,
            text=f"🎤  {IDOL_FULLNAME}  |  {IDOL_GROUP}",
            font=("Arial", 10, "bold"), fill=DARK_NAVY)
        canvas.create_text(300, 455,
            text=f"🎂 {IDOL_BIRTHDATE}   ·   📏 {IDOL_HEIGHT}   ·   ⭐ {IDOL_POSITION}",
            font=("Arial", 9), fill=MID_BLUE)

    # ──────────────────────────────────────────────
    #  LAYAR 2: FAN CARD LENGKAP
    # ──────────────────────────────────────────────
    def _goto_fancard(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Oops!", "Isi nama kamu dulu ya! 😊")
            return
        self.root.geometry("1100x850")
        self._clear()
        self.refs.clear()
        self._build_fancard(name)

    def _build_fancard(self, name):
        # ── scrollable canvas ──
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        vbar   = ttk.Scrollbar(outer, orient="vertical",
                               command=canvas.yview)
        scroll = tk.Frame(canvas, bg=BG)

        scroll.bind("<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.configure(yscrollcommand=vbar.set)
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(
                int(-1*(e.delta/120)), "units"))

        canvas.pack(side="left", fill="both", expand=True)
        vbar.pack(side="right", fill="y")

        # ═══════════════════════════════════════════
        #  HEADER
        # ═══════════════════════════════════════════
        hdr = tk.Frame(scroll, bg=DARK_NAVY, pady=22)
        hdr.pack(fill="x", padx=18, pady=(18, 0))

        tk.Label(hdr, text="💙  K - P O P   F A N   C A R D  💙",
                 font=("Georgia", 10, "bold"),
                 fg=LIGHT_GOLD, bg=DARK_NAVY).pack()
        tk.Label(hdr,
                 text=f"Hallo semua! Perkenalkan saya  {name}  👋",
                 font=("Georgia", 20, "bold"),
                 fg=WHITE, bg=DARK_NAVY).pack(pady=6)
        tk.Label(hdr,
                 text=f"dengan bias saya  💛  {IDOL_NAME}  dari  {IDOL_GROUP}  💛",
                 font=("Arial", 13),
                 fg=LIGHT_GOLD, bg=DARK_NAVY).pack()

        # ═══════════════════════════════════════════
        #  INFO STRIP
        # ═══════════════════════════════════════════
        strip = tk.Frame(scroll, bg=MID_BLUE, pady=10)
        strip.pack(fill="x", padx=18)

        info = (f"🎤  {IDOL_FULLNAME}     "
                f"🎸  {IDOL_GROUP}     "
                f"🎂  {IDOL_BIRTHDATE}     "
                f"📏  {IDOL_HEIGHT}     "
                f"⭐  {IDOL_POSITION}")
        tk.Label(strip, text=info,
                 font=("Arial", 10, "bold"),
                 fg=WHITE, bg=MID_BLUE,
                 wraplength=1050).pack()

        # ═══════════════════════════════════════════
        #  PESAN
        # ═══════════════════════════════════════════
        msg_outer = tk.Frame(scroll, bg=GOLD, padx=3, pady=3)
        msg_outer.pack(fill="x", padx=18, pady=14)
        msg_inner = tk.Frame(msg_outer, bg=LIGHT_BLUE, padx=28, pady=20)
        msg_inner.pack(fill="x")

        tk.Label(msg_inner,
                 text="💬  Kata-kata dari saya",
                 font=("Arial", 10, "bold"),
                 fg=GOLD, bg=LIGHT_BLUE,
                 anchor="w").pack(fill="x")

        msg = self._gen_message(name)
        tk.Label(msg_inner, text=msg,
                 font=("Arial", 11),
                 fg=TEXT_DARK, bg=LIGHT_BLUE,
                 wraplength=1010, justify="left").pack(
                     fill="x", pady=(8, 0))

        # ═══════════════════════════════════════════
        #  GALERI FOTO
        # ═══════════════════════════════════════════
        tk.Label(scroll,
                 text="━━━━━━━━   📸  PHOTO GALLERY  📸   ━━━━━━━━",
                 font=("Arial", 12, "bold"),
                 fg=DARK_NAVY, bg=BG).pack(pady=(6, 4))

        # ── portrait row ──
        p_row = tk.Frame(scroll, bg=BG)
        p_row.pack(pady=5)
        self._load_photos(p_row, PORTRAIT_IMGS, (210, 373))

        # ── landscape row ──
        l_row = tk.Frame(scroll, bg=BG)
        l_row.pack(pady=5)
        self._load_photos(l_row, LANDSCAPE_IMGS, (330, 186))

        # ═══════════════════════════════════════════
        #  FOOTER
        # ═══════════════════════════════════════════
        ftr = tk.Frame(scroll, bg=DARK_NAVY, pady=16)
        ftr.pack(fill="x", padx=18, pady=(14, 18))

        tk.Label(ftr,
                 text="💙  Always support SEVENTEEN — MINGYU  💙",
                 font=("Arial", 12, "bold"),
                 fg=LIGHT_GOLD, bg=DARK_NAVY).pack()
        tk.Label(ftr,
                 text="#SEVENTEEN  #SVT  #Mingyu  #Kpop  #김민규",
                 font=("Arial", 9),
                 fg=MID_BLUE, bg=DARK_NAVY).pack(pady=3)

        back = tk.Button(ftr, text="← Kembali",
                         command=self._show_input,
                         font=("Arial", 10),
                         bg=MID_BLUE, fg=WHITE,
                         relief="flat", cursor="hand2",
                         padx=15, pady=5)
        back.pack(pady=(5, 0))

    # ──────────────────────────────────────────────
    #  LOAD & TAMPILKAN FOTO
    # ──────────────────────────────────────────────
    def _load_photos(self, parent, fnames, size):
        for fname in fnames:
            path = os.path.join(SCRIPT_DIR, fname)
            try:
                img = Image.open(path)
                img = img.resize(size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.refs.append(photo)

                border = tk.Frame(parent, bg=GOLD, padx=3, pady=3)
                border.pack(side="left", padx=10)
                tk.Label(border, image=photo, bg=GOLD).pack()
            except Exception as e:
                placeholder = tk.Frame(parent,
                    bg=LIGHT_BLUE, width=size[0], height=size[1])
                placeholder.pack_propagate(False)
                placeholder.pack(side="left", padx=10)
                tk.Label(placeholder, text=f"📷\n{fname}\ntidak ditemukan",
                         font=("Arial", 9), fg=MID_BLUE,
                         bg=LIGHT_BLUE).pack(expand=True)

    # ──────────────────────────────────────────────
    #  GENERATE PESAN
    # ──────────────────────────────────────────────
    def _gen_message(self, name):
        return (
            f"Halo semua, nama saya {name} dan saya mau jujur nih — "
            f"saya ini udah lama banget tergila-gila sama satu sosok: "
            f"{IDOL_NAME} dari {IDOL_GROUP}, lahir {IDOL_BIRTHDATE}. "
            f"Sebagai sesama cowok, ngeliat dia tuh... aduh, bikin insecure parah. "
            f"Tinggi {IDOL_HEIGHT}, wajahnya rapih, style-nya keren, "
            f"suaranya bagus, dance-nya powerful — dia tuh paket lengkap banget sih.\n\n"
            f"Tiap nonton konsernya atau liat foto shoots-nya, "
            f"saya langsung auto ngebandingin diri sendiri dan ya... kalah telak haha. "
            f"Tapi bukan berarti saya nyerah — justru {IDOL_NAME} yang bikin "
            f"saya makin termotivasi buat upgrade diri. Kalau dia bisa se-totalitas "
            f"itu di panggung sambil tetap humble, kenapa saya nggak bisa lebih "
            f"serius sama hidup saya sendiri? Dia itu buat saya kayak benchmark "
            f"— 'Mingyu aja bisa, masa kamu nggak!'\n\n"
            f" {IDOL_NAME} adalah bukti "
            f"nyata bahwa kerja keras + bakat + attitude yang baik itu bisa "
            f"membawa seseorang ke level yang luar biasa. "
            f"Makanya saya tergila-gila sama dia — bukan karena apa-apa, "
            f"tapi murni kagum dan terinspirasi! 💙✨"
        )

    # ──────────────────────────────────────────────
    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()


# ======================================================
if __name__ == "__main__":
    root = tk.Tk()
    app  = MingYuApp(root)
    root.mainloop()
