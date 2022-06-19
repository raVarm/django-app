from re import template
from sre_constants import SUCCESS
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm,PassResetForm,setPass

urlpatterns = [
    path('', views.ProductView.as_view(), name='home' ),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('quantitycart/', views.quantitycart, name='quantitycart'),
    path('buy/', views.buy_now, name='buy-now'),
    # path('profile/', views.profile, name='profile'),

    path('profile/', views.ProfileView.as_view(),name='profile'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passchange.html',form_class = MyPasswordChangeForm,success_url="/passchanged/"), name='passchange'),
    path('passchanged/', auth_views.PasswordChangeDoneView.as_view(template_name="app/home.html"), name="passchanged"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/pass_reset.html', form_class=PassResetForm, success_url ='/password-reset/done/'), name='pass_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/pass_reset_done.html'), name="pass_reset_done" ),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/pass_reset_confirm.html',form_class = setPass,success_url="/password-reset-complete/"), name='pass_reset_confirm'),    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='pass_reset_complete'),

    path('mobile/', views.mobile, name='mobile'),
    path('laptop/', views.laptop, name='laptop'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form = LoginForm), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout' ),
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/',views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.paymentdone, name='paymentdone'),
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
