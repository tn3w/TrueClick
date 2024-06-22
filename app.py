from time import sleep
from flask import Flask, Response, send_file, render_template, jsonify, request
from trueclick import TrueClick

app = Flask(__name__)
trueclick = TrueClick(hardness = 2)

@app.route('/', methods = ['GET', 'POST'])
def index() -> Response:
    """
    Route for serving the index.html file.

    :return: The index.html file.
    """

    if request.method == 'POST':
        if not trueclick.is_trueclick_valid():
            return 'Error: Invalid captcha'

        return 'Captcha verified'

    return render_template('example.html')

@app.route('/create_trueclick_challenge', methods = ['POST'])
def create_trueclick_challenge() -> Response:
    """
    Route for creating a trueclick challenge.

    :return: A JSON object containing the trueclick challenge.
    """

    sleep(10)

    captcha_challenge = trueclick.generate_captcha('ai-dogs')

    return jsonify(
        {
            'status': 'ok',
            'error': None,
            'challenge': captcha_challenge,
            'dataset': 'ai-dogs'
        }
    )


@app.route('/verify_trueclick_challenge', methods = ['POST'])
def verify_trueclick_challenge() -> Response:
    """
    Route for verifying a trueclick challenge.

    :return: A JSON object containing the trueclick challenge.
    """

    if not request.is_json:
        return jsonify({'status': 'error', 'error': 'Invalid request'})
    data = request.get_json()

    captcha_id, captcha_token = data.get('id'), data.get('token')
    selected_indices = [int(digit) for digit in data.get('selected', '') if digit.isdigit()]

    if not captcha_id or not captcha_token or not selected_indices:
        return jsonify({'status': 'error', 'error': 'Invalid request'})

    is_verified = trueclick.verify_captcha(captcha_id, captcha_token, selected_indices)

    return jsonify(
        {
            'status': 'ok' if is_verified else 'error',
            'error': 'Invalid captcha' if not is_verified else None,
            'challenge': trueclick.generate_captcha('ai-dogs') if not is_verified else None,
            'dataset': 'ai-dogs'
        }
    )


@app.route('/trueclick.js')
def trueclick_js() -> Response:
    """
    Route for serving the trueclick.js file.

    :return: The trueclick.js file.
    """

    return send_file('ressources/trueclick.js')


if __name__ == '__main__':
    app.run()
