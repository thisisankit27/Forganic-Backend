from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import ArticleModel
from .serializers import ArticleSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from Authentication.models import VerifiedEmail


class SendNotificationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, id):
        try:
            article = ArticleModel.objects.get(id=id)
        except ArticleModel.DoesNotExist:
            return Response({"detail": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the list of user emails with verified emails
        recipient_list = [
            verified_email.user.email for verified_email in VerifiedEmail.objects.filter()]

        if not recipient_list:
            return Response({"detail": "No verified users with emails found"}, status=status.HTTP_404_NOT_FOUND)

        # Send notification email to all verified users
        subject = "New Article Notification"
        message = f"A new article '{article.title}' has been published. Check it out!"
        from_email = settings.EMAIL_HOST_USER  # Update with your email

        send_mail(subject, message, from_email, recipient_list)

        return Response({"detail": "Email notification sent successfully"}, status=status.HTTP_200_OK)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any user to list comments with item_id
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        if serializer.is_valid():
            # Only update 'comment' and 'rating' fields
            for attr, value in serializer.validated_data.items():
                if attr in ['title', 'short_description', 'description']:
                    setattr(instance, attr, value)

            instance.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
