import pytest
from kupon_modul import kupon_indirimi_hesapla

# ==========================================
# Standart ve Geçerli Senaryolar
# ==========================================

def test_normal_indirim():
    """Standart bir indirim yüzdesi ile indirimli fiyatı doğru hesaplamalıdır."""
    assert kupon_indirimi_hesapla(100, 20) == 80.0
    assert kupon_indirimi_hesapla(200, 50) == 100.0

def test_sifir_indirim():
    """%0 indirim uygulandığında fiyat değişmemelidir."""
    assert kupon_indirimi_hesapla(100, 0) == 100.0

def test_tam_indirim():
    """%100 indirim uygulandığında fiyat 0.0 olmalıdır."""
    assert kupon_indirimi_hesapla(150, 100) == 0.0

def test_100den_buyuk_indirim_yuzdesi():
    """%100'den büyük indirim yüzdeleri %100 olarak üst sınırlandırılmalıdır."""
    assert kupon_indirimi_hesapla(100, 150) == 0.0
    assert kupon_indirimi_hesapla(50, 200) == 0.0

def test_ondalikli_fiyat_ve_indirim():
    """Ondalıklı fiyat ve indirim oranları ile doğru hesaplama yapmalıdır."""
    assert kupon_indirimi_hesapla(99.99, 10) == pytest.approx(89.991)
    assert kupon_indirimi_hesapla(100.0, 12.5) == 87.5

def test_sifir_fiyat():
    """Fiyat 0 olduğunda sonuç 0.0 olmalıdır."""
    assert kupon_indirimi_hesapla(0, 25) == 0.0


# ==========================================
# Tip Hataları
# ==========================================

def test_gecersiz_veri_tipleri():
    """Sayısal olmayan girdiler için TypeError fırlatılmalıdır."""
    with pytest.raises(TypeError):
        kupon_indirimi_hesapla("100", 20)
    with pytest.raises(TypeError):
        kupon_indirimi_hesapla(100, "20")


# ==========================================
# Uç Durumlar ve Tespit Edilen BUG'lar (xfail)
# ==========================================

@pytest.mark.xfail(reason="BUG: Negatif indirim yüzdesi fiyatı ARTIRMAKTADIR. İndirim asla fiyatı artırmamalı, ValueError fırlatılmalı veya 0 kabul edilmelidir.")
def test_negatif_indirim_yuzdesi():
    """
    # BUG: Fonksiyon negatif indirim yüzdesinde (örn: -20) fiyatı artırmaktadır (100 - (100 * -20 / 100) = 120).
    Negatif indirim yüzdesi geçersiz bir girdidir ve ValueError fırlatmalıdır.
    """
    with pytest.raises(ValueError):
        kupon_indirimi_hesapla(100, -20)


@pytest.mark.xfail(reason="BUG: Negatif ürün fiyatı kabul edilmektedir. Ürün fiyatı negatif olamaz, ValueError fırlatılmalıdır.")
def test_negatif_fiyat():
    """
    # BUG: Fonksiyon negatif fiyat kabul edip hesaplama yapmaktadır.
    Negatif fiyat mantıksız bir girdidir ve ValueError fırlatmalıdır.
    """
    with pytest.raises(ValueError):
        kupon_indirimi_hesapla(-100, 20)
