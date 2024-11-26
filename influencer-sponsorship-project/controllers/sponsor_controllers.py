from flask import render_template, request, redirect, flash, session
from app import app, db
from models import *
from datetime import datetime


@app.route('/sponsor/signup', methods=['GET', 'POST'])
def sponsor_signup():
    return render_template('sponsor_signup.html')

@app.route('/sponsor/login', methods=['GET', 'POST'])
def sponsor_login():
    return render_template('sponsor_login.html')

@app.route('/sponsor', methods=['GET','POST'])
def sponsor():
    # Sign up form
    if request.method == 'POST' and request.form['submit'] == 'Register':
        sponsor_username = request.form['sponsor_username']
        sponsor = Sponsors.query.filter(Sponsors.sponsor_username == sponsor_username).all()
        count_usernames = len(sponsor)
        if count_usernames >= 1 : # username already exists
            flash("Username already exists. Please choose a different username", "warning")
            return redirect('/sponsor/signup')
        sponsor_name = request.form['sponsor_name']
        sponsor_industry = request.form['sponsor_industry']
        sponsor_budget = request.form['sponsor_budget']
        sponsor_password = request.form['sponsor_password']
        sponsor_confirm_password = request.form['sponsor_confirm_password']
        if sponsor_password != sponsor_confirm_password:
            flash('Passwords do not match. Please check and type the password again', 'warning')
            return redirect('/sponsor/signup')
        sponsor = Sponsors(sponsor_name=sponsor_name, sponsor_industry=sponsor_industry, sponsor_budget=sponsor_budget, sponsor_username=sponsor_username, sponsor_password=sponsor_password)
        db.session.add(sponsor)
        db.session.commit()
        flash('You have successfully signed up. Please login to continue.', 'success')
        return redirect('/sponsor/login')
    # Login form
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        sponsor_username = request.form['sponsor_username']
        sponsor_password = request.form['sponsor_password']
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        if sponsor:
            if sponsor.sponsor_password == sponsor_password:
                session['USERNAME'] = sponsor_username
                return redirect('/sponsor/' + sponsor_username + '/dashboard')
            else:
                flash('Your password is incorrect. Please try again.', 'danger')
                return redirect('/sponsor/login') # incorrect Password. Stays on the login page
        else:
            flash('Your Username is incorrect. Please try again.', 'danger')
            return redirect('/sponsor/login') # no user found with username
        
    else:
        flash('Invalid request. Action not allowed. Please Login/SignUp to continue.', 'danger')
        return redirect('/sponsor/login') # GET request

