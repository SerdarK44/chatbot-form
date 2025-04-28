from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os
import re

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "erdiari/llama3-turkish:latest"
FORM_DATA_FILE = "form_data.json"

# İlk JSON dosyasını oluştur
if not os.path.exists(FORM_DATA_FILE):
    with open(FORM_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)


# ——— Yardımcı Fonksiyonlar ———

def extract_json(text: str) -> dict:
    """
    Gelen metindeki ilk {...} bloğunu bulur ve dict olarak döner.
    """
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if not match:
        raise ValueError("Yanıtta JSON bulunamadı")
    return json.loads(match.group(1))


def field_to_question(field: str) -> str:
    questions = {
        "isim": "Lütfen isminizi yazar mısınız?",
        "soyisim": "Lütfen soyisminizi yazar mısınız?",
        "dogum_tarihi": "Lütfen doğum tarihinizi yazar mısınız?",
        "email": "Lütfen e-posta adresinizi yazar mısınız?",
        "telefon": "Lütfen telefon numaranızı yazar mısınız?",
        "adres": "Lütfen adresinizi yazar mısınız?"
    }
    return questions.get(field, f"{field} bilgisi eksik, tamamlar mısınız?")


def clean_name(name: str) -> str:
    return " ".join(w.capitalize() for w in name.split())


def clean_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return f"0{digits[:3]} {digits[3:6]} {digits[6:]}"
    elif len(digits) == 11:
        return f"{digits[:4]} {digits[4:7]} {digits[7:]}"
    return phone.strip()


def clean_email(email: str) -> str:
    return email.strip().lower()


def clean_address(address: str) -> str:
    addr = address.strip()
    return addr.capitalize() if addr else addr


def clean_form(form: dict) -> dict:
    return {
        "isim": clean_name(form.get("isim", "")),
        "soyisim": clean_name(form.get("soyisim", "")),
        "dogum_tarihi": form.get("dogum_tarihi", "").strip(),
        "email": clean_email(form.get("email", "")),
        "telefon": clean_phone(form.get("telefon", "")),
        "adres": clean_address(form.get("adres", ""))
    }


def ask_ollama(message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": f"""
Kullanıcıdan gelen metni analiz et ve aşağıdaki alanları JSON formatında çıkart:
- isim
- soyisim
- dogum_tarihi
- email
- telefon
- adres

Eğer eksik bilgi varsa boş string ("") olarak dön.

Mesaj: {message}

Sadece JSON formatında cevap ver.
""",
        "stream": False
    }
    resp = requests.post(OLLAMA_API_URL, json=payload)
    resp.raise_for_status()
    return resp.json().get("response", "")


def is_invalid_response(val: str) -> bool:
    invalids = {"", "hayır", "bilmiyorum", "yok", "boş"}
    return val.strip().lower() in invalids


# ——— API Endpoint ———

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    current_form = body.get("current_form", {})
    beklenen = body.get("beklenen_alan")

    try:
        # 1) Spesifik alan soruluyorsa doğrudan ata
        if beklenen:
            current_form[beklenen] = message.strip()
        else:
            # 2) Aksi halde Ollama'dan genel tahmin al
            raw = ask_ollama(message)
            tahmin = extract_json(raw)
            for k, v in tahmin.items():
                if not current_form.get(k):
                    current_form[k] = v.strip()

        # 3) Eksik veya invalid alanları tespit et
        alanlar = ["isim","soyisim","dogum_tarihi","email","telefon","adres"]
        eksik = [f for f in alanlar if is_invalid_response(current_form.get(f,""))]

        # 4) Eğer hiç eksik kalmadıysa kaydet
        if not eksik:
            temiz = clean_form(current_form)
            with open(FORM_DATA_FILE, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(temiz)
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
            return {
                "status": "completed",
                "data": temiz,
                "message": "Form başarıyla tamamlandı. Teşekkürler!"
            }

        # 5) Eksik alan varsa sıradakini sor
        next_field = eksik[0]
        return {
            "status": "incomplete",
            "data": current_form,
            "next_question": field_to_question(next_field),
            "beklenen_alan": next_field
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
