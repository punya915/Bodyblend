from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import  datetime
import cv2
import base64
####header for skintone detection
###end header
####constants

mediapath = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\"

####end constants


# Create your views here.
from myapp.models import *


def login(request):
    return render(request, "admin/login.html")

def log_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    var=Login.objects.filter(username=username,password=password)
    if var.exists():
        var1 = Login.objects.get(username=username, password=password)
        request.session['lid']=var1.id
        if var1.type=='admin':
            return redirect('/myapp/home/')
        elif var1.type=='user':
            return redirect('/myapp/uhome/')
        else:
            return HttpResponse('''<script>alert("Not found");window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid");window.location="/myapp/login/"</script>''')


def home(request):
    return render(request,"admin/home.html")

def add_category(request):
    return render(request, "admin/add category.html")



def addcat_post(request):
    name=request.POST['textfield']
    var=Category()
    var.catname=name
    var.save()
    return HttpResponse('''<script>alert("Successful");window.location="/myapp/add_category/"</script>''')


def change_password(request):
    return render(request, "admin/change password.html")

def changepas_post(request):
    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    res=Login.objects.filter(password=currentpassword,id=request.session['lid'])
    if res.exists():
        res1 = Login.objects.get(password=currentpassword, id=request.session['lid'])
        if newpassword==confirmpassword:
            res2 = Login.objects.filter(password=currentpassword, id=request.session['lid']).update(password=confirmpassword)
            return HttpResponse('''<script>alert("Changed Successfully");window.location="/myapp/login/"</script>''')
        else :
            return HttpResponse('''<script>alert("Password mismatch");window.location="/myapp/change_password/"</script>''')
    else :
        return HttpResponse('''<script>alert("Invalid password");window.location="/myapp/change_password/"</script>''')

def edit_category(request,cid):
    res=Category.objects.get(id=cid)
    return render(request,"admin/edit category.html",{'data':res})

def edit_post(request):
    cid=request.POST['cid']
    catname = request.POST['textfield']
    res=Category.objects.filter(id=cid).update(catname=catname)
    return HttpResponse('''<script>alert("Successful");window.location="/myapp/VIEW_CATEGORY/"</script>''')

def delete_category(request,cid):
    res=Category.objects.filter(id=cid).delete()
    return HttpResponse('''<script>alert("Successfully deleted");window.location="/myapp/VIEW_CATEGORY/"</script>''')


def RESPONSE(request):
    return render(request,"admin/RESPONSE.html")

def resp_post(request):
    response = request.POST['textarea']
    return HttpResponse("ok")


def VIEW_CATEGORY(request):
    res=Category.objects.all()
    return render(request,"admin/VIEW CATEGORY.html",{'data':res})

def viewcat_post(request):
    search = request.POST['textfield']
    res = Category.objects.filter(catname__icontains=search)
    return render(request, "admin/VIEW CATEGORY.html", {'data': res})


def VIEW_SUGGESTION(request):
    res=Suggestion.objects.all()
    return render(request,"admin/VIEW SUGGESTION.html",{'data':res})

def viewsug(request):
    fromd = request.POST['textfield']
    tod = request.POST['textfield2']
    res = Suggestion.objects.filter(date__range=[fromd,tod])
    return render(request, "admin/VIEW SUGGESTION.html", {'data': res})


def viewuser(request):
    res=User.objects.all()
    return render(request,"admin/viewuser.html",{'data':res})

def viewuser_post(request):
    text = request.POST['textfield']
    res = User.objects.filter(name__icontains=text)
    return render(request, "admin/viewuser.html", {'data': res})

def send_reply(request,id):

    request.session['cid']=id
    return render(request,"admin/send_reply.html")

def send_repy_post(request):

    res = Suggestion.objects.get(id=request.session['cid'])

    res.response = request.POST['reply']
    res.status = "replied"

    res.save()
    return VIEW_SUGGESTION(request)

def Adddress(request):
    data=Category.objects.all()
    return render(request,"admin/ADD DRESS.html",{'dt':data})

