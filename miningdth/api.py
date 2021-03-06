#!flask/bin/python

from flask import Flask, jsonify
from modules.mining import Mining
from modules.IR import IR
from datetime import date

app = Flask(__name__)

json_cache = {}


def get_json(year, month, day):
    ir = IR().getInfo(date(year, month, day))
    lst = Mining(ir).build()
    lstdict = [{'word': a[0], 'value':a[1]} for a in lst]
    return {'dict': lstdict}


@app.route('/api/miningDTH/v1.0/<int:year>/<int:month>/<int:day>',
           methods=['GET'])
def get_tasks(year, month, day):
    print('started')
    json = json_cache.get((year, month, day), None)
    if not json:
        json = get_json(year, month, day)
        json_cache[(year, month, day)] = json

    return jsonify(json)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)
