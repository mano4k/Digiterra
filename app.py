from flask import Flask, render_template, request, redirect, flash, url_for
from email.message import EmailMessage
import os, ssl, smtplib, re, html

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/services')
def service():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# @app.route('/propos')
# def contact():
#     return render_template('propos.html')

@app.route('/base', methods=["GET", "POST"]) 
def gestion_mail():
    
    if request.method == "POST":
        nom= request.form.get("nom","").strip()
        email= request.form.get("courriel","").strip()
        message= request.form.get("message","").strip()
        
        subject  = f"[Contact] Nouveau message de {nom}"
        body_txt = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}\n"
        body_html = (
            f"<h3>Nouveau message de {html.escape(nom)}</h3>"### protrion contre les injection xss
            f"<p><b>Email :</b> {html.escape(email)}</p>"
            f"<p><b>Message :</b><br>{html.escape(message).replace('\n','<br>')}</p>"
        )
        
        try:
            envoi_mail(subject, body_txt, body_html, os.environ["ADMIN_EMAIL"],reply_to=email)
            print("Merci ! Votre message a été envoyé.", "success")
        except Exception as e:
            print("Erreur SMTP:", e)
        
        # print(message)
        # flash("message envoye avec succes")
        return "succes"
    
    return render_template("service.html")

@app.route('/vente')
def vente():
    return render_template('vente.html')

def envoi_mail(subject, body_txt, body_html, to_email, reply_to=None):
    server = os.environ["MAIL_SERVER"]
    port   = int(os.environ.get("MAIL_PORT", 587))
    user   = os.environ["MAIL_USERNAME"]
    pwd    = os.environ["MAIL_PASSWORD"]
    sender = os.environ["MAIL_DEFAULT_SENDER"]
    secret_key=os.environ["SECRET_KEY"]

    par_ssl = os.environ.get("MAIL_USE_SSL", "False") == "True"
    par_tls = os.environ.get("MAIL_USE_TLS", "True") == "True"
    
    messag=EmailMessage()
    messag["subject"]=subject
    messag["FROM"]=sender
    messag["TO"]=to_email
    
    if reply_to:
        messag["Reply-To"] = reply_to   
    messag.set_content(body_txt)
    messag.add_alternative(body_html, subtype="html")
    
    if par_ssl:
        with smtplib.SMTP_SSL(server, port, context=ssl.create_default_context()) as s:
            s.login(user, pwd)
            s.send_message(messag)
    else:
        with smtplib.SMTP(server, port) as s:
            if par_tls:
                s.starttls(context=ssl.create_default_context())
            s.login(user, pwd)
            s.send_message(messag)
if __name__ == '__main__':
    app.run(debug=True)