def adddress_POST(request):
    dname=request.POST['textfield4']
    amnt=request.POST['tf1']
    photo=request.FILES['fileField']
    description=request.POST['textarea']
    category=request.POST['select']
    skintone=request.POST['checkbox']
    gender=request.POST['select2']
    bodytype = request.POST['select3']
    amnt = request.POST['tf1']
    occassions=request.POST.getlist('occassions')
    oc=""
    for i in occassions:
        if oc!="":
            oc+=","+i
        else:
            oc=i
    from datetime import datetime
    date="dress/"+datetime.now().strftime('%Y%m%d-%H%M%S')+".jpg"
    fs=FileSystemStorage()
    fs.save(date,photo)
    path=fs.url(date)

    dobj=Dress()
    dobj.dname=dname
    dobj.amount=amnt
    dobj.photo=path
    dobj.description=description
    dobj.CATEGORY_id=category
    dobj.skintone=skintone
    dobj.bodytype=bodytype
    dobj.occasions=oc
    dobj.gender=gender
    dobj.save()
    return HttpResponse('''<script>alert("Successfully added");window.location="/myapp/home/"</script>''')

def deletedress(request,id):
    data=Dress.objects.get(id=id)
    data.delete()
    return HttpResponse('''<script>alert("Successfully deleted");window.location="/myapp/viewdress/"</script>''')


def editdress(request,id):

    d=Dress.objects.get(id=id)
    data = Category.objects.all()
    request.session['did']=id
    return render(request,"admin/EDIT DRESS.html",{'data': d,'dd':data})

def editdress_POST(request):
    dname = request.POST['textfield4']
    amnt = request.POST['tf1']

    description = request.POST['textarea']
    category = request.POST['select']
    skintone = request.POST['checkbox']
    gender = request.POST['select2']
    bodytype = request.POST['select3']
    occassions = request.POST.getlist('occassions')
    oc = ""
    for i in occassions:
        if oc != "":
            oc += "," + i
        else:
            oc = i
    from datetime import datetime


    dobj = Dress.objects.get(id=request.session['did'])
    dobj.dname = dname
    if 'fileField' in request.FILES:

        photo = request.FILES['fileField']
        if photo:
            date = "dress/" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, photo)
            path = fs.url(date)
            dobj.photo = path
    dobj.description = description
    dobj.CATEGORY_id = category
    dobj.skintone = skintone
    dobj.amount = amnt
    dobj.bodytype = bodytype
    dobj.occasions = oc
    dobj.gender = gender
    dobj.save()
    return viewdress(request)


def viewdress(request):
    data=Dress.objects.all()
    cat=Category.objects.all()
    return render(request,"admin/VIEW DRESS.html",{'dt':data,'cat':cat})

def viewdress_POST(request):
    c=request.POST["select"]
    data = Dress.objects.filter(CATEGORY_id=c)
    cat = Category.objects.all()
    return render(request, "admin/VIEW DRESS.html", {'dt': data, 'cat': cat})


def searchdress(request):
    return render(request,"admin/VIEW DRESS.html")

def searchdress_POST(request):
    return HttpResponse("ok")




def user_post(request):

    name=request.POST['name']
    password=request.POST['password']

    image=request.POST['image']
    gender=request.POST['gender']
    phone=request.POST['phone']
    email=request.POST['email']

    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    with open(mediapath + filename, mode='wb') as h:
        h.write(base64.b64decode(image))


    uobj=User()
    uobj.name=name
    uobj.phone=phone
    uobj.email=email
    uobj.photo="/media/"+ filename
    uobj.gender=gender

    lobj=Login()
    lobj.username= email
    lobj.password=password
    lobj.type="user"
    lobj.save()

    uobj.LOGIN= lobj
    uobj.save()


    return JsonResponse({'status':'ok'})

def login2(request):
    uname=request.POST['uname']
    psw=request.POST['psw']

    lobjs= Login.objects.filter(username=uname,password=psw)
    if lobjs.exists():

        lobjs=lobjs[0]

        return JsonResponse({'status':'ok', 'lid': lobjs.id})
    return JsonResponse({'status':'no'})


def  user_changepassword(request):

    lid= request.POST["lid"]
    newpassword= request.POST["newpassword"]



    lobj=Login.objects.get(id=lid)
    lobj.password= newpassword
    lobj.save()
    return JsonResponse({'status': 'ok'})



