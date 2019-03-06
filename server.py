from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import hashlib
import random
import requests
import time

app = Flask(__name__)
cors = CORS(app)


def translate_youdao(i):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Referer': 'http://fanyi.youdao.com/',
        'contentType': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    s = requests.Session()
    s.get('http://fanyi.youdao.com/')
    m = hashlib.md5()

    salt = str(int(time.time() * 1000) + random.randint(0, 9))
    n = 'fanyideskweb' + i + salt + "p09@Bn{h02_BIEe]$P^nG"
    m.update(n.encode('utf-8'))
    sign = m.hexdigest()
    data = {
        'i': i,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'doctype': 'json',
        'bv': '59a2ee1b62619c43589e27bb52c2517a',
        'version': "2.1",
        'keyfrom': "fanyi.web",
        'action': "FY_BY_DEFAULT",
        'typoResult': 'false'
    }
    resp = s.post(url, headers=headers, data=data)
    result = resp.json()
    translateResult = result['translateResult'][0]
    ret = ''
    for t in translateResult:
        ret += t['tgt']
    return ret


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/home')
def home():
    return app.send_static_file('home.html')


@app.route('/translate', methods=['POST'])
def translate():
    i = request.form['i']
    ret = translate_youdao(i)
    result = {
        'result': ret
    }
    return jsonify(result)


@app.route('/save', methods=['post'])
def save():
    text = request.form['text']
    fw = open('save.md', 'w', encoding='utf-8')
    fw.write(text)
    return jsonify({'success': 'true'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8081)
