from django.shortcuts import render,HttpResponseRedirect,HttpResponse

from .models import Product,Offers,Cart,Save,RegisterationRequest

from .forms import ProductForm

from datetime import date,timedelta

from django.contrib import messages

from django.db.models import Q,F

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail

from django.conf import settings


# Create your views here.


def Index(request):
    if request.method=='POST':
        data=request.POST.get('preference')
        cdata=request.POST.get('category')
        
        
    return render(request,'admin/index1.html')

def Display(request):
    data=Product.objects.all()
    return render(request,'admin/display.html',{"ddata":data})

def Delete(request,id):
    if request.method=="POST":
        Product.objects.get(pk=id).delete()

        messages.success(request,"Product Deleted Successfully....")

        return HttpResponseRedirect("/display/")

def Update(request,id):
    if request.method=="POST":
        os=Product.objects.get(pk=id)
        fm=ProductForm(request.POST,request.FILES,instance=os)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Product Updated Successfully....")
            return HttpResponseRedirect("/display/")

        


    else:
        os=Product.objects.get(pk=id)
        fm=ProductForm(instance=os)

    return render(request,"admin/update.html",{"uform":fm})


def UserBase(request):
    if request.user.is_authenticated:
        userprofile=request.user

        count=Cart.objects.filter(user_id=request.user).count()
        return render(request,"user/base.html",{'count':count,'user':userprofile})
    else:
        return HttpResponseRedirect('/')

def UserIndex(request):
    if request.user.is_authenticated:
        Ndata=Product.objects.all().order_by('-id')[:7]
        odata=Offers.objects.all()
        # best seller from order table
        Bdata=Product.objects.all()[:7]
        count=Cart.objects.filter(user_id=request.user).count()

        return render(request,"user/index.html",{'odata':odata,"Ndata":Ndata,'bdata':Bdata,'count':count})
    else:
        return HttpResponseRedirect('/')

def AllProducts(request):
    if request.user.is_authenticated:
        apdata=Product.objects.all()
        count=Cart.objects.filter(user_id=request.user).count()
        return render(request,"user/products.html",{'apdata':apdata,'count':count})
    else:
        return HttpResponseRedirect('/')

def Details(request,id,category,brand):
    if request.user.is_authenticated:
    
    
        date1=date.today()
        days=timedelta(days=7)
        delivery_date=date1+days
        ddata=Product.objects.filter(pk=id)
        similar_products=Product.objects.filter(category=category).exclude(id=id)
        brand_products=Product.objects.filter(brand=brand).exclude(id=id)
        count=Cart.objects.filter(user_id=request.user).count()

        return render(request,"user/details.html",{"ddata":ddata,'ddate':delivery_date,'sdata':similar_products,'bproduct':brand_products,'count':count})
    else:
        return HttpResponseRedirect('/')

