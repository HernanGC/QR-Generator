from flask import Flask, request, render_template
from flask import redirect, url_for

from inspect import currentframe
from random import randrange

import os
import io
import simplejson as json
import qrcode
import qrcode.image.svg

app = Flask(__name__)

ERROR_MESSAGE = json.dumps({
    'status': 'failed',
    'message': 'There has been an error processing your request'
})


@app.route('/', methods=['GET'])
def index():
    if request.method != 'GET':
        return redirect(url_for('error_router'))
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def post_qr():
    if request.method != 'POST':
        return redirect(url_for('error_router'))
    if request.form['qr-text']:
        try:
            code_path = 'static/qr-image.svg'
            if os.path.exists(code_path):
                os.remove(code_path)
            factory = qrcode.image.svg.SvgImage
            img = qrcode.make(request.form['qr-text'], image_factory=factory, box_size=20)
            img_io = io.BytesIO()
            img.save(img_io)
            img = img_io.getvalue().decode()
            if not os.path.exists(code_path):
                with open(code_path, 'x') as img_file:
                    img_file.write(img)
            rand = randrange(99)
            return render_template('code.html', img=f'{code_path}?{rand}')
        except Exception as Ex:
            print(
                f'[PythonError en linea: {currentframe().f_lineno}] - [{type(Ex)}-ErrorMessage: {Ex}] - [ErrorArgs: {Ex.args}]')
            return redirect(url_for('error_router'))
    return redirect(url_for('error_router'))


@app.route('/error', methods=['GET', 'POST'])
def error_router(content='Sorry, there has been an error processing your request. Please, try again later.'):
    return render_template('4xx_error.html', message=content)


# API
@app.route('/qr/api/v1/post', methods=['POST'])
def main():
    try:
        if request.method == 'POST' and request.args.get('qr-text'):
            try:
                factory = qrcode.image.svg.SvgImage
                img = qrcode.make(request.args.get('qr-text'), image_factory=factory, box_size=20)
                try:
                    img_io = io.BytesIO()
                    img.save(img_io)
                    img = img_io.getvalue().decode()
                except Exception as PythonError:
                    print(
                        f'[PythonError en linea: {currentframe().f_lineno}] - [{type(PythonError)}-ErrorMessage: {PythonError}] - [ErrorArgs: {PythonError.args}]')
                    img = 'Failed'
            except Exception as PythonError:
                print(
                    f'[PythonError en linea: {currentframe().f_lineno}] - [{type(PythonError)}-ErrorMessage: {PythonError}] - [ErrorArgs: {PythonError.args}]')
                return ERROR_MESSAGE
        else:
            print(f'PythonError en linea: {currentframe().f_lineno}')
            return json.dumps({
                'status': 'failed',
                'message': 'Sorry, you must provide the "qr-text" parameter in order to process the request'
            })
        return json.dumps({
            'status': 'success',
            'message': 'Your request has been processed successfully',
            'format': 'svg',
            'image': img
        })
    except Exception as PythonError:
        print(
            f'[PythonError en linea: {currentframe().f_lineno}] - [{type(PythonError)}-ErrorMessage: {PythonError}] - [ErrorArgs: {PythonError.args}]')
        return ERROR_MESSAGE
