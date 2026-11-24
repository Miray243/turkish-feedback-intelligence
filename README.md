# Turkish Customer Feedback Intelligence

Türkçe müşteri geri bildirimlerini CSV dosyalarından incelemek için geliştirilen bir Python projesi. Proje Python 3.12'yi hedefler. Uygulama kodu `src/turkish_feedback/`, testler `tests/` altında yer alır.

## İlk CSV sözleşmesi

- Tek zorunlu sütun `feedback_text`. Ek sütunlar kabul edilir.
- Dosya virgülle ayrılır ve UTF-8 kodlaması kullanır. UTF-8 BOM kabul edilir.
- Duygu etiketleri, konu etiketleri ve zaman damgaları ileriki aşamalarda eklenebilir.

Gerçek veri kümelerindeki sütun adları farklı olabilir. Kaynak CSV dosyaları korunur. Daha sonra eklenecek ayrı eşleme ve dönüştürme adımı, proje sözleşmesine uygun bir çıktı üretir. Veri kaynakları ve lisansları [veri kümesi belgesinde](docs/datasets.md) kaydedilir.
