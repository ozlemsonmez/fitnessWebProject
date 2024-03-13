from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
 
a= "12345"
client = MongoClient("mongodb+srv://melekmbbal:"+a+"@melek.5jcbucj.mongodb.net/?retryWrites=true&w=majority")
db = client["Yazlab"] # database
collection = db["kullanicilar"] # collection
temp_mail = None


@csrf_exempt  # CSRF korumasını devre dışı bırakmak için. Güvenlik açısından dikkatli olmalısınız.
def contact_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            email = data.get('email')
            
            
            collection.update_one(
                {'email': email},
                {'$set': {'danismanMessage': message}}
            )
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def upload_profile_photo(request):
    if request.method == 'POST':
        photo = request.POST.get('photo')
        email = request.POST.get('email')

        try:
            # MongoDB'deki veriyi güncelle
            collection.update_one(
                {'email': email},
                {'$set': {'profilphoto': photo}}
            )
            response_data = {'status': 'success'}
        except Exception as e:
            print(e)
            response_data = {'status': 'error', 'message': 'Veri güncelleme hatası'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Geçersiz istek methodu'})

@csrf_exempt
def save_progres_changes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        kilo = data.get('kilo')
        boy = data.get('boy')
        yagorani = data.get('yag_orani')
        kasorani = data.get('kas_orani')
        email = data.get('email')
        
        
        
        user = collection.find_one({'email': email})


        try:
            # MongoDB'deki veriyi güncelle
            collection.update_one(
                {'email': email},
                {'$set': {'boy': boy, 'kilo': kilo, 'yag_orani': yagorani, 'kas_orani': kasorani, 'pastkilo': user['kilo'], 'pastyag_orani': user['yag_orani'], 'pastkas_orani': user['kas_orani'],'pastboy':user['boy']}}
            )
            response_data = {'status': 'success'}
        except Exception as e:
            print(e)
            response_data = {'status': 'error', 'message': 'Veri güncelleme hatası'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Geçersiz istek methodu'})


@csrf_exempt
def save_profile_changes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name')
        telefon = data.get('telefon')
        cinsiyet = data.get('cinsiyet')
        dogumtarihi = data.get('dogumtarihi')

        try:
            # MongoDB'deki veriyi güncelle
            collection.update_one(
                {'email': email},
                {'$set': {'name': name, 'telefon': telefon, 'cinsiyet': cinsiyet, 'dogumtarihi': dogumtarihi}}
            )
            response_data = {'status': 'success'}
        except Exception as e:
            print(e)
            response_data = {'status': 'error', 'message': 'Veri güncelleme hatası'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Geçersiz istek methodu'})


@csrf_exempt  
def client(request):
    email = None
    if request.method == 'POST':
        email = request.POST.get('email')
        temp_mail = email
    
    user = collection.find_one({'email': email})
    
    context = {
        'user': user,
    }
    
    print(user)
    return render(request, "client.html",context)
    
    
# Create your views here.
