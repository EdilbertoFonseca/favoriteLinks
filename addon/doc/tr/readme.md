# Favori Bağlantılar

* **Yazar**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Oluşturma Tarihi**: 04/11/2024
* **Lisans**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Giriş

**Favori Bağlantılar** eklentisi, favori bağlantılarınızı düzenli ve verimli bir şekilde yönetmenizi sağlayan bir araçtır. Bu araçla, bağlantıları kategorize edilmiş bir listede kaydedebilir, düzenleyebilir ve silebilirsiniz. Kullanıcı dostu arayüzü, yeni bağlantılar ekleme, başlıkları düzenleme, istenmeyen bağlantıları kaldırma ve kategorileri yönetme gibi kapsamlı işlevler sunar. Eklentiyi açtığınızda, favori bağlantılarınıza hızlı erişim sağlarsınız ve seçilen bağlantıyı doğrudan tarayıcıda açabilirsiniz.

Not: Favori Bağlantılar eklentisi, bazı fonksiyonların oluşturulması ve optimizasyonu için ChatGPT'nin yardımıyla geliştirilmiş ve ayrıca kod organizasyonu için kullanılmıştır.

## Kurulum

Favori Bağlantılar eklentisini NVDA'ya kurmak için aşağıdaki talimatları izleyin:

1. **Eklenti kurulum dosyasını indirin**: Dosyayı Eklentiler Mağazası'ndan veya resmi [Favori Bağlantılar](https://github.com/EdilbertoFonseca/favoriteLinks/releases/download/2024.2.1/favoriteLinks-2024.2.1.nvda-addon) sayfasından edinin.
   **Not**: Eklenti mağazadan indirildiyse kurulum otomatik olarak gerçekleşecektir. Aksi takdirde aşağıdaki talimatları izleyin.
2. **Eklentiyi yükleyin**: İndirilen eklenti dosyası üzerinde Enter tuşuna basın.
3. **Ekrandaki talimatları izleyin**: Talimatları tamamlayın.
4. **NVDA'yı yeniden başlatın**: Eklentiyi etkinleştirmek için NVDA'yı yeniden başlatmanız gerekmektedir.
5. **Kurulumu doğrulayın**: "NVDA + N" tuşlarına basarak NVDA menüsünü açın, "Araçlar" menüsüne gidin ve Favori Bağlantılar seçeneğinin listelenip listelenmediğini kontrol edin.

## Yapılandırma

Bağlantılar dosyanızı kaydetmek için varsayılan konumdan farklı bir yer seçebilirsiniz. Bunu yapmak için NVDA menüsünde Ayarlar iletişim kutusunda, Favori Bağlantılar kategorisine erişin ve "Dizin seçin veya ekleyin" düğmesini kullanarak farklı bir klasör seçin.

## Kullanım

### Eklentiye Erişim

"Alt+Windows+K" tuşlarına basarak veya NVDA menüsünden (NVDA+N) > Araçlar > Favori Bağlantılar seçeneğini kullanarak eklentiyi açabilirsiniz.

### Ana Arayüz

Gösterilen diyalogda iki ana alan bulunur:

1. **Kategori**: İstenilen kategoriyi seçebileceğiniz bir açılır kutu.
2. **Bağlantılar Listesi**: Seçilen kategoriye ait bağlantılar burada görüntülenir.

### Mevcut İşlemler

Bağlantılar ve kategorilerle ilgili seçeneklere erişmek için NVDA bağlam menüsünü (uygulama tuşu) kullanabilirsiniz.

### Kategori

Kategori açılır kutusunda konumlandığınızda, aşağıdaki seçenekler görüntülenir:

* **Kategori Ekle**: Listeye bir kategori eklemenizi sağlar.
* **Kategori Düzenle**: Mevcut bir kategoriyi yeniden adlandırmanızı sağlar.
* **Kategoriyi Sil**: Bir kategoriyi ve tüm ilişkili bağlantıları silmenizi sağlar.
* **Bağlantıları Dışa Aktar**: JSON dosyasında kaydedilmiş bağlantıları ve kategorileri dışa aktarmanızı sağlar.
* **Bağlantıları İçe Aktar**: Önceden kaydedilmiş bağlantıları ve kategorileri JSON dosyasından içe aktarmanızı sağlar.

