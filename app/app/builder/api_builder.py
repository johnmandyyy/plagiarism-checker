from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import *
from app.helpers.helpers import SerializerHelpers
from ..api import *
from django.db import models
from django.views.decorators.csrf import csrf_exempt

class APIBuilder:

    def __init__(self, model_name: str, app_name: str, model_instance: models) -> None:
        """An API Generics Builder"""

        self.model_name = model_name
        self.model = model_instance
        self.app_name = app_name
        self.list_create = None
        self.get_update_destroy = None

    def build(self):

        class ListCreate(ListCreateAPIView):

            queryset = self.model.objects.all()
            serializer_class = SerializerHelpers().create_serializer(
                self.model_name, self.app_name
            )

            def __init__(self):
                self.authentication_classes = []

            @csrf_exempt
            def post(self, request, *args, **kwargs):
                return super().post(request, *args, **kwargs)

        class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):

            queryset = self.model.objects.all()
            serializer_class = SerializerHelpers().create_serializer(
                self.model_name, self.app_name
            )
            lookup_field = "pk"

        self.list_create = ListCreate()
        self.get_update_destroy = GetUpdateDestroy()

        return self
