from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AuthView(APIView):

    def post(self, request):
        phone = str(request.data.get("phone")).strip()
        if phone.isdigit() and len(phone)==10:
            if request.data.get("otp"):
                return self.verifyOtp(request,phone)
            return self.sendOtp(request)
        return Response({"message":"Not a valid number"},status=401)

    def sendOtp(self, request):
        otp_sent = str(random.randint(100000, 999999))
        phone = str(request.data.get("phone")).strip()
        cache.set(f"otp_{phone}", otp_sent, timeout=120)
        return Response({"message":otp_sent},status=200)

    def verifyOtp(self, request, phone):
        saved_otp = cache.get(f"otp_{phone}")
        print(saved_otp)
        if request.data.get("otp") == saved_otp:
            user, created = User.objects.get_or_create(username=phone)
            refresh = RefreshToken.for_user(user)
            refresh_tkn = str(refresh)
            access_tkn = str(refresh.access_token)
            print("created: ",created)
            cache.delete(f"otp_{phone}")
            return Response({"accesss":access_tkn,"refresh":refresh_tkn},status=200)
        else:
            return Response({"message":"OTP invalid/expired"},status=401)


        
        
