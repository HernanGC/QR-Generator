from flask import Flask, request
from flask import redirect, url_for

from PIL import Image
from inspect import currentframe

import io
import simplejson as json
import qrcode

app = Flask(__name__)


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