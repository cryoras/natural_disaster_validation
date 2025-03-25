import pandas as pd
import random
from datetime import datetime, timedelta

# ========== KONFIGURASI ==========
JUMLAH_PER_LABEL = 2000  # Diubah sesuai kebutuhan
LOKASI = {
    "gempabumi": ["Aceh", "Palu", "Cianjur", "Lombok", "Yogyakarta"],
    "tsunami": ["Banda Aceh", "Palu", "Kepulauan Mentawai", "Pantai Selatan Jawa"],
    "banjir": ["Jakarta", "Banjarmasin", "Semarang", "Medan", "Surabaya"],
    "tanah_longsor": ["Bogor", "Puncak", "Banjarnegara", "Agam", "Pacitan"]
}

# ========== FUNGSI GENERATOR ==========
def generate_tanggal():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

def generate_laporan(label):
    if label == "gempabumi":
        teks = f"Gempa {random.uniform(3.0, 7.0):.1f} SR mengguncang {random.choice(LOKASI[label])} pada {generate_tanggal()}. {random.randint(10, 500)} rumah rusak."
    elif label == "banjir":
        teks = f"Banjir setinggi {random.uniform(0.5, 3.0):.1f} meter melanda {random.choice(LOKASI[label])}. {random.randint(5, 100)} RT terendam."
    elif label == "tsunami":
        teks = f"Peringatan tsunami di {random.choice(LOKASI[label])} setelah gempa {random.uniform(5.0, 8.0):.1f} SR. Gelombang setinggi {random.randint(1, 15)} meter."
    elif label == "tanah_longsor":
        teks = f"Tanah longsor di {random.choice(LOKASI[label])} pada {generate_tanggal()}. {random.randint(1, 50)} rumah tertimbun."
    else:
        teks = random.choice([
            "Pemadaman listrik di wilayah tersebut",
            "Kegiatan sosial masyarakat berjalan lancar",
            "Rapat koordinasi penanggulangan bencana",
            "Kucing itu melompat ke atas meja dengan lincah.",
    "Hari ini langit sangat cerah dan biru.",
    "Aku lupa di mana meletakkan kunci motorku.",
    "Musim hujan membuat jalanan menjadi licin.",
    "Burung-burung berkicau merdu di pagi hari.",
    "Anak kecil itu berlari mengejar kupu-kupu.",
    "Sepeda tua di garasi itu masih bisa digunakan.",
    "Aku ingin mencoba memasak resep baru hari ini.",
    "Di taman kota, banyak orang berolahraga setiap pagi.",
    "Lampu jalan mulai menyala saat matahari terbenam."
        ])
    return {"text": teks, "label": label}

# ========== GENERATE DATASET ==========
labels = ["gempabumi", "banjir", "tanah_longsor", "tsunami", "not_relevant"]
data = []
for label in labels:
    data += [generate_laporan(label) for _ in range(JUMLAH_PER_LABEL)]

df = pd.DataFrame(data)
df.to_csv("dataset_bencana_seimbang.csv", index=False)

# Verifikasi distribusi
print(df["label"].value_counts())