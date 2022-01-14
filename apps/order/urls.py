from django.urls import path
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView,CommentView

urlpatterns = [
    path("place", OrderPlaceView.as_view(), name="place"),
    path("commit", OrderCommitView.as_view(), name="commit"),
    path("pay", OrderPayView.as_view(), name="pay"),
    path("check", CheckPayView.as_view(), name="check"),
    path("comment/<int:order_id>", CommentView.as_view(), name="comment"),
]
