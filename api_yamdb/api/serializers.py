from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.core.mail import EmailMessage
import uuid
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ( "username", "email",)
        

class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.UUIDField()

    
# class CommentViewSet(viewsets.ModelViewSet):
#     """Класс для работы с комментариями."""
#     serializer_class = CommentSerializer
#     permission_classes = (AuthorOrReadOnly,)

#     def get_queryset(self):
#         """Изменение выдаваемого queryset."""
#         post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
#         return post.comments.all()

#     def perform_create(self, serializer):
#         """Создание комментария."""
#         post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
#         serializer.save(author=self.request.user, post=post)