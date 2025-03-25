import pandas as pd
import random
from datetime import datetime, timedelta
import re

# ========== KONFIGURASI ==========
JUMLAH_PER_LABEL = 2000  # Sesuaikan jika perlu
SEED = 42  # Untuk reproducibility
random.seed(SEED)

# Lokasi spesifik per bencana
LOKASI = {
    "gempabumi": ["Aceh", "Palu", "Cianjur", "Lombok", "Yogyakarta", "Padang", "Bengkulu"],
    "tsunami": ["Banda Aceh", "Palu", "Kepulauan Mentawai", "Pantai Selatan Jawa", "Sulawesi Tenggara"],
    "banjir": ["Jakarta", "Banjarmasin", "Semarang", "Medan", "Surabaya", "Bandung", "Pekalongan"],
    "tanah_longsor": ["Bogor", "Puncak", "Banjarnegara", "Agam", "Pacitan", "Wonosobo", "Garut"]
}

# Template untuk laporan not_relevant (lebih natural)
NOT_RELEVANT_TEMPLATES = [
    "Rapat koordinasi BPBD {lokasi} membahas kesiapsiagaan bencana",
    "Pemantauan harian cuaca di {lokasi} menunjukkan kondisi stabil",
    "Pelatihan mitigasi bencana di {lokasi} diikuti {angka} peserta",
    "Posko {lokasi} melaporkan tidak ada aktivitas darurat hari ini",
    "Simulasi evakuasi mandiri dilakukan di {lokasi} oleh {angka} warga",
    "Laporan inventaris logistik darurat di {lokasi} dalam kondisi lengkap",
    "Masyarakat {lokasi} mengadakan kerja bakti rutin",
    "Pemeriksaan rutin infrastruktur jalan di {lokasi} selesai dilaksanakan",
    "Sosialisasi pengurangan risiko bencana di {lokasi} berjalan lancar",
    "{lokasi} dalam kondisi aman berdasarkan pemantauan terakhir",
    "Pembangunan posko baru di {lokasi} selesai {waktu} ini",
    "Monitoring harian di {lokasi} tidak mencatat kejadian signifikan"
]

# ========== FUNGSI GENERATOR ==========
def generate_tanggal(day_offset=365*5):
    """Generate random date within last N years"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=day_offset)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

def generate_not_relevant():
    """Generate realistic non-disaster reports"""
    template = random.choice(NOT_RELEVANT_TEMPLATES)
    lokasi = random.choice(list(set(
        LOKASI["gempabumi"] + 
        LOKASI["banjir"] + 
        LOKASI["tsunami"] + 
        LOKASI["tanah_longsor"]
    )))
    
    return template.format(
        lokasi=lokasi,
        angka=random.randint(10, 100),
        waktu=random.choice(["minggu", "bulan", "tahun"])
    )

def generate_gempa():
    magnitude = round(random.uniform(3.0, 7.0), 1)
    lokasi = random.choice(LOKASI["gempabumi"])
    tanggal = generate_tanggal()
    kerusakan = random.choice([
        f"{random.randint(10, 500)} rumah rusak",
        f"Retakan tanah selebar {random.randint(1, 20)} meter",
        f"{random.randint(1, 10)} fasilitas publik rusak berat"
    ])
    return f"Gempa {magnitude} SR mengguncang {lokasi} pada {tanggal}. {kerusakan}."

def generate_banjir():
    ketinggian = round(random.uniform(0.5, 3.0), 1)
    lokasi = random.choice(LOKASI["banjir"])
    durasi = random.randint(1, 72)
    dampak = random.choice([
        f"{random.randint(5, 50)} RT terendam",
        f"Jalan protokol tergenang {random.randint(100, 1000)} meter",
        f"{random.randint(100, 5000)} warga mengungsi"
    ])
    return f"Banjir setinggi {ketinggian} meter melanda {lokasi} selama {durasi} jam. {dampak}."

def generate_tsunami():
    lokasi = random.choice(LOKASI["tsunami"])
    magnitude = round(random.uniform(5.0, 8.0), 1)
    tinggi_gelombang = random.randint(1, 15)
    return f"Peringatan tsunami di {lokasi} setelah gempa {magnitude} SR. Gelombang setinggi {tinggi_gelombang} meter terdeteksi."

def generate_tanah_longsor():
    lokasi = random.choice(LOKASI["tanah_longsor"])
    tanggal = generate_tanggal()
    luas = random.randint(1, 50)
    return f"Tanah longsor di {lokasi} pada {tanggal}. Area seluas {luas} hektar terdampak."

# ========== GENERATE DATASET ==========
labels = ["gempabumi", "banjir", "tanah_longsor", "tsunami", "not_relevant"]
generators = {
    "gempabumi": generate_gempa,
    "banjir": generate_banjir,
    "tanah_longsor": generate_tanah_longsor,
    "tsunami": generate_tsunami,
    "not_relevant": generate_not_relevant
}

data = []
for label in labels:
    print(f"Generating {JUMLAH_PER_LABEL} data for {label}...")
    data += [{"text": generators[label](), "label": label} 
             for _ in range(JUMLAH_PER_LABEL)]

# Convert to DataFrame
df = pd.DataFrame(data)

# ========== POST-PROCESSING ==========
# Contoh cleaning sederhana (opsional)
def simple_clean(text):
    text = re.sub(r'[^\w\s.,!?]', ' ', text)  # Hapus karakter aneh
    text = re.sub(r'\s+', ' ', text)          # Hapus spasi berlebih
    return text.strip()

df['text'] = df['text'].apply(simple_clean)

# ========== SAVE & VERIFY ==========
df.to_csv("dataset_bencana_seimbang.csv", index=False)
print("\n=== Distribusi Label ===")
print(df['label'].value_counts())

print("\n=== Contoh Data ===")
print(df.sample(5))