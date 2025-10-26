from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from django.utils import timezone
from .models import Entry
from .serializers import EntrySerializer

# Create your views here.
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
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
        

    @extend_schema(
        summary="Approve a pending entry",
        description="Allows an admin to approve a pending entry. The entry must be in PENDING status.",
        responses={
            200: EntrySerializer,
            400: "Entry is not pending and cannot be approved.",
            403: "Forbidden - Admin access required.",
            404: "Entry not found."
        },
        examples=[
            OpenApiExample(
                'Approve Entry',
                value={},
                request_only=True,
                description='No request body required for approval.'
            ),
            OpenApiExample(
                'Approved Entry Response',
                value={
                    "id": 1,
                    "user": 1,
                    "title": "Sample Entry",
                    "amount": "100.00",
                    "entry_date": "2023-10-01",
                    "description": "Sample description",
                    "category": "PERSONAL",
                    "status": "APPROVED",
                    "approved_by": 2,
                    "approved_at": "2023-10-02T10:00:00Z",
                    "rejection_reason": None,
                    "created_at": "2023-10-01T09:00:00Z",
                    "updated_at": "2023-10-02T10:00:00Z"
                },
                response_only=True
            )
        ]
    )
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

    @extend_schema(
        summary="Reject a pending entry",
        description="Allows an admin to reject a pending entry with a required rejection reason. The entry must be in PENDING status.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'rejection_reason': {
                        'type': 'string',
                        'description': 'Reason for rejecting the entry.',
                        'example': 'Invalid amount or insufficient documentation.'
                    }
                },
                'required': ['rejection_reason']
            }
        },
        responses={
            200: EntrySerializer,
            400: "Entry is not pending and cannot be rejected. or Rejection reason is required.",
            403: "Forbidden - Admin access required.",
            404: "Entry not found."
        },
        examples=[
            OpenApiExample(
                'Reject Entry',
                value={
                    "rejection_reason": "Amount exceeds allowed limit."
                },
                request_only=True
            ),
            OpenApiExample(
                'Rejected Entry Response',
                value={
                    "id": 1,
                    "user": 1,
                    "title": "Sample Entry",
                    "amount": "100.00",
                    "entry_date": "2023-10-01",
                    "description": "Sample description",
                    "category": "PERSONAL",
                    "status": "REJECTED",
                    "approved_by": 2,
                    "approved_at": "2023-10-02T10:00:00Z",
                    "rejection_reason": "Amount exceeds allowed limit.",
                    "created_at": "2023-10-01T09:00:00Z",
                    "updated_at": "2023-10-02T10:00:00Z"
                },
                response_only=True
            )
        ]
    )
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
        return Response(self.get_serializer(entry).data)
