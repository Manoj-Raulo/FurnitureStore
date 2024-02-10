from django.shortcuts import render,HttpResponseRedirect,HttpResponse

from .models import Product,Offers,Cart,Save,RegisterationRequest,SellerDetails

from .forms import ProductForm

from datetime import date,timedelta

from django.contrib import messages

from django.db.models import Q,F

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail

from django.conf import settings

import uuid

from django.urls import reverse


# Create your views here.


def Index(request):
    if request.method=='POST':
        data=request.POST.get('preference')
        cdata=request.POST.get('category')
        
        
    return render(request,'admin/index1.html')

def Display(request):
    data=Product.objects.all()
    return render(request,'admin/display.html',{"ddata":data})

# def Delete(request,id):
#     if request.method=="POST":
#         Product.objects.get(pk=id).delete()

#         messages.success(request,"Product Deleted Successfully....")

#         return HttpResponseRedirect("/display/")

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


def SellerPanel(request):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
        
        sellerdata=SellerDetails.objects.filter(seller_id=request.user)
        
        
        
        userprofile=request.user
        
        return render(request,'admin/SellerPanel.html',{'sdata':sellerdata,'sname':userprofile})
    else:
        return HttpResponseRedirect("/sellerlogin/")

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



 
def SellerSignup(request):
    if request.method=='POST':
        bname=request.POST.get('bname')
        email=request.POST.get('email')
        rid=request.POST.get('id')
        contact=request.POST.get('contact')
        shopaddress=request.POST.get('shopaddress')
        branddesc=request.POST.get('branddesc')
        

        



        password=str(uuid.uuid4().hex)[:8:]
        bname1=bname+"@sellar"

        print(bname1,email,password)
        user=User.objects.create_user(bname1,email,password)
        user.is_staff=True
        user.save()
        subject=f"Update from WoodMagic Furnitures  {bname}"
        message=f"""
                Dear {bname},

                Congratulations ! We are happy to inform you that you are now a seller on our website,
                WoodMagic Firnitures. Welcome to our community. We are happy to have you on board.

                We had go through your brand details, got the information about your all product and 
                their quality.I believe that your brands would make a great impact and by working together,
                we could offer our customers a unique and valuable experience.

                Thank you for considering this opportunity. We look forward to the possibility of working with you.
                Start adding your Products on Our Website.

                these are your login credentials,
                Username: {bname1}
                Password: {password}(You can change this letter)

                if you have any doubt you can contact on this number:-9876543210
                you can also mail us on wmagicfurnitutres@gmail.com          
                        
                    
                'Note: Please do not reply to this mail because it is auto-generated'
                    
                """
        mail_from=settings.EMAIL_HOST_USER
        mail_to=email

        send_mail(subject,message,mail_from,[mail_to])
        RegisterationRequest.objects.filter(pk=rid).update(Status='Accepted')
        brand_id=(User.objects.filter(username=bname1).values_list('id',flat=True))
        print(brand_id)

        SellerDetails.objects.create(seller_id=brand_id[0],bname=bname,email=email,contact=contact,shopaddress=shopaddress,branddesc=branddesc)

    return HttpResponse("Seller Added Successfully....")  
    
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

def SellerProfile(request):
    sellerdata=SellerDetails.objects.filter(seller_id=request.user)
    userprofile=request.user
    return render(request,'admin/SellerProfile.html',{'sdata':sellerdata,'sname':userprofile})


def SellerUpdate(request):
    if request.method == 'POST':
        # Retrieve form data
        bname = request.POST.get('bname')
        shopaddress = request.POST.get('shopaddress')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        branddesc = request.POST.get('branddesc')
        brandlogo = request.FILES.get('brandlogo')

        # Fetch the SellerDetails object
        seller_details = SellerDetails.objects.filter(seller=request.user).first()
        if seller_details:
            # Update fields
            seller_details.bname = bname
            seller_details.shopaddress = shopaddress
            seller_details.email = email
            seller_details.contact = contact
            seller_details.branddesc = branddesc
            if brandlogo:
                seller_details.brandlogo = brandlogo  # Update the brandlogo only if a new image is uploaded
            # Save the updated object
            seller_details.save()

        return HttpResponseRedirect('/SellerProfile/')

    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/sellerupdate.html', {'sdata': sellerdata, 'sname': userprofile})

def SellerLogout(request):
    logout(request)
    return HttpResponseRedirect('/sellerlogin/')

def SellerCategory(request,pref):

    slcatproducts=Product.objects.filter(Q(seller=request.user) & Q(preference=pref))
    
    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/sellercategory.html', {'sdata': sellerdata, 'sname': userprofile,'cdata':slcatproducts,'pref':pref})

def SelpDetails(request,id):
    
    slddata=Product.objects.filter(pk=id)
    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/selpdetails.html', {'sdata': sellerdata, 'sname': userprofile,'slddata':slddata})

