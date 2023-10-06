from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer
from djangoproject.settings import STRIPE_SECRET_KEY, STRIPE_SECRET_WEBHOOK
from users.models import User, Profile


class SubscriptionPlansList(ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CreateCheckOutSession(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        subscription_id = self.kwargs["pk"]
        try:
            selected_plan = SubscriptionPlan.objects.get(pk=subscription_id)
            user_obj = self.request.user
            profile = Profile.objects.get(user=user_obj)
            if profile.user_type == 'basic':
                message = "You can buy this plan."
            else:
                message = "You are already a premium user and don't need to buy the plan again."

            plan_data = {
                'plan_name': selected_plan.plan_name,
                'plan_price': selected_plan.plan_price,
                'user_message': message,
            }

            return Response(plan_data, status=HTTP_200_OK)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Plan not found.'}, status=HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        sub_id = self.kwargs["pk"]
        user_obj = self.request.user
        try:
            subscription = SubscriptionPlan.objects.get(id=sub_id)
            stripe.api_key = STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(subscription.plan_price * 100),
                            'product_data': {
                                'name': subscription.plan_name,
                            }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id": subscription.id
                },
                mode='payment',
                success_url='http://localhost:5173/checkout-success',
                cancel_url='http://localhost:5173/checkout-cancelled',
                customer_email= user_obj.email,
            )
            # return redirect(checkout_session.url)
            return Response({'url': checkout_session.url, 'session_id': checkout_session.id}, status=200)
        except Exception as e:
            return Response({'msg': 'something went wrong while creating stripe session', 'error': str(e)}, status=500)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return Response('Invalid payload', status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response('Invalid signature', status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)
        user_email = session['customer_details']['email']
        user = User.objects.get(username=user_email)
        user.profile.user_type = 'premium'
        user.save()

    # Passed signature verification
    return HttpResponse('Passed signature verification', status=200)
