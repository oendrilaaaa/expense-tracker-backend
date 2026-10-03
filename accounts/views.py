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

class LoginView(APIView):
    def validate_mobile(mobile):
        if mobile.isdigit() and len(mobile)==10:
            return True
        else:
            return False


    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def login_api(request):
        if request.method == 'POST':
            payload = request.data
            mobile = payload.get('mobile')
            otp = payload.get('otp')

            # validating provided mobile
            if not validate_mobile(mobile=mobile):
                return Response({"error":"provide a valid mobile number"}, status=400)

            # check if this mobile number exist in user table or not 
            found_user = User.objects.filter(username=mobile).first()
            if found_user:
                # check otp is valid or not
                is_otp_valid = str(cache.get(f"otp_{mobile}")) == str(otp)
                if is_otp_valid:
                    return Response({
                        "username": found_user.username,
                        "first_name": found_user.first_name,
                        "last_name": found_user.last_name,
                        "email": found_user.email,
                        "tokens": get_tokens_for_user(found_user),
                    })
                else:
                    return Response({"error":"provide a valid mobile number"}, status=400)
            else:
                #throw error account doesnt exist
                return Response({"error":"account not found"}, status=400)

        else:
            return Response({"error":"method not allowed"}, status=400)
            
        