"""
URL configuration for furniturestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from furnapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.Index,name='index'),
    path('display/',views.Display,name='display'),
    path('delete/<int:id>',views.Delete,name='delete'),
    path('update/<int:id>',views.Update,name='update'),
    path('userindex/',views.UserIndex,name='userindex'),
    path('base/',views.UserBase,name='base'),
    path('allproducts/',views.AllProducts,name='allproducts'),
    path('details/<int:id>/<str:category>/<str:brand>',views.Details,name='details'),
    path('cart/',views.AddCart,name='cart'),
    path('removecart/<int:id>',views.RemoveCart,name='removecart'),
    path('save/',views.SaveLater,name='save'),
    path('movecart/',views.MoveCart,name='movecart'),
    path('savedel/<int:id>',views.SaveDelete,name='savedel'),
    path('search/',views.ComponentSearch,name='search'),
    path('signup/',views.SignUp,name='signup'),
    path('',views.LogIn,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('preferpage/',views.Preferpage,name='preferpage'),
    path('adminpanel/',views.AdminSup,name='adminpanel'),
    path('sellerpanel/',views.SellerPanel,name='sellerpanel'),
    path('sellerlogin/',views.SellerLogin,name='sellerlogin'),
    # path('sellersignup/',views.SellerSignup,name='sellersignup'),
    path('selleregisteration/',views.SellerRegisteration,name='selleregisteration'),
    path('requestbrand/<int:id>',views.BrandDetails,name='requestbrand'),


    
    
    

    
   



    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA2_URL,document_root=settings.MEDIA2_ROOT)