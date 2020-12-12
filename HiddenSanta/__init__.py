from flask import Flask, request, render_template, abort
import uuid
import random
app = Flask(__name__)

names = ['Николая М.', 'Натальи', 'Ивана',
         'Алины', 'Артёма', 'Коли Р.', 'Марии']
links = {}
for i in range(len(names)):
    links[str(uuid.uuid4())] = names.pop(random.randint(0, len(names)-1))

print(links)

@app.route('/')
def hello():
    return 'Its Hidden Santa!'

@app.route('/links')
def return_links():
    html_links = ""
    for i, link in enumerate(links.items()):
        html_links += '<a href="%s%s" target="_blank">%d</a><br>' % (
            request.host_url, link[0], i+1)
    return html_links


@app.route('/<uuid>')
def index(uuid):
    if links.get(uuid, True):
        abort(404)
    return render_template('santa.html', name=links[uuid])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
