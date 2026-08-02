
"""
Agent döngüsü: test üret -> çalıştır -> hata varsa modele bildir -> düzelt -> tekrar dene.
Çalıştırmak için: python agent_loop.py
"""

import os
import subprocess
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MAX_DENEME = 3  # Sonsuz döngüye girmesin diye bir üst sınır


# --- Test edeceğimiz, bilerek zayıf noktası olan fonksiyon ---
KOD_ORNEGI = """
def kupon_indirimi_hesapla(fiyat, indirim_yuzdesi):
    if indirim_yuzdesi > 100:
        indirim_yuzdesi = 100
    indirimli_fiyat = fiyat - (fiyat * indirim_yuzdesi / 100)
    return indirimli_fiyat
"""

# Yukarıdaki fonksiyonu gerçek bir modül dosyasına yazıyoruz (import edilebilsin diye)
with open("kupon_modul.py", "w", encoding="utf-8") as f:
    f.write(KOD_ORNEGI)


def test_dosyasina_yaz(dosya_adi: str, icerik: str) -> str:
    """Verilen içeriği bir Python test dosyasına yazar."""
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(icerik)
    print(f"[LOG] '{dosya_adi}' dosyası yazıldı.")
    return f"'{dosya_adi}' başarıyla oluşturuldu."


def testleri_calistir(dosya_adi: str) -> tuple[bool, str]:
    """Pytest'i çalıştırır, (basarili_mi, cikti) döndürür."""
    sonuc = subprocess.run(
        ["python", "-m", "pytest", dosya_adi, "-v"],
        capture_output=True,
        text=True,
    )
    basarili = sonuc.returncode == 0
    cikti = sonuc.stdout + sonuc.stderr
    return basarili, cikti


TEST_DOSYASI = "test_agent_generated.py"

# --- İlk istek: testleri üret ---
prompt = f"""
Aşağıdaki Python fonksiyonu için kapsamlı Pytest test senaryoları yaz.

Fonksiyon:
{KOD_ORNEGI}

ÖNEMLİ: Negatif, sıfır ve aşırı büyük girdiler gibi uç durumları test ederken,
önce şunu düşün: "Bu girdi için doğru/mantıklı davranış ne olmalıydı?"
Eğer fonksiyonun MEVCUT davranışı mantıksız veya hatalıysa (örneğin negatif
indirim yüzdesi fiyatı ARTIRIYORSA, bu bir bug'dır çünkü indirim asla fiyatı
artırmamalı), bunu doğrulayan bir test YAZMA. Bunun yerine:
1. Fonksiyonun koduna, tespit ettiğin bug'ı açıklayan bir yorum (# BUG: ...) ekle
2. Test dosyasında bu senaryoyu `pytest.mark.xfail(reason="...")` ile işaretleyerek
   "bu şu an başarısız oluyor çünkü bilinen bir bug var" şeklinde belgele

Üretilen testleri 'test_dosyasina_yaz' aracını kullanarak
'{TEST_DOSYASI}' dosyasına yaz. Testler pytest formatında,
'from kupon_modul import kupon_indirimi_hesapla' importu ile başlamalı.
"""

for deneme in range(1, MAX_DENEME + 1):
    print(f"\n{'='*50}")
    print(f"DENEME {deneme}/{MAX_DENEME}")
    print(f"{'='*50}")

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(tools=[test_dosyasina_yaz]),
    )
    print("Model cevabı:", response.text[:200], "...")

    # Testleri çalıştır
    basarili, cikti = testleri_calistir(TEST_DOSYASI)

    if basarili:
        print("\n✅ TÜM TESTLER GEÇTİ! Agent görevi tamamladı.")
        break
    else:
        print("\n❌ Bazı testler başarısız oldu. Modele geri bildirim gönderiliyor...")
        # Hatayı modele geri gönder, düzeltmesini iste
        prompt = f"""
        Az önce '{TEST_DOSYASI}' dosyasına yazdığın testler çalıştırıldığında
        şu hata/sonuç alındı:

        {cikti[-1500:]}

        Bu sonucu incele. Eğer testte bir hata varsa (kodun kendisi değil,
        test senaryosu yanlışsa) düzelt. Eğer gerçek bir bug bulduysan
        (fonksiyonun kendisi yanlış davranıyorsa), bunu açıkla ama testi
        yine de doğru beklenen davranışı kontrol edecek şekilde tut.
        Düzeltilmiş tam test dosyasını yine 'test_dosyasina_yaz' aracıyla
        '{TEST_DOSYASI}' dosyasına yaz.
        """
else:
    print(f"\n⚠️ {MAX_DENEME} denemede tüm testler geçirilemedi.")