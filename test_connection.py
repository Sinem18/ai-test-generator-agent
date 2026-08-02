
"""
Gemini API bağlantı testi (güncel google-genai kütüphanesi).
Çalıştırmak için: python test_connection.py
"""

import os
from dotenv import load_dotenv
from google import genai

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# API key'i ortam değişkeninden al
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Basit bir istek gönder
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Merhaba! Sen kimsin, kısaca tanıt."
)

print(response.text)