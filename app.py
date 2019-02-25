from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

from aiida import load_dbenv
load_dbenv()

from aiida.orm import Group, JobCalculation, Computer
from aiida.orm.querybuilder import QueryBuilder


def get_computer_names():
    qb_computer_name = QueryBuilder(
    )  # Instantiating instance. One instance -> one query
    qb_computer_name.append(
        Computer,
        project=['id', 'name'],
    )
    tmp = qb_computer_name.dict()
    computer_dict = {}
    for computer in tmp:
        computer_dict[computer['computer_1']
                      ['id']] = computer['computer_1']['name']

    return computer_dict


def reformat_calc_list(result, computer_dict):
    calc_dict_list = []
    for calc in result:
        calc_dict = {
            'date': calc['ctime'].strftime("%Y-%m-%d"),
            'time': calc['ctime'].strftime("%H-%M-%S"),
            'state': calc['state'],
            'computer': computer_dict[calc['dbcomputer_id']],
            'pk': calc['id'],
            'code': calc['type'].split('.')[-3]
        }
        calc_dict_list.append(calc_dict)
    return calc_dict_list


def get_job_calc_data(computer_dict):
    all_job_calc_qb = QueryBuilder()
    all_job_calc_qb.append(
        JobCalculation,
        project=['type', 'id', 'ctime', 'state', 'dbcomputer_id'],
    )
    tmp = all_job_calc_qb.dict()
    result = [calc['JobCalculation_1'] for calc in tmp]
    return reformat_calc_list(result, computer_dict)


# @app.route('/')
# def index():
#    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    computer_dict = get_computer_names()
    calc_rows = get_job_calc_data(computer_dict)
    return render_template('dashboard.html', calc_rows=calc_rows)


if __name__ == '__main__':
    app.run(debug=True)