### Bağlantı Listesi

Bağlantı listesinde konumlandığınızda, aşağıdaki seçenekler görüntülenir:

* **Bağlantıyı Aç**: Seçilen bağlantıyı sistemin varsayılan tarayıcısında açar. **Not**: Seçilen bağlantı üzerinde Enter tuşuna basmak, bağlantıyı sistemin varsayılan tarayıcısında açacaktır.
* **Bağlantı Ekle**: Adresini ve kategorisini girerek yeni bir bağlantı eklemenizi sağlar.
  **Not**: Başlık otomatik olarak alınır. Başlık alınamadığında, başlığı el ile eklemeniz için bir diyalog görünecektir.
* **Bağlantı Düzenle**: Mevcut bir bağlantının başlığını ve adresini düzenlemenizi sağlar.
* **Bağlantıyı Sil**: Listeden bir bağlantıyı silmenizi sağlar.
* **Bağlantıları Dışa Aktar**: JSON dosyasında kaydedilmiş bağlantıları ve kategorileri dışa aktarmanızı sağlar.
* **Bağlantıları İçe Aktar**: Önceden kaydedilmiş bağlantıları ve kategorileri JSON dosyasından içe aktarmanızı sağlar.
* **Bağlantıları Sırala**: Bağlantıları alfabetik sıraya göre sıralamanızı sağlar.

## Kısayollar

Bazı seçenekler, arayüzde doğrudan kısayollar aracılığıyla kullanılabilir. Bunlar:

* **Bağlantıyı aç, Alt+A**: Seçilen bağlantıyı sistemin varsayılan tarayıcısında açar.
  **Not**: Seçilen bağlantı üzerinde Enter tuşuna basmak, bağlantıyı sistemin varsayılan tarayıcısında açacaktır.
* **Bağlantı ekle, Alt+B**: Adresini ve kategorisini girerek yeni bir bağlantı eklemenizi sağlar.
  **Not**: Başlık otomatik olarak alınır. Başlık alınamadığında, başlığı elle eklemeniz için bir diyalog görünecektir.
* **Bağlantıyı düzenle, Alt+E**: Mevcut bir bağlantının başlığını ve Adresini düzenlemenizi sağlar.
* **Bağlantıyı Sil, Alt+S**: Listeden bir bağlantıyı kaldırmanızı sağlar.
* **Kategori ekle, Alt+K**: Listeye bir kategori eklemenizi sağlar.
* **Çık, (Alt+Ç)**: Diyaloğu kapatır. Ayrıca "Escape" tuşunu veya Alt+F4 tuşlarını kullanabilirsiniz.

## Yeni Bağlantı Ekleme Diyaloğu

1. **Kategori**: İstenilen kategoriyi seçebileceğiniz bir açılır kutu.
2. **Bağlantı Adresi ekleme alanı**: Adresi yapıştırabileceğiniz bir metin kutusu.
   **Not**: Adresi zaten kopyaladıysanız, otomatik olarak düzenleme kutusuna yerleştirilecektir.
3. **Tamam, Alt+T**: Bağlantıyı listeye ekler.
   **Not**: Başlık otomatik olarak alınır. Başlık alınamadığında, başlığı el ile eklemeniz için bir diyalog görünecektir.
4. **İptal, Alt+P**: Diyaloğu kapatır. Ayrıca "Escape" tuşunu veya Alt+F4 tuşlarını kullanabilirsiniz.

## Teşekkürler

Bu projeyi geliştirmek için test ve önerileriyle katkıda bulunan Rui Fontes ve Ângelo Abrantes ile projenin verimliliği ve kalitesi için kritik olan iş akışını cömertçe paylaşan Marlon Brandão de Sousa'ya teşekkür ederim.
