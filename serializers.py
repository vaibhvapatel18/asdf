from rest_framework import serializers
from apiapp.models import User,Restaurant,MenuItem,UserLikeRetaurant,Userlikemenuitem,Usersavemenuitem
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail 
from django.conf import settings
from rest_framework.response import Response
from apiapp.models import UserLikeRetaurant


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style= {'input_type':'password'}, write_only = True) 
    class Meta: 
        model = User
        fields=['email','name','password','password2', 'tc']
        extra_kwargs={'write_only':True}

    def validate(self, attrs):
        password = attrs.get('password') 
        password2 = attrs.get('password2') 
        if password != password2:
            raise serializers.ValidationError("password not match")
        return attrs
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ["email", "password"]
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255 ,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255 ,style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password') 
        password2 = attrs.get('password2') 
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("password not match")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        Fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email') 
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/resetpasswordemail/'+uid+'/'+token
            subject = 'password reset'
            massage = f"your password reset linl==> {link}"
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, massage, from_email, [user.email])
            print(link)
            return attrs
        else:
            raise serializers.ValidationError("not register user")


class EmailLinkPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255 ,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255 ,style={'input_type':'password'},write_only=True)

    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password') 
            password2 = attrs.get('password2') 
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError("password not match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValueError('token not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValueError('token not valid or expired')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'like','price','name' ]

class RestaurantSerializer(serializers.ModelSerializer):
    manuiteams = MenuSerializer(many=True,read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name','like', 'description','user', 'address','phone_number','opening_time','closing_time', 'manuiteams']
        
class MenuItemCreateSerializer(serializers.ModelSerializer):
        restaurant = RestaurantSerializer(read_only=True)
        class Meta:
            model = MenuItem
            fields = ['restaurant','id','price','name']


class UserLikeResSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLikeRetaurant
        fields = ['restaurant','likes']
    def validate(self, validated_data):
        global user
        user = self.context.get('user')
        restaurant = validated_data['restaurant']
        likes = validated_data['likes']

        existing_data = UserLikeRetaurant.objects.filter(user=user, restaurant=restaurant,likes=True).first()
        existing_da = UserLikeRetaurant.objects.filter(user=user, restaurant=restaurant,likes=False).first()

        if likes == True: 
            if likes == True and existing_data:
                raise serializers.ValidationError("already liked" )
            elif likes == True and not existing_data and not existing_da:
                rest = Restaurant.objects.get(name=restaurant)
                rest.like += 1
                print("ok")
                rest.save()
                UserLikeRetaurant.objects.create(user=user, restaurant=restaurant, likes=likes)
                return validated_data
            elif likes == True and existing_da:
                p = UserLikeRetaurant.objects.get(user=user, restaurant=restaurant,likes=False)
                p.delete()
                rest = Restaurant.objects.get(name=restaurant)
                rest.like += 1
                print("ok")
                rest.save()
                return validated_data

        if likes == False: 
            if likes == False and existing_da:
                raise serializers.ValidationError("already unliked" )
            elif likes == False and not existing_data and not existing_da:
                rest = Restaurant.objects.get(name=restaurant)
                rest.like -= 1
                print("ok")
                rest.save()
                UserLikeRetaurant.objects.create(user=user, restaurant=restaurant, likes=likes)
                return validated_data
            elif likes == False and existing_data:
                p = UserLikeRetaurant.objects.get(user=user, restaurant=restaurant,likes=True)
                p.delete()
                rest = Restaurant.objects.get(name=restaurant)
                rest.like -= 1
                print("ok")
                rest.save()
                return validated_data
    def create(self, validated_data):
        return validated_data

        
    
class UserLikemenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userlikemenuitem
        fields = ['menu','likes']
    def validate(self, attrs):
        
        user = self.context.get('user')
        return attrs
    def create(self, validated_data):
        user = self.context.get('user')
        menu = validated_data['menu']
        likes = validated_data['likes']

        existing_like = Userlikemenuitem.objects.filter(user=user, menu=menu,likes=True).first()
        existing_li = Userlikemenuitem.objects.filter(user=user, menu=menu,likes=False).first()
        
        if likes == True: 
            if likes == True and existing_like:
                raise serializers.ValidationError("already liked" )
            elif likes == True and not existing_like and not existing_li:
                menu = MenuItem.objects.get(name = menu)
                menu.like += 1
                print("ok")
                menu.save()
                Userlikemenuitem.objects.create(user=user, menu=menu, likes=likes)
                return validated_data
            elif likes == True and existing_li:
                p = Userlikemenuitem.objects.get(user=user, menu=menu, likes=False)
                p.delete()
                menu = MenuItem.objects.get(name = menu)
                menu.like += 1
                print("ok")
                menu.save()
                return validated_data
        if likes == False: 
            if likes == False and existing_li:
                raise serializers.ValidationError("already unliked" )
            elif likes == False and not existing_like and not existing_li:
                menu = MenuItem.objects.get(name = menu)
                menu.like -= 1
                print("ok")
                menu.save()
                Userlikemenuitem.objects.create(user=user, menu=menu, likes=likes)
                return validated_data
            elif likes == False and existing_like:
                p = Userlikemenuitem.objects.get(user=user, menu=menu, likes=True)
                p.delete()
                menu = MenuItem.objects.get(name = menu)
                menu.like -= 1
                print("ok")
                menu.save()
                return validated_data
    

class UsersavemenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usersavemenuitem
        fields = ['menu','sdate']
    def validate(self, attrs):
        return attrs
    
    def create(self, validate_data):
        sdate=validate_data['sdate']
        menu = validate_data['menu']
        user = self.context.get('user')

        menusave = Usersavemenuitem.objects.filter(user = user , menu = menu, sdate=True).first()

        if sdate == True:
            if sdate == True and not menusave:
                Usersavemenuitem.objects.create(user=user, menu=menu, sdate=True)
                return validate_data
            elif sdate == True and menusave:
                raise serializers.ValidationError("already saved" )
        elif sdate == False:
            if sdate == False and menusave:
                menusav = Usersavemenuitem.objects.get(user = user , menu = menu, sdate=True)
                menusav.delete()
                return validate_data
            elif sdate == False and not menusave:
                print('ok')
                raise serializers.ValidationError("not saved menu" )
  

