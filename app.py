from flask import Flask, request, render_template
from flask import redirect, url_for

from PIL import Image
from inspect import currentframe

import io
import simplejson as json
import qrcode

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.method != 'GET':
        return 'Error'
    return render_template('index.html', name='something')


@app.route('/generate', methods=['POST'])
def post_qr():
    if request.method != 'POST':
        return 'Error'
    if request.form['qr-text']:
        try:
            img = qrcode.make(request.form['qr-text'])
            img_io = io.BytesIO()
            img.save(img_io, format='PNG', quality=100)
            img = img_io.decode('utf-8')
            return render_template('code.html', img=img_io)
        except Exception as Ex:
            print(f'[PythonError en linea: {currentframe().f_lineno}] - [{type(Ex)}-ErrorMessage: {Ex}] - [ErrorArgs: {Ex.args}]')
            return 'Error'


# API
@app.route('/qr/api/v1/post', methods=['POST'])
def main():
    try:
        if request.method == 'POST' and request.args.get('text'):
            try:
                img = qrcode.make(request.args.get('text'))
                try:
                    img_byte_array = io.BytesIO()
                    img.save(img_byte_array, format='JPEG')
                    img_byte_array = img_byte_array.getvalue()
                except Exception as PythonError:
                    print(f'[PythonError en linea: {currentframe().f_lineno}] - [{type(PythonError)}-ErrorMessage: {PythonError}] - [ErrorArgs: {PythonError.args}]')
                    img_byte_array = img 
            except Exception as PythonError:
                print(f'[PythonError en linea: {currentframe().f_lineno}] - [{type(PythonError)}-ErrorMessage: {PythonError}] - [ErrorArgs: {PythonError.args}]')
                return json.dumps({
                    'status': 'failed',
                    'message': 'There has been an error processing your request'
                    })
        else:
            print(f'PythonError en linea: {currentframe().f_lineno}')
            return json.dumps({
                'status': 'failed',
                'message': 'Sorry, you must provide the "text" parameter in order to process the request'
                })
        return json.dumps({
            'status': 'success',
            'message': 'Your request has been processed successfully',
            # TODO: Arreglar este return, no me deja encodear a utf-8
            'image': img_byte_array
            })
    except Exception as PythonError:
        print(f'[PythonError en linea: {currentframe().f_lineno}] - [{type(PythonError)}-ErrorMessage: {PythonError}] - [ErrorArgs: {PythonError.args}]')
        return json.dumps({
            'status': 'failed',
            'message': 'There has been an error processing your request'
            })


@app.route('/')
def base():
    return 'Sorry, the url you are requesting is not available'

@app.route('/qr')
def redirect_urls():
    return redirect(url_for('base'))