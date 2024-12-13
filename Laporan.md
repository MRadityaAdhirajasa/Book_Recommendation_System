# Laporan Proyek Machine Learning - M. Raditya Adhirajasa

## Project Overview

Rekomendasi buku merupakan salah satu bentuk implementasi sistem rekomendasi yang sangat bermanfaat dalam membantu pengguna menemukan buku yang sesuai dengan preferensi dan minat mereka. Dalam dunia literasi yang kaya akan pilihan, jumlah buku yang tersedia di pasaran terus meningkat, sehingga pengguna seringkali merasa kesulitan untuk menemukan buku yang relevan dengan kebutuhan mereka. Di sinilah sistem rekomendasi memainkan peran penting untuk menyederhanakan proses pencarian dan meningkatkan pengalaman pengguna.

Sistem rekomendasi merupakan sistem yang menyaring informasi dengan memprediksi peringkat atau preferensi konsumen untuk barang yang ingin digunakan oleh konsumen. Sistem ini mencoba 
merekomendasikan barang kepada konsumen sesuai dengan kebutuhan dan seleranya. Sistem rekomendasi menggunakan dua metode untuk menyaring informasi - Content-Based dan
Collaborative (Rana & Deeba, 2019). Content-Based Filtering mempelajari konten item seperti produk untuk mengkategorikan ke pengguna yang sesuai berdasarkan preferensi dari profil pengguna. Sedangkan Collaborative Filtering akan mencocokkan preferensi antara pengguna lainnya (Kurmashov et al., 2015).

Dalam proyek ini, sistem rekomendasi buku dibuat dengan menggunakan dua pendekatan utama, yaitu Collaborative Filtering dengan metode Singular Value Decomposition (SVD) dan Content-Based Filtering dengan teknik Cosine Similarity. Kedua pendekatan ini digunakan untuk memberikan rekomendasi personal yang akurat berdasarkan data historis pengguna dan kesamaan konten buku.

**Mengapa masalah ini harus diselesaikan?**
- Meningkatkan Kepuasan Pengguna

  Dengan memberikan rekomendasi buku yang sesuai, proyek ini bertujuan untuk meningkatkan kepuasan pengguna dalam pengalaman membaca dan membantu mereka menemukan buku yang sesuai minat.
- Mengatasi Overload Informasi

  Dalam era digital, pengguna dihadapkan pada jumlah informasi yang sangat besar, termasuk ribuan judul buku yang tersedia di pasaran. Sistem rekomendasi dapat membantu menyaring pilihan ini dan menghadirkan opsi yang paling relevan dengan kebutuhan dan preferensi pengguna.
- Meningkatkan Penjualan Buku

  Dari sisi penerbit atau penjual buku, sistem rekomendasi ini dapat mendorong penjualan dengan menampilkan buku-buku yang memiliki kemungkinan besar untuk dibeli oleh pengguna berdasarkan preferensi mereka.

**Referensi**

