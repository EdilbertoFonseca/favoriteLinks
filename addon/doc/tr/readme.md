# Favori Bağlantılar

* **Author**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Oluşturulma Tarihi**: 04/11/2024
* **Lisans**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Giriş

**Favori Bağlantılar** eklentisi, favori bağlantılarınızı düzenli ve verimli bir şekilde yönetmenizi sağlayan bir araçtır. Yeni bağlantılar ekleme, başlıkları yeniden adlandırma, istenmeyen girişleri kaldırma ve kategorileri yönetme gibi özelliklere sahip sezgisel bir arayüz sunarak, kategorize edilmiş bir listedeki bağlantıları kaydetmenize, düzenlemenize ve kaldırmanıza olanak tanır. Ayrıca eklenti, tarayıcılar tarafından dışa aktarılan HTML dosyalarından yer işaretlerinin doğrudan içe aktarılmasına olanak tanır.

Eklentiyi açtığınızda bağlantılarınıza hızlı bir şekilde erişebilir ve bunları doğrudan varsayılan tarayıcıda açabilirsiniz. Daha fazla esnekliğe ihtiyacınız olması durumunda, artık bağlantıları ikincil bir tarayıcıda açma desteği de mevcut.

## Kurulum

**Favori Bağlantılar** eklentisini NVDA'ya yüklemek için aşağıdaki adımları izleyin:

1. NVDA'da **Araçlar** menüsünü açın ve **Eklenti Mağazası**'nı seçin.
2. **Kullanılabilir Eklentiler** sekmesinde **Arama** alanına gidin.
3. "Favori Bağlantılar"ı arayın. Sonuçlarda **Enter** veya **Uygula** tuşuna basın ve ardından **Yükle**'yi seçin.
4. Değişiklikleri uygulamak için NVDA'yı yeniden başlatın.

## Yapılandırma

Bağlantılarınızın nereye kaydedildiği ve bunları hangi tarayıcının açacağı konusunda tam kontrole sahipsiniz.

1. NVDA menüsüne erişin: `NVDA+N` > *Tercihler* > *Ayarlar*.
2. Kategori listesinde **Favori Bağlantılar**'ı seçin.

**"Dizin seç veya ekle"** düğmesini (`Alt+S`) kullanarak bağlantılar dosyasını kaydetmek için özel bir konum seçebilirsiniz.

Yüklü veya taşınabilir ikincil bir tarayıcı tanımlamak için:

1. "Sekme" tuşunu kullanarak **Tarayıcı yolu** alanına gidin.
2. İstediğiniz tarayıcının yürütülebilir dosyasını eklemek için **"Tarayıcı yolunu seç"** düğmesini (`Alt+N`) kullanın.

## Kullanım

### Eklentiye Erişim

* 'Alt+Windows+K' tuşlarına basın.
* Veya `NVDA+N` > *Araçlar* > *Favori Bağlantılar* yoluyla erişin.

### Ana Arayüz

Ana arayüz, 'Sekme' tuşu kullanılarak dolaşılabilen iki ana alandan oluşur:

1. **Kategori**: Mevcut kategorileri içeren bir açılır kutu.
2. **Bağlantı Listesi**: Seçilen kategoriyle ilişkili bağlantıları gösteren liste.

Ek seçeneklere erişmek için bu alanların herhangi birinde **bağlam menüsünü** (uygulama Tuşu) kullanın.

### Mevcut Eylemler

#### Kategoriler Birleşik Giriş Kutusunda

* **Kategori Ekle**: Yeni bir kategori oluşturur.
* **Kategoriyi Düzenle**: Seçilen kategoriyi yeniden adlandırır.
* **Kategoriyi Sil**: Kategoriyi ve içerdiği tüm bağlantıları siler.
* **Bağlantıları Dışa Aktar**: Tüm bağlantıları ve kategorileri bir ".json" dosyasına kaydeder.
* **Bağlantıları İçe Aktar**: Bağlantıları ve kategorileri bir `.json` dosyasından yükler.

#### Bağlantılar Listesinde

* **Bağlantıyı Aç**: Bağlantıyı yapılandırdığınız tarayıcıda açar.
> **Not**: İkincil tarayıcıyı önceden ayarlarda yapılandırmak gerekir.
* **Bağlantı Ekle**: Yeni bir Adres eklenmesine izin verir. Başlık otomatik olarak alınacaktır ancak alma işlemi başarısız olursa manuel olarak girebilirsiniz.
* **Bağlantıyı Düzenle**: Mevcut bir bağlantının başlığını ve URL'sini değiştirir.
* **Bağlantıyı Sil**: Seçilen bağlantıyı siler.
* **Bağlantıları Dışa Aktar** / **Bağlantıları İçe Aktar**: Kategori seçenekleriyle aynıdır.
* **HTML Yer İşaretlerini İçe Aktar**: Tarayıcılar tarafından dışa aktarılan bir `.html` dosyasındaki bağlantıları içe aktarır.
* **Bağlantıları Sırala**: Geçerli kategorinin bağlantılarını alfabetik sıraya göre düzenler.

