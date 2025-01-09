# -*- coding: utf-8 -*-
"""Book_Recommendation_System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D3Dw5GQE5L1mIC_Ibzp1Xf0LsKbQgb6P

# Book Recommendation System

## Load Data

Tahap awal yang harus dilakukan adalah mendownload data dari kaggle
"""

!kaggle datasets download -d arashnic/book-recommendation-dataset --unzip -p book-recommendation-dataset

"""## Library

Tahap selanjutnya melakukan import library yang diperlukan seperti berikut:

*   **numpy** : Digunakan untuk operasi numerik, seperti perhitungan vektor dan matriks.
*   **pandas** : Digunakan untuk manipulasi dan analisis data berbasis tabel.
*   **matplotlib** : Digunakan Untuk visualisasi data, seperti membuat grafik.
*   **TruncatedSVD** : Digunakan Untuk reduksi dimensi matriks sparse.
*   **csr_matrix** : Digunakan untuk merepresentasikan matriks dalam format sparse guna menghemat memori ketika bekerja dengan dataset besar yang memiliki banyak nilai nol
, seperti matriks rating.
*   **cosine_similarity** : Digunakan untuk menghitung kesamaan antar-vektor.
*   **TfidfVectorizer** : Digunakan untuk mengonversi teks menjadi representasi numerik menggunakan metode TF-IDF.
*   **warnings** : Digunakan untuk mengontrol pesan warning, seperti menyembunyikan pesan warning.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

"""## Exploratory Data Analysis

Pada tahap ini dilakukan eksplorasi pada dataset guna mengetahui lebih lanjut karakteristik dataset seeprti jumlah, tipe data, isi data, dll.
"""

books = pd.read_csv('/content/book-recommendation-dataset/Books.csv')
books.head(2)

ratings = pd.read_csv('/content/book-recommendation-dataset/Ratings.csv')
ratings.head(2)

users = pd.read_csv('/content/book-recommendation-dataset/Users.csv')
users.head(2)

books.info()

ratings.info()

users.info()

"""Berdasarkan eksplorasi diatas, data memiliki beragam tipe data seperti object, integer, dan float. Tahap selanjutnya adalah memilih feature penting yang akan digunakan. Pada data buku hanya akan menggunakan ISBN, judul, dan nama author. Sedangkan pada data user akan menggunakan id dan lokasi."""

# pilih feature yang akan digunakan

books = books[['ISBN', 'Book-Title', 'Book-Author']]
users = users[['User-ID', 'Location']]

"""Selanjutnya melakukan rename agar feature menjadi lebih mudah dibaca."""

# rename feature

ratings = ratings.rename(columns={'User-ID': 'User', 'Book-Rating': 'Rating'})
users = users.rename(columns={'User-ID': 'User'})
books = books.rename(columns={'Book-Title': 'Title', 'Book-Author': 'Author'})

"""Pada feature lokasi, akan digunakan data nama negara saja karena akan lebih mengelompokkan lokasi asal pembaca/user dengan lebih baik."""

# split location

users['Location'] = users['Location'].str.split(',').str[-1].str.strip()
users.head(2)

"""Berikut dapat dilihat jumlah data pada setiap dataframe. Data tersebut sangat banyak, data buku dan user lebih dari 270 ribu sedangkan rating lebih dari 1 juta."""

# lihat data tiap df

print('jumlah data books: ', books.shape)
print('jumlah data ratings: ',ratings.shape)
print('jumlah data users: ',users.shape)

"""Proses selanjutnya adalah memeriksa missing value pada tiap dataframe. Karena missing value tidak banyak dan hanya ada di buku maka dihapus saja."""

# Check for missing values in each DataFrame

print("Missing values in books DataFrame:\n", books.isnull().sum())
print("\nMissing values in ratings DataFrame:\n", ratings.isnull().sum())
print("\nMissing values in users DataFrame:\n", users.isnull().sum())

# drop missing value

books.dropna(inplace=True)

"""Karena memerlukan feature pada dataframe buku dan ratings, maka merge data dilakukan berdasarkan ISBN."""

# merge data ratings dan books

ratings_books_titles = ratings.merge(books,on='ISBN')

ratings_books_titles.head(2)

"""Memeriksa apakah ada missing value, duplicate, dan ukuran data yang telah di merge."""

print("Missing values in ratings_books_titles DataFrame:\n", ratings_books_titles.isnull().sum(),"\n")
print("Duplicated in ratings_books_titles DataFrame: ", ratings_books_titles.duplicated().sum(),"\n")
print("shape in ratings_books_titles DataFrame: ", ratings_books_titles.shape)

"""Melakukan identifikasi mengenai jumlah judul buku, jumlah pembaca, dan lokasi pembaca."""

#identifikasi jumlah

print('Jumlah judul buku: ', len(ratings_books_titles.ISBN.unique()))
print('Jumlah pembaca: ', len(ratings_books_titles.User.unique()))
print('Jumlah lokasi pembaca: ', len(users.Location.unique()))

"""Melakukan visualisasi untuk melihat buku apa yang paling populer di antara user. Buku dipilih berdasarkan yang paling banyak diberi rating oleh user. Hasilnya didapatkan bahwa buku berjudul Wild Animus adalah yang paling populer."""

# Group by book title dan hitung jumlah ratings
popular_books = ratings_books_titles.groupby('Title')['Rating'].count().reset_index()

# Sort by rating count dalam descending order
top_5_books = popular_books.sort_values('Rating', ascending=False).head(5)

# Plotting
plt.figure(figsize=(12, 6))
plt.barh(top_5_books['Title'], top_5_books['Rating'], color='skyblue')
plt.xlabel("Number of Ratings")
plt.ylabel("Book Title")
plt.title("Top 5 Books")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

"""Visualisasi untuk melihat lokasi dengan user paling banyak. Hasilnya menunjukkan bahwa usa merupakan lokasi dengan user atau pembaca terbanyak."""

# Group by location dan count number users
location_counts = users.groupby('Location')['User'].count().reset_index()

# Sort by user count dalam descending order
top_5_locations = location_counts.sort_values('User', ascending=False).head(5)

# Plotting
plt.figure(figsize=(12, 6))
plt.barh(top_5_locations['Location'], top_5_locations['User'], color='skyblue')
plt.xlabel("Number of Users")
plt.ylabel("Location")
plt.title("Top 5 Locations with the Most Users")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

"""## Data Preparation

