import pymysql

from parser import read
import administration_db


file = 'eFw3Cefj.json'
db = 'test'

table = read(file)

adm_db = administration_db.AdminDB(table, file)

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

print(table_from_db)

def get_regions():
    regions = []
    for row in table_from_db:
        name = row[adm_db.table['structure'][0]]
        if {'name': name} not in regions:
            regions.append({'name': name})
    return regions

regions = get_regions()


def get_data_for_region(name):
    data = []
    print(name)
    for row in table_from_db:
        if row[adm_db.table['structure'][0]] == name:
            data.append([row[adm_db.table['structure'][1]], int(float(row[adm_db.table['structure'][2]]))])
    return data




from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', regions=regions)


@app.route('/', methods=['POST'])
def test():
    if request.method == 'POST':
        selected_region = request.form.get('name_selected')
        data = get_data_for_region(selected_region)
        return render_template('index.html', regions=regions, data=data, selected_region=selected_region)


if __name__ == '__main__':
    app.run(debug=True)