def user_skintonedetection(request):
    from . import face_detect
    from . import kMeansImgPy
    import cv2
    from . import allotSkinTone

    img= request.POST["img"]
    mediapath="C:\\22-23\\trendtrove\\media\\"

    filename= datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"

    with open(mediapath+ filename, mode='wb') as h:
        h.write(base64.b64decode(img))


    imgpath = mediapath+ filename
    image = cv2.imread(imgpath)

    # Detect face and extract
    face_extracted = face_detect.detect_face(image)
    # Pass extracted face to kMeans and get Max color list
    colorsList = kMeansImgPy.kMeansImage(face_extracted)

    print("Main File : ")
    print("Red Component : " + str(colorsList[0]))
    print("Green Component : " + str(colorsList[1]))
    print("Blue Component : " + str(colorsList[2]))

    # Allot the actual skinTone to a certain shade
    allotedSkinToneVal = allotSkinTone.allotSkin(colorsList)
    print("alloted skin tone : ")
    print(allotedSkinToneVal)

    tones = [
        "tone1",
        "tone2",
        "tone3",
        "tone4",
        "tone5",
    ]
    colors = [
        [59, 34, 25],  # tone1
        [161, 110, 75],  # tone2
        [212, 170, 120],  # tone3
        [230, 188, 152],  # tone4
        [255, 231, 209]  # tone5
    ]
    mindex = colors.index(allotedSkinToneVal)
    print(tones[mindex])



    return JsonResponse({'status':'ok', 'tone': tones[mindex]})


def userget_reccomendatins(request):
    tone= request.POST['tone']
    lid= request.POST['lid']

    userobj= User.objects.get(LOGIN_id=lid) 


    print(userobj.gender,"gender")

    print(tone,"tone")


    dressobjs= Dress.objects.filter(skintone=tone,gender=userobj.gender)

    ls=[]

    for i in dressobjs:
        ls.append({'id': i.id, 'dname':i.dname, 'photo':i.photo,'description':i.description, 'catname':i.CATEGORY.catname})


    print(ls)


    return JsonResponse({'status':'ok', 'data':ls})





def user_view_dress_adminadded(request):


    lid= request.POST["lid"]



    userobj = User.objects.get(LOGIN_id=lid)






    dressobjs= Dress.objects.all()

    ls=[]

    for i in dressobjs:
        ls.append({'id': i.id, 'dname':i.dname, 'photo':i.photo,'description':i.description, 'catname':i.CATEGORY.catname})
    print(ls)
    return JsonResponse({'status':'ok', 'data':ls,  'name': userobj.name, 'photo':userobj.photo})


def user_view_dress_adminadded_search(request):


    lid= request.POST["lid"]

    search= request.POST["search"]



    userobj = User.objects.get(LOGIN_id=lid)






    dressobjs= Dress.objects.filter(dname__icontains=search)

    ls=[]

    for i in dressobjs:
        ls.append({'id': i.id, 'dname':i.dname, 'photo':i.photo,'description':i.description, 'catname':i.CATEGORY.catname})
    print(ls)
    return JsonResponse({'status':'ok', 'data':ls,  'name': userobj.name, 'photo':userobj.photo})






def userviewprofile(request):
    lid= request.POST['lid']
    userobj = User.objects.get(LOGIN_id=lid)

    return JsonResponse({'status': 'ok', 'name': userobj.name, 'email': userobj.email, 'phone': userobj.phone, 'gender': userobj.gender, 'photo':userobj.photo})




def user_edit_post(request):

    lid=request.POST['lid']
    name=request.POST['name']


    image=request.POST['image']
    gender=request.POST['gender']
    phone=request.POST['phone']
    email=request.POST['email']





    uobj=User.objects.get(LOGIN_id=lid)
    uobj.name=name
    uobj.phone=phone
    uobj.email=email
    if len(image)>0:
        mediapath = "C:\\22-23\\trendtrove\\media\\"

        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        with open(mediapath + filename, mode='wb') as h:
            h.write(base64.b64decode(image))
        uobj.photo="/media/"+ filename
    uobj.save()


    return JsonResponse({'status':'ok'})





def user_delete_dress(request):
    mydressid= request.POST["mydressid"]

    Mydress.objects.filter(id=mydressid).delete()

    return JsonResponse({'status': 'ok'})



def user_send_suggestion(request):
    lid=request.POST["lid"]
    compaint= request.POST["complaint"]


    obj= Suggestion()
    obj.compaint=compaint
    obj.status="pending"
    obj.date= datetime.now()
    obj.response="pending"
    obj.USER= User.objects.get(LOGIN_id=lid)
    obj.save()

    return JsonResponse({'status': 'ok'})


