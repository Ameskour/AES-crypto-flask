from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from simple_aes_cipher import AESCipher, generate_secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret key you want'
Bootstrap(app)

class CryptoForm(FlaskForm):
    secret_key = StringField('Secret Key', validators=[DataRequired()])
    message = TextAreaField('Message')
    submit = SubmitField('Encrypt/Decrypt')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = CryptoForm()
    secret_key = ""
    message = ""
    if form.validate_on_submit():
        secret_key = generate_secret_key(form.secret_key.data)
        cipher = AESCipher(secret_key)
        try:
            message = cipher.decrypt(form.message.data)
        except ValueError:
            try:
                message = cipher.encrypt(form.message.data)
            except Exception:
                message = "Error: Invalid input."
        form.message.data = message
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