def AddCart(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            cid=request.POST.get('cid')
            filter1=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
            if int(cid) not in filter1:
                Cart.objects.create(product_id=cid,user=request.user)
            else:
                messages.success(request,'This product is already added to the cart')
            # sid2=request.POST.get('sid2')
            # Save.objects.filter(product_id=sid2).delete()
            # Cart.objects.create(product_id=sid2)
        
        cpid=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        cartdata=Product.objects.filter(id__in=cpid)
        svid=Save.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        Savedata=Product.objects.filter(id__in=svid)
        amount=Product.objects.filter(id__in=cpid).values_list('price',flat=True)
        count=Cart.objects.filter(user_id=request.user).count()
        amt=0
        for i in amount:
            amt=amt+i
        return render(request,'user/cart.html',{'cdata':cartdata,'svdata':Savedata,'amt':amt,'count':count})
    else:
        return HttpResponseRedirect('/')    

def SaveLater(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            sid=request.POST.get('sid')
            Cart.objects.filter(product_id=sid).delete()
            Save.objects.create(product_id=sid,user=request.user)
            
            return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')       

def MoveCart(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            sid2=request.POST.get('sid2')
            Save.objects.filter(product_id=sid2).delete()
            Cart.objects.create(product_id=sid2,user=request.user)
            return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')       
    
def RemoveCart(request,id):
    if request.user.is_authenticated:
        Cart.objects.filter(product_id=id).delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')

def SaveDelete(request,id):
    if request.user.is_authenticated:
        Save.objects.filter(product_id=id).delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')

def ComponentSearch(request):
    if request.user.is_authenticated:
        try:
            if request.method=="POST":
                search=request.POST.get("search")
                sdata=Product.objects.filter(Q(category=search) | Q(pname__icontains=search) | Q(brand=search) | Q(desc__icontains=search) | Q(price__icontains=search))
                count=Cart.objects.filter(user_id=request.user).count()
            return render(request,'user/search.html',{'sdata':sdata,'count':count})
        except:
            return HttpResponseRedirect('/userindex/')
    else:
        return HttpResponseRedirect('/')

def SignUp(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        print(uname,email,pass1)
        User.objects.create_user(uname,email,pass1)
        subject=f"Welcome to WoodMagic Furnitures {uname}"
        message=f"""
                Dear {uname},

                You have Successfully register to WoodMagic Furnitures
                with {email} this mail,

                Welcome to WoodMagic Furnitures- where excellence meets experience!
                We're thrilled to have you join our community of valued customers,
                and we can't wait to be part of your journey.

                Dive into our wide range of products/services designed to meet your needs.
                From Good quality furnitures to a new customize option where, from your views we design !
                we're here to make your experience seamless and enjoyable.  

                Keep Shopping.......!
                 
                'Note: Please do not reply to this mail because it is auto-generated'
                 
                """
        mail_from=settings.EMAIL_HOST_USER
        mail_to=email

        send_mail(subject,message,mail_from,[mail_to])
        # messages.success(request,'Signup Successfully')
        return HttpResponseRedirect('/')
    return render(request,'user/signup.html')

def LogIn(request):
    if request.method=="POST":
        username=request.POST.get('uname')
        password=request.POST.get('pass1')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/userindex/')
    return render(request,'user/login.html')

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def Preferpage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pf=request.POST.get('room_type')
            pfdata=Product.objects.filter(preference=pf)
            
        return render(request,'user/preference.html',{'pfdata':pfdata,'pf':pf})
    else:
        return HttpResponseRedirect('/')

def AdminSup(request):
    rdata=RegisterationRequest.objects.all().order_by('-id')[:3]
    return render(request,'admin/AdminPanel.html',{'rdata':rdata})

def SellerPanel(request):
    if request.user.is_staff and request.user.is_authenticated:
        return render(request,'admin/SellerPanel.html')
    else:
        return HttpResponse("please signup or login")

def SellerRegisteration(request):
    if request.method == 'POST':
        bname=request.POST.get('bname')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        shopaddress=request.POST.get('shopaddress')
        branddesc=request.POST.get('branddesc')
        RegisterationRequest.objects.create(bname=bname,email=email,contact=contact,shopaddress=shopaddress,branddesc=branddesc)
        messages.success(request,'Applied successfully')


    return render(request,'admin/selleregisteration.html')

def BrandDetails(request,id):
    brdata=RegisterationRequest.objects.filter(pk=id)
    return render(request,'admin/requestbrand.html',{'brdata':brdata})



 
# def SellerSignup(request):
#     if request.method == "POST":
#         uname=request.POST.get("uname")
#         email=request.POST.get("email")
#         password=request.POST.get("pass1")
#         user=User.objects.create_user(uname,email,password)
#         user.is_staff=True
        
        
#         user.save()
#     return render(request,"admin/Sellersignup.html")


def SellerLogin(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass1")
        user = authenticate(request, username=username, password=password)
        print(f"Username: {username}, Password: {password}")

        if user is not None and user.is_staff:
            login(request, user)
            return HttpResponseRedirect("/sellerpanel/")
    return render(request,'admin/Sellerlogin.html')










    

    







        
        

    


    




        

    