Tahap ini dilakukan untuk mempersiapkan data agar dapat diproses pada tahap pembuatan model rekomendasi.

### Preparation Collaborative Filtering

Karena data yang terlalu banyak maka hanya akan menggunakan sample yang mewakili keseluruhan data, agar proses komputasi tidak berat. Data yang akan digunakan untuk Collaborative Filtering akan di filter dengan ketentuan seperti berikut:

*   Data user yang telah memberi rating lebih dari 100 buku.
*   Data buku yang telah diberi rating lebih dari 200 kali.
"""

# Filter user yang telah memberi rating lebih dari 100 buku
user_rating_counts = ratings_books_titles.groupby('User')['Rating'].count()
active_users = user_rating_counts[user_rating_counts > 100].index

# Filter buku yang telah diberi rating lebih dari 200 kali
book_rating_counts = ratings_books_titles.groupby('ISBN')['Rating'].count()
popular_books = book_rating_counts[book_rating_counts > 200].index

# Filter rating
filtered_CF = ratings_books_titles[
    ratings_books_titles['User'].isin(active_users) &
    ratings_books_titles['ISBN'].isin(popular_books)
]

print(filtered_CF.shape)

"""Selanjutnya membangun matriks yang akan digunakan pada model SVD untuk Collaborative Filtering."""

utility_matrix_filtered = filtered_CF.pivot_table(
    index='User', columns='Title', values='Rating'
).fillna(0).T

print(f"Sparse Matrix Shape: {utility_matrix_filtered.shape}")

utility_matrix_filtered.head(5)

"""konversi utility matriks menjadi sparse matriks, sparse matrix hanya menyimpan nilai non-nol, sehingga lebih hemat memori dan efisien untuk dataset yang besar dan jarang terisi."""

# Ubah matriks menjadi sparse matrix
sparse_utility_matrix = csr_matrix(utility_matrix_filtered.values)

"""### Preparation Content-Based Filtering