def user_dress_combinations(request):
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

    # Load a pre-trained CNN model (ResNet-50)
    base_model = ResNet50(weights='imagenet', include_top=False)

    # Define a custom head for similarity computation
    inputs = keras.Input(shape=(224, 224, 3))
    x = base_model(inputs)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation='relu')(x)
    outputs = layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1))(x)  # L2 normalization
    model = keras.Model(inputs, outputs)
    # Load and preprocess dress images (replace these paths with your dataset)
    lid= request.session["lid"]
    topdress= Mydress.objects.filter(USER__LOGIN_id= lid,dresstype='top')
    botdress= Mydress.objects.filter(USER__LOGIN_id= lid,dresstype='bottom')
    if not  ( len(topdress) >0 and len(botdress)>0):
        return JsonResponse({'status':'insuffcicientdresscount'})
    top_dress_image_paths = []
    bottom_dress_image_paths = []
    for i in topdress:
        top_dress_image_paths.append("C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\" + i.dressphoto.replace("/media/",""))
    for i in botdress:
        bottom_dress_image_paths.append("C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\" + i.dressphoto.replace("/media/",""))

        # Function to load and preprocess an image
    def load_and_preprocess_image(image_path):
        img = image.load_img(image_path, target_size=(224, 224))
        img = image.img_to_array(img)
        img = preprocess_input(img)
        return img

    # Extract features for all top and bottom dresses
    top_dress_features = []
    bottom_dress_features = []

    for top_image_path in top_dress_image_paths:
        top_dress_img = load_and_preprocess_image(top_image_path)
        top_dress_features.append(model.predict(np.expand_dims(top_dress_img, axis=0)))

    for bottom_image_path in bottom_dress_image_paths:
        bottom_dress_img = load_and_preprocess_image(bottom_image_path)
        bottom_dress_features.append(model.predict(np.expand_dims(bottom_dress_img, axis=0)))
    # Calculate cosine similarity between all pairs of top and bottom dresses
    similarities = np.dot(np.vstack(top_dress_features), np.vstack(bottom_dress_features).T)
    # Display the similarity matrix
    print("Similarity Matrix:")
    print(similarities)
    # You can set a threshold to determine if the dresses match or not
    threshold = 0.6  # Adjust this threshold as needed
    ls=[]
    # Find and display matching combinations
    for i, top_similarities in enumerate(similarities):
        matching_bottom_indices = np.where(top_similarities >= threshold)[0]
        if matching_bottom_indices.any():
            # print(f"Top Dress {i + 1} matches with Bottom Dress(es): {matching_bottom_indices + 1}")

            # print(i,matching_bottom_indices[0], type(i), type(matching_bottom_indices[0]))
            ls.append({'top':topdress[i].dressphoto ,'bottom':botdress[int(matching_bottom_indices[0])].dressphoto   })
        else:
            print(f"No matching Bottom Dress found for Top Dress {i + 1}")



    return render(request,"user/vd.html",{'status':'ok', 'data':ls})




def adminindex(request):
    return render(request,"admin/index.html")

def usignup(request):

    return render(request, "user/user_register.html")

def user_signup(request):

    full=request.POST["fullname"]
    phone=request.POST["phone"]
    gender=request.POST["gender"]
    email=request.POST["email"]
    password=request.POST["password"]
    img=request.FILES["photo"]
    from datetime import datetime
    date = "user/"+datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, img)
    path = fs.url(date)
    l=Login()
    l.username=email
    l.password=password
    l.type="user"
    l.save()

    u=User()
    u.name=full
    u.photo=path
    u.phone=phone
    u.gender=gender
    u.email=email
    u.LOGIN_id=l.id
    u.save()
    return  HttpResponse('''<script>alert("Success");window.location="/myapp/login/"</script>''')


def uhome(request):
    return render(request,"user/home.html")

def uprofile(request):
    u=User.objects.get(LOGIN_id=request.session["lid"])
    return render(request,"user/userprofile.html",{'data':u})


def profile_update(request):
    u=User.objects.get(LOGIN_id=request.session["lid"])
    return render(request,"user/user_updateprofile.html",{'data':u})

def profile_update_post(request):
    u=User.objects.get(LOGIN_id=request.session["lid"])
    full = request.POST["fullname"]
    phone = request.POST["phone"]
    gender = request.POST["gender"]
    email = request.POST["email"]
    u.name=full
    u.phone=phone
    u.gender=gender
    u.email=email
    if 'photo' in request.FILES:
        img = request.FILES["photo"]
        if img:
            from datetime import datetime
            date = "user/" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, img)
            path = fs.url(date)
            u.photo=path
    u.save()
    return uprofile(request)




