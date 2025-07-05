from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
# @app.route('/services')
# def service():
#     return render_template('services.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)





