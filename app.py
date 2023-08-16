from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import send_from_directory
import os
from flask import render_template
from dotenv.main import load_dotenv
from datetime import datetime
import pandas as pd
import io

load_dotenv()
app = Flask(__name__)

print(os.getenv('DATABASE_URL'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

engine = create_engine(os.getenv('DATABASE_URL'))

db_session = scoped_session(sessionmaker(bind=engine))


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.Text, nullable=True)
    subcategory = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)
    value = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Tool %r>' % self.id


class IssuanceOfATool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker = db.Column(db.Text, nullable=True)
    tool = db.Column(db.Text, nullable=True)
    value = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<IssuanceOfATool %r>' % self.id


class Delete_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_one = db.Column(db.Text, nullable=True)
    data_two = db.Column(db.Text, nullable=True)
    data_three = db.Column(db.Integer, nullable=True)
    data_date = db.Column(db.DateTime, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Delete %r>' % self.id


class Workers(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    worker = db.Column(db.Text, nullable=True)
    room = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)


# ================================================================= #

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='favicon.ico')


@app.route('/')
def index():
    return render_template('index.html')

# ================================================================= #
# SET


@app.route('/set_tool', methods=['POST'])
def set_tool():
    main = request.form['main']
    subcategory = request.form['subcategory']
    name = request.form['name']
    value = request.form['value']
    try:
        data_add = Tool(main=main, subcategory=subcategory,
                        name=name, value=value)

        db_session.add(data_add)
        db_session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


@app.route('/set_issuance_of_a_tool', methods=['POST'])
def set_issuance_of_a_tool():
    worker = request.form['worker']
    tool = request.form['tool']
    value = int(request.form['value'])
    try:
        data = Tool.query.filter_by(name=tool).first()

        value_all = data.value

        if value <= value_all:
            data_add = IssuanceOfATool(worker=worker, tool=tool,
                                       value=value)
            value_all -= value
            data.value = value_all
            db.session.commit()

        db_session.add(data_add)
        db_session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


@app.route('/set_workers', methods=['POST'])
def set_workers():
    worker = request.form['worker']
    room = request.form['room']
    try:
        data_add = Workers(worker=worker, room=room)

        db_session.add(data_add)
        db_session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404

# ================================================================= #
# GET


