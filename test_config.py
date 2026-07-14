"""
Configuration file untuk test_chatbot_performance.py
Edit file ini untuk customize test parameters tanpa harus edit script utama
"""

# ==================== TEST PARAMETERS ====================
# Jumlah pertanyaan unik untuk testing
NUM_TEST_QUESTIONS = 10

# Berapa kali setiap pertanyaan diulang
NUM_REPETITIONS = 10

# Top-K untuk perhitungan metrik (Recall@K, Precision@K, NDCG@K)
# Biasanya sama dengan jumlah dokumen yang di-retrieve
TOP_K = 7

# ==================== PATH CONFIGURATION ====================
PERSIST_DIRECTORY = "chroma_db"
TEST_RESULTS_DIR = "test_results"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ==================== TEST DATA ====================
# Format: dictionary dengan "question", "ground_truth_keywords", dan "relevant_documents"
TEST_QUESTIONS = [
    {
        "question": "Apa itu Pangandaran?",
        "ground_truth_keywords": ["Pangandaran", "wisata", "pantai", "destinasi"],
        "relevant_documents": ["wisata_lists.toon"]
    },
    {
        "question": "Berapa harga tiket masuk?",
        "ground_truth_keywords": ["harga", "tiket", "masuk", "biaya"],
        "relevant_documents": ["harga_tiket_lists.toon"]
    },
    {
        "question": "Apa saja hotel yang tersedia?",
        "ground_truth_keywords": ["hotel", "penginapan", "tempat menginap"],
        "relevant_documents": ["hotel_lists.toon"]
    },
    {
        "question": "Bagaimana cara transportasi ke Pangandaran?",
        "ground_truth_keywords": ["transportasi", "cara", "perjalanan", "kendaraan"],
        "relevant_documents": ["transportasi.txt"]
    },
    {
        "question": "Dimana lokasi kantor polisi dan puskesmas Pangandaran?",
        "ground_truth_keywords": ["polisi", "puskesmas", "kantor", "alamat", "jalan"],
        "relevant_documents": ["tempat_penting_lists.toon"]
    },
    {
        "question": "Berapa harga paket wisata?",
        "ground_truth_keywords": ["paket", "wisata", "harga", "tour", "jetski"],
        "relevant_documents": ["paket_wisata_lists.toon"]
    },
    {
        "question": "Layanan emergency contact apa saja yang tersedia?",
        "ground_truth_keywords": ["polisi", "puskesmas", "telkom", "bank", "telpon"],
        "relevant_documents": ["nomor_penting_lists.toon"]
    },
    {
        "question": "Objek wisata apa yang wajib dikunjungi?",
        "ground_truth_keywords": ["wisata", "objek", "kunjungi", "destinasi"],
        "relevant_documents": ["wisata_lists.toon"]
    },
    {
        "question": "Bagaimana kondisi jalan menuju Pangandaran?",
        "ground_truth_keywords": ["jalan", "kondisi", "akses", "transportasi"],
        "relevant_documents": ["transportasi.txt"]
    },
    {
        "question": "Berapa biaya transportasi dari Bandung ke Pangandaran?",
        "ground_truth_keywords": ["Bandung", "Pangandaran", "transportasi", "harga", "rupiah", "tiket"],
        "relevant_documents": ["transportasi.txt"]
    }
]

# ==================== PERFORMANCE TARGETS ====================
# Target performa untuk reference
PERFORMANCE_TARGETS = {
    "query_time_ms": {
        "excellent": 500,      # < 500ms
        "good": 1000,          # 500-1000ms
        "acceptable": 2000,    # 1000-2000ms
    },
    "recall_at_k": {
        "excellent": 0.8,
        "good": 0.6,
        "fair": 0.4,
    },
    "precision_at_k": {
        "excellent": 0.8,
        "good": 0.6,
        "fair": 0.4,
    },
    "ndcg": {
        "excellent": 0.85,
        "good": 0.70,
        "fair": 0.50,
    }
}

# ==================== LOGGING ====================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
ENABLE_VERBOSE_OUTPUT = True  # Print detailed progress

# ==================== ADVANCED OPTIONS ====================
# Backup vector DB sebelum insertion time test
BACKUP_VECTORDB_BEFORE_TEST = True

# Calculate percentiles untuk query time stats
CALCULATE_PERCENTILES = [25, 50, 75, 95, 99]

# Format number di Excel
DECIMAL_PLACES = 4