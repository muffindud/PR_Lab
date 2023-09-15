from flask import Flask, request


# Create the application instance
app = Flask(__name__)


# Create a URL route in our application for "/yaass"
@app.route('/yaass')
def yaass():
    return {
        'message1': 'yaasss',
        'message2': 'queen',
        'message3': 'slay'
    }


# Create a URL route in our application for "/bread"
@app.route('/bread')
def bread():
    return 'butter'


# Create a URL route in our application for "/gimme"
# Also accept POST requests
@app.route('/gimme', methods=['GET', 'POST'])
def gimme():
    if request.method == 'GET':
        return {
            'message': 'No, you gimme the DATA'
        }
    elif request.method == 'POST':
        payload = request.json
        print(payload)
        return {
            'message': 'Thank you for the DATA'
        }


# Start the server
app.run()