Untuk pendekatan Content-Based Filtering akan digunakan 1000 sample data dari dataframe books, data yang digunakan ialah data author yang telah menulis lebih dari 1 buku.
"""

books_list = books.copy()

author_counts = books.groupby('Author')['ISBN'].count()
authors_more_than_one_book = author_counts[author_counts > 2].index
books_list = books[books['Author'].isin(authors_more_than_one_book)]
books_list.head()

filtered_CBF = books_list.head(1000)
filtered_CBF.shape

"""Selanjutnya melakukan ekstraksi fitur menggunakan TF-IDF Vectorizer, dengan menghitung nilai TF-IDF Author"""

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# Melakukan perhitungan idf pada data author
tf.fit(filtered_CBF['Author'])

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names_out()

"""Langkah ini mengubah data teks Author menjadi bentuk numerik berupa matriks TF-IDF. Matriks ini digunakan untuk merepresentasikan Author dalam ruang fitur berdasarkan kata-kata unik, sehingga dapat digunakan dalam perhitungan kesamaan atau sebagai input untuk algoritma lain."""

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(filtered_CBF['Author'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

"""Selanjutnya mengonversi data teks pada kolom Author menjadi matriks dense, yang merupakan representasi numerik dari teks yang akan menjadi dasar untuk mengukur kesamaan antar buku berdasarkan Author."""

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

"""## Modelling

Pada tahap ini membuat model untuk sistem rekomendasi. SVD untuk Collaborative Filtering sedangkan Cosine Similarity untuk Content-Based Filtering.

## SVD untuk Collaborative Filtering

Pada proses ini terdapat beberapa tahapan penting seperti:
* menentukan jumlah fitur laten sebanyak 50 untuk mengurangi dimensi data.
* implementasi truncated SVD
* rekontruksi matriks kembali menggunakan hasil SVD
"""

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

"""Membuat fungsi untuk memberikan rekomendasi buku dengan pendekatan Collaborative Filtering. Rekomendasi dibuat berdasarkan id user dan akan mengurutkan 5 buku teratas."""

def recommended_books_CF(user_id, utility_matrix, reconstructed_matrix, books_metadata, top_n=5):
    """
    Memberikan rekomendasi buku berdasarkan ID user.

    Args:
    user_id (int): ID user yang ingin diberi rekomendasi.
    utility_matrix (pd.DataFrame): Matriks utility (rating user terhadap buku).
    reconstructed_matrix (np.array): Matriks yang direkonstruksi setelah SVD.
    books_metadata (pd.DataFrame): DataFrame berisi metadata buku (Title, Author).
    top_n (int): Jumlah buku teratas yang akan direkomendasikan (default 5).

    Returns:
    pd.DataFrame: DataFrame dengan kolom Title, Author, dan Predicted Rating.
    """
    # Ambil indeks user di matriks
    user_index = utility_matrix.columns.get_loc(user_id)

    # Prediksi rating untuk semua buku yang belum dinilai oleh user
    predicted_ratings = reconstructed_matrix[:, user_index]

    # Ambil buku dengan rating prediksi tertinggi (buku yang belum diberi rating)
    unrated_books = utility_matrix.index[utility_matrix.loc[:, user_id] == 0]
    predicted_ratings_for_unrated = [(book, predicted_ratings[utility_matrix.index.get_loc(book)])
                                     for book in unrated_books]

    # Urutkan berdasarkan prediksi rating tertinggi
    predicted_ratings_for_unrated.sort(key=lambda x: x[1], reverse=True)

    # Ambil top_n buku teratas
    top_recommended_books = predicted_ratings_for_unrated[:top_n]

    # Gabungkan dengan metadata buku
    recommendations_df = pd.DataFrame(top_recommended_books, columns=['Title', 'Predicted Rating'])
    recommendations_df = recommendations_df.merge(books_metadata, on='Title', how='left')

    # Pilih hanya kolom yang relevan
    recommendations_df = recommendations_df[['Title', 'Author', 'Predicted Rating']]

    return recommendations_df

# Metadata buku dengan kolom ISBN, Title, dan Author
books_metadata = books[['Title', 'Author']]

"""Memberikan rekomendasi untuk user 254"""

user_id = 254

top_recommended_CF = recommended_books_CF(user_id, utility_matrix_filtered, reconstructed_matrix, filtered_CF, top_n=5)

# drop duplicated untuk melihat 5 buku teratas
top_recommended_CF = top_recommended_CF.drop_duplicates()
top_recommended_CF

"""## Cosine Similarity untuk Content-Based Filtering

