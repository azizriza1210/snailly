import pandas as pd
import metadata_parser
import numpy as np
import urllib
import mimetypes
import re
import joblib


def __deletion_baseoncharacter(url):
    pattern_list = [r'.*\.js$', r'.*\.js\?.*',
                    r'.*\.png$', r'.*\.png\?.*',
                    r'.*\.jpg$', r'.*\.jpg\?.*',
                    r'.*\.jpeg$', r'.*\.jpeg\?.*',
                    r'.*\.gif$', r'.*\.gif\?.*',
                    r'.*\.svg$', r'.*\.svg\?.*',
                    r'.*\.webp$', r'.*\.webp\?.*',
                    r'.*\.json$', r'.*\.json\?.*',
                    r'.*\.gif$', r'.*\.gif\?.*']
    
    for p in pattern_list:
        pattern = re.compile(p)
        if re.match(pattern, url):
            return(True)
    
    return(False)

def __deletion_baseoncharacter2(url):
    pattern_list = [r'.*auth.*',
                    r'.*auth.*',
                    r'.*[-\/.]api$',r'.*[-\/.]api[-\/.].*',r'^api[-\/.].*',
                    r'.*[-\/.]captcha$',r'.*[-\/.]captcha[-\/.].*',r'^captcha[-\/.].*',
                    r'.*[-\/.]recaptcha$',r'.*[-\/.]recaptcha[-\/.].*',r'^recaptcha[-\/.].*',
                    r'.*[-\/.]validatecaptcha$',r'.*[-\/.]validatecaptcha[-\/.].*',r'^validatecaptcha[-\/.].*',
                    r'.*mega\.co\.nz.*']
    
    for p in pattern_list:
        pattern = re.compile(p)
        if re.match(pattern, url):
            return(True)
    
    return(False)

def __guess_type_url(link, strict=True):
    """
        Fungsi ini akan mengembalikan nilai jenis dari link berupa string
        contoh : 
          'https://m-w.com' -> 'application/x-msdos-program'
          'https://cornell.edu' -> 'text/html' 
    """
    try :
      link_type, _ = mimetypes.guess_type(link)
      if link_type is None and strict:
          u = urllib.request.urlopen(link)
          link_type = u.headers.get_content_type()
    except Exception as e: 
      link_type = "[ERROR] " + str(e)
    return link_type

def __get_metadata(url, meta_name = ['description', 'title']):
    """
        Fungsi ini akan mengembalikan nilai meta-tag dari url berbentuk list berurutan sesuai meta_name
    """
    content = []
    url_file_type = __guess_type_url(url)
    if url_file_type in ['application/x-msdos-program', 'text/html']:
      try:
          page = metadata_parser.MetadataParser(url)
      except:
          return ['error']*len(meta_name)+[url_file_type]
      for m in meta_name:
          try:
              content.append(page.get_metadata(m, strategy=['meta','page','og','dc']))
          except:
              content.append('error')
      content+=[url_file_type]
    else :
      content = ['error']*len(meta_name)+[url_file_type]
    return np.array(content)  

def __cron_meta_data(df, meta_name = ['description', 'title']):
    """
        df : dataframe
        meta_name : meta tag name, column name
    """
    
    column = [m+"_raw" for m in meta_name] + ['url_type']
    data = df.url.apply(lambda x : __get_metadata(x,meta_name))
    df[column] = np.array([np.array(z) for z in zip(*data)]).T

def __no_meta_tag(df, column_names = ['description_raw','title_raw']):
    subset = np.full(len(df), True)
    for c in column_names:
        subset = (subset & (df[c] != 'error') & (df[c] != '') & (df[c].values != None ) & (pd.notna(df[c])))
    return np.invert(subset)

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
# nltk.download('omw-1.4')
# nltk.download()
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
stopword_id = stopwords.words('indonesian')
stopword_en = stopwords.words('english')
stopword_all = stopword_id + stopword_en

lemmatizer = WordNetLemmatizer()
id_stem = StemmerFactory().create_stemmer()

def __case_folding(str_data):
    return str_data.lower()

def __digits_removal(str_data):
    return re.sub('[0-9]+', '', str_data)

def __breaking_hyphens(str_data):
    return re.sub('[-]', ' ', str_data)

def __punctuation_mark_removal(str_data):
    str_data_t = re.sub(r'https?:\/\/.*[\r\n]*', '', str_data)
    str_data_t = re.sub(r'\n',' ',str_data_t)
    str_data_t = re.sub(r'[?|$.!_:")(+,*&%#@]','',str_data_t)
    str_data_t = re.sub(' +', ' ', str_data_t)
    str_data_t = str_data_t.strip()
    return str_data_t