@app.route('/sponsor/<sponsor_username>/dashboard', methods=['GET', 'POST'])
def sponsor_dashboard(sponsor_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out', 'success')
            return redirect('/')
        flags = Flags.query.filter_by(flag_user=sponsor_username).first()
        if flags:
            session.pop('USERNAME')
            flash('Your account has been flagged. Please contact the admin for more details. You cannot Login', 'danger')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        adrequests = AdRequests.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
        return render_template('sponsor_dashboard.html', sponsor=sponsor, adrequests=adrequests)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    

@app.route('/sponsor/<sponsor_username>/campaigns', methods=['GET', 'POST'])
def sponsor_campaigns(sponsor_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        campaign = Campaigns.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
        return render_template('sponsor_campaigns.html', sponsor=sponsor, campaign=campaign)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')

@app.route('/sponsor/<sponsor_username>/campaigns/create_campaign', methods=['GET', 'POST'])
def create_campaigns(sponsor_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        if request.method=="GET":
            return render_template('create_campaigns.html', sponsor=sponsor)
        sponsor_id = sponsor.sponsor_id
        campaign_name = request.form['campaign_name']
        campaign_description = request.form['campaign_description']
        campaign_start_date = request.form['campaign_start_date']
        campaign_start_date = datetime.strptime(campaign_start_date, '%Y-%m-%d').date()
        campaign_end_date = request.form['campaign_end_date']
        campaign_end_date = datetime.strptime(campaign_end_date, '%Y-%m-%d').date()
        campaign_budget = request.form['campaign_budget']
        campaign_visibility = request.form['campaign_visibility']
        campaign_goals = request.form['campaign_goals']
        campaign = Campaigns(sponsor_id=sponsor_id, campaign_name=campaign_name, campaign_description=campaign_description, campaign_start_date=campaign_start_date, campaign_end_date=campaign_end_date, campaign_budget=campaign_budget, campaign_visibility=campaign_visibility, campaign_goals=campaign_goals)
        db.session.add(campaign)
        db.session.commit()
        flash('You have successfully created a campaign', 'success')
        return redirect('/sponsor/' + sponsor.sponsor_username + '/campaigns')
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    
@app.route('/sponsor/<sponsor_username>/find', methods=['GET', 'POST'])
def sponsor_find(sponsor_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        influencer = Influencers.query.all()
        return render_template('sponsor_find.html', sponsor=sponsor, influencer=influencer)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    

@app.route('/sponsor/<sponsor_username>/campaigns/<campaign_id>/edit', methods=['GET', 'POST'])
def edit_campaigns(sponsor_username, campaign_id):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()
        return render_template('edit_campaigns.html', sponsor=sponsor, campaign=campaign)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    
@app.route('/sponsor/<sponsor_username>/campaigns/<campaign_id>', methods=['GET', 'POST'])
def campaign_changes(sponsor_username, campaign_id):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()
        if request.method=="POST" and request.form['submit'] == "Edit":
            campaign.campaign_name = request.form['campaign_name']
            campaign.campaign_description = request.form['campaign_description']
            campaign_start_date = request.form['campaign_start_date']
            campaign.campaign_start_date = datetime.strptime(campaign_start_date, '%Y-%m-%d').date()
            campaign_end_date = request.form['campaign_end_date']
            campaign.campaign_end_date = datetime.strptime(campaign_end_date, '%Y-%m-%d').date()
            campaign.campaign_budget = request.form['campaign_budget']
            campaign.campaign_visibility = request.form['campaign_visibility']
            campaign.campaign_goals = request.form['campaign_goals']
            db.session.commit()
            flash('You have successfully edited the campaign.', 'success')
            return redirect('/sponsor/' + sponsor.sponsor_username + '/campaigns')
        if request.method=="POST" and request.form['submit'] == "Delete":
            db.session.delete(campaign)
            db.session.commit()
            flash('You have successfully deleted the campaign', 'success')
            return redirect('/sponsor/' + sponsor.sponsor_username + '/campaigns')
        if request.method=="POST" and request.form['submit'] == "Ad-Request":
            return "Ad-request works"
        # return render_template('sponsor_campaign_edit_adrequest.html', sponsor=sponsor, campaign=campaign)
        return "hi"
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    
@app.route('/sponsor/<sponsor_username>/campaigns/<campaign_id>/influencers', methods=['GET', 'POST'])
def select_influencer(sponsor_username, campaign_id):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
        campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()
        influencer = Influencers.query.all()
        return render_template('campaigns_viewinfluencers.html', sponsor=sponsor, campaign=campaign, influencer=influencer)
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')

@app.route('/sponsor/<sponsor_username>/campaigns/<campaign_id>/<influencer_id>', methods=['GET', 'POST'])
def ad_request_create(sponsor_username, campaign_id, influencer_id):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        if request.method=='GET': 
            sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
            campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()
            influencer = Influencers.query.filter_by(influencer_id=influencer_id).first()
            return render_template('sponsor_create_adrequest.html', sponsor=sponsor, campaign=campaign, influencer=influencer)
        if request.method=='POST' and request.form['submit'] == 'Create Ad-request':
            sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
            campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()
            influencer = Influencers.query.filter_by(influencer_id=influencer_id).first()
            ad_messages = request.form['ad_messages']
            ad_requirements = request.form['ad_requirements']
            ad_payment_amount = request.form['ad_payment_amount']
            ad_status = 'Pending'
            request_last_modified_by = sponsor.sponsor_name
            adrequest = AdRequests(sponsor_id=sponsor.sponsor_id, campaign_id=campaign.campaign_id, influencer_id=influencer.influencer_id, ad_messages=ad_messages, ad_requirements=ad_requirements, ad_payment_amount=ad_payment_amount, ad_status=ad_status, request_last_modified_by=request_last_modified_by)
            db.session.add(adrequest)
            db.session.commit()
            adrequests = AdRequests.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
            flash('You have successfully created an Ad-request. You can view them here in dashboard', 'success')
            return render_template('sponsor_dashboard.html',sponsor=sponsor, campaign=campaign, influencer=influencer ,adrequests=adrequests)
        if request.method == 'POST' and request.form['submit'] == 'Accept':
            request_id = request.form['request_id']
            sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
            influencer = Influencers.query.filter_by(influencer_id=influencer_id).first()
            adrequests = AdRequests.query.filter_by(request_id=request_id).first()
            adrequests.ad_status = "Accepted"
            db.session.commit()
            flash('You have successfully accepted the Ad Request', 'success')
            adrequests = AdRequests.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
            return render_template('sponsor_dashboard.html', sponsor=sponsor, adrequests=adrequests)
        if request.method == 'POST' and request.form['submit'] == 'Reject':
            request_id = request.form['request_id']
            sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
            influencer = Influencers.query.filter_by(influencer_id=influencer_id).first()
            adrequests = AdRequests.query.filter_by(request_id=request_id).first()
            adrequests.ad_status = "Rejected"
            db.session.commit()
            flash('You have successfully rejected the Ad Request', 'success')
            adrequests = AdRequests.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
            return render_template('sponsor_dashboard.html', sponsor=sponsor, adrequests=adrequests)
        # Redirect to edit the ad request
        if request.method == 'POST' and request.form['submit'] == 'Re-Negotiate':
            request_id = request.form['request_id']
            adrequests = AdRequests.query.filter_by(request_id=request_id).first()
            return render_template('sponsor_negotiate.html', adrequest=adrequests, request_id=request_id)
        # Process edited request
        if request.method == "POST" and request.form['submit'] =="Re-Negotiate Request":
            request_id = request.form['request_id']
            sponsor = Sponsors.query.filter_by(sponsor_username=sponsor_username).first()
            adrequests = AdRequests.query.filter_by(request_id=request_id).first()
            adrequests.ad_payment_amount = request.form['ad_payment_amount']
            adrequests.request_last_modified_by = sponsor.sponsor_name
            adrequests.ad_status = "Re-Negotiating"
            adrequests.ad_messages = request.form['ad_messages']
            adrequests.ad_requirements = request.form['ad_requirements']
            db.session.commit()
            flash('You have re-negotiated the adrequest. Please wait for a response', 'success')
            adrequests = AdRequests.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
            return render_template('sponsor_dashboard.html', sponsor=sponsor, adrequests=adrequests)
            
            
            
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    
    
@app.route('/sponsor/<sponsor_username>/flag/<influencer_username>', methods=['GET', 'POST'])
def flag_influencer(sponsor_username, influencer_username):
    if session.get("USERNAME", None) is not None:
        if session['USERNAME'] != sponsor_username:
            flash("You are not authorized to view this page. Please Login with your account or signup", "danger")
            return redirect('/sponsor/login')
        if request.method=="POST" and request.form['submit'] == 'Logout':
            session.pop('USERNAME') # remove the username from the session
            flash('You have successfully logged out. Thank you for using our services.', 'success')
            return redirect('/')
        if request.method == 'POST' and request.form['submit'] == 'Flag Influencer':
            flag = Flags.query.filter_by(flag_user=influencer_username, flag_created_by=sponsor_username).all()
            count_reports = len(flag)
            if count_reports >= 1:
                flash("You have already flagged this influencer. Admin will look into it. Please don't spam flag the influencer.", 'danger')
                return redirect('/sponsor/' + sponsor_username + '/find')
            flags = Flags(flag_user=influencer_username, flag_user_type="Influencer", flag_created_by=sponsor_username, flag_status="Pending")
            db.session.add(flags)
            db.session.commit()
            flash('Thank you for flagging the influencer. Admin will look into it', 'success')
            return redirect('/sponsor/' + sponsor_username + '/find')
    else:
        flash("You need to Login to continue", "info")
        return redirect('/sponsor/login')
    