def change_passwordu(request):
    return render(request, "admin/change password.html")

def changepas_postu(request):
    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    res=Login.objects.filter(password=currentpassword,id=request.session['lid'])
    if res.exists():
        res1 = Login.objects.get(password=currentpassword, id=request.session['lid'])
        if newpassword==confirmpassword:
            res2 = Login.objects.filter(password=currentpassword, id=request.session['lid']).update(password=confirmpassword)
            return HttpResponse('''<script>alert("Changed Successfully");window.location="/myapp/login/"</script>''')
        else :
            return HttpResponse('''<script>alert("Password mismatch");window.location="/myapp/change_password/"</script>''')
    else :
        return HttpResponse('''<script>alert("Invalid password");window.location="/myapp/change_password/"</script>''')


def VIEW_SUGGESTION_u(request):
    res=Suggestion.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request,"user/VIEW SUGGESTION.html",{'data':res})

def viewsug_u(request):

    res = Suggestion()
    res.compaint=request.POST['complaint']
    res.response="pending"
    res.status="pending"
    res.USER=User.objects.get(LOGIN_id=request.session["lid"])
    res.date=datetime.now().date()
    res.save()
    return VIEW_SUGGESTION_u(request)


def skintone(request):

    return render(request,"user/skintone_identify.html")


def skintone_post(request):
    gender=request.POST['select2']
    body=request.POST['select3']
    occassion=request.POST['occassions']
    from . import face_detect
    from . import kMeansImgPy
    import cv2
    from . import allotSkinTone
    from django.db.models import Q


    img = request.FILES["fileField"]
    from datetime import datetime
    date = "Checking/" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, img)
    path = fs.url(date)

    imgpath = r"C:\Users\PUNYA\OneDrive\Desktop\Project\Project\trendtrove\trendtrove\trendtrove\media\Checking\\" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    image = cv2.imread(imgpath)

    # Detect face and extract
    face_extracted = face_detect.detect_face(image)
    # Pass extracted face to kMeans and get Max color list
    colorsList = kMeansImgPy.kMeansImage(face_extracted)

    print("Main File : ")
    print("Red Component : " + str(colorsList[0]))
    print("Green Component : " + str(colorsList[1]))
    print("Blue Component : " + str(colorsList[2]))

    # Allot the actual skinTone to a certain shade
    allotedSkinToneVal = allotSkinTone.allotSkin(colorsList)
    print("alloted skin tone : ")
    print(allotedSkinToneVal)

    tones = [
        "tone1",
        "tone2",
        "tone3",
        "tone4",
        "tone5",
    ]
    colors = [
        [59, 34, 25],  # tone1
        [161, 110, 75],  # tone2
        [212, 170, 120],  # tone3
        [230, 188, 152],  # tone4
        [255, 231, 209]  # tone5
    ]
    myg=gog(image)
    # =======================================================================================================================
    if gender == 'UNISEX':
            print('UNISEX========================================================================')
            mindex = colors.index(allotedSkinToneVal)
            print(tones[mindex])
            d=Dress.objects.filter(skintone=tones[mindex],gender=gender)
            d = Dress.objects.filter(Q(skintone=tones[mindex],gender='UNISEX') | Q(skintone=tones[mindex]), gender='UNISEX')
            ld=[]
            for i in d:
                if i.bodytype == "ALL":
                    d=str(i.occasions).split(",")
                    if occassion in d:

                        ld.append({"id":i.id,"photo":i.photo,"dname":i.dname,"description":i.description,"category":i.CATEGORY.catname,"skintone":i.skintone,"bodytype":i.bodytype,'gender':i.gender})
                elif i.bodytype == body:
                    d = str(i.occasions).split(",")
                    if occassion in d:
                        ld.append({"id": i.id, "photo": i.photo, "dname": i.dname, "description": i.description,
                            "category": i.CATEGORY.catname, "skintone": i.skintone, "bodytype": i.bodytype,'gender': i.gender})
                else:
                    pass
            return render(request, "user/skintone_identify.html",{"dresses":ld})
        
    # =======================================================================================================================
    print(myg,gender)
    if myg == gender:
        mindex = colors.index(allotedSkinToneVal)
        print(tones[mindex])
        d=Dress.objects.filter(skintone=tones[mindex],gender=gender)
        from django.db.models import Q


        # Retrieve dresses with skintone 'light' OR 'medium' AND gender 'female'
        d = Dress.objects.filter(Q(skintone=tones[mindex],gender=myg) | Q(skintone=tones[mindex]), gender=myg)
        ld=[]
        for i in d:
            if i.bodytype == "ALL":
                d=str(i.occasions).split(",")
                print(d,occassion)
                if occassion in d:

                    ld.append({"id":i.id,"photo":i.photo,"dname":i.dname,"description":i.description,"category":i.CATEGORY.catname,"skintone":i.skintone,"bodytype":i.bodytype,'gender':i.gender})
            elif i.bodytype == body:
                d = str(i.occasions).split(",")
                if occassion in d:
                    ld.append({"id": i.id, "photo": i.photo, "dname": i.dname, "description": i.description,
                        "category": i.CATEGORY.catname, "skintone": i.skintone, "bodytype": i.bodytype,'gender': i.gender})
            else:
                pass
        print(ld)
        return render(request, "user/skintone_identify.html",{"dresses":ld})
    else:
        return HttpResponse("<script>alert('Picture chosen and Gender chosen are different');window.location='/skintone'</script>")


