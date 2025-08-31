from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import AppInfo, PushHistory
from . import db
from .fetcher import fetch_rss
from .filter import filter_apps
from .pusher import push_to_telegram
import yaml
import os

bp = Blueprint("main", __name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def get_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@bp.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "")
    apps_query = AppInfo.query.order_by(AppInfo.created_at.desc())
    if q:
        apps_query = apps_query.filter(AppInfo.title.contains(q))
    apps = apps_query.limit(50).all()
    return render_template("index.html", apps=apps, query=q)

@bp.route("/fetch", methods=["POST"])
def fetch():
    cfg = get_config()
    rss_url = cfg["rss_url"]
    keywords = cfg.get("filter", {}).get("keywords", [])
    exclude_keywords = cfg.get("filter", {}).get("exclude_keywords", [])
    apps = fetch_rss(rss_url)
    apps = filter_apps(apps, keywords, exclude_keywords)
    cnt = 0
    for app in apps:
        exists = AppInfo.query.filter_by(link=app["link"]).first()
        if not exists:
            db.session.add(AppInfo(**app))
            cnt += 1
    db.session.commit()
    flash(f"抓取并入库 {cnt} 个新App")
    return redirect(url_for("main.index"))

@bp.route("/push/<int:app_id>", methods=["GET"])
def push(app_id):
    cfg = get_config()
    tg_cfg = cfg.get("telegram", {})
    app = AppInfo.query.get_or_404(app_id)
    if not app.pushed:
        ok = push_to_telegram(app, tg_cfg["bot_token"], tg_cfg["chat_id"])
        if ok:
            app.pushed = True
            db.session.add(PushHistory(app_id=app.id, channel="telegram"))
            db.session.commit()
            flash("推送成功")
        else:
            flash("推送失败")
    else:
        flash("已推送过")
    return redirect(url_for("main.index"))

@bp.route("/del/<int:app_id>", methods=["GET"])
def delete(app_id):
    app = AppInfo.query.get_or_404(app_id)
    db.session.delete(app)
    db.session.commit()
    flash("已删除该App")
    return redirect(url_for("main.index"))