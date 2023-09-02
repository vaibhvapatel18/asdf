from django.contrib import admin
from django.urls import path,include
from apiapp.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordEmailView,Restaurantadd,EmailLinkPasswordResetView,Restaurantmanuadd,UserlikeRestaurant,Userlikemenuitem,UserlikeRestaurant,Usersavemenuitem
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('restaurantadd', Restaurantadd, basename='restaurantlist')
router.register('restaurantaddmenu', Restaurantmanuadd, basename='restaurantaddmenu')
# router.register('userlikerestaurant', UserlikeRestaurant, basename='userlikerestaurant')
# router.register('userlikemenuitem', Userlikemenuitem, basename='userlikemenuitem')


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name = 'changepassword'),
    path('resetpasswordlink/', SendPasswordEmailView.as_view(), name = 'resetpasswordlink'),
    path('resetpasswordemail/<uid>/<token>/', EmailLinkPasswordResetView.as_view(), name='resetpasswordemail'),
    path('userlikerestaurant/', UserlikeRestaurant.as_view(), name='userlikerestaurant'),
    path('userlikemenuitem/', Userlikemenuitem.as_view(), name='userlikemenuitem'),
    path('usersavemenuitem/', Usersavemenuitem.as_view(), name='usersavemenuitem'),
    # path('userunlikerestaurant/', UserunlikeRestaurant.as_view(), name='userunlikerestaurant/'),
    path('',include(router.urls)),

]