def skintones(request):
    import cv2
    return render(request,"user/p.html")


def skintone_posts(request):
    import cv2
    camera = cv2.VideoCapture(0)
    if 'b' in request.POST:
        ret, frame = camera.read()
        # frame_with_faces, faces = detect_faces(frame)
        # if frame:
        import datetime
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = now + ".jpg"
        cv2.imwrite(r"C:\Users\PUNYA\OneDrive\Desktop\Project\Project\trendtrove\trendtrove\trendtrove\media\Checking\\" + filename, frame)
        request.session['fname']=filename
        
        return render(request,"user/p.html",{"img":"/media/Checking/"+filename})

    else:
        gender=request.POST['select2']
        body=request.POST['select3']
        occassion=request.POST['occassions']
        from . import face_detect
        from . import kMeansImgPy
        import cv2
        from . import allotSkinTone
        from django.db.models import Q


        from datetime import datetime
        date = "Checking/" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"


        imgpath = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\Checking\\" + request.session['fname']
        image = cv2.imread(imgpath)

        # Detect face and extract
        face_extracted = face_detect.detect_face(image)
        # Pass extracted face to kMeans and get Max color list
        colorsList = kMeansImgPy.kMeansImage(face_extracted)

        print("Main File : ")
        print("Red Component : " + str(colorsList[0]))
        print("Green Component : " + str(colorsList[1]))
        print("Blue Component : " + str(colorsList[2]))

        # Allot the actual skinTone to a certain shade
        allotedSkinToneVal = allotSkinTone.allotSkin(colorsList)
        print("alloted skin tone : ")
        print(allotedSkinToneVal)

        tones = [
            "tone1",
            "tone2",
            "tone3",
            "tone4",
            "tone5",
        ]
        colors = [
            [59, 34, 25],  # tone1
            [161, 110, 75],  # tone2
            [212, 170, 120],  # tone3
            [230, 188, 152],  # tone4
            [255, 231, 209]  # tone5
        ]
    
        myg=gog(image)
        # =============================================================
        if gender == 'UNISEX':
            print('UNISEX========================================================================')
            mindex = colors.index(allotedSkinToneVal)
            print(tones[mindex])
            d=Dress.objects.filter(skintone=tones[mindex],gender=gender)
            d = Dress.objects.filter(Q(skintone=tones[mindex],gender='UNISEX') | Q(skintone=tones[mindex]), gender='UNISEX')
            ld=[]
            for i in d:
                if i.bodytype == "ALL":
                    d=str(i.occasions).split(",")
                    if occassion in d:

                        ld.append({"id":i.id,"photo":i.photo,"dname":i.dname,"description":i.description,"category":i.CATEGORY.catname,"skintone":i.skintone,"bodytype":i.bodytype,'gender':i.gender})
                elif i.bodytype == body:
                    d = str(i.occasions).split(",")
                    if occassion in d:
                        ld.append({"id": i.id, "photo": i.photo, "dname": i.dname, "description": i.description,
                            "category": i.CATEGORY.catname, "skintone": i.skintone, "bodytype": i.bodytype,'gender': i.gender})
                else:
                    pass
            return render(request, "user/skintone_identify.html",{"dresses":ld})
        
        # ================================================================================================================================
        
        print(myg,gender,"genderrrrrrrrrrr")
        if gender == myg:
                mindex = colors.index(allotedSkinToneVal)
                print(tones[mindex])
                d=Dress.objects.filter(skintone=tones[mindex],gender=gender)
                d = Dress.objects.filter(Q(skintone=tones[mindex],gender=myg) | Q(skintone=tones[mindex]), gender=myg)
                ld=[]
                for i in d:
                    if i.bodytype == "ALL":
                        d=str(i.occasions).split(",")
                        if occassion in d:

                            ld.append({"id":i.id,"photo":i.photo,"dname":i.dname,"description":i.description,"category":i.CATEGORY.catname,"skintone":i.skintone,"bodytype":i.bodytype,'gender':i.gender})
                    elif i.bodytype == body:
                        d = str(i.occasions).split(",")
                        if occassion in d:
                            ld.append({"id": i.id, "photo": i.photo, "dname": i.dname, "description": i.description,
                                "category": i.CATEGORY.catname, "skintone": i.skintone, "bodytype": i.bodytype,'gender': i.gender})
                    else:
                        pass
                return render(request, "user/skintone_identify.html",{"dresses":ld})
        else:
            return HttpResponse("<script>alert('Picture chosen and Gender chosen are different');window.location='/skintone'</script>")


