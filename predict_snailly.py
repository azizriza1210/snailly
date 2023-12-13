from sqlalchemy import create_engine, text
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from deep_translator import GoogleTranslator
from sklearn.metrics import accuracy_score, classification_report
import pickle
import cfscrape 
import preprocessing_cron as pre
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs

# Ganti nilai berikut sesuai dengan kredensial dan pengaturan basis data Anda
db_url = "postgresql://postgres:password@localhost:5432/snailly"
engine = create_engine(db_url)

log_ids = []
urls = []
status = []

# Fungsi untuk menghapus pengulangan kata
def remove_duplicate_words(text):
    words = text.split()
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return ' '.join(unique_words)

def add_spasi(text):
    hasil = re.sub(r'(?<=[a-z])([A-Z])', r' \1', text)
    return hasil 

def get_data(log_id, url) :
    connection = engine.connect()

    # Menjalankan query menggunakan objek text
    query = text("""SELECT log_activity.log_id, url from log_activity 
                LEFT OUTER JOIN classified_url on log_activity.log_id = classified_url.log_id 
                WHERE classified_url.cu_id IS NULL""")
    result = connection.execute(query)

    # Menampilkan hasil query
    for row in result:
        log_ids.append(row[0])
        urls.append(row[1])

    # Menutup koneksi
    connection.close()
    
def insert_data(sql) :
    connection = engine.connect()

    # Menjalankan query menggunakan objek text
    query = text(sql)
    connection.execute(query)

    connection.commit()
    # Menutup koneksi
    connection.close()

def scrap(url) :
    scraper = cfscrape.create_scraper() 
    scraped_data = scraper.get(url) 

    soup = BeautifulSoup(scraped_data.text, 'html.parser')
    text = soup.get_text()
    
    # clean dikit
    kalimat = add_spasi(text)
    kalimat = remove_duplicate_words(kalimat.lower())
    return kalimat[:255]
    # return kalimat[:500]
    # return kalimat

def selenium_scrap(url) :
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--start-maximized")  # Buka browser dalam mode layar penuh

    driver = webdriver.Chrome(options=chrome_options)

    if "duckduckgo.com" in url:
        link_awal = "https://duckduckgo.com/"
        input_tag = "//input[@aria-label='Search with DuckDuckGo']"
    else : 
        link_awal = "https://www.google.com/"
        input_tag = "//textarea[@type='search']"
        

    # Menganalisis URL
    parsed_url = urlparse(url)

    # Mengambil parameter pencarian "q" dari URL
    query_params = parse_qs(parsed_url.query)

    # Cetak kata kunci pencarian
    if 'q' in query_params:
        search_query = query_params['q'][0]
        driver.get(link_awal)
        time.sleep(2)
        
        element_input = driver.find_element(By.XPATH, input_tag)
        element_input.send_keys(search_query)
        element_input.send_keys(Keys.RETURN)
        
        teks = driver.find_element(By.XPATH, "/html/body").text
        
        # clean dikit
        kalimat = add_spasi(teks)
        kalimat = remove_duplicate_words(kalimat.lower())
        return kalimat[200:]
        # return kalimat[:500]
    else:
        driver.get(link_awal)
        time.sleep(2)
        
        teks = driver.find_element(By.XPATH, "/html/body").text
        
        # clean dikit
        kalimat = add_spasi(teks)
        kalimat = remove_duplicate_words(kalimat.lower())
        return kalimat[200:]

    

def selenium_scrap_twitter(url) :
    username = "azzzzz28463957"
    password = "S41fa1Ip"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--start-maximized")  # Buka browser dalam mode layar penuh

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://twitter.com")
    time.sleep(2)

    username = "snail3976"
    password = "snail011013"

    element_signIn = driver.find_element(By.XPATH, "//a[@data-testid='loginButton']")
    element_signIn.click()      
    time.sleep(3.5)
    element_input = driver.find_element(By.XPATH, "//input[@name='text']")
    element_input.send_keys(username)

    element_next = driver.find_element(By.XPATH, "//div[@class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu']")
    element_next.click()
    time.sleep(2)
    element_password = driver.find_element(By.XPATH, "//input[@name='password']")
    element_password.send_keys(password)
    element_login = driver.find_element(By.XPATH, "//div[@data-testid='LoginForm_Login_Button']")
    element_login.click()
    time.sleep(4)
    
    driver.get(url)
    time.sleep(2)
    
    teks = driver.find_element(By.XPATH, "/html/body").text
    
    # clean dikit
    kalimat = add_spasi(teks)
    kalimat = remove_duplicate_words(kalimat.lower())
    return kalimat[:500]

def predict(text) :
    with open('Model/tfidf_vectorizer_snailly.pkl', 'rb') as file:
        loaded_tfidf_vectorizer = pickle.load(file)

    with open('Model/model_snaily_1.pkl', 'rb') as file:
        loaded_svm_model = pickle.load(file)

    new_text_vector = loaded_tfidf_vectorizer.transform([text])

    # Gunakan model yang dimuat untuk membuat prediksi
    new_predictions = loaded_svm_model.predict(new_text_vector)

    return new_predictions

i =   1  

while i == 1 :
    # get_data(log_ids, urls)    
    connection = engine.connect()

    # Menjalankan query menggunakan objek text
    query = text("""SELECT log_activity.log_id, url from log_activity 
                LEFT OUTER JOIN classified_url on log_activity.log_id = classified_url.log_id 
                WHERE classified_url.cu_id IS NULL""")
    result = connection.execute(query)

    # Menampilkan hasil query
    for row in result:
        log_ids.append(row[0])
        urls.append(row[1])

    # Menutup koneksi
    connection.close()
    # print("ini url : ", urls)

    if urls :
        no = 0
        predik = []
        for url in urls :
            print("ini url : ",url)
            url = str(url)
            if "twitter" in url.lower():
                hasil_scrap = selenium_scrap_twitter(url)
            elif "google" in url.lower():
                hasil_scrap = selenium_scrap(url)
            elif "duckduckgo" in url.lower():
                hasil_scrap = selenium_scrap(url)
            elif "bing" in url.lower():
                hasil_scrap = selenium_scrap(url)
            else :
                hasil_scrap = scrap(url)
            
            hasil_clean = pre.remove_tag(hasil_scrap)
            hasil_clean = pre.remove_punctuation(hasil_clean)
            hasil_clean = pre.translate(hasil_clean)
            hasil_clean = pre.remove_tag(hasil_clean)
            hasil_clean = pre.remove_punctuation(hasil_clean)
            hasil_clean = pre.expand_contractions_id(hasil_clean)
            hasil_clean = pre.ubah_angka(hasil_clean)
            hasil_clean = pre.remove_number(hasil_clean)
            hasil_clean = pre.remove_links(hasil_clean)
            hasil_clean = pre.remove_single_letter_words(hasil_clean)
            hasil_clean = pre.stopword(hasil_clean)
            
            hasil_predict = predict(str(hasil_clean[:500]).lower())
            predik.append(hasil_predict[0])
            status.append(hasil_predict[0])
            sql = """INSERT INTO public.classified_url(url_type, description, log_id, "FINAL_label") VALUES ('"""+str(url)+"""', '"""+str(hasil_clean)[:1000]+"""', '"""+str(log_ids[no])+"""', '"""+str(hasil_predict[0])+"""');"""
            insert_data(sql)
            no += 1
    
    