### HTML Yer İşaretlerini İçe Aktar

FavoriteLinks ayrıca tarayıcılar (Chrome, Firefox, Edge ve diğerleri) tarafından dışa aktarılanlar gibi yer işaretlerinin doğrudan HTML dosyalarından içe aktarılmasına da olanak tanır.

Bu özellik, mevcut yer işaretlerinizi eklentiye hızlı ve düzenli bir şekilde taşımak için kullanışlıdır.

#### Yer imleri bir HTML dosyasından nasıl içe aktarılır

1. **Favori Bağlantılar** eklentisini açın.
2. **Kategoriler Açılan Kutu**'daki içerik menüsüne erişin veya ana menüdeki seçeneği kullanın.
3. **HTML yer işaretlerini içe aktar**'ı seçin.
4. Tarayıcınızdan dışa aktarılan `.html` dosyasını seçin.
5. Bağlantıların işlenmesini bekleyin.

İçe aktarma sırasında:

* İlerleme durumu bir ilerleme çubuğunda görüntülenir.
* **İşlemi istediğiniz zaman iptal edebilirsiniz**.
* NVDA tüm süreç boyunca duyarlı olmaya devam ediyor.

#### İçe aktarılan bağlantıların organizasyonu

* İçe aktarılan bağlantılar, eklenti tercihlerinde yapılandırılan JSON dosyasına otomatik olarak eklenir.
* Varsayılan olarak yer imleri **“İçe Aktarılan Yer İmleri”** kategorisine eklenir.
* Yinelenen bağlantılar (aynı Adrese sahip) tekrar eklenmez.

İçe aktarmanın sonunda bir onay mesajı görüntülenir ve eklenti arayüzü otomatik olarak güncellenir.

### Kısayollar

| İşlev | Kısayol |
| :--- | :--- |
| Bağlantıyı Aç | 'Alt+A' veya 'Enter' (bağlantılar listesinde) |
| Bağlantı Ekle | 'Alt+B' |
| Kategori Ekle | 'Alt+G' |
| Bağlantıyı Düzenle | 'Alt+E' veya 'F2' |
| Bağlantıyı Sil | 'Alt+B' veya 'Del' |
| Geçerli sayfanın Adresini kaydet | 'Üst Karakter+Kontrol+D' |
| Geçerli sayfanın Adresini göster | `Windows+Control+P` İki kez basıldığında Adres panoya kopyalanır. |
| Çıkış | `Alt+ı`, `Esc` or `Alt+F4` |

## "Yeni Bağlantı Ekle" İletişim Kutusu

1. **Kategori**: İstediğiniz kategoriyi seçin.
2. **Adres**: Bağlantı adresini yapıştırın veya yazın.
> Zaten bir Adresi kopyaladıysanız otomatik olarak yapıştırılacaktır.
3. **Tamam (`Alt+T`)**: Bağlantıyı ekler.
> Başlık otomatik olarak getirilecektir. Alma başarısız olursa, manuel olarak girebileceksiniz.
4. **İptal (`Alt+P`)**: İletişim kutusunu kapatır. 'Esc' veya 'Alt+F4' de çalışır.

## "Bağlantıyı Düzenle" İletişim Kutusu

1. **Kategori**: Burada kategori değiştirildiğinde bağlantı yeni kategoriye taşınacaktır.
2. **Başlık**: Bağlantı başlığını düzenleyin.
3. **Adres**: Bağlantı adresini değiştirin.
4. **Tamam (`Alt+T`)**: Değişiklikleri kaydeder.
5. **İptal (`Alt+P`)**: Kaydetmeden kapanır. 'Esc' veya 'Alt+F4' de çalışır.

## Teşekkür

**Rue Fontes** ve **Ângelo Abrantes**'e yapılan testler ve bu projenin geliştirilmesine önemli ölçüde katkıda bulunan değerli önerileri için özellikle teşekkür ederiz.

Ayrıca **Abel Passos**'a HTML dosyalarından yer imlerini içe aktarma işlevine yaptığı katkı için teşekkür ederim.

Favori Bağlantılar eklentisi **ChatGPT** ile **Google Gemini**'nin yardımıyla geliştirildi.  İşlevler oluşturmak, kodu optimize etmek, yeniden düzenlemek ve belgeleri geliştirmek için kullanıldı.

## 🌍 Çevirmenler

* 🇸🇦 **Arapça** — Ahmed Bakr
* 🇧🇷 **Portekizce (Brezilya)** — Edilberto Fonseca
* 🇵🇹 **Portekizce (Portekiz)** — Edilberto Fonseca
* 🇷🇺 **Rusça (Rusya)** — Valentin Kupriyanov
* 🇹🇷 **Türkçe (Türkiye)** — Umut KORKMAZ
* 🇺🇦 **Ukraynaca (Ukrayna)** — Heorhii Halas
* 🇻🇳 **Vietnamca (Tiếng Việt)** - Hoàng Long
