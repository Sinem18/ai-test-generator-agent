
# AI Test Generator Agent

Bir Python fonksiyonunun kodunu analiz edip, kapsamlı Pytest test senaryoları otomatik üreten, üretilen testleri kendi çalıştırıp doğrulayan ve gerekirse kendini düzelten bir AI agent'ı. Google Gemini API'nin tool/function calling özelliği kullanılarak geliştirildi.

## Bu Proje Ne Yapıyor?

1. Bir Python fonksiyonunun kodu agent'a verilir
2. Agent, eşdeğerlik sınıfları ve sınır değer analizi tekniklerini kullanarak kapsamlı Pytest test senaryoları üretir
3. Ürettiği testleri gerçek bir dosyaya yazar (tool/function calling ile)
4. Testleri otomatik çalıştırır
5. Başarısız test varsa, hatayı kendisine geri bildirim olarak gönderir ve testi düzeltir (agent döngüsü, maksimum deneme sınırıyla)
6. Kodda gerçek bir bug tespit ederse, bunu `pytest.mark.xfail(reason="...")` ile şeffaf şekilde işaretler — "testler geçti" görüntüsü vermek yerine bilinen sorunları açıkça raporlar

## Neden Önemli?

Çoğu "AI kod üretici" örneği, üretilen kodun doğruluğunu hiç sorgulamaz. Bu proje, LLM'lerin varsayılan eğilimini (belirsiz durumda mevcut davranışı doğrulayan test yazma) bilinçli olarak aşarak, modele **"bu davranış doğru mu?"** sorusunu sormasını ve gerçek bug'ları ayırt etmesini öğretiyor.

## Örnek Çıktı

`kupon_indirimi_hesapla()` fonksiyonu test edildiğinde, agent:
- 7 geçerli senaryoyu test edip doğruladı (normal indirim, sıfır indirim, %100 indirim vb.)
- 2 gerçek bug tespit etti (negatif indirim yüzdesi fiyatı artırıyor, negatif fiyat kabul ediliyor) ve bunları `xfail` ile işaretledi
- ## Dosyalar

- **test_connection.py** — Gemini API ile temel bağlantı testi
- **test_tool_calling.py** — Tool/function calling temel örneği (modelin gerçek bir Python fonksiyonunu çağırması)
- **agent_loop.py** — Ana agent döngüsü: test üret → çalıştır → başarısızsa geri bildirimle düzelt (maks. 3 deneme)

## Kullanılan Teknolojiler

- Python
- Google Gemini API (`google-genai`)
- Pytest
- Tool/Function Calling
- Agent tasarım deseni (generate → execute → reflect → retry)

## Çalıştırma

```bash
pip install google-genai python-dotenv pytest
```

`.env` dosyası oluşturup içine kendi Gemini API key'ini ekle:
Sonra:
```bash
python agent_loop.py
```

## Not

Bu proje, test mühendisliği ve AI mühendisliği alanlarındaki öğrenme sürecimin bir parçası olarak geliştirildi. Amaç, LLM tabanlı otomasyonun sadece "kod üretmek" değil, ürettiği sonucu eleştirel şekilde değerlendirebilmesini sağlamaktı.
