# 🔐 Playfair Shifr Algoritmi

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Playfair (Two-Square) shifrlash algoritmining **Hacker Terminal** uslubidagi interaktiv GUI dasturi. Python va PyQt5 yordamida yaratilgan.

---

## 📸 Ko'rinish

> Dastur qora fon, yashil terminal uslubida ishlaydi. Matritsalar real vaqtda yangilanadi, natija animatsiya bilan chiqadi.

---

## ✨ Imkoniyatlar

- 🔒 **Shifrlash** — matnni Playfair algoritmi bilan shifrlash
- 🔓 **Deshifrlash** — shifrlangan matnni asl holatiga qaytarish
- 📊 **Ikki 5×5 matritsa** — Matritsa 1 (standart alifbo) + Matritsa 2 (kalit asosida)
- ✨ **Animatsiyalar** — boot flicker, typing effekt, katak yonib-o'chishi
- 🔍 **Interaktiv harflar** — alifbo panelida harfga sichqon olib borganingizda ikki matritsada pozitsiya ko'rsatiladi
- 🟡 **I/J bitta katakda** — Playfair qoidasiga muvofiq, oltin rang bilan ajratilgan
- 💾 **Nusxalash** — natijani bir tugma bilan buferga nusxalash
- 📝 **Bo'sh joy saqlanadi** — deshifrlashda so'zlar orasidagi bo'sh joy qaytariladi

---

## 🚀 O'rnatish

### Talablar
- Python 3.10 yoki yuqori
- PyQt5

### Qadamlar

```bash
# 1. Repozitoriyani klonlang
git clone https://github.com/coder06-cpp/playfair-cipher.git
cd playfair-cipher

# 2. Kutubxonalarni o'rnating
pip install -r requirements.txt

# 3. Dasturni ishga tushiring
python playfair_gui.py
```

---

## 📖 Ishlatish

1. **Kalit so'z** maydoniga kalit kiriting (masalan: `UZBEKISTON`)
2. **Kiruvchi matn** maydoniga matn kiriting
3. **🔒 SHIFRLASH** tugmasini bosing — natija animatsiya bilan chiqadi
4. Deshifrlash uchun shifrlangan matnni kiriting va **🔓 DESHIFRLASH** tugmasini bosing

### Kontrol misol
```
Kalit:       UZBEKISTON
Matn:        INTILEKT
Shifrlangan: KI IH AF FO
Deshifr:     INTILEKT ✅
```

---

## 🧮 Algoritm haqida

**Two-Square Playfair** — klassik Playfair shifrining kuchaytirilgan varianti:

| | Matritsa 1 | Matritsa 2 |
|--|--|--|
| Tarkibi | Standart alifbo (A–Z, J yo'q) | Kalit so'z asosida quriladi |
| Rangi | 🟢 Yashil | 🔵 Ko'k |

### Shifrlash qoidalari
- **Bir xil qatorda** → o'ngga siljish (aylanib)
- **To'rtburchak** → `M1[r2][c1]` va `M2[r1][c2]`
- **J harfi** → har doim I bilan almashtiriladi

---

## 📁 Fayl tuzilishi

```
playfair-cipher/
├── playfair_gui.py    # Asosiy dastur (algoritm + GUI)
├── requirements.txt   # Kutubxonalar
└── README.md          # Hujjat
```

---

## 🛠 Texnologiyalar

| Texnologiya | Maqsad |
|--|--|
| Python 3.10+ | Asosiy til |
| PyQt5 | Grafik interfeys |
| QTimer | Animatsiyalar |
| QPainter | CRT scanline effekti |

---

## 👨‍💻 Muallif

**Quvonchbek** — [@coder06-cpp](https://github.com/coder06-cpp)

TATU Samarqand filiali — Kompyuter injiniringi fakulteti, Sun'iy intellekt yo'nalishi

---

## 📄 Litsenziya

MIT License — erkin foydalanish mumkin.