def EditProducts(request,id):
    if request.method=='POST':
        pid=request.POST.get('pid')
        pname=request.POST.get('pname')
        category=request.POST.get('category')
        preference=request.POST.get('preference')
        size=request.POST.get('size')
        material=request.POST.get('material')
        finishtype=request.POST.get('finishtype')
        dimension=request.POST.get('dimension')
        colour=request.POST.get('colour')
        brand=request.POST.get('brand')
        features=request.POST.get('features')
        desc=request.POST.get('desc')
        price=request.POST.get('price')
        weight=request.POST.get('weight')
        stock=request.POST.get('stock')
        img1=request.FILES.get('img1')
        img2=request.FILES.get('img2')
        img3=request.FILES.get('img3')
        img4=request.FILES.get('img4')
        img5=request.FILES.get('img5')
        product_details = Product.objects.filter(pk=pid).first()
        
        if product_details:
            product_details.pname=pname
            product_details.category=category
            product_details.preference=preference
            product_details.size=size
            product_details.material=material
            product_details.finishtype=finishtype
            product_details.dimension=dimension
            product_details.colour=colour
            product_details.brand=brand
            product_details.features=features
            product_details.desc=desc
            product_details.price=price
            product_details.weight=weight
            product_details.stock=stock
            if img1:
                product_details.img1=img1
            if img2:
                product_details.img2=img2
            if img3:
                product_details.img3=img3
            if img4:
                product_details.img4=img4
            if img5:
                product_details.img5=img5
            product_details.save()
        return HttpResponseRedirect(reverse('selpdetails', args=(pid,)))
        



    pdata=Product.objects.filter(pk=id)
    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/EditProducts.html', {'sdata': sellerdata, 'sname': userprofile,'pdata':pdata})

def AddProducts(request):
    if request.method=='POST':
        pname=request.POST.get('pname')
        category=request.POST.get('category')
        preference=request.POST.get('preference')
        size=request.POST.get('size')
        material=request.POST.get('material')
        finishtype=request.POST.get('finishtype')
        dimension=request.POST.get('dimension')
        colour=request.POST.get('colour')
        brand=request.POST.get('brand')
        features=request.POST.get('features')
        desc=request.POST.get('desc')
        price=request.POST.get('price')
        weight=request.POST.get('weight')
        stock=request.POST.get('stock')
        img1=request.FILES.get('img1')
        img2=request.FILES.get('img2')
        img3=request.FILES.get('img3')
        img4=request.FILES.get('img4')
        img5=request.FILES.get('img5')
        Product.objects.create(pname=pname,category=category,preference=preference,size=size,material=material,finishtype=finishtype,dimension=dimension,
        colour=colour,brand=brand,features=features,desc=desc,price=price,weight=weight,stock=stock,img1=img1,img2=img2,img3=img3,img4=img4,img5=img5,seller=request.user)
        return HttpResponse('Product Added Successfully')

    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/addproducts.html', {'sdata': sellerdata, 'sname': userprofile})

def MyProducts(request):
    myproducts=Product.objects.filter(seller=request.user)

    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/sellerproducts.html', {'sdata': sellerdata, 'sname': userprofile,'mpdata':myproducts})


def SellerSearch(request):
    try:
        if request.method == "POST":
            search = request.POST.get("search")
            if search:
                srdata = Product.objects.filter(Q(seller_id=request.user) & Q(pname__icontains=search))
            
        sellerdata = SellerDetails.objects.filter(seller=request.user)
        userprofile = request.user    
        return render(request, 'admin/sellersearch.html', {'srdata': srdata, 'sdata': sellerdata, 'sname': userprofile, 'search': search})
    except:
        return HttpResponseRedirect('/sellerpanel/')



def DeleteProducts(request,id):
    Product.objects.filter(pk=id).delete()
    sellerdata = SellerDetails.objects.filter(seller=request.user)
    userprofile = request.user
    return render(request, 'admin/productdeleted.html', {'sdata': sellerdata, 'sname': userprofile})

def AdminLogin(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass1")
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request,user)
            return HttpResponseRedirect("/adminpanel/")
    return render(request,'admin/AdminLogin.html')

def AdminPanel(request):
    if request.user.is_superuser and request.user.is_authenticated:
        rdata=RegisterationRequest.objects.all().order_by('-id')[:3]
        return render(request,'admin/AdminPanel.html',{'rdata':rdata})
    else:
        return HttpResponseRedirect('/adminlogin/')

def AdminLogout(request):
    logout(request)
    return HttpResponseRedirect('/adminlogin/')

def AdminSearch(request):
    try:
        if request.method == "POST":
            search = request.POST.get("search")
            if search:
                srdata=Product.objects.filter(Q(category=search) | Q(pname__icontains=search) | Q(brand=search) | Q(desc__icontains=search) | Q(price__icontains=search))
              
        return render(request, 'admin/adminsearch.html', {'srdata': srdata,'search': search})
    except:
        return HttpResponseRedirect('/adminpanel/')

def FurnCategory(request,pref):
    furncatproducts=Product.objects.filter(preference=pref)
    return render(request, 'admin/furncategory.html', {'fcdata':furncatproducts,'pref':pref})

def FurnDetails(request,id):
    
    slddata=Product.objects.filter(pk=id)
    return render(request, 'admin/furndetails.html', {'fddata':slddata})








    

        
        

   

        
    










    

    







        
        

    


    




        

    








