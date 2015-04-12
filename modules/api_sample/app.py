from flask import Flask, render_template, redirect, jsonify, request, json, session
import requests
app = Flask(__name__)


app.secret_key = 'why would I tell you my secret key?'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/_getjson", methods=['GET'])
def do_chart():
    date = request.args['date'].split('-')

    api_url = 'http://127.0.0.1:8888/api/miningDTH/v1.0/{year}/{month}/{day}'.format(
        year=int(date[0]), month=int(date[1]), day=int(date[2]))

    try:
        response = requests.get(api_url)
        if(response.status_code == 200):
            response = json.loads(response.text)
            apod_chart = {'name': 'apodchart', 'children': []}
            children = {'name': 'ch-apod', 'children': []}

            response = response['dict']
            elems = response[:10] + response[len(response) - 10:]

            for elem in elems:
                chart_elem = {
                    'name': 'elem-apod', 'children': [{
                        'name': elem['word'], 'size':elem['value']}]}
                children['children'].append(chart_elem)

            apod_chart['children'].append(children)

            return jsonify(apod_chart)
        else:
            return jsonify(results=[])
    except:
        return jsonify(results=[])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )
