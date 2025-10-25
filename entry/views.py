from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Entry
from .serializers import EntrySerializer
# Create your views here.
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Admins can see all entries.
        Users can only see their own entries.
        """
        if self.request.user.role == 'ADMIN':
            return Entry.objects.all()
        return Entry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        entry = self.get_object()
        if entry.status != 'PENDING':
            return Response(
                {"detail": "Entry is not pending and cannot be approved."},
                status=status.HTTP_400_BAD_REQUEST
            )
        entry.status = 'APPROVED'
        entry.approved_by = request.user
        entry.approved_at = timezone.now()
        entry.rejection_reason = None
        entry.save()
        return Response(self.get_serializer(entry).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        entry = self.get_object()
        if entry.status != 'PENDING':
            return Response(
                {"detail": "Entry is not pending and cannot be rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )
        rejection_reason = request.data.get('rejection_reason')
        if not rejection_reason:
            return Response(
                {"detail": "Rejection reason is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        entry.status = 'REJECTED'
        entry.approved_by = request.user
        entry.approved_at = timezone.now()
        entry.rejection_reason = rejection_reason
        entry.save()
        return Response(self.get_serializer(entry))
