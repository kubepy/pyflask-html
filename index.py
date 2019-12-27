#!/bin/python
import flask
import subprocess
import time

app = flask.Flask(__name__, static_url_path='', static_folder='',)

@app.route('/')
def root():
    return app.send_static_file('static_web.html')

@app.route('/api/start/ansible')
def start():
    def inner():
        proc = subprocess.Popen(
            ['ansible-playbook -i inventory site.yml'],
            shell=True,
            stdout=subprocess.PIPE
        )

        for line in iter(proc.stdout.readline,''):
            time.sleep(0.1) 
            yield line.rstrip() + '<br/>\n'

    return flask.Response(inner(), mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
