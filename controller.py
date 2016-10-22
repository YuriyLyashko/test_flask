import pymysql

from parser import read
import administration_db, for_html


incoming_file = 'eFw3Cefj.json'
db = 'test'

table = read(incoming_file)

adm_db = administration_db.AdminDB(table, incoming_file)

try:
    adm_db.connect_db(db)
except pymysql.err.InternalError:
    try:
        adm_db.create_db(db)
    except:
        raise ConnectionError
finally:
    adm_db.use_db(db)
    try:
        adm_db.create_table(adm_db.name_table_data)
    except:
        adm_db.drop_table(adm_db.name_table_data)
        adm_db.create_table(adm_db.name_table_data)
    finally:
        adm_db.write_into(adm_db.name_table_data, adm_db.table)
        table_from_db = adm_db.read_from(adm_db.name_table_data)
        adm_db.close_connection()

data_for_html = for_html.ForHtml(table_from_db, adm_db.table['structure'])