from flask import render_template, request, redirect, flash, session
from app import app, db
from models import *


@app.route('/influencer/signup', methods=['GET', 'POST'])
def influencer_signup():
    return render_template('influencer/influencer_signup.html')


@app.route('/influencer/login', methods=['GET', 'POST'])
def influencer_login():
    return render_template('/influencer/influencer_login.html')

@app.route('/influencer', methods=['GET','POST'])
def influencer():
    # Sign up form
    if request.method == 'POST' and request.form['submit'] == 'Register':
        influencer_username = request.form['influencer_username']
        influencer = Influencers.query.filter(Influencers.influencer_username == influencer_username).all()
        count_usernames = len(influencer)
        if count_usernames >= 1 : # username already exists
            flash("Username already exists. Please choose a different username", "warning")
            return redirect('/influencer/signup')
        influencer_name = request.form['influencer_name']
        influencer_category = request.form['influencer_category']
        influencer_niche = request.form['influencer_niche']
        influencer_reach = request.form['influencer_reach']
        influencer_password = request.form['influencer_password']
        influencer_confirm_password = request.form['influencer_confirm_password']
        if influencer_password != influencer_confirm_password:
            flash('Passwords do not match. Please check and type the password again', 'warning')
            return redirect('/influencer/signup')
        influencer = Influencers(influencer_name=influencer_name, influencer_category=influencer_category, influencer_niche=influencer_niche, influencer_reach=influencer_reach, influencer_username=influencer_username, influencer_password=influencer_password)
        db.session.add(influencer)
        db.session.commit()
        flash('You have successfully signed up. Please login to continue.', 'success')
        return redirect('/influencer/login')
    # Login form
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        influencer_username = request.form['influencer_username']
        influencer_password = request.form['influencer_password']
        influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
        if influencer:
            if influencer.influencer_password == influencer_password:
                session['USERNAME'] = influencer_username
                return redirect('/influencer/' + influencer_username + '/dashboard')
            else:
                flash('Your password is incorrect. Please try again.', 'danger')
                return redirect('/influencer/login') # incorrect Password. Stays on the login page
        else:
            flash('Your Username is incorrect. Please try again.', 'danger')
            return redirect('/influencer/login') # no user found with username
        
    else:
        flash('Invalid request. Action not allowed. Please Login/SignUp to continue.', 'danger')
        return redirect('/influencer/login') # GET request
    
@app.route('/influencer/<influencer_username>/dashboard', methods=['GET', 'POST'])
def influencer_dashboard(influencer_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != influencer_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/influencer/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        if request.method == 'POST' and request.form['submit'] == 'Accept':
            request_id = request.form['request_id']
            influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
            adrequests = AdRequests.query.filter_by(request_id=request_id).first()
            adrequests.ad_status = "Accepted"
            db.session.commit()
            flash('You have successfully accepted the Ad Request', 'success')
            adrequests = AdRequests.query.filter_by(influencer_id=influencer.influencer_id).all()
            return render_template('/influencer/influencer_dashboard.html', influencer=influencer, adrequests=adrequests)
        if request.method == 'POST' and request.form['submit'] == 'Reject':
            request_id = request.form['request_id']
            influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
            adrequests = AdRequests.query.filter_by(request_id=request_id).first()
            adrequests.ad_status = "Rejected"
            db.session.commit()
            flash('You have successfully rejected the Ad Request', 'success')
            adrequests = AdRequests.query.filter_by(influencer_id=influencer.influencer_id).all()
            return render_template('/influencer/influencer_dashboard.html', influencer=influencer, adrequests=adrequests)
        
        if request.method == 'POST' and request.form['submit'] == 'Negotiate Payment':
            request_id = request.form['request_id']
            influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
            adrequest = AdRequests.query.filter_by(request_id=request_id).first()
            x = adrequest.ad_payment_amount
            if x==float(request.form['ad_payment_amount']):
                flash("You haven't changed any payment amount to negotiate. The old ad request still remains the same", 'danger')
                adrequests = AdRequests.query.filter_by(influencer_id=influencer.influencer_id).all()
                return render_template('/influencer/influencer_dashboard.html', influencer=influencer, adrequests=adrequests)
            else:
                adrequest.ad_payment_amount = request.form['ad_payment_amount']
                adrequest.request_last_modified_by = influencer.influencer_name
                adrequest.ad_status = "Negotiating"
                db.session.commit()
                flash('Your request for negotiating the ad payment amount has been sent. You can check its status in the dashboard.', 'success')
                adrequests = AdRequests.query.filter_by(influencer_id=influencer.influencer_id).all()
                return render_template('/influencer/influencer_dashboard.html', influencer=influencer, adrequests=adrequests)
                
        flags = Flags.query.filter_by(flag_user=influencer_username).first()
        if flags:
            session.pop('USERNAME')
            flash('Your account has been flagged. Please contact the admin for more details. You cannot Login', 'danger')
            return redirect('/')
        influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
        adrequests = AdRequests.query.filter_by(influencer_id=influencer.influencer_id).all()
        return render_template('influencer/influencer_dashboard.html', influencer=influencer, adrequests=adrequests)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/influencer/login')
    
@app.route('/influencer/<influencer_username>/find', methods=['GET', 'POST'])
def influencer_find(influencer_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != influencer_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/influencer/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
        campaign_public = Campaigns.query.filter_by(campaign_visibility="Public").all()
        return render_template('influencer/influencer_find.html', influencer=influencer, campaign_public=campaign_public)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/influencer/login')
    
    
@app.route('/influencer/<influencer_username>/negotiate', methods=['GET', 'POST'])
def influencer_negotiate(influencer_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != influencer_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/influencer/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME')
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        if request.method=="POST" and request.form['submit'] == 'Negotiate':
            influencer = Influencers.query.filter_by(influencer_username=influencer_username).first()
            request_id = request.form['request_id']
            adrequest = AdRequests.query.filter_by(request_id=request_id).first()
            return render_template('influencer/influencer_negotiate.html', influencer=influencer, adrequest=adrequest)
        # return redirect('/influencer/' + influencer_username + '/dashboard')
    
    
    else:
        flash("You need to Login to continue", "info")
        return redirect('/influencer/login')
    
@app.route('/influencer/<influencer_username>/flag/<sponsor_username>', methods=['GET', 'POST'])
def flag_sponsor(sponsor_username, influencer_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != influencer_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/influencer/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        if request.method == 'POST' and request.form['submit'] == 'Flag Inappropriate':
            flag = Flags.query.filter_by(flag_user=sponsor_username, flag_created_by=influencer_username).all()
            count_reports = len(flag)
            if count_reports >= 1:
                flash("You have already flagged this sponsor. Admin will look into it. Please don't spam flag the sponsor.", 'danger')
                return redirect('/influencer/' + influencer_username + '/find')
            flags = Flags(flag_user=sponsor_username, flag_user_type="Sponsor", flag_created_by=influencer_username, flag_status="Pending")
            db.session.add(flags)
            db.session.commit()
            flash('Thank you for flagging the sponsor. Admin will look into it', 'success')
            return redirect('/influencer/' + influencer_username + '/find')
    else:
        flash("You need to Login to continue", "info")
        return redirect('/influencer/login')