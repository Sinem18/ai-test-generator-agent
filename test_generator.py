
"""
Python fonksiyonlarını analiz edip otomatik Pytest test senaryosu üreten agent.
Çalıştırmak için: python test_generator.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# --- Test edeceğimiz örnek fonksiyon ---
# Gerçek kullanımda bu, herhangi bir dosyadan okunabilir.
# Şimdilik basit tutuyoruz, kodun kendisini bir metin (string) olarak veriyoruz.
KOD_ORNEGI = """
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
"""


# --- Modelin çağırabileceği araç: test dosyasına yazma ---
def test_dosyasina_yaz(dosya_adi: str, icerik: str) -> str:
    """Verilen içeriği bir Python test dosyasına yazar."""
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(icerik)
    print(f"[LOG] '{dosya_adi}' dosyası yazıldı ({len(icerik)} karakter)")
    return f"'{dosya_adi}' başarıyla oluşturuldu."


# --- Modele görevi tanımlıyoruz ---
prompt = f"""
Aşağıdaki Python fonksiyonu için kapsamlı Pytest test senaryoları yaz.
Eşdeğerlik sınıflarını ve sınır değerleri dikkate al (örneğin negatif sayılar,
0, 1, küçük asal sayılar, büyük asal olmayan sayılar gibi).

Fonksiyon:
{KOD_ORNEGI}

Üretilen testleri 'test_dosyasina_yaz' aracını kullanarak
'test_generated_is_prime.py' dosyasına yaz. Testler pytest formatında,
'from is_prime_module import is_prime' importu ile başlamalı.
"""

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[test_dosyasina_yaz]
    ),
)

print("\nModelin cevabı:")
print(response.text)