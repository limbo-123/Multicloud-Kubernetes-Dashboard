from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/exec/(?P<namespace>[^/]+)/(?P<pod_name>[^/]+)/(?P<container_name>[^/]+)/$', consumers.ExecConsumer.as_asgi()),
]
