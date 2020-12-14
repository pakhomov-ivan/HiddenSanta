from flask import Flask, request, render_template, abort
import hashlib as hl
import uuid
import random
app = Flask(__name__)

names = ['Николая М.', 'Натальи', 'Ивана',
         'Алины', 'Артёма', 'Коли Р.', 'Марии']
links = {}
for i in range(len(names)):
    links[str(uuid.uuid4())] = names.pop(random.randint(0, len(names)-1))


logins_passwords = {
    'kolyam': {'literal_name': 'Коли М', 'whos_santa': '', 'password': 'd101e579f9c5031dbe2e2175bfe9498f'}, #1 c4ca4238a0b923820dcc509a6f75849b
    'natasha': {'literal_name': 'Наташи', 'whos_santa': '', 'password': 'e072e2d4ff6cf0ba4fd101bb787449c3'}, #2 c81e728d9d4c2f636f067f89cc14862c
    'ivan': {'literal_name': 'Ивана', 'whos_santa': '', 'password': 'b33da7a629e59c1170772e63e4dd13b4'}, #3 eccbc87e4b5ce2fe28308fd9f2a7baf3
    'alina': {'literal_name': 'Алины', 'whos_santa': '', 'password': '346df3075bcd56cb29d3c2c052ae260e'}, #4 a87ff679a2f3e71d9181a67b7542122c
    'artyom': {'literal_name': 'Артёма', 'whos_santa': '', 'password': 'e4da3b7fbbce2345d7772b0674a318d5'}, #5 e4da3b7fbbce2345d7772b0674a318d5
    'kolyar': {'literal_name': 'Коли Р', 'whos_santa': '', 'password': '53ca2bc739d6b415b4f434cbb3c5c3b5'}, #6 1679091c5a880faf6fb5e6087eb1b2dc
    'masha': {'literal_name': 'Маши', 'whos_santa': '', 'password': 'fee2539beb140d4a5008ca1ecec613ce'}, #7 8f14e45fceea167a5a36dedd4bea2543
}
# random.shuffle(logins_passwords)
lit_names = list(
    map(lambda item: item['literal_name'], logins_passwords.values()))
random.shuffle(lit_names)
for i, item in enumerate(logins_passwords.values()):
    if(item['literal_name'] == lit_names[i]):
        if(i + 1 < len(logins_passwords)):
            lit_names[i+1], lit_names[i] = lit_names[i], lit_names[i+1]
        else:
            lit_names[1], lit_names[i] = lit_names[i], lit_names[1]

for i, item in enumerate(logins_passwords.values()):
    item['whos_santa'] = lit_names[i]
print(logins_passwords)


@app.route('/santa/<name>', methods=['GET', 'POST'])
def your_santa(name):
    if logins_passwords.get(name, False):
        if request.method == 'GET':
            return render_template('santa_login.html')
        if request.method == 'POST':
            password = request.form.get('password')
            if logins_passwords[name]['password'] == hl.md5(password.encode()).hexdigest():
                return render_template('santa.html', name=logins_passwords[name]['whos_santa'])
            else:
                return render_template('santa_login.html')
    abort(404)


@app.route('/links')
def return_links():
    html_links = ""
    for i, link in enumerate(links.items()):
        html_links += '<a href="%s%s" target="_blank">%s%s</a><br>' % (
            request.host_url, link[0], request.host_url, link[0])
    return html_links


@app.route('/<uuid>')
def index(uuid):
    if links.get(uuid, False):
        return render_template('santa.html', name=links[uuid])
    abort(404)


@app.route('/')
def hello():
    return 'Its Hidden Santa!'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run()
