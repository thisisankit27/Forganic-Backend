from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import Comments, Item
from .serializers import CommentsSerializer
from django.db.models import Avg

# Create your views here.

from rest_framework import permissions


class IsCommentCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request user is the creator of the comment
        return obj.created_by == request.user.username


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Comments.objects.all()
        # Get the 'item_id' from the URL query parameters
        item_id = self.request.query_params.get('item_id')
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        return queryset

    def get_permissions(self):
        if self.action == 'list' and 'item_id' in self.request.query_params:
            # Allow any user to list comments with item_id
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Allow only the comment's creator to update or delete
            return [IsCommentCreator()]
        elif self.action == 'create':
            # Allow any authenticated user (including admins) to create comments
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        try:
            # Attempt to save the comment with created_by set to the username of the authenticated user
            serializer.save(created_by=self.request.user.username)

            self.update_item_average_rating(
                serializer.validated_data['item_id'].id)
        except Exception as e:
            # Handle any exceptions that may occur during the saving process
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        if serializer.is_valid():
            # Only update 'comment' and 'rating' fields
            for attr, value in serializer.validated_data.items():
                if attr in ['comment', 'rating']:
                    setattr(instance, attr, value)

            item_id = instance.item_id.id  # item_id is a ForeignKey
            instance.save()
            self.update_item_average_rating(item_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_item_average_rating(self, item_id):
        # Calculate and update the average rating for the associated item
        avg_rating = Comments.objects.filter(
            item_id=item_id).aggregate(Avg('rating'))['rating__avg']
        Item.objects.filter(id=item_id).update(rating=avg_rating)
