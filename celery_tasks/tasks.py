from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import loader, RequestContext
import os
import time

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_dailyfresh_project.settings")
django.setup()

from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection

app = Celery("celery_tasks.tasks", broker="redis://127.0.0.1:6379/1")


@app.task
def send_register_active_email(to_email, username, token):
    """define task func"""
    subject = "Welcome to Dailyfresh!"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = (
        "<h1>Hi %s, thank you for registering.<h1>"
        "Please click the following link to activate your Dailyfresh account.<br/>"
        '<a href="http://127.0.0.1:8000/user/active/%s">'
        "http://127.0.0.1:8000/user/active/%s</a>" % (username, token, token)
    )
    send_mail(subject,message=message,from_email=sender,recipient_list=receiver,html_message=html_message)
    time.sleep(5)


@app.task
def generate_static_index_html():

    types = GoodsType.objects.all()
    goods_banners = IndexGoodsBanner.objects.all().order_by("index")
    promotion_banners = IndexPromotionBanner.objects.all().order_by("index")

    for type in types:
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by("index")
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by("index")
        type.image_banners = image_banners
        type.title_banners = title_banners

    context = {
        "types": types,
        "goods_banners": goods_banners,
        "promotion_banners": promotion_banners,
    }

    temp = loader.get_template("static_index.html")
    static_index_html = temp.render(context)
    save_path = os.path.join(settings.BASE_DIR, "static\\index.html")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(static_index_html)
