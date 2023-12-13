from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, ForeignKey, Enum

user = 'sql6513783'
password = 'YAGmMztyGf'
host = 'sql6.freemysqlhosting.net'
port = 3306
database = 'sql6513783'

def get_connection():
	return create_engine(
		url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
			user, password, host, port, database
		)
	)

engine = get_connection()

meta = MetaData()

log_user = Table(
    'log_user', meta, 
   Column('log_id', Integer, primary_key = True), 
   Column('url', String(2048))
)

classified_url = Table(
    'classified_url', meta, 
   Column('cu_id', Integer, primary_key = True), 
   Column('log_id', Integer, ForeignKey("log_user.log_id"), nullable=False),
   Column('classified_status', Enum('classified','not_classified')),
   Column('del_status', String(32)),
   Column('description_raw', String(255)),
   Column('title_raw', String(255)),
   Column('url_type', String(32)),
   Column('description', String(255)),
   Column('title', String(255)),
   Column('SVM_desc_label', Enum('aman','berbahaya')),
   Column('SVM_desc_decfunc', Float),
   Column('SVM_title_label', Enum('aman','berbahaya')),
   Column('SVM_title_decfunc', Float),
   Column('FINAL_label', Enum('aman','berbahaya')),
   Column('FINAL_decfunc', Float),
)

meta.create_all(engine)

