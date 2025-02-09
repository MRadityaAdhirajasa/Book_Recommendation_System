# 📚 Book Recommendation System

## 🔍 Project Overview
Sistem rekomendasi buku ini dikembangkan untuk membantu pengguna menemukan buku yang sesuai dengan preferensi mereka menggunakan dua pendekatan utama:
1. **Collaborative Filtering (SVD)** – Menggunakan interaksi pengguna untuk menemukan pola preferensi dalam memberikan rating buku.
2. **Content-Based Filtering (Cosine Similarity)** – Merekomendasikan buku berdasarkan kesamaan kontennya, seperti nama penulis.

Dengan jumlah buku yang terus meningkat, sistem ini bertujuan untuk menyaring informasi dan memberikan rekomendasi yang lebih relevan bagi pengguna.

## 🎯 Goals
- Memberikan rekomendasi buku yang dipersonalisasi.
- Mengatasi informasi yang berlebihan dan membantu pengguna menemukan buku yang relevan.
- Meningkatkan pengalaman membaca dan potensi penjualan buku.

## 🛠️ Technologies Used
- **Python**
- **Pandas & NumPy** untuk manipulasi data
- **Scikit-learn** untuk implementasi SVD dan Cosine Similarity
- **Surprise Library** untuk model rekomendasi berbasis Collaborative Filtering
- **Matplotlib & Seaborn** untuk visualisasi data

## 📂 Dataset
Dataset yang digunakan terdiri dari tiga file utama:
- **Books.csv**: Berisi informasi buku (judul, penulis, tahun terbit, penerbit, dll.).
- **Users.csv**: Berisi informasi pengguna (ID pengguna, lokasi, umur).
- **Ratings.csv**: Berisi data interaksi pengguna dengan buku (User-ID, ISBN, dan rating).

📌 Dataset diambil dari **[Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)**.

## 📊 Methodology
### **Collaborative Filtering (SVD)**
- Membangun **utility matrix** berdasarkan rating pengguna terhadap buku.
- Menggunakan **Singular Value Decomposition (SVD)** untuk mendekomposisi matriks rating dan menangkap pola laten preferensi pengguna.
- Menggunakan **matriks yang telah direkonstruksi** untuk memprediksi rating buku yang belum diberi rating oleh pengguna.
- Merekomendasikan buku berdasarkan rating prediksi tertinggi.

### **Content-Based Filtering (Cosine Similarity)**
- Menggunakan **TF-IDF Vectorizer** untuk mengekstraksi fitur dari nama penulis.
- Menghitung **Cosine Similarity** antar buku berdasarkan kemiripan fitur penulis.
- Merekomendasikan buku dengan **penulis yang paling mirip** dengan buku yang telah disukai pengguna.

## 📢 Conclusion

Pendekatan ini memungkinkan sistem rekomendasi untuk memberikan hasil yang lebih baik dengan menggabungkan Collaborative Filtering dan Content-Based Filtering. Kedua metode ini dapat digunakan untuk meningkatkan pengalaman pengguna dan mendukung penerbit dalam mempromosikan buku dengan lebih efektif.
