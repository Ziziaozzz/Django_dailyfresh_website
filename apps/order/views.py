from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import View
from django_redis import get_redis_connection
from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from utils.mixin import LoginRequiredMixin
from datetime import datetime
from alipay import AliPay
import os

# OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView, CommentView

class OrderPlaceView(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        sku_ids = request.POST.getlist("sku_ids")

        if not sku_ids:
            return redirect(reverse("cart:show"))

        conn = get_redis_connection("default")
        cart_key = "cart_%d" % user.id

        skus = []
        total_count = 0
        total_price = 0
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            count = conn.hget(cart_key, sku_id)

            count = count.decode()

            amount = sku.price * int(count)
            sku.count = count
            sku.amount = amount
            skus.append(sku)
            total_count += int(count)
            total_price += amount

        transit_price = 10

        total_pay = total_price + transit_price

        addrs = Address.objects.filter(user=user)

        sku_ids = ",".join(sku_ids)
        context = {
            "skus": skus,
            "total_count": total_count,
            "total_price": total_price,
            "transit_price": transit_price,
            "total_pay": total_pay,
            "addrs": addrs,
            "sku_ids": sku_ids,
        }

        return render(request, "place_order.html", context)

class OrderCommitView(View):

    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"res": 0, "errmsg": "Please login"})

        addr_id = request.POST.get("addr_id")
        pay_method = request.POST.get("pay_method")
        sku_ids = request.POST.get("sku_ids")

        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({"res": 1, "errmsg": "Incomplete data"})

        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({"res": 2, "errmsg": "Payment method not supported"})

        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({"res": 3, "errmsg": "Address does not exist"})

        order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)

        transit_price = 10

        total_count = 0
        total_price = 0

        save_id = transaction.savepoint()
        try:
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price,
            )

            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id

            sku_ids = sku_ids.split(",")
            for sku_id in sku_ids:
                try:
                    sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                except:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({"res": 4, "errmsg": "The product does not exist"})

                count = conn.hget(cart_key, sku_id)

                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({"res": 6, "errmsg": "Out of stock"})

                OrderGoods.objects.create(
                    order=order, sku=sku, count=count, price=sku.price
                )

                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                amount = sku.price * int(count)
                total_count += int(count)
                total_price += amount

            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({"res": 7, "errmsg": "Fail to place the order"})

        transaction.savepoint_commit(save_id)
        conn.hdel(cart_key, *sku_ids)
        return JsonResponse({"res": 5, "message": "Successfully create the order"})


class OrderPayView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':0, 'errmsg':'Please login'})

        order_id = request.POST.get('order_id')

        if not order_id:
            return JsonResponse({'res':1, 'errmsg':'Invalid order id'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res':2, 'errmsg':'Wrong order'})

        alipay = AliPay(
            appid="", # need to set the appid
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem'),
            sign_type="RSA2",
            debug=True
        )

        total_pay = order.total_price+order.transit_price
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(total_pay),
            subject='dailyfresh%s'%order_id,
            return_url=None,
            notify_url=None
        )

        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res':3, 'pay_url':pay_url})


class CheckPayView(View):
    def post(self, request):

        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'Please login'})

        order_id = request.POST.get('order_id')

        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': 'Invalid order id'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': 'Incorrect order'})

        alipay = AliPay(
            appid="", # need to set the appid
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem'),
            sign_type="RSA2",
            debug=True
        )

        while True:
            response = alipay.api_alipay_trade_query(order_id)
            code = response.get('code')

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':

                trade_no = response.get('trade_no')
                order.trade_no = trade_no
                order.order_status = 4
                order.save()
                return JsonResponse({'res':3, 'message':'Successful payment'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                import time
                time.sleep(5)
                continue
            else:
                print(code)
                return JsonResponse({'res':4, 'errmsg':'Fail to make the payment'})


class CommentView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        user = request.user
        if not order_id:
            return redirect(reverse("user:order"))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

        order_skus = OrderGoods.objects.filter(order_id=order_id)
        for order_sku in order_skus:
            amount = order_sku.count * order_sku.price
            order_sku.amount = amount
        order.order_skus = order_skus

        return render(request, "order_comment.html", {"order": order})

    def post(self, request, order_id):
        user = request.user
        if not order_id:
            return redirect(reverse("user:order"))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        total_count = request.POST.get("total_count")
        total_count = int(total_count)

        for i in range(1, total_count + 1):
            sku_id = request.POST.get("sku_%d" % i)
            content = request.POST.get(
                "content_%d" % i, ""
            )
            try:
                order_goods = OrderGoods.objects.get(order=order, sku_id=sku_id)
            except OrderGoods.DoesNotExist:
                continue

            order_goods.comment = content
            order_goods.save()

        order.order_status = 5
        order.save()

        return redirect(reverse("user:order", kwargs={"page": 1}))