def __tokenizing(str_data):
    return (word_tokenize(str_data))

def __get_wordnet_pos(word):
    treebank_tag = pos_tag([word])[0][1]
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def __lemmatize(word):
    pos_tag = __get_wordnet_pos(word)
    return lemmatizer.lemmatize(word, pos=pos_tag)

def __stemming(list_str_data):
    list_str_data_t = []
    for s in list_str_data:
        content_id = id_stem.stem(s)
        content_en = __lemmatize(s)
        content = content_id if content_en == s else content_en
        list_str_data_t.append(content)
    return list_str_data_t

def __stopword_removal(list_str_data):
    list_str_data_t = []
    for s in list_str_data:
        if s not in stopword_all:
            list_str_data_t.append(s)
    return list_str_data_t

def __preprocessing(str_data):
    str_data_t = __case_folding(str_data)
    str_data_t = __digits_removal(str_data_t)
    str_data_t = __breaking_hyphens(str_data_t)
    str_data_t = __punctuation_mark_removal(str_data_t)
    str_data_t = __tokenizing(str_data_t)
    str_data_t = __stemming(str_data_t)
    str_data_t = __stopword_removal(str_data_t)
    return " ".join(str_data_t)

def __decfunc_final(x):
    desc_decfunc_value = 0.98/1.85
    title_decfunc_value = 0.87/1.85
    return x['SVM_desc_decfunc'] * desc_decfunc_value + x['SVM_title_decfunc'] * title_decfunc_value 

def do_cron(df):
    df['del_status'] = 'not_deleted'

    mask_duplicated = df.duplicated(subset=['url'])
    df_temp = df.loc[mask_duplicated,:].copy()
    df_temp['del_status'] = 'duplicate'
    df = df[~mask_duplicated]
    df_del = df_temp.copy()

    mask_deletion_baseoncharacter = df.url.apply(__deletion_baseoncharacter)
    df_temp = df.loc[mask_deletion_baseoncharacter,:].copy()
    df_temp['del_status'] = 'char_del'
    df = df[~mask_deletion_baseoncharacter]
    df_del = pd.concat([df_del,df_temp])

    mask_deletion_baseoncharacter2 = df.url.apply(__deletion_baseoncharacter2)
    df_temp = df.loc[mask_deletion_baseoncharacter2,:].copy()
    df_temp['del_status'] = 'char_del2'
    df = df[~mask_deletion_baseoncharacter2]
    df_del = pd.concat([df_del,df_temp])

    __cron_meta_data(df)

    mask_no_meta_tag = __no_meta_tag(df)
    df_temp = df.loc[mask_no_meta_tag,:].copy()
    df_temp['del_status'] = 'no_meta_tag'
    df = df[~mask_no_meta_tag]
    df_del = pd.concat([df_del,df_temp])

    
    df['description'] = df.description_raw.apply(__preprocessing)
    df['title'] = df.title_raw.apply(__preprocessing)

    if df.shape[0] == 0 :
        return df,df_del

    vect_desc = joblib.load('saved_model/vect_desc.pkl')
    vect_title = joblib.load('saved_model/vect_title.pkl')
    svm_desc = joblib.load('saved_model/SVM_desc.pkl')
    svm_title = joblib.load('saved_model/SVM_title.pkl')

    X_desc = vect_desc.transform(df.description)
    X_title = vect_title.transform(df.title)

    predicted_test_desc = svm_desc.predict(X_desc)
    decfunc_test_desc = svm_desc.decision_function(X_desc)
    predicted_test_title = svm_title.predict(X_title)
    decfunc_test_title= svm_title.decision_function(X_title)

    df['SVM_desc_label'] = predicted_test_desc
    df['SVM_desc_decfunc'] = decfunc_test_desc*-1
    df['SVM_title_label'] = predicted_test_title
    df['SVM_title_decfunc'] = decfunc_test_title*-1

    df['FINAL_decfunc'] = df.apply(__decfunc_final, axis=1)
    df['FINAL_label'] = df['FINAL_decfunc'].apply(lambda x: "aman" if  x > 0 else "berbahaya" ) 

    return df,df_del
    # df.to_csv('cron_ouput_labeled_websites.csv')
    # df_del.to_csv('cron_ouput_failed_url.csv')
    
# sql_df = pd.read_csv(r'temp.csv', index_col=0)
# df_hasil,df_del = do_cron(sql_df)
# df0 = pd.concat([df_hasil,df_del],ignore_index = True)
# df0.to_csv('temp2.csv')
