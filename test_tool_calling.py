
"""
Gemini ile temel tool/function calling örneği.
Çalıştırmak için: python test_tool_calling.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# --- 1) Modelin çağırabileceği gerçek Python fonksiyonu ---
def iki_sayiyi_carp(a: float, b: float) -> float:
    """İki sayıyı çarpar ve sonucu döndürür."""
    print(f"[LOG] iki_sayiyi_carp çağrıldı: {a} x {b}")
    return a * b


# --- 2) Modele bu fonksiyonu bir "araç" olarak tanıtıyoruz ---
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="847 ile 293'ü çarparsan sonuç ne olur?",
    config=types.GenerateContentConfig(
        tools=[iki_sayiyi_carp]
    ),
)

print("\nModelin cevabı:")
print(response.text)