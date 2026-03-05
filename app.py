from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/schedule-a-quote')
def quote():
    return render_template('schedule-quote.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

# Implement a event tab that updates with current giveaways and etc
if __name__ == '__main__':
    app.run()
