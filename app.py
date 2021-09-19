from flask import Flask, request, render_template
import socket

app = Flask(__name__)

def printSomething(text):
    print(text)

@app.route("/", methods=['POST', 'GET'])
def index():
    data = {'message': None,'myIP': None}
    data['message'] = None
    try:
        data['myIP'] = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    except Exception:
        data['myIP'] = "Can't find an IP"
    
    if request.method == 'POST':
        if request.form.get('action1') == 'Do Something':
            data['message'] = 'first button pushed'
        if request.form.get('action2') == 'Do Something Else':
            data['message'] = 'second button pushed'
        return render_template('index.html', data=data)
    # print('Hi')
    # if request.method == 'POST':
    #     print('YYY')
    #     if request.form.get('action1') == 'Do+Something':
    #         pass # do something
    #         return printSomething('Button 1')
    #     elif  request.form.get('action2') == 'Do+Something+Else':
    #         pass # do something else
    #         return printSomething('Button 2')
    #     else:
    #         pass # unknown
    #         return printSomething('WUT')
    elif request.method == 'GET':
        return render_template('index.html', data=data)

