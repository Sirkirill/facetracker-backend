from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from photos.models import Post
from photos.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('move__camera__to_room__company')\
        .filter(move__camera__to_room__company__is_active=True)
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.select_related('move__camera__to_room__company')\
            .filter(move__camera__to_room__company_id=request.user.company_id)\
            .order_by('-move__date')[:60]
        return Response(data=self.serializer_class(queryset, many=True).data)
