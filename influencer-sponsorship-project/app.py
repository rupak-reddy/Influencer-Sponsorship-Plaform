from flask import Flask, render_template, request, redirect, flash
from flask import session
from datetime import datetime
from flask_migrate import Migrate
from models import *

app = None

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.secret_key = 'super secret key'
db.init_app(app)

with app.app_context():
    db.session.commit()
# Route for home page
app.app_context().push()
migrate=Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

from controllers.sponsor_controllers import *
from controllers.influencer_controllers import *
from controllers.admin_controllers import *

if __name__ == '__main__':
    app.run(debug=True)
