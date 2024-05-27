"""
Definition of urls for app.
"""

from django.urls import path, include
from django.contrib import admin
from app.views import TemplateView
from .api import *
import app.constants.url_constants as URLConstants
from app.constants import app_constants
from django.conf.urls.static import static
from . import settings
from app.api import AnalyzePaper

MainView = TemplateView()

list_create_patterns = URLConstants.GenericAPI.list_create_patterns
get_update_destroy_patterns = URLConstants.GenericAPI.retrieve_update_delete_patterns

api_patterns = [
    path("api/", include((list_create_patterns, app_constants.APP_NAME))),
    path("api/", include((get_update_destroy_patterns, app_constants.APP_NAME))),
]

predefined_patterns = [path("api/analyze-paper/<str:id>/", AnalyzePaper.as_view())]

template_patterns = [
    path("home/", MainView.home, name="home"),
    path("datasets/", MainView.datasets, name="datasets"),
    path("library/", MainView.library, name="library"),
    path("credibility/", MainView.credibility, name="credibility"),
    path("admin/", admin.site.urls),
    path("logout/", MainView.user_logout, name="logout"),
    path("login/", MainView.login, name="login"),
    path("authenticate_user/", MainView.authenticate_user, name="authenticate_user"),
]

urlpatterns = (
    template_patterns
    + api_patterns + predefined_patterns
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
