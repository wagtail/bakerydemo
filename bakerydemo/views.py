from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from waffle.models import Flag
from .serializers import WaffleFlagSerializer

class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = Flag.objects.all()
    serializer_class = WaffleFlagSerializer
    lookup_field = 'name'
    
    @action(detail=False, methods=['post'])
    def update_feature(self, request):
        """
        Enable/Disable feature for this client
        Payload: {
            "feature_name": "dashboard",
            "is_enabled": true/false
        }
        """
        print("Request Data:", request.data)
        feature_name = request.data.get('feature_name')
        is_enabled = request.data.get('is_enabled', False)
        
        flag, created = Flag.objects.get_or_create(
            name=feature_name,
            defaults={'everyone': is_enabled}
        )
        
        if not created:
            flag.everyone = is_enabled
            flag.save()
        
        return Response({
            'status': 'success',
            'feature': feature_name,
            'enabled': is_enabled
        }, status=status.HTTP_200_OK)