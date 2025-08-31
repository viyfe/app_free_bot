from . import db
from datetime import datetime

class AppInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.Text)
    link = db.Column(db.String(300))
    src = db.Column(db.String(50))
    pushed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PushHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('app_info.id'))
    channel = db.Column(db.String(50))
    pushed_at = db.Column(db.DateTime, default=datetime.utcnow)
