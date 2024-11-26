from flask import render_template, request, redirect, flash, session
from app import app
from models import *




@app.route('/admin', methods=['GET','POST'])
def admin():
    # Login form
    if request.method == 'POST' and request.form['submit'] == 'Login':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        admin = Admins.query.filter_by(admin_username=admin_username).first()
        if admin:
            if admin.admin_password == admin_password:
                session['USERNAME'] = admin_username
                return redirect('/admin/' + admin_username + '/dashboard')
            else:
                flash('Your password is incorrect. Please try again.', 'danger')
                return redirect('/admin') # incorrect Password. Stays on the login page
        else:
            flash('Your Username is incorrect. Please try again.', 'danger')
            return redirect('/admin') # no user found with username
    else:

        return render_template('admin/admin_login.html') # GET request
    
@app.route('/admin/<admin_username>/dashboard', methods=['GET', 'POST'])
def admin_dashboard(admin_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != admin_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/admin')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        if request.method=='POST' and request.form['submit'] == 'Accept':
            flag_id = request.form['flag_id']
            flag = Flags.query.filter_by(flag_id=flag_id).first()
            flag.flag_status = 'Accepted'
            db.session.commit()
            flash('User Flagged successfully', 'success')
            return redirect('/admin/' + admin_username + '/dashboard')
        if request.method=='POST' and request.form['submit'] == 'Reject':
            flag_id = request.form['flag_id']
            flag = Flags.query.filter_by(flag_id=flag_id).first()
            flag.flag_status = 'Rejected'
            db.session.commit()
            flash('User is not Flagged', 'success')
            return redirect('/admin/' + admin_username + '/dashboard')
        
        admin = Admins.query.filter_by(admin_username=admin_username).first()
        flags = Flags.query.all()
        return render_template('admin/admin_dashboard.html', admin=admin, flags=flags)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/admin')
    
    
@app.route('/admin/<admin_username>/sponsors', methods=['GET', 'POST'])
def admin_sponsors(admin_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != admin_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/admin')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        
        admin = Admins.query.filter_by(admin_username=admin_username).first()
        sponsors = Sponsors.query.all()
        return render_template('admin/admin_sponsors.html', admin=admin, sponsors=sponsors)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/admin')
    
@app.route('/admin/<admin_username>/influencers', methods=['GET', 'POST'])
def admin_influencers(admin_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != admin_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/admin')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        influencers = Influencers.query.all()
        admin = Admins.query.filter_by(admin_username=admin_username).first()
        return render_template('admin/admin_influencers.html', admin=admin, influencers=influencers)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/admin')
    
@app.route('/admin/<admin_username>/campaigns', methods=['GET', 'POST'])
def admin_campaigns(admin_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != admin_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/admin')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        campaigns = Campaigns.query.all()
        admin = Admins.query.filter_by(admin_username=admin_username).first()
        return render_template('admin/admin_campaigns.html', admin=admin, campaigns=campaigns)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/admin')
    
@app.route('/admin/<admin_username>/adrequests', methods=['GET', 'POST'])
def admin_adrequests(admin_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != admin_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/admin')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        adrequests = AdRequests.query.all()
        admin = Admins.query.filter_by(admin_username=admin_username).first()
        return render_template('admin/admin_adrequests.html', admin=admin, adrequests=adrequests)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/admin')