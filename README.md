# Chatbot Form Doldurma Uygulaması

Türkçe AI destekli chatbot ile form toplama uygulaması.

## ⚙️ Teknolojiler

- **Backend:** Python, FastAPI, Uvicorn, Requests
- **AI Model:** Ollama üzerinde `erdiari/llama3-turkish:latest` (Llama 3 Turkish)
- **Frontend:** HTML, CSS, JavaScript
- **Veri Kayıt:** `form_data.json` (JSON formatında, UTF-8)

## 🚀 Kurulum

### 1. Depoyu klonlayın
```bash
git clone https://github.com/SerdarK44/chatbot-form.git
cd chatbot-form
```

### 2. Backend kurulumu
```bash
cd backend
python -m venv venv       # opsiyonel: sanal ortam oluşturma
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install fastapi uvicorn requests
```

### 3. Ollama Modelini Başlatın
```bash
ollama run erdiari/llama3-turkish:latest
```

### 4. FastAPI Sunucusunu Çalıştırın
```bash
uvicorn main:app --reload --port 8000
```

### 5. Frontend sunucusunu çalıştırın
```bash
cd ../frontend
python -m http.server 8080
```

## 🌐 Kullanım

1. Tarayıcıyı açın: `http://127.0.0.1:8080`
2. Chat arayüzünde sorulan sorulara cevap verin.
3. Tüm alanlar doldurulduğunda form `form_data.json` dosyasına kaydedilecek.

## 📁 Proje Yapısı

```
/chatbot-form/
├── backend/
│   ├── main.py            # FastAPI sunucusu & form işleme
│   ├── form_data.json     # Kaydedilen form verileri
│   └── venv/              # (opsiyonel) sanal ortam
├── frontend/
│   ├── index.html         # Chat arayüzü
│   ├── style.css          # Stil tanımları
│   └── app.js             # Frontend mesaj yönetimi
└── README.md              # Proje tanıtımı ve kurulum
```

## 🛠️ Özellikler

- Türkçe doğal dil ile form doldurma
- Eksik veya geçersiz ("hayır", "bilmiyorum") cevaplar için tekrar sorgulama
- Ad, Soyad, Doğum Tarihi, E-posta, Telefon, Adres alanları
- Veri temizleme (ad/soyad büyük harf, telefon formatlama, e-posta küçültme)
- Responsive, modern chat UI

## 📄 Lisans

Bu proje MIT lisansı ile sunulmuştur. Detaylar için `LICENSE` dosyasına bakınız.