def getFaceBox(faceNet, frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), [104, 117, 123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    faceBoxes = []
    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frameWidth)
            y1 = int(detection[0, 0, i, 4] * frameHeight)
            x2 = int(detection[0, 0, i, 5] * frameWidth)
            y2 = int(detection[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    return frame, faceBoxes
def gog(cvvv):





    faceProto = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\gender\\opencv_face_detector.pbtxt"
    faceModel = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\gender\\opencv_face_detector_uint8.pb"

    ageProto = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\gender\\age_deploy.prototxt"
    ageModel = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\gender\\age_net.caffemodel"

    genderProto = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\gender\\gender_deploy.prototxt"
    genderModel = "C:\\Users\\PUNYA\\OneDrive\\Desktop\\Project\\Project\\trendtrove\\trendtrove\\trendtrove\\media\\gender\\gender_net.caffemodel"

    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['MALE', 'FEMALE']

    # video = cv2.VideoCapture(0)

    padding = 20



    frame, faceBoxes = getFaceBox(faceNet, cvvv)

    if not faceBoxes:
        print("No face detected")

    for faceBox in faceBoxes:
        face = frame[max(0, faceBox[1] - padding):min(faceBox[3] + padding, frame.shape[0] - 1),
            max(0, faceBox[0] - padding):min(faceBox[2] + padding, frame.shape[1] - 1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        genderNet.setInput(blob)
        genderPred = genderNet.forward()
        gender = genderList[genderPred[0].argmax()]

        ageNet.setInput(blob)
        agePred = ageNet.forward()
        age = ageList[agePred[0].argmax()]

        labelGender = "{}".format("Gender : " + gender)
        labelAge = "{}".format("Age : " + age + "Years")
        

    return gender



def viewdress_u(request):
    data=Dress.objects.all()
    cat=Category.objects.all()
    return render(request,"user/VIEW DRESS.html",{'dt':data,'cat':cat})

def viewdress_POST_u(request):
    c=request.POST["select"]
    data = Dress.objects.filter(CATEGORY_id=c)
    cat = Category.objects.all()
    return render(request, "user/VIEW DRESS.html", {'dt': data, 'cat': cat})


def user_add_dress_get(request):
    return render(request,"user/add_mydress.html")

def user_add_dress(request):

    dressphoto=request.FILES['fileField']
    dresstype=request.POST['select']



    from datetime import datetime
    date = "mydress/" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, dressphoto)
    path = fs.url(date)
    mobj=Mydress()
    mobj.USER= User.objects.get(LOGIN_id=request.session['lid'])
    mobj.dresstype= dresstype
    mobj.dressphoto=path
    mobj.save()

    return HttpResponse('''<script>alert('Added');window.location='/myapp/user_add_dress_get/'</script>''')



def user_view_dress(request):
    lid= request.session["lid"]

    dressobjs=Mydress.objects.filter(USER__LOGIN_id=lid)

    ls = []

    for i in dressobjs:
        ls.append({'id': i.id, 'dressphoto': i.dressphoto, 'dresstype': i.dresstype})

    return render(request, "user/view_dress_my.html",{"data":ls})
def delete_drs(request,id):
    Mydress.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert('deleted');window.location='/myapp/user_view_dress/'</script>''')








def qty(request,id):
    request.session['pid']=id
    cobj=Cart()
    cobj.DRESS=Dress.objects.get(id=request.session['pid'])
    cobj.USER=User.objects.get(LOGIN__id=request.session['lid'])
    cobj.save()
    return HttpResponse('''<script>alert('Added');window.location='/myapp/user_viewcart/'</script>''')




def user_addtocart(request):
    lid=request.session['lid']
    qty=request.POST['tf1']
    cobj=Cart()
    cobj.DRESS=Dress.objects.get(id=request.session['pid'])
    cobj.USER=User.objects.get(LOGIN__id=lid)
   
    cobj.save()
    return HttpResponse('''<script>alert('Added');window.location='/myapp/user_viewcart/'</script>''')

def user_viewcart(request):
    lid=request.session['lid']
    print(lid)
    res = Cart.objects.filter(USER__LOGIN__id=lid)
    print(res,"llhlllh")
    l = []
    total=0
    for i in res:
        l.append({'id': i.id,"did":i.DRESS.id, 'pname': i.DRESS.dname,'description': i.DRESS.description,'amount': i.DRESS.amount,'photo':i.DRESS.photo})
        total += float(i.DRESS.amount)
        request.session['total']=total
    print(total)
    return render(request,'user/cart.html',{"data": l,"tamount":str(total)})
#
#
def user_removecart(request,id):
    # cid=request.POST['cid']
    ob=Cart.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Removed');window.location='/myapp/user_viewcart/'</script>''')
#
#
def payment_get(request):
    return render(request,"user/payment.html",{"tamnt":request.session['total']})


def user_makepayment(request):
    lid = request.session['lid']
    Accn = request.POST['textfield']
    Acname = request.POST['textfield2']
    Ifsc = request.POST['textfield3']
    Cvv = request.POST['textfield4']
    Amount = float(request.POST['textfield5'])
    if Payment.objects.filter(Acname=Acname, Accn=Accn, Ifsc=Ifsc, Cvv=Cvv, Balance__gte=Amount).exists():
        res = Cart.objects.filter(USER__LOGIN_id=lid)
        for i in res:
            print(i)
            res2 = Cart.objects.filter(USER__LOGIN_id=lid, DRESS_id=i.DRESS.id)
            print(res2, "hiii")
            quantity = int(1)
            boj = order_main()
            boj.USER = User.objects.get(LOGIN_id=lid)
            boj.amount = 0
            import datetime
            boj.date = datetime.datetime.now().date().today()
            boj.save()
            mytotal = 0
            st = 0
            for j in res2:
                # print(j)
                bs = order_sub()
                bs.ORDER_MAIN_id = boj.id
                bs.DRESS_id = j.DRESS.id
                bs.quantity = int(1)
                bs.save()
                mytotal += (float(j.DRESS.amount) * int(1))
            print(mytotal)
            Cart.objects.filter(DRESS_id=i.DRESS.id, USER__LOGIN_id=lid).delete()
            print(boj)
            boj = order_main.objects.get(id=boj.id)
            boj.amount = mytotal
            boj.save()
            qt=Payment.objects.get(Acname=Acname, Accn=Accn, Ifsc=Ifsc, Cvv=Cvv)
            qry=Payment.objects.filter(Acname=Acname, Accn=Accn, Ifsc=Ifsc, Cvv=Cvv).update(Balance=qt.Balance-mytotal)
            #
            # for i in
        return HttpResponse('''<script>alert('Successfull');window.location="/myapp/uhome/"</script>''')
    else:
        return HttpResponse('''<script>alert('not');window.location="/myapp/uhome/"</script>''')


def user_view_oder(request):
    res=order_main.objects.filter(USER__LOGIN__id=request.session['lid'])
    return render(request,"user/View_order.html",{"data":res})

def user_view_oder_more(request,oid):
    res=order_sub.objects.filter(ORDER_MAIN__id=oid)
    return render(request,"user/View_order_more.html",{"data":res})


def admin_view_oder(request):
    res=order_main.objects.all()
    return render(request,"admin/View_order.html",{"data":res})

def admin_view_oder_more(request,oid):
    res=order_sub.objects.filter(ORDER_MAIN__id=oid)
    return render(request,"admin/View_order_more.html",{"data":res})

