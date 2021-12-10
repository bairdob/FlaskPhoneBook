from flask import Flask
from flask import request, make_response, redirect, abort, render_template
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

try:
    conn = psycopg2.connect(dbname='phone_book',
                            user="bair",
                            password="",
                            host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
except (Exception, Error) as error:
    print("Error: ", error)

cursor.execute('SELECT * FROM name')
nameTable = cursor.fetchall()

nameDict = []
for it in nameTable:
    temp = {'name_id': it[0], 'name_value': it[1]}
    nameDict.append(temp)

nameValues = []
for i in range(len(nameDict)):
    nameValues.append(nameDict[i]['name_value'])

query = 'SELECT main.u_id AS u_id, surname.sname_value AS surname, \
                name.name_value AS name, patronymic.patr_value AS patronymic, \
                street.street_value AS street, main.building as building, \
                main.corpus AS corpus, phone AS phone \
         FROM main \
         JOIN patronymic ON main.patronymic = patronymic.patr_id \
         JOIN surname ON main.surname = surname.sname_id \
         JOIN street ON main.street = street.street_id \
         JOIN name ON main.name = name.name_id WHERE TRUE'
cursor.execute(query)
mainTable = cursor.fetchall()

mainDict = []
for it in mainTable:
    temp = {'u_id': it[0], 'surname': it[1], 'name': it[2], 'patronymic': it[3],
            'street': it[4], 'building': it[5], 'corpus': it[6], 'phone': it[7]}
    mainDict.append(temp)


@app.route('/')
def index():
    return render_template('index2.html', mainTable=mainDict, option=nameValues)


@app.route('/name/add', methods=['post', 'get'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        cursor.execute('INSERT INTO name(name_value) VALUES(\'%s\');' % name)
        conn.commit()
        cursor.execute('SELECT * FROM name WHERE name_value = \'%s\'' % name)
        nameRow = cursor.fetchall()
        currentName = {'name_id': nameRow[0][0], 'name_value': name}
        nameDict.append(currentName)
    return render_template('nameAdd.html', nameList=nameDict)


@app.route('/name/delete', methods=['post', 'get'])
def delete():
    name = request.form.get('name')
    print(name)
    cursor.execute('DELETE FROM name WHERE name_value = \'%s\'' % name)
    conn.commit()
    for i in range(len(nameDict)):
        if nameDict[i]['name_value'] == name:
            del nameDict[i]
            break
    return render_template('nameDelete.html', nameList=nameDict)


if __name__ == '__main__':
    app.run(debug=True)
