import pandas as pd
import re 
from deep_translator import GoogleTranslator
import nltk

# contractions
with open('Prepo/kbba.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
data = [line.strip().split('\t') for line in lines]
data_singkatan = pd.DataFrame(data, columns=['Contraction', 'Meaning'])
df_en = pd.read_csv("Prepo/contractions.csv")
df_singkatan = pd.concat([data_singkatan, df_en], ignore_index=True)
kontraksi_dict = dict(zip(df_singkatan['Contraction'], data_singkatan['Meaning']))

# Fungsi untuk menghapus kata-kata dengan satu huruf
def remove_tag(text):
    words = text.split()
    filtered_words = [word for word in words if not word.startswith('#')]  # Menghapus kata-kata yang dimulai dengan '#'
    filtered_words = [word for word in filtered_words if not word.startswith('http')]  # Menghapus kata-kata yang dimulai dengan '#'
    filtered_words = [word for word in filtered_words if not word.startswith('https')]  # Menghapus kata-kata yang dimulai dengan '#'
    return ' '.join(filtered_words)

# Fungsi untuk menghapus tanda baca
def remove_punctuation(text):
    hasil = re.sub(r'[^\w\s]', '', text)
    return hasil

# Fungsi untuk mengatasi kontraksi dalam bahasa Indonesia
def expand_contractions_id(text):
    kontraksi_dict
    
    words = text.split()
    expanded_text = [kontraksi_dict[word] if word in kontraksi_dict else word for word in words]
    return ' '.join(expanded_text)

def ubah_angka(text):
    # Menggunakan regular expression untuk mengganti karakter alay
    teks_benar = re.sub(r'3', 'e', text)
    teks_benar = re.sub(r'4', 'a', teks_benar)
    teks_benar = re.sub(r'1', 'i', teks_benar)
    teks_benar = re.sub(r'0', 'o', teks_benar)
    return teks_benar

def remove_number(text) :
    hasil = re.sub(r'\d', '', text)
    return hasil

# Fungsi untuk menghapus tautan dari teks
def remove_links(text):
    # Menggunakan ekspresi reguler untuk mencari dan menghapus tautan
    return re.sub(r'http\S+|www\S+|https\S+', '', text)

# Fungsi untuk menghapus kata-kata dengan satu huruf
def remove_single_letter_words(text):
    text = re.sub(r'\b\w\b', '', text)
    
    hapus = ['rj','lc','en','ar','mc','vt','rob','ny','dc','az','va']
    words = text.split()

    # Memfilter kata-kata yang tidak ada dalam array yang akan dihapus
    kata_kata_tanpa_kata_yang_dihapus = [kata for kata in words if kata not in hapus]

    # Menggabungkan kata-kata yang tersisa menjadi kalimat baru
    kalimat_tanpa_kata_yang_dihapus = ' '.join(kata_kata_tanpa_kata_yang_dihapus)
    return kalimat_tanpa_kata_yang_dihapus

def translate(text):
    # to_translate = 'I want to translate this text'
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    return translated

def stopword(text) :
    try:
        from nltk.corpus import stopwords
    except LookupError:
        nltk.download('stopwords')
        
    # Ambil daftar stopwords dalam bahasa Inggris
    stop_words = set(stopwords.words('english'))

    stop_words = list(stop_words)
    tambahan = ['english','language','tagged','indo','click','images','videos','search','tools','time','entertainment','recreation','joined','june','following','iek','followers','create','agree','terms','service','sep','media','privacy','policy','including','use','relevant','google','apple','bookmarks','signing','account','follow','instagram','happening','people','know','post','conversation','twitter','dont','whats','first','sign','news','maps','share','feedback','indonesia','ay','setting','settings','eop','iim','iomin','ioop','op','welcome','paling','skip','content','menu','belum','ai','month','year','day','lanjut','access','ads','ok','must','ee','ao','login','oa','data','connection','ia','cookies','us','log','kami','dlvr','id','co','p','ly','youtu','bal','nder','nak','http','rm','whq','com','st','pth','html','bz','ss','cc','tt','oi','ie','io','ii','oe','ik','cookie','eo','ak','ek','ioo','vr','ea','oo','ei','usc']
    stop_words.extend(tambahan)

    # Menghapus stopwords dari kolom 'text'
    # df['text'] = df['text'].apply(lambda x: stopword_remover.remove(x))
    teks = ' '.join([word for word in text.split() if word.lower() not in stop_words])
    return teks