Pada tahap ini menghitung cosine similarity pada matriks untuk melihat kemiripan antar buku
"""

# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

cosine_sim_df = pd.DataFrame(cosine_sim, index=filtered_CBF['Title'], columns=filtered_CBF['Title'])

# Melihat similarity matrix
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""Setelah melakukan proses tersebut, fungsi untuk rekomendasi buku dengan pendekatan Content-Based Filtering dibuat. Fungsi akan memberi rekomendasi berdasarkan input judul buku dan mencari kemiripan berdasarkan Author."""

def recommended_books_CBF(judul_buku, similarity_data=cosine_sim_df, items=filtered_CBF[['Title', 'Author']], k=5):
    """
    Rekomendasi buku berdasarkan kemiripan dataframe

    Parameter:
    ---
    judul_buku : tipe data string (str)
    similarity_data : tipe data pd.DataFrame (object)
                      Kesamaan dataframe, simetrik,
    items : tipe data pd.DataFrame (object)
            Mengandung kedua nama dan fitur lainnya yang digunakan untuk mendefinisikan kemiripan
    k : tipe data integer (int)
        Banyaknya jumlah rekomendasi yang diberikan
    ---

    Pada index ini, kita mengambil k dengan nilai similarity terbesar
    pada index matrix yang diberikan (i).
    """


    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan
    index = similarity_data.loc[:,judul_buku].to_numpy().argpartition(
        range(-1, -k, -1))

    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Drop judul_buku agar nama resto yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(judul_buku, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

"""Memberikan rekomendasi buku yang mirip Night Watch"""

title = 'Night Watch'

target_CBF = filtered_CBF[filtered_CBF.Title.eq(title)]
target_CBF

top_recommended_CBF = recommended_books_CBF(title)
top_recommended_CBF

"""## Evaluasi

### Evaluasi SVD untuk Collaborative Filtering

Evaluasi dilakukan dengan menghitung precision. buku yang relevant diambil dari data buku yang telah diberi rating oleh user. Lalu hitung relevant_in_recommendations dengan jumlah buku yang sama antara relevant dengan recomended. Selanjutnya precision didapat dari total buku relevant_in_recommendations dibagi dengan total buku recommended.
"""

# Definisikan threshold untuk menentukan buku yang relevan
relevance_threshold = 3

# Ambil ground truth buku relevan untuk pengguna
relevant_books_per_user = ratings_books_titles[ratings_books_titles['Rating'] >= relevance_threshold].groupby('User')['Title'].apply(set)

# Ambil buku yang direkomendasikan oleh model
recommended_books = set(top_recommended_CF['Title'])

# Ambil buku yang relevan untuk user
relevant_books = relevant_books_per_user.get(user_id, set())

# Hitung jumlah buku relevan di rekomendasi
relevant_in_recommendations = recommended_books.intersection(relevant_books)

# Precision: proporsi buku relevan di antara buku yang direkomendasikan
precision_CF = len(relevant_in_recommendations) / len(recommended_books) if recommended_books else 0


print(f"Precision {precision_CF:.2f}")

"""### Evaluasi Cosine Similarity untuk Content-Based Filtering

Evaluasi dilakukan dengan menghitung precision. Jumlah rekomendasi yang relevan (input) dibagi jumlah rekomendasi, dengan Author untuk melihat kemiripannya.
"""

# ambil data author dari buku yang relevan (input) dan jadikan list
relevant_CBF = target_CBF['Author'].tolist()

# ambil data author dari buku yang direkomendasikan (input) dan jadikan list
recomended_CBF = top_recommended_CBF['Author'].tolist()

# hitung jumlah rekomendasi yang sesuai dengan relevan
relevant_recommendation_CBF = len(top_recommended_CBF[top_recommended_CBF['Author'] == relevant_CBF[0]])

# hitung precision
precision_CBF = relevant_recommendation_CBF / len(recomended_CBF) if len(recomended_CBF) > 0 else 0

print(f"Precision: {precision_CBF}")