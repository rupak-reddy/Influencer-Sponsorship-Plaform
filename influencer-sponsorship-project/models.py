from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admins(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String, nullable=False)
    admin_username = db.Column(db.String, nullable=False, unique=True)
    admin_password = db.Column(db.String, nullable=False)

class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    sponsor_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    sponsor_name = db.Column(db.String, nullable=False)
    sponsor_industry = db.Column(db.String, nullable=False)
    sponsor_budget = db.Column(db.Float, nullable=False)
    sponsor_username = db.Column(db.String, nullable=False, unique=True)
    sponsor_password = db.Column(db.String, nullable=False)
    campaigns = db.relationship('Campaigns', backref='sponsors', lazy=True)
    campaign_adrequests = db.relationship('AdRequests', backref='sponsors', lazy=True)
    
class Influencers(db.Model):
    __tablename__ = 'influencers'
    influencer_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    influencer_name = db.Column(db.String, nullable=False)
    influencer_category = db.Column(db.String, nullable=False)
    influencer_niche = db.Column(db.String, nullable=False)
    influencer_reach = db.Column(db.Float, nullable=False)
    influencer_username = db.Column(db.String, nullable=False, unique=True)
    influencer_password = db.Column(db.String, nullable=False)
    influencer_adrequests = db.relationship('AdRequests', backref='influencers', lazy=True)
    
class Campaigns(db.Model):
    __tablename__ = 'campaigns'
    campaign_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.sponsor_id'), nullable=False)
    campaign_name = db.Column(db.String, nullable=False)
    campaign_description = db.Column(db.Text, nullable=False)
    campaign_start_date = db.Column(db.Date, nullable=False)
    campaign_end_date = db.Column(db.Date, nullable=False)
    campaign_budget = db.Column(db.Float, nullable=False)
    campaign_visibility = db.Column(db.String, nullable=False)
    campaign_goals = db.Column(db.Text, nullable=False)
    campaign_adrequests = db.relationship('AdRequests', backref='campaigns', lazy=True)
    
class AdRequests(db.Model):
    __tablename__ = 'ad_requests'
    request_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.sponsor_id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.influencer_id'), nullable=False)
    ad_messages = db.Column(db.Text, nullable=False)
    ad_requirements = db.Column(db.Text, nullable=False)
    ad_payment_amount = db.Column(db.Float, nullable=False)
    ad_status = db.Column(db.String, nullable=False)
    request_last_modified_by = db.Column(db.String, nullable=False)
    

class Flags(db.Model):
    __tablename__ = 'flags'
    flag_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    flag_user = db.Column(db.String, nullable=False)
    flag_user_type = db.Column(db.String, nullable=False)
    flag_created_by = db.Column(db.String, nullable=False)
    flag_status = db.Column(db.String, nullable=False)
    