[Rana, A. & Deeba, K., 2019. Online Book Recommendation System using Collaborative Filtering (With Jaccard Similarity). Journal of Physics: Conference Series, 1362, p. 012130](https://iopscience.iop.org/article/10.1088/1742-6596/1362/1/012130/pdf) 

[Kurmashov, N., Latuta, K. & Nussipbekov, A., 2015. Online Book Recommendation System. 2015 12th International Conference on Electronics Computer and Computation (ICECCO), pp. 1–4.](https://www.researchgate.net/publication/300412849_Online_book_recommendation_system) 

## Business Understanding

### Problem Statements

- Bagaimana membantu pengguna menemukan buku yang sesuai dengan preferensi mereka di tengah banyaknya pilihan yang tersedia?
- Bagaimana penerbit dan penjual buku dapat meningkatkan penjualan dengan menargetkan pengguna secara lebih personal?

### Goals

- Mengembangkan sistem rekomendasi buku yang dapat memberikan rekomendasi personal bagi pengguna berdasarkan data historis dan kesamaan buku.
- Membantu penerbit dan penjual buku untuk meningkatkan penjualan dengan menyarankan buku yang lebih mungkin menarik minat pengguna.

### Solution Statements
- Collaborative Filtering menggunakan Singular Value Decomposition (SVD).

  Pendekatan ini memanfaatkan data historis berupa rating pengguna terhadap buku. Dengan SVD, matriks utility (rating pengguna terhadap buku) direduksi menjadi matriks yang lebih kecil, sehingga memungkinkan prediksi rating untuk buku-buku yang belum dinilai pengguna. Rekomendasi diberikan berdasarkan buku dengan prediksi rating tertinggi.

- Content-Based Filtering menggunakan Cosine Similarity.

  Pendekatan ini digunakan untuk merekomendasikan buku berdasarkan kemiripan konten antar buku. Fitur dari setiap buku dianalisis dan direpresentasikan menggunakan teknik TF-IDF Vectorizer. Kesamaan antar buku kemudian dihitung menggunakan cosine similarity, sehingga sistem dapat mengidentifikasi buku yang memiliki konten serupa dengan preferensi buku yang telah dibaca atau dinilai positif oleh pengguna.

- Teknik Evaluasi dengan Precision.

  Evaluasi sistem rekomendasi dilakukan menggunakan metrik precision, yaitu perbandingan antara jumlah rekomendasi yang relevan dengan jumlah rekomendasi yang diberikan. Precision memberikan gambaran seberapa efektif sistem dalam menyajikan rekomendasi yang relevan untuk pengguna.

## Data Understanding
Dataset ini terdiri dari 3 file yaitu: User berisi informasi pengguna dan demografinya, Books berisi informasi buku, dan Ratings berisi informasi pengguna yang memberikan rating.

Contoh: [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset).

File **Ratings** berjumlah 1.149.780 dan memiliki variabel:
- User-ID : ID pengguna
- ISBN : Nomor Buku
- Book-Rating : Rating buku yang diberikan oleh pengguna

File **Books** berjumlah 271.360 dan memiliki variabel:
- ISBN : Nomor buku
- Book-Title : Judul buku
- Book-Author : Nama penulis
- Year-Of-Publication : Tahun terbit
- Publisher : Penerbit
- Image-URL-S : Gambar sampul skala kecil
- Image-URL-M : Gambar sampul skala sedang
- Image-URL-L : Gambar sampul skala besar

File **Users** berjumlah 278.858 dan memiliki variabel:
- User-ID : ID pengguna
- Location : Lokasi pengguna
- Age : Umur pengguna

### Exploratory Data Analytic

- Deskripsi Data

  Melihat deskripsi dataset dengan menggunakan fungsi info(). Hal ini diperlukan agar dapat memahami data lebih lanjut seperti jumlah data, jumlah kolom, tipe data tiap kolom, dll. Berdasarkan deskripsi data tersebut bisa diapatkan gambaran singkat tentang struktur dataset, termasuk jumlah data yang valid di setiap kolom dan tipe data yang perlu diproses lebih lanjut. Data tersebut memilikitipe object, float, dan integer.

- Memilih Feature

  Tahap selanjutnya adalah memilih feature penting yang akan digunakan. Pada data buku hanya akan menggunakan ISBN, judul, dan nama author. Sedangkan pada data user akan menggunakan id dan lokasi. Selanjutnya melakukan rename agar feature menjadi lebih mudah dibaca. Pada feature lokasi, akan digunakan data nama negara saja karena akan lebih mengelompokkan lokasi asal pembaca/user dengan lebih baik.

- Melihat Ukuran Data

  Berikut dapat dilihat jumlah data pada setiap dataframe. Data tersebut sangat banyak, data buku dan user lebih dari 270 ribu sedangkan rating lebih dari 1 juta.

  - jumlah data books:  (271360, 3)
  - jumlah data ratings:  (1149780, 3)
  - jumlah data users:  (278858, 2)

- Memeriksa Missing Value

  Proses selanjutnya adalah memeriksa missing value pada tiap dataframe. Karena missing value tidak banyak dan hanya ada di buku maka dihapus saja.

  ![image](https://github.com/user-attachments/assets/085b8708-8d40-42d8-9448-9f1153ccaadd)

- Merge Data

  Karena memerlukan feature pada dataframe buku dan ratings, maka merge data dilakukan berdasarkan ISBN. Lalu periksa apakah ada missing value, duplicate, dan ukuran data yang telah di merge.

  ![image](https://github.com/user-attachments/assets/502345f4-803d-4e10-b2f5-510672ec3696)

  ![image](https://github.com/user-attachments/assets/437d6ef3-b7a9-4e8b-8cbd-67a30048d3f3)

- Identifikasi Jumlah Data

  Melakukan identifikasi mengenai jumlah judul buku, jumlah pembaca, dan lokasi pembaca. Ada lebih dari 270 ribu buku dan lebih dari 92 ribu pengguna yang berasal dari sekitar 700 lokasi.

  ![image](https://github.com/user-attachments/assets/e74d5002-9ed9-474b-a047-c42e1e2dbe31)

- Visualisasi Data

  Melakukan visualisasi untuk melihat buku apa yang paling populer di antara user. Buku dipilih berdasarkan yang paling banyak diberi rating oleh user. Hasilnya didapatkan bahwa buku berjudul Wild Animus adalah yang paling populer.

  ![image](https://github.com/user-attachments/assets/4f7e4575-ed96-423e-8549-d3407d76ed6c)

Visualisasi untuk melihat lokasi dengan user paling banyak. Hasilnya menunjukkan bahwa usa merupakan lokasi dengan user atau pembaca terbanyak.

![image](https://github.com/user-attachments/assets/e4a3bc5d-fdd2-4798-9fd7-71eac2e312a2)

## Data Preparation

### Preparation Collaborative Filtering

- Filter Data

  Karena data yang terlalu banyak maka hanya akan menggunakan sample yang mewakili keseluruhan data, agar proses komputasi tidak berat. Data yang akan digunakan untuk Collaborative Filtering akan di filter dengan ketentuan seperti berikut:
  - Data user yang telah memberi rating lebih dari 100 buku.
  - Data buku yang telah diberi rating lebih dari 200 kali.

- Membangun Matriks Utilitas

  Membangun matriks utilitas yang menjadi dasar untuk collaborative filtering. Matriks ini menyimpan interaksi (rating) antara pengguna dan buku. Mengubah matriks ke format yang sesuai untuk model rekomendasi, misalnya untuk menghitung kesamaan atau memproses dengan algoritma seperti SVD.

  ![image](https://github.com/user-attachments/assets/0d06c056-ceff-450f-b21c-03733d3100c4)

- Konversi menjadi Sparse Matriks

  Membangun matriks utilitas yang menjadi dasar untuk collaborative filtering. Matriks ini menyimpan interaksi (rating) antara pengguna dan buku. Mengubah matriks ke format yang sesuai untuk model rekomendasi, misalnya untuk menghitung kesamaan atau memproses dengan algoritma seperti SVD.

### Preparation Content-Based Filtering

- Filter Data

  Untuk pendekatan Content-Based Filtering akan digunakan 1000 sample data dari dataframe books, data yang digunakan ialah data author yang telah menulis lebih dari 1 buku.

- Ekstraksi Feature dengan TF-IDF Vectorizer

  Proses ini bertujuan untuk mengekstraksi fitur dari Author dan menghitung bobot TF-IDF untuk setiap kata. Dengan representasi ini, dapat diukur pentingnya setiap kata dalam konteks data secara numerik, sehingga memungkinkan analisis kesamaan antar item berdasarkan fitur teks.

  ![image](https://github.com/user-attachments/assets/14ee766c-94df-494c-ab55-e04cdee5a8aa)

- Melakukan Fit dan Transform TF-IDF

  Langkah ini mengubah data teks Author menjadi bentuk numerik berupa matriks TF-IDF. Matriks ini digunakan untuk merepresentasikan Author dalam ruang fitur berdasarkan kata-kata unik, sehingga dapat digunakan dalam perhitungan kesamaan atau sebagai input untuk algoritma lain.

- Konversi ke Dense Matrix

  Langkah ini bertujuan untuk mengubah representasi matriks TF-IDF dari format hemat memori (sparse) menjadi format lengkap (dense). Hal ini dilakukan untuk mempermudah visualisasi, debugging, atau pemrosesan lebih lanjut.

  ![image](https://github.com/user-attachments/assets/73023327-d64a-44e0-89a6-c737904e7362)

## Modeling
Pada tahap ini membuat model untuk sistem rekomendasi. SVD untuk Collaborative Filtering sedangkan Cosine Similarity untuk Content-Based Filtering.

### SVD untuk Collaborative Filtering

- Kelebihan SVD:
  -  SVD dapat mengurangi dimensionalitas matriks utilitas, sehingga mampu menangani masalah sparsity (kelangkaan data) yang umum terjadi pada dataset rating.
  -  Dengan mendekonstruksi matriks utilitas, SVD dapat menemukan pola-pola laten atau hubungan tersembunyi antara pengguna dan item, yang tidak terlihat dalam analisis langsung.
  -  Algoritma ini menghasilkan rekomendasi yang personal karena didasarkan pada pola preferensi pengguna lain dengan kesamaan perilaku.

- Kekurangan SVD:
  -  SVD membutuhkan jumlah data yang cukup besar untuk menghasilkan dekomposisi matriks yang akurat. Jika data pengguna sedikit, performa akan menurun.
  -  Proses dekomposisi membutuhkan sumber daya komputasi yang besar, terutama untuk dataset dengan ukuran besar.
  -  Tidak dapat memberikan rekomendasi untuk pengguna atau item baru karena metode ini bergantung pada data historis pengguna.

#### Tahapan SVD
Pada proses ini terdapat beberapa tahapan penting seperti:

- menentukan jumlah fitur laten sebanyak 50 untuk mengurangi dimensi data.
- implementasi truncated SVD.
- rekontruksi matriks kembali menggunakan hasil SVD.
  
  ```
  # Tentukan jumlah komponen yang ingin dipertahankan
  n_components = 50 
  
  # Terapkan Truncated SVD
  svd = TruncatedSVD(n_components=n_components)
  svd_matrix = svd.fit_transform(sparse_utility_matrix)
  
  # Rekonstruksi matriks dari hasil SVD
  reconstructed_matrix = np.dot(svd_matrix, svd.components_)
  
  # Tampilkan dimensi matriks SVD dan rekonstruksi
  print(f"Shape of SVD Matrix: {svd_matrix.shape}")
  print(f"Shape of Reconstructed Matrix: {reconstructed_matrix.shape}")
  ```
- membuat fungsi untuk memberikan rekomendasi buku dengan pendekatan Collaborative Filtering. Rekomendasi dibuat berdasarkan id user dan akan mengurutkan 5 buku teratas.
- Berikut adalah top 5 rekomendasi buku untuk user 254:
  
  ![image](https://github.com/user-attachments/assets/e9fa9822-a67a-4a25-82e4-7c5f393d928e)


### Cosine Similarity untuk Content-Based Filtering

- Kelebihan Cosine Similarity:
  -  Cosine similarity hanya bergantung pada konten item (fitur) dan tidak memerlukan informasi interaksi pengguna, sehingga bermanfaat dalam tahap awal penerapan sistem rekomendasi.
  -  Algoritma ini mudah diimplementasikan dan dihitung dengan efisiensi tinggi, terutama jika menggunakan representasi sparse matrix.
  -  Cosine similarity menghitung sudut antara dua vektor, bukan jarak absolutnya. Ini berarti ukuran data tidak memengaruhi hasil, sehingga cocok untuk data TF-IDF yang berisi nilai bobot relatif.

- Kekurangan Cosine Similarity:
  -  Kinerja cosine similarity sangat bergantung pada kualitas dan representasi fitur (misalnya, TF-IDF). Jika fitur yang digunakan tidak informatif, hasilnya akan kurang akurat.
  -  Jika pengguna belum memiliki data preferensi atau interaksi dengan item, sistem tidak dapat memberikan rekomendasi yang sepenuhnya personal.
  
#### Tahapan Cosine Similarity
Pada tahap ini terdapat beberapa proses yang harus dilakukan seperti:

- Menghitung similarity, matriks cosine similarity digunakan untuk mengetahui seberapa mirip konten antar buku.
- Membuat representasi yang mudah dibaca Dengan mengubah array menjadi DataFrame dan menggunakan label judul buku, analisis data menjadi lebih intuitif.

  ```
  # Menghitung cosine similarity pada matrix tf-idf
  cosine_sim = cosine_similarity(tfidf_matrix)
  
  cosine_sim_df = pd.DataFrame(cosine_sim, index=filtered_CBF['Title'], columns=filtered_CBF['Title'])
  ```
  
  ![image](https://github.com/user-attachments/assets/67b1eeab-b946-4d4a-8aff-8db0ea231e7d)

- membuat fungsi untuk rekomendasi buku dengan pendekatan Content-Based Filtering dibuat. Fungsi akan memberi rekomendasi berdasarkan input judul buku dan mencari kemiripan berdasarkan Author.
- Berikut adalah top 5 rekomendasi buku yang mirip Night Watch

  ![image](https://github.com/user-attachments/assets/7e688c8a-1d01-40dc-ae31-09e7f7e84ed2)


## Evaluation

**Precision**

Precision adalah salah satu metrik evaluasi yang digunakan untuk mengukur relevansi rekomendasi yang diberikan oleh sistem rekomendasi. Precision mengukur proporsi item yang direkomendasikan oleh sistem yang relevan terhadap total item yang direkomendasikan.

![image](https://github.com/user-attachments/assets/22d896e3-24a3-4fbb-8501-c29a533b4000)

### Precision Collaborative Filtering

Evaluasi dilakukan dengan menghitung precision. buku yang relevant diambil dari data buku yang telah diberi rating oleh user. Lalu hitung relevant_in_recommendations dengan jumlah buku yang sama antara relevant dengan recomended. Selanjutnya precision didapat dari total buku relevant_in_recommendations dibagi dengan total buku recommended.

Buku yang relevan untuk user 254:
```
{'1984',
 'Always A Bridesmaid (Harlequin American Romance, No 266)',
 'American Gods',
 'American Gods: A Novel',
 'Animal Farm',
 'Neverwhere'}
```

Buku yang direkomendasikan untuk user 254:
```
{'Angels &amp; Demons',
 "Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))",
 'Neverwhere',
 'Prodigal Summer: A Novel',
 'Watership Down'}
```

Hitung precision untuk user 254
```
# Hitung jumlah buku relevan di rekomendasi
relevant_in_recommendations = recommended_books.intersection(relevant_books)

# Precision: proporsi buku relevan di antara buku yang direkomendasikan
precision_CF = len(relevant_in_recommendations) / len(recommended_books) if recommended_books else 0

print(f"Precision {precision_CF:.2f}")
```
Hasilnya Precision 0.20


### Precision Content-Based Filtering

Evaluasi dilakukan dengan menghitung precision. Jumlah rekomendasi yang relevan (input) dibagi jumlah rekomendasi, dengan Author untuk melihat kemiripannya.

Buku yang relevan dengan judul Night Watch:

![image](https://github.com/user-attachments/assets/d3043e44-cfc2-4e70-a5f1-02e0dedd240d)

Buku yang direkomendasikan mirip dengan Night Watch:

![image](https://github.com/user-attachments/assets/149743b7-7ba9-4c2c-92e3-3cf26f4dc9a1)

Hitung precision untuk buku Night Watch
```
# hitung jumlah rekomendasi yang sesuai dengan relevan
relevant_recommendation_CBF = len(top_recommended_CBF[top_recommended_CBF['Author'] == relevant_CBF[0]])

# hitung precision
precision_CBF = relevant_recommendation_CBF / len(recomended_CBF) if len(recomended_CBF) > 0 else 0

print(f"Precision: {precision_CBF}")
```
Hasilnya Precision 1.0


### Kesimpulan

Pendekatan Content-Based Filtering menunjukkan precision yang baik, model berhasil memberikan rekomendasi buku yang mirip berdasarkan nama author. Sedangkan untuk pendekatan Collaborative Filterung, rekomendasi untuk user = 254 menunjukkan precision yang cukup baik dalam memberikan rekomendasi buku yang relevan untuk pengguna, namun ada kemungkinan precision akan lebih baik untuk pengguna yang lain. Penerapan SVD untuk Collaborative Filtering dan Cosine Similarity untuk Content-Based Filtering memberikan hasil rekomendasi yang cukup baik dan relevan untuk pengguna. Kedua pendekatan tersebut dapat digunakan untuk memberi rekomendasi buku yang lebih relevan untuk pengguna dan dapat memberikan manfaat bagi penerbit untuk meningkatkan penjualan karena dapat memberikan rekomendasi buku yang relevan bagi masing-masing pengguna.
