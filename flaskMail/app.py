from flask import Flask, render_template, request, flash, redirect,url_for
from flask_mail import Mail, Message

app = Flask(__name__)
# mail = Mail(app)
app.config['SECRET_KEY'] = 'secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hidden4508@gmail.com'
app.config['MAIL_PASSWORD'] = 'arhuqxlfetypdovl'
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app)





@app.route('/',methods=['GET','POST'])
def home():  # put application's code here

    if request.method == 'POST':
        subject = request.form.get('subject')
        recipient = request.form.get('recipient')
        body = request.form.get('body')
        msg = Message(
            subject,
            sender='bookShop@gmail.com',
            recipients=[recipient]
        )
        msg.body = body
        mail.send(msg)
        flash(f"Message Sent", "success")
        return redirect(url_for('home'))

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
