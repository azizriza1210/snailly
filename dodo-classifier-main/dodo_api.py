from flask import Flask, jsonify, Response
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Float, Enum
import cron_website_label
import json
import cron_website_label
import pandas as pd
from flask import Flask, request
from waitress import serve
app = Flask(__name__)
api = Api(app)

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

class GetWebsiteLabel(Resource):
    def post(self):
        try:
            url = request.form.get('url')
            sql_df = pd.read_sql("""SELECT * \
                from log_user LEFT JOIN classified_url \
                on log_user.log_id = classified_url.log_id \
                WHERE log_user.url = '{}' \
                """.format(url),
                con=engine)
            if sql_df.shape[0] != 0:
                if sql_df.loc[0].FINAL_label != None:
                    return jsonify(status = 'success',
                    label = sql_df.loc[0].FINAL_label)
                else:
                    return jsonify(status = 'success',
                    label = 'not_classified')
            else:
                insert_df = pd.DataFrame({'url':[url]})
                insert_df.to_sql(con=engine, name='log_user',if_exists='append', dtype={
                    'url': String(2048)},index=False)
                print(sql_df)
                return jsonify(status = 'success',
                label = 'not_classified')
        except Exception as e:
            return jsonify(status = 'failed',
            message=str(e))


class GetWebsiteBerbahaya(Resource):
    def get(self):
        try:
            sql_df = pd.read_sql("""SELECT url, description, title ,FINAL_label \
                from log_user LEFT JOIN classified_url \
                on log_user.log_id = classified_url.log_id \
                WHERE classified_url.FINAL_label = 'berbahaya' \
                """,
                con=engine)
            result = sql_df.to_json(orient="records")
            parsed = json.loads(result)
            data = json.dumps({'status':'success','data': parsed},indent=4)
            return Response(data, mimetype='application/json')
        except Exception as e:
            return jsonify(status = 'failed',
            message=str(e))


class DoCron(Resource):
    def get(self):
        try:
            while True:
                sql_df = pd.read_sql("""SELECT log_user.log_id, url \
                    from log_user LEFT JOIN classified_url \
                    on log_user.log_id = classified_url.log_id \
                    WHERE classified_url.cu_id IS NULL \
                    LIMIT 2
                    """,
                    con=engine)

                if sql_df.shape[0] <= 0 :
                    break
                else:       
                    print("=qwerty=")             
                    df_hasil,df_del = cron_website_label.do_cron(sql_df)
                    df = pd.concat([df_hasil,df_del],ignore_index = True)
                    df.drop(columns=['url'], inplace=True)

                    df.to_sql(con=engine, name='classified_url',if_exists='append', dtype={
                        'log_id':Integer,
                        'classified_status' : Enum('classified','not_classified'),
                        'del_status' : String(32),
                        'description_raw' : String(255),
                        'title_raw' : String(255),
                        'url_type' : String(32),
                        'description' : String(255),
                        'title' : String(255),
                        'SVM_desc_label' : Enum('aman','berbahaya'),
                        'SVM_desc_decfunc' : Float,
                        'SVM_title_label' : Enum('aman','berbahaya'),
                        'SVM_title_decfunc' : Float,
                        'FINAL_label' : Enum('aman','berbahaya'),
                        'FINAL_decfunc' : Float,
                        },index=False)
                
        except Exception as e:
            print('=ERROR MESSAGE=')
            print(e)
            return jsonify(status = 'failed',
            message=str(e))

        return jsonify(status = 'success')

api.add_resource(GetWebsiteLabel, '/getwebsitelabel')
api.add_resource(GetWebsiteBerbahaya, '/getwebsiteberbahaya')
api.add_resource(DoCron, '/startcronjob')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    print("starting..")
    #serve(app, host="0.0.0.0", port=8080)
   # print("started.." )   
