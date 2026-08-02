
def kupon_indirimi_hesapla(fiyat, indirim_yuzdesi):
    if indirim_yuzdesi > 100:
        indirim_yuzdesi = 100
    indirimli_fiyat = fiyat - (fiyat * indirim_yuzdesi / 100)
    return indirimli_fiyat
