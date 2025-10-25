from rest_framework import serializers
from .models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'updated_at', 'approved_by', 'approved_at', 'rejection_reason')
