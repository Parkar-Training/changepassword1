from django.http import JsonResponse
from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view


import hashlib

from rest_framework.views import APIView

from changePassword.serializationclass import *
from user.models import *
from changePassword.serializationclass import *




class changePassword(APIView):
    print("inside change password")

    def put(self,request):
        try:
            print("fetched data", request.data)
            #------- validations------------------
            if request.data['emailid'] == "":
                return JsonResponse({"msg": "plz enter emailid"})

            if request.data['password'] == "":
                return JsonResponse({"msg": "plz enter old password"})
            if request.data['newpassword'] == "":
                return JsonResponse({"msg": "plz enter new password"})

            old_password = request.data['password']
            encrypted_password = hashlib.md5(old_password.encode()).hexdigest()
            user_detail = {}
            user_detail['emailid'] = request.data['emailid']
            user_detail['password'] = encrypted_password

            print("user detail", user_detail)
            print("type of request data",type(request.data))
            confirmed_user_detail = users_new.objects.filter(**user_detail)
            # print("confirmed user detail", list(confirmed_user_detail.values_list()[0]))

            #---------validations-------------


            if confirmed_user_detail.exists():
                if request.data['password'] == request.data['newpassword']:
                    return JsonResponse({"Msg": "old and new password can't be same . plz enter different password  and try again"})
                print("inside confirmed_user_detail exists")
                encrypted_new_password = hashlib.md5(request.data['newpassword'].encode()).hexdigest()
                request.data['password'] = encrypted_new_password
                print("request data after new encryption password",request.data)
                s = ChangePasswordSerializerClass(users_new.objects.get(emailid=user_detail['emailid']),
                                                                  data=request.data)
                #print(s.data)
                if s.is_valid():
                    print("inside valid form")
                    s.save()
                    return JsonResponse({"msg":"password changed"})
                return JsonResponse({"Msg": "some error occured in data"})

            else:
                return JsonResponse({"msg":"wrong crendentials !!"})
        except ValueError:
            return Response("some error",status=status.HTTP_400_BAD_REQUEST)



