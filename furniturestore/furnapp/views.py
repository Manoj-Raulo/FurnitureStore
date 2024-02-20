from django.shortcuts import render,HttpResponseRedirect,HttpResponse

from .models import Product,Offers,Cart,Save,RegisterationRequest,SellerDetails,Address,Order,UserDetails

from .forms import ProductForm

from datetime import date,timedelta,datetime

from django.contrib import messages

from django.db.models import Q,F

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail

from django.conf import settings

import uuid

from django.urls import reverse

import razorpay

from django.views.decorators.csrf import csrf_exempt



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
        profile=UserDetails.objects.filter(user=request.user)
        



        count=Cart.objects.filter(user_id=request.user).count()
        return render(request,"user/base.html",{'count':count,'user':userprofile,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')

def UserIndex(request):
    if request.user.is_authenticated:
        Ndata=Product.objects.all().order_by('-id')[:7]
        odata=Offers.objects.all()
        # best seller from order table
        Bdata=Product.objects.all()[:7]
        count=Cart.objects.filter(user_id=request.user).count()
        profile=UserDetails.objects.filter(user=request.user)

        return render(request,"user/index.html",{'odata':odata,"Ndata":Ndata,'bdata':Bdata,'count':count,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')

def AllProducts(request):
    if request.user.is_authenticated:
        apdata=Product.objects.all()
        count=Cart.objects.filter(user_id=request.user).count()
        profile=UserDetails.objects.filter(user=request.user)
        return render(request,"user/products.html",{'apdata':apdata,'count':count,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')

def Details(request,id,category,brand):
    if request.user.is_authenticated:
    
    
        date1=date.today()
        days=timedelta(days=7)
        delivery_date=date1+days
        ddata=Product.objects.filter(pk=id)
        similar_products=Product.objects.filter(category=category).exclude(id=id)
        brand_products=Product.objects.filter(brand=brand).exclude(id=id)
        count=Cart.objects.filter(user_id=request.user).count()
        profile=UserDetails.objects.filter(user=request.user)

        return render(request,"user/details.html",{"ddata":ddata,'ddate':delivery_date,'sdata':similar_products,'bproduct':brand_products,'count':count,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')

def AddCart(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            cid=request.POST.get('cid')
            filter1=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
            if int(cid) not in filter1:
                Cart.objects.create(product_id=cid,user=request.user)
            else:
                messages.success(request,'This product is already added to the cart')
            
        
        cpid=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        cartdata=Product.objects.filter(id__in=cpid)
        svid=Save.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        Savedata=Product.objects.filter(id__in=svid)
        amount=Product.objects.filter(id__in=cpid).values_list('price',flat=True)
        count=Cart.objects.filter(user_id=request.user).count()
        amt=0
        for i in amount:
            amt=amt+i
        profile=UserDetails.objects.filter(user=request.user)
        return render(request,'user/cart.html',{'cdata':cartdata,'svdata':Savedata,'amt':amt,'count':count,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')    

def SaveLater(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            sid=request.POST.get('sid')
            Cart.objects.filter(product_id=sid).delete()
            Save.objects.create(product_id=sid,user=request.user)
            
            return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/signup/')       

def MoveCart(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            sid2=request.POST.get('sid2')
            Save.objects.filter(product_id=sid2).delete()
            Cart.objects.create(product_id=sid2,user=request.user)
            return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/signup/')       
    
def RemoveCart(request,id):
    if request.user.is_authenticated:
        Cart.objects.filter(product_id=id).delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/signup/')

def SaveDelete(request,id):
    if request.user.is_authenticated:
        Save.objects.filter(product_id=id).delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/signup/')

def CartAddress(request):
    if request.user.is_authenticated:
        

        #Here we are fetching date from address table
        #product_id=id
        cid=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
    
        amount=Product.objects.filter(id__in=cid).values_list("price", flat=True)
        camt=0
        for i in list(amount):
            camt=camt+i

        count=Cart.objects.filter(user_id=request.user).count()
        data = Address.objects.filter(user_id=request.user)
        profile=UserDetails.objects.filter(user=request.user)    
        return render(request,'user/cartaddress.html',{"adata":data,'camt':camt,'count':count,'profile':profile})
            
    else:
        return HttpResponseRedirect("/signup/")

def DeleteAddress(request,id):
    if request.user.is_authenticated:
        Address.objects.filter(pk=id).delete() 
        messages.success(request,'Address Deleted Successfully')
        return HttpResponseRedirect('/cartaddress/')
    else:
        return HttpResponseRedirect("/signup/")

def CartPreorder(request,aid):
    if request.user.is_authenticated:
        address_data=Address.objects.filter(pk=aid)
        cid=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        product_data=Product.objects.filter(id__in=cid)

        date1=date.today()
        days=timedelta(days=7)
        delivery_date=date1+days
        count=Cart.objects.filter(user_id=request.user).count()
        amount=Product.objects.filter(id__in=cid).values_list("price", flat=True)
        camt=0
        for i in list(amount):
            camt=camt+i
            

        profile=UserDetails.objects.filter(user=request.user)
        return render(request,"user/cartpreorder.html",{"adata":address_data,"pdata":product_data,'date':delivery_date,'aid':aid,'count':count,'camt':camt,'profile':profile})
    else:
        return HttpResponseRedirect("/signup/")


def AllAddress(request):
    if request.user.is_authenticated:
        data = Address.objects.filter(user_id=request.user)
        profile=UserDetails.objects.filter(user=request.user)
        
        return render(request,"user/AllAddress.html",{"adata":data,'profile':profile})
    else:
        return HttpResponseRedirect("/signup/") 

def UpdateAddress(request,aid):
    if request.user.is_authenticated:
        if request.method == "POST":
            uid=request.POST.get("uid")
            cname=request.POST.get("cname")
            flat=request.POST.get("flat")
            area=request.POST.get("area")
            landmark=request.POST.get("landmark")
            city=request.POST.get("city")
            state=request.POST.get("state")
            pincode=request.POST.get("pincode")
            contact=request.POST.get("contact")
            acontact=request.POST.get("acontact")
            Address.objects.filter(pk=aid).update(name=cname,flat=flat,area=area,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)
            return HttpResponseRedirect('/alladdress/')
                
        adata = Address.objects.filter(pk=aid)
        profile=UserDetails.objects.filter(user=request.user)

        return render(request,"user/updateddress.html",{"adata":adata,'profile':profile})
    else:
        return HttpResponseRedirect("/signup/") 

def AddnewAddress(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            cname=request.POST.get("cname")
            flat=request.POST.get("flat")
            area=request.POST.get("area")
            landmark=request.POST.get("landmark")
            city=request.POST.get("city")
            state=request.POST.get("state")
            pincode=request.POST.get("pincode")
            contact=request.POST.get("contact")
            acontact=request.POST.get("acontact")
            Address.objects.create(user=request.user,name=cname,flat=flat,area=area,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)
            return HttpResponseRedirect('/alladdress/')
        profile=UserDetails.objects.filter(user=request.user)
        return render(request,'user/addnewadd.html',{'profile':profile})
    else:
        return HttpResponseRedirect("/signup/")

def CartPayment(request,aid):
    client = razorpay.Client(auth=("rzp_test_XSrXax5DSnhkOL", "zze0FObUulnws58AD4flVJPI"))
    cid=Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        
    amount=Product.objects.filter(id__in=cid).values_list("price", flat=True)
    camt=0
    for i in list(amount):

        camt=camt+i

    context={}
    context['amt']=camt*100
    context['aid']=aid
    context['payment']=camt
        
        


    data = { "amount": camt, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)
        
    return render(request,'user/cartpay.html',context)
      
        
    

@csrf_exempt
def CartOrderConfirm(request,aid,payment):
    try:
        date1 = datetime.now()
        datef = date1.strftime("%Y%m%d%H%M%S")
        adata=Address.objects.filter(pk=aid)

        unique_id=str(uuid.uuid4().hex)[:6:]
        address_id = aid
        product_id = Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        current_date = datetime.now().date()
        days = timedelta(days=5)
        delivery_date = current_date + days
        delivery_date_final = delivery_date.strftime('%Y-%m-%d')

        oid=request.user

        order_id=f"WM{datef}-{unique_id}"
        for i in list(product_id):
            Order.objects.create(user=oid,product_id=i,address_id=address_id,order_id=order_id,order_date=current_date,Estimated_delivery_date=delivery_date_final)
        
            

        Oproduct_id=Order.objects.filter(user_id=request.user).values_list("product_id",flat=True)
        Cart.objects.filter(product_id__in=Oproduct_id).delete()
        

        return render(request,'user/cartorder_placed.html',{'adata':adata,'date':delivery_date})

        
        

            


            
        
    except:
        
        return render(request,'user/addressconfirm.html',{'adata':adata,'payment':payment})
         
    
        
            
    
    
    
        



def CartEditAddress(request,aid,payment):
    if request.user.is_authenticated:
        if request.method == "POST":
            uid=request.POST.get("uid")
            cname=request.POST.get("cname")
            flat=request.POST.get("flat")
            area=request.POST.get("area")
            landmark=request.POST.get("landmark")
            city=request.POST.get("city")
            state=request.POST.get("state")
            pincode=request.POST.get("pincode")
            contact=request.POST.get("contact")
            acontact=request.POST.get("acontact")
            Address.objects.filter(pk=aid).update(name=cname,flat=flat,area=area,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)
            
            return HttpResponseRedirect(reverse('cartorderconfirm', args=(aid,payment,)))
        profile=UserDetails.objects.filter(user=request.user)        
        adata = Address.objects.filter(pk=aid)

        return render(request,"user/carteditddress.html",{"adata":adata,'profile':profile})
    else:
        return HttpResponseRedirect("/signup/")


def AddressConfirm(request,aid):
    if request.user.is_authenticated:
        date1 = datetime.now()
        datef = date1.strftime("%Y%m%d%H%M%S")
        adata=Address.objects.filter(pk=aid)

        unique_id=str(uuid.uuid4().hex)[:6:]
        address_id = aid
        product_id = Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        current_date = datetime.now().date()
        days = timedelta(days=5)
        delivery_date = current_date + days
        delivery_date_final = delivery_date.strftime('%Y-%m-%d')

        oid=request.user

        order_id=f"WM{datef}-{unique_id}"
        for i in list(product_id):
            Order.objects.create(user=oid,product_id=i,address_id=address_id,order_id=order_id,order_date=current_date,Estimated_delivery_date=delivery_date_final)
        
            

        Oproduct_id=Order.objects.filter(user_id=request.user).values_list("product_id",flat=True)
        Cart.objects.filter(product_id__in=Oproduct_id).delete()
        profile=UserDetails.objects.filter(user=request.user)

        return render(request,'user/cartorder_placed.html',{'adata':adata,'date':delivery_date,'profile':profile})
    else:
        return HttpResponseRedirect("/signup/")




def ComponentSearch(request):

    if request.user.is_authenticated:
        try:
            if request.method=="POST":
                search=request.POST.get("search")
                sdata=Product.objects.filter(Q(category=search) | Q(pname__icontains=search) | Q(brand=search) | Q(desc__icontains=search) | Q(price__icontains=search))
                count=Cart.objects.filter(user_id=request.user).count()
            profile=UserDetails.objects.filter(user=request.user)
            return render(request,'user/search.html',{'sdata':sdata,'count':count,'profile':profile})
        except:
            return HttpResponseRedirect('/userindex/')
    else:
        return HttpResponseRedirect('/signup/')

def PayAddress(request,pid,amt):
    if request.user.is_authenticated:
        product_id=pid
        amount=amt
        
        adata = Address.objects.filter(user_id=request.user)
        count=Cart.objects.filter(user_id=request.user).count()
        profile=UserDetails.objects.filter(user=request.user)

        return render(request,'user/address.html',{"adata":adata,'bamt':amt,'count':count,'pid':product_id,'bamt':amount,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')


def Preorder(request,aid,pid,bamt):
    if request.user.is_authenticated:
        address_data=Address.objects.filter(pk=aid)
        product_data=Product.objects.filter(pk=pid)

        date1=date.today()
        days=timedelta(days=5)
        delivery_date=date1+days
        count=Cart.objects.filter(user_id=request.user).count()
        amount=bamt
        profile=UserDetails.objects.filter(user=request.user)
        return render(request,'user/preorder.html',{"adata":address_data,'pdata':product_data,'count':count,'bamt':amount,'date':delivery_date,'pid':pid,'aid':aid,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')
    
def Payment(request,aid,pid):
    if request.user.is_authenticated:
    
        product_amount=Product.objects.filter(pk=pid).values_list("price", flat=True)
        
        
        client = razorpay.Client(auth=("rzp_test_XSrXax5DSnhkOL", "zze0FObUulnws58AD4flVJPI"))
        amount=product_amount[0]
        
        print(amount)

        context={}
        context['amt']=amount*100
        context['aid']=aid
        context['pid']=pid
        context['payment']=amount


        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        return render(request,'user/pay.html',context)
    else:
        return HttpResponseRedirect('/signup/')

@csrf_exempt
def Orderconfirm(request,aid,pid,payment):
    
    try:
        date1 = datetime.now()
        datef = date1.strftime("%Y%m%d%H%M%S")
        adata=Address.objects.filter(pk=aid)

        unique_id=str(uuid.uuid4().hex)[:6:]
        address_id = aid
        product_id = pid
        current_date = datetime.now().date()
        days = timedelta(days=5)
        delivery_date = current_date + days
        delivery_date_final = delivery_date.strftime('%Y-%m-%d')

        oid=request.user

        order_id=f"WM{datef}-{unique_id}"
            
        Order.objects.create(user=oid,product_id=product_id,address_id=address_id,order_id=order_id,order_date=current_date,Estimated_delivery_date=delivery_date_final)
            

            

            


        
        return render(request,'user/order_placed.html',{'adata':adata,'date':delivery_date})
    except:
        return render(request,'user/payaddressconfirm.html',{'adata':adata,'pid':pid,'payment':payment})
    

def PayAddressConfirm(request,aid,pid):
    if request.user.is_authenticated:
        date1 = datetime.now()
        datef = date1.strftime("%Y%m%d%H%M%S")
        adata=Address.objects.filter(pk=aid)

        unique_id=str(uuid.uuid4().hex)[:6:]
        address_id = aid
        product_id = pid
        current_date = datetime.now().date()
        days = timedelta(days=5)
        delivery_date = current_date + days
        delivery_date_final = delivery_date.strftime('%Y-%m-%d')

        oid=request.user

        order_id=f"WM{datef}-{unique_id}"
        profile=UserDetails.objects.filter(user=request.user)
            
        Order.objects.create(user=oid,product_id=product_id,address_id=address_id,order_id=order_id,order_date=current_date,Estimated_delivery_date=delivery_date_final)
        return render(request,'user/order_placed.html',{'adata':adata,'date':delivery_date,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')   

def EditAddress(request,aid,pid):
    if request.user.is_authenticated:
        if request.method == "POST":
            uid=request.POST.get("uid")
            cname=request.POST.get("cname")
            flat=request.POST.get("flat")
            area=request.POST.get("area")
            landmark=request.POST.get("landmark")
            city=request.POST.get("city")
            state=request.POST.get("state")
            pincode=request.POST.get("pincode")
            contact=request.POST.get("contact")
            acontact=request.POST.get("acontact")
            Address.objects.filter(pk=aid).update(name=cname,flat=flat,area=area,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)
            # return HttpResponseRedirect('/alladdress/')
            return HttpResponseRedirect(reverse('payaddressconfirm', args=(aid,pid,)))
        profile=UserDetails.objects.filter(user=request.user)       
        adata = Address.objects.filter(pk=aid)

        return render(request,"user/editddress.html",{"adata":adata,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')   



        


        
    

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
        return HttpResponseRedirect('/login/')
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
    return HttpResponseRedirect('/login/')

def UserProfile(request):
    profile=UserDetails.objects.filter(user=request.user)
    
    udata=UserDetails.objects.filter(user=request.user)
    return render(request,'user/userprofile.html',{'udata':udata,'profile':profile})

def AddProfile(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        contact=request.POST.get('contact')
        address=request.POST.get('address')
        profileicon=request.FILES.get('profileicon')
        
        UserDetails.objects.create(user=request.user,fullname=uname,contact=contact,permanantaddress=address,profileimage=profileicon)
        return HttpResponseRedirect('/userprofile/')
    profile=UserDetails.objects.filter(user=request.user)


    return render(request,'user/addprofile.html',{'profile':profile})

def EditProfile(request, id):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        profileimage = request.FILES.get('profileimage')  # Access the uploaded image file
        
        user_details = UserDetails.objects.filter(user=request.user).first()
        if user_details:
            user_details.uname = uname
            user_details.contact = contact
            user_details.address = address
            
            if profileimage:
                user_details.profileimage = profileimage  # Update the profile image if a new image is uploaded
            user_details.save()
            
        return HttpResponseRedirect('/userprofile/')
    profile=UserDetails.objects.filter(user=request.user)
    
    udata = UserDetails.objects.filter(pk=id)
    return render(request, 'user/updateprofile.html', {'udata': udata,'profile':profile})




def Preferpage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pf=request.POST.get('room_type')
            pfdata=Product.objects.filter(preference=pf)
        profile=UserDetails.objects.filter(user=request.user)
            
        return render(request,'user/preference.html',{'pfdata':pfdata,'pf':pf,'profile':profile})
    else:
        return HttpResponseRedirect('/signup/')


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
    if request.user.is_superuser and request.user.is_authenticated:
        brdata=RegisterationRequest.objects.filter(pk=id)
        return render(request,'admin/requestbrand.html',{'brdata':brdata})
    else:
        return HttpResponseRedirect('/adminlogin/')



 
def SellerSignup(request):
    if request.method=='POST':
        bname=request.POST.get('bname')
        email=request.POST.get('email')
        rid=request.POST.get('id')
        contact=request.POST.get('contact')
        shopaddress=request.POST.get('shopaddress')
        branddesc=request.POST.get('branddesc')
        

        



        password=str(uuid.uuid4().hex)[:8:]
        bname1=bname+"@seller"

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
    messages.success(request,"Seller Added Successfully....")
    return HttpResponseRedirect("/adminpanel/")

      
    
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
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
        sellerdata=SellerDetails.objects.filter(seller_id=request.user)
        userprofile=request.user
        return render(request,'admin/SellerProfile.html',{'sdata':sellerdata,'sname':userprofile})
    else:
        return HttpResponseRedirect("/selleregisteration/")


def SellerUpdate(request):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
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
    else:
        return HttpResponseRedirect("/selleregisteration/")

def SellerLogout(request):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
        logout(request)
        return HttpResponseRedirect('/sellerlogin/')
    else:
        return HttpResponseRedirect("/selleregisteration/")

def SellerCategory(request,pref):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:

        slcatproducts=Product.objects.filter(Q(seller=request.user) & Q(preference=pref))
        
        sellerdata = SellerDetails.objects.filter(seller=request.user)
        userprofile = request.user
        return render(request, 'admin/sellercategory.html', {'sdata': sellerdata, 'sname': userprofile,'cdata':slcatproducts,'pref':pref})
    else:
        return HttpResponseRedirect("/selleregisteration/")

def SelpDetails(request,id):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
    
        slddata=Product.objects.filter(pk=id)
        sellerdata = SellerDetails.objects.filter(seller=request.user)
        userprofile = request.user
        return render(request, 'admin/selpdetails.html', {'sdata': sellerdata, 'sname': userprofile,'slddata':slddata})
    else:
        return HttpResponseRedirect("/selleregisteration/")

def EditProducts(request,id):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
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
    else:
        return HttpResponseRedirect("/selleregisteration/")

def AddProducts(request):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
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
            return HttpResponseRedirect('/myprod/')

        sellerdata = SellerDetails.objects.filter(seller=request.user)
        userprofile = request.user
        return render(request, 'admin/addproducts.html', {'sdata': sellerdata, 'sname': userprofile})
    else:
        return HttpResponseRedirect("/selleregisteration/")

def MyProducts(request):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
        myproducts=Product.objects.filter(seller=request.user)

        sellerdata = SellerDetails.objects.filter(seller=request.user)
        userprofile = request.user
        return render(request, 'admin/sellerproducts.html', {'sdata': sellerdata, 'sname': userprofile,'mpdata':myproducts})
    else:
        return HttpResponseRedirect("/selleregisteration/")


def SellerSearch(request):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
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
    else:
        return HttpResponseRedirect("/selleregisteration/")



def DeleteProducts(request,id):
    if request.user.is_staff and request.user.is_authenticated and not  request.user.is_superuser:
        Product.objects.filter(pk=id).delete()
        sellerdata = SellerDetails.objects.filter(seller=request.user)
        userprofile = request.user
        return render(request, 'admin/productdeleted.html', {'sdata': sellerdata, 'sname': userprofile})
    else:
        return HttpResponseRedirect("/selleregisteration/")

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
        odata=Offers.objects.all()
        return render(request,'admin/AdminPanel.html',{'rdata':rdata,'odata':odata})
    else:
        return HttpResponseRedirect('/adminlogin/')

def AdminLogout(request):
    if request.user.is_superuser and request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/adminlogin/')
    else:
        return HttpResponseRedirect('/adminlogin/')

def AdminSearch(request):
    if request.user.is_superuser and request.user.is_authenticated:
        try:
            if request.method == "POST":
                search = request.POST.get("search")
                if search:
                    srdata=Product.objects.filter(Q(category=search) | Q(pname__icontains=search) | Q(brand=search) | Q(desc__icontains=search) | Q(price__icontains=search))
                
            return render(request, 'admin/adminsearch.html', {'srdata': srdata,'search': search})
        except:
            return HttpResponseRedirect('/adminpanel/')
    else:
        return HttpResponseRedirect('/adminlogin/')

def FurnCategory(request,pref):
    if request.user.is_superuser and request.user.is_authenticated:
        furncatproducts=Product.objects.filter(preference=pref)
        return render(request, 'admin/furncategory.html', {'fcdata':furncatproducts,'pref':pref})
    else:
        return HttpResponseRedirect('/adminlogin/')

def FurnDetails(request,id):
    if request.user.is_superuser and request.user.is_authenticated:
    
        slddata=Product.objects.filter(pk=id)
        return render(request, 'admin/furndetails.html', {'fddata':slddata})
    else:
        return HttpResponseRedirect('/adminlogin/')

def EditFurnproducts(request,id):
    if request.user.is_superuser and request.user.is_authenticated:
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
            return HttpResponseRedirect(reverse('furndetails', args=(pid,)))
        pdata=Product.objects.filter(pk=id)
        return render(request, 'admin/EditfurnProducts.html', {'pdata':pdata})
    else:
        return HttpResponseRedirect('/adminlogin/')

def AllFurnitures(request):
    if request.user.is_superuser and request.user.is_authenticated:
        Allproducts=Product.objects.all()
        return render(request, 'admin/allfurnitures.html', {'aldata':Allproducts})
    else:
        return HttpResponseRedirect('/adminlogin/')

def DeleteFurniture(request,id):
    if request.user.is_superuser and request.user.is_authenticated:
        Product.objects.filter(pk=id).delete()
        
        return render(request, 'admin/furndeleted.html')
    else:
        return HttpResponseRedirect('/adminlogin/')

def AdminProfile(request):
    if request.user.is_superuser and request.user.is_authenticated:
    
        return render(request,'admin/AdminProfile.html')
    else:
        return HttpResponseRedirect('/adminlogin/')

def PublicBase(request):
    return render(request,"public/base.html")
    


def PublicIndex(request):
    Ndata=Product.objects.all().order_by('-id')[:7]
    odata=Offers.objects.all()
        # best seller from order table
    Bdata=Product.objects.all()[:7]
    

    return render(request,"public/index.html",{'odata':odata,"Ndata":Ndata,'bdata':Bdata})

def PublicSearch(request):
    try:
        if request.method=="POST":
                search=request.POST.get("search")
                sdata=Product.objects.filter(Q(category=search) | Q(pname__icontains=search) | Q(brand=search) | Q(desc__icontains=search) | Q(price__icontains=search))
                
        return render(request,'public/search.html',{'sdata':sdata})
    except:
        return HttpResponseRedirect('/publicindex/')

def PublicProducts(request):
    apdata=Product.objects.all()
        
    return render(request,"public/products.html",{'apdata':apdata})

def ProductDetails(request,id,category,brand):
    date1=date.today()
    days=timedelta(days=7)
    delivery_date=date1+days
    ddata=Product.objects.filter(pk=id)
    similar_products=Product.objects.filter(category=category).exclude(id=id)
    brand_products=Product.objects.filter(brand=brand).exclude(id=id)
    

    return render(request,"public/details.html",{"ddata":ddata,'ddate':delivery_date,'sdata':similar_products,'bproduct':brand_products})

def PublicPrefer(request):
    if request.method == 'POST':

        pf=request.POST.get('room_type')
        pfdata=Product.objects.filter(preference=pf)
            
        return render(request,'public/preference.html',{'pfdata':pfdata,'pf':pf})

def UpdateOffers(request,id):
    if request.method=='POST':
        
        
        offer1=request.FILES.get('offer1')
        offer2=request.FILES.get('offer2')
        offer3=request.FILES.get('offer3')
        offer4=request.FILES.get('offer4')
        offer5=request.FILES.get('offer5')
        offer_details = Offers.objects.filter(pk=3).first()
        
        if offer1:
            offer_details.offer1=offer1
        if offer2:
            offer_details.offer2=offer2
        if offer3:
            offer_details.offer3=offer3
        if offer4:
            offer_details.offer4=offer4
        if offer5:
            offer_details.offer5=offer5
        offer_details.save()
        return HttpResponseRedirect('/userindex/')


        # Offers.objects.filter(pk=oid).update(offer1=offer1,offer2=offer2,offer3=offer3,offer4=offer4,offer5=offer5)
        



    odata=Offers.objects.all()
    return render(request,'admin/updateoffer.html',{'odata':odata})









    

        
        

   

        
    










    

    







        
        

    


    




        

    








