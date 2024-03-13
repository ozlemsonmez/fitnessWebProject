from django.http import JsonResponse
from django.shortcuts import render
from flask import redirect
import json
import pymongo
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt


a= "12345"
client = MongoClient("mongodb+srv://melekmbbal:"+a+"@melek.5jcbucj.mongodb.net/?retryWrites=true&w=majority")
db = client["Yazlab"] # database
collection = db["kullanicilar"] # collection


def home(request):
    return render(request, "index.html")

def administrator(request): 
    users = collection.find()  # burada tüm kullanıcıları çekiyoruz.

    return render(request, "administrator.html", {"users": users})


#collection.insert_many(data)


for i in collection.find({},{"_id":0, "name":1, "address":1 , "password":1}):
    print(i)


def login_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        user_type = body.get('userType')
        email = body.get('email')
        password = body.get('password')
        
        print(body.get('email'))

        print('User Type:', user_type)
        print('email:', email)
        print('Password:', password)
        
        existing_user = collection.find_one({"email": email , "password": password,"usertype":user_type})
        if existing_user:
            if user_type == 'admin':
                return JsonResponse({'status': 'success', 'redirect_url': '/administrator'})
            elif user_type == 'client':
                return JsonResponse({'status': 'success', 'redirect_url': '/client'})
            elif user_type == 'coach':
                return JsonResponse({'status': 'success', 'redirect_url': '/coach'})
        else:
            return JsonResponse({'message': 'Kullanıcı adı veya şifre yanlış!', 'status': 'error'})
   
        

    return redirect('home')

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        try:
            # Gelen veriyi JSON formatında oku
            data = json.loads(request.body)
            
            # E-posta adresini al
            email = data.get('email')
            
            myquery = { "email": email }

            collection.delete_one(myquery)
            


            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def forgot_password(request):
    if request.method == 'POST':
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body.get('email')
        new_password = body.get('new_password')
        confirm_password = body.get('confirm_password')
        
        print('Email:', email)
        print('New Password:', new_password)
        print('Confirm Password:', confirm_password)
        
        if new_password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Şifreler eşleşmiyor.'})

        # Kullanıcı bilgilerini MongoDB'den al
        user = collection.find_one({'email': email})
        
        print(user)

        if user :
            # Kullanıcının şifresini güncelle
            collection.update_one({'_id': user['_id']}, {'$set': {'password': new_password}}) 
            return JsonResponse({'status': 'success', 'redirect_url': '/client'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Geçersiz e-posta adresi.'})

    return render(request, 'forgot_password.html')


def admin_register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        name = body.get('username')
        password = body.get('password')
        email = body.get('email')
        usertype = body.get('userType')
        coach =None
        
        new_user = None
        
        if(usertype == "client"):
            clients = collection.find({'usertype': "coach"})  # burada tüm kullanıcıları çekiyoruz.
            for i in clients:
                if int(i["danismansayisi"]) < 5:
                    coach = i["email"]
                    temp = int(i["danismansayisi"]) + 1
                    collection.update_one(
                    {'email': i['email']},
                    {'$set': {'danismansayisi': temp}}
                    )
                    break
                    
                    
            new_user = {
                "name": name,
                "password": password,
                "email": email,
                "usertype": usertype,
                "coach": coach,
                "kilo": "0",
                "yag_orani": "0",
                "kas_orani": "0",
                "boy": "0",
            }
        elif(usertype == "coach"):
            new_user = {
                "name": name,
                "password": password,
                "email": email,
                "usertype": usertype,
                "danismansayisi": "0",
            }
            
            
                
        existing_user = collection.find_one({"email": email})
        if existing_user:
            return JsonResponse({'message': 'Kullanıcı adı veya email kullanılmaktadır!', 'status': 'error'})
            
        try:
            collection.insert_one(new_user)
            return JsonResponse({'status': 'success', 'redirect_url': '/client'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

            
            
        



def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        name = body.get('username')
        password = body.get('password')
        email = body.get('email')
        usertype = 'client'
        coach =None
        
        
        clients = collection.find({'usertype': "coach"})  # burada tüm kullanıcıları çekiyoruz.
        for i in clients:
            if int(i["danismansayisi"]) < 5:
                coach = i["email"]
                temp = int(i["danismansayisi"]) + 1
                collection.update_one(
                {'email': i['email']},
                {'$set': {'danismansayisi': temp}}
                )
                break
                
                
        new_user = {
            "name": name,
            "password": password,
            "email": email,
            "usertype": usertype,
            "coach": coach,
            "kilo": "0",
            "yag_orani": "0",
            "kas_orani": "0",
            "boy": "0",
        }
        
                
        existing_user = collection.find_one({"email": email})
        if existing_user:
            return JsonResponse({'message': 'Kullanıcı adı veya email kullanılmaktadır!', 'status': 'error'})
        
        try:
            collection.insert_one(new_user)
            return JsonResponse({'status': 'success', 'redirect_url': '/client'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'register.html')