@app.route('/get_tool', methods=['GET'])
def get_tool():
    data = Tool.query.all()
    result = [{'id': i.id, 'main': i.main,
               'subcategory': i.subcategory,
               'name': i.name, 'value': i.value,
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    return result, 200


@app.route('/get_issuance_of_a_tool', methods=['GET'])
def get_issuance_of_a_tool():
    data = IssuanceOfATool.query.all()
    result = [{'id': i.id, 'worker': i.worker, 'tool': i.tool,
               'value': i.value,
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    return result, 200


@app.route('/get_delete_data', methods=['GET'])
def get_delete_data():
    data = Delete_data.query.all()
    result = [{'id': i.id,
               'data_one': i.data_one,
               'data_two': i.data_two, 'data_three': i.data_three,
               'data_date': i.data_date.strftime('%H:%M:%S %d-%m-%Y'),
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    return result, 200


@app.route('/get_workers', methods=['GET'])
def get_workers():
    data = Workers.query.all()
    result = [{'id': i.id,
               'worker': i.worker,
               'room': i.room,
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    return result, 200


# ================================================================= #
# DEL

@app.route('/del_tool', methods=['POST'])
def del_tool():
    id = request.form['id']
    try:

        db_session.query(Tool).filter_by(id=id).delete()
        db_session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


@app.route('/del_issuance_of_a_tool', methods=['POST'])
def del_issuance_of_a_tool():
    id = request.form['id']
    try:
        i = IssuanceOfATool.query.filter_by(id=id).first()
        data_add = Delete_data(
                               data_one=i.worker, data_two=i.tool,
                               data_three=i.value, data_date=i.date)

        db_session.add(data_add)
        db_session.commit()

        db_session.query(IssuanceOfATool).filter_by(id=id).delete()
        db_session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


@app.route('/del_workers', methods=['POST'])
def del_workers():
    id = request.form['id']
    try:

        db_session.query(Workers).filter_by(id=id).delete()
        db_session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404

# ================================================================= #
# WHERE ID


@app.route('/get_tool_id', methods=['POST'])
def get_tool_id():
    id = request.form['id']
    try:
        i = Tool.query.filter_by(id=id).first()
        result = {'id': i.id, 'main': i.main,
                  'subcategory': i.subcategory,
                  'name': i.name, 'value': i.value,
                  'date': i.date.strftime('%H:%M:%S %d-%m-%Y')}
        return result, 200
    except Exception:
        return {}


@app.route('/get_issuance_of_a_tool_id', methods=['POST'])
def get_issuance_of_a_tool_id():
    id = request.form['id']
    try:
        i = IssuanceOfATool.query.filter_by(id=id).first()
        result = {'id': i.id, 'worker': i.worker, 'tool': i.tool,
                  'value': i.value,
                  'date': i.date.strftime('%H:%M:%S %d-%m-%Y')}
        return result, 200
    except Exception:
        return {}


@app.route('/get_workers_id', methods=['POST'])
def get_workers_id():
    id = request.form['id']
    try:
        i = Workers.query.filter_by(id=id).first()
        result = {'id': i.id, 'worker': i.worker, 'room': i.room,
                  'date': i.date.strftime('%H:%M:%S %d-%m-%Y')}
        return result, 200
    except Exception:
        return {}


# ================================================================= #
# SEARCH


@app.route('/get_tool_search', methods=['POST'])
def get_tool_search():
    name_date = request.form['name']
    try:
        info = Tool.query.filter(Tool.name.like(f'%{name_date}%')).all()
        result = [{'id': i.id, 'main': i.main,
                   'subcategory': i.subcategory,
                   'name': i.name, 'value': i.value,
                   'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in info]
        return result, 200
    except Exception:
        return {}


@app.route('/get_issuance_of_a_tool_search', methods=['POST'])
def get_issuance_of_a_tool_search():
    worker = request.form['worker']
    try:
        info = IssuanceOfATool.query.filter(
            IssuanceOfATool.worker.like(f'%{worker}%')).all()
        result = [{'id': i.id, 'worker': i.worker, 'tool': i.tool,
                   'value': i.value,
                   'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in info]
        return result, 200
    except Exception:
        return {}


@app.route('/get_delete_data_search', methods=['POST'])
def get_delete_data_search():
    worker = request.form['worker']
    try:
        info = Delete_data.query.filter(
            Delete_data.data_one.like(f'%{worker}%')).all()
        result = [
            {'id': i.id,
             'data_one': i.data_one,
             'data_two': i.data_two, 'data_three': i.data_three,
             'data_date': i.data_date.strftime('%H:%M:%S %d-%m-%Y'),
             'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in info]
        return result, 200
    except Exception:
        return {}


@app.route('/get_workers_search', methods=['POST'])
def get_workers_search():
    worker = request.form['worker']
    try:
        info = Workers.query.filter(Workers.worker.like(f'%{worker}%')).all()
        result = [{'id': i.id,
                   'worker': i.worker,
                   'room': i.room,
                   'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in info]
        return result, 200
    except Exception:
        return {}

# ================================================================= #
# UPDATE


@app.route('/update_tool', methods=['POST'])
def update_tool():
    id = request.form['id']
    main = request.form['main']
    subcategory = request.form['subcategory']
    name = request.form['name']
    value = request.form['value']

    try:
        data = Tool.query.filter_by(id=id).first()

        data.main = main
        data.subcategory = subcategory
        data.name = name
        data.value = value

        db.session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


@app.route('/update_issuance_of_a_tool', methods=['POST'])
def update_issuance_of_a_tool():
    id = request.form['id']
    worker = request.form['worker']
    tool = request.form['tool']
    value = int(request.form['value'])
    try:
        data = IssuanceOfATool.query.filter_by(id=id).first()

        data_tool = Tool.query.filter_by(name=tool).first()

        value_issuance_of_a_tool = data.value
        value_tool = data_tool.value

        value_issuance_of_a_tool += value_tool
        value_tool = value
        value_issuance_of_a_tool -= value_tool

        if value_issuance_of_a_tool >= 0:
            data.value = value_tool
            data_tool.value = value_issuance_of_a_tool
            data.worker = worker
            data.tool = tool

        db.session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


@app.route('/update_workers', methods=['POST'])
def update_workers():
    id = request.form['id']
    worker = request.form['worker']
    room = request.form['room']

    try:
        data = Workers.query.filter_by(id=id).first()

        data.worker = worker
        data.room = room

        db.session.commit()
        return 'Ok', 200
    except Exception as e:
        return f'Error: {e}', 404


# ================================================================= #
# UPDATE

@app.route('/excel', methods=['GET'])
def excel():
    row = []

    data = Tool.query.all()
    result = [{'id': i.id, 'main': i.main,
               'subcategory': i.subcategory,
               'name': i.name, 'value': i.value,
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    for i in result:
        info = (i['id'], i['main'], i['subcategory'],
                i['name'], i['value'], i['date'])
        row.append(info)
    df1 = pd.DataFrame(row, columns=[
        'id', 'Основаная категория',
        'Доп. категория', 'Наименование',
        'Кол-во', 'Дата'])
    row = []

    data = IssuanceOfATool.query.all()
    result = [{'id': i.id, 'worker': i.worker, 'tool': i.tool,
               'value': i.value,
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    for i in result:
        info = (i['id'], i['worker'], i['tool'],
                i['value'], i['date'])
        row.append(info)
    df2 = pd.DataFrame(row, columns=[
        'id', 'Работник',
        'Инструмент',
        'Кол-во', 'Дата'])
    row = []

    data = Delete_data.query.all()
    result = [{'id': i.id,
               'data_one': i.data_one,
               'data_two': i.data_two, 'data_three': i.data_three,
               'data_date': i.data_date.strftime('%H:%M:%S %d-%m-%Y'),
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    for i in result:
        info = (i['id'], i['data_one'], i['data_two'],
                i['data_three'], i['data_date'], i['date'])
        row.append(info)
    df3 = pd.DataFrame(row, columns=[
        'id', 'Работник',
        'Инструмент',
        'Кол-во', 'Дата создания',
        'Дата удаления'])
    row = []

    data = Workers.query.all()
    result = [{'id': i.id,
               'worker': i.worker,
               'room': i.room,
               'date': i.date.strftime('%H:%M:%S %d-%m-%Y')} for i in data]
    for i in result:
        info = (i['id'], i['worker'], i['room'], i['date'])
        row.append(info)
    df4 = pd.DataFrame(row, columns=[
        'id', 'Работник',
        'Цех',
        'Дата'])
    row = []

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='Инструмент', index=False)
        df2.to_excel(writer, sheet_name='Выдача инст.', index=False)
        df3.to_excel(writer, sheet_name='История выдачи', index=False)
        df4.to_excel(writer, sheet_name='Работники', index=False)

    output.seek(0)

    return send_file(
        output, as_attachment=True,
        mimetype='application/vnd.openxmlformats-\
officedocument.spreadsheetml.sheet',
        download_name='excel.xlsx'), 200


if __name__ == '__main__':
    from waitress import serve
    serve(app)
