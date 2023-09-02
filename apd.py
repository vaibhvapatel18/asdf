# class UserLikeResSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserLikeRetaurant
#         fields = '__all__'

#     def validate(self, attrs):
#         return attrs
#     def create(self, validate_data):
#         print(validate_data['restaurant'])
#         print(validate_data['user'])
#         print(validate_data['likes'])
#         if validate_data['likes'] == True:
#             likedata = UserLikeRetaurant.objects.filter(user = validate_data['user'], restaurant = validate_data['restaurant']).first()
#             print(likedata)
#             if likedata and likedata.likes == True:
#                 raise serializers.ValidationError("already liked")
#             likedata = UserLikeRetaurant.objects.filter(user = validate_data['user'], restaurant = validate_data['restaurant'],likes = False).all()
#             if likedata:
#                 likedata.delete()
#                 like = Restaurant.objects.get(name = validate_data['restaurant'])
#                 like.like += 1
#                 like.save()
#             like = Restaurant.objects.get(name = validate_data['restaurant'])
#             like.like += 1
#             like.save()
#             return UserLikeRetaurant.objects.create(**validate_data)
#         if validate_data['likes'] == False:
#             likedata = UserLikeRetaurant.objects.filter(user = validate_data['user'], restaurant = validate_data['restaurant']).first()
#             if likedata and likedata.likes == False:
#                     raise serializers.ValidationError("already unliked")
#             likedata = UserLikeRetaurant.objects.filter(user = validate_data['user'], restaurant = validate_data['restaurant'], likes = True).all()
#             if likedata:
#                 likedata.delete()
#                 like = Restaurant.objects.get(name = validate_data['restaurant'])
#                 like.like -= 1
#                 like.save()
#             like = Restaurant.objects.get(name = validate_data['restaurant'])
#             like.like -= 1
#             like.save()
#             return UserLikeRetaurant.objects.create(**validate_data)