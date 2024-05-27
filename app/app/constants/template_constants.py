from app.builder.template_builder import Builder
from app.constants import app_constants
from app.models import *
HOME = (
    Builder()
    .addPage("app/home.html")
    .addTitle("home")
    .addContext(
    {
        "title": "Home - Page",
        "obj_name": "home",
        "research": len(Research.objects.all()),
        "credibility": len(Credibility.objects.all()),
        "datasets": len(Datasets.objects.all()),
        "plagiarism": len(Credibility.objects.all().filter(is_plagirized = True)),
    }
    )
)

HOME.build()

DATASETS = (
    Builder()
    .addPage("app/datasets.html")
    .addTitle("datasets")
)

DATASETS.build()

LIBRARY = (
    Builder()
    .addPage("app/library.html")
    .addTitle("library")
)

LIBRARY.build()

CREDIBILITY = (
    Builder()
    .addPage("app/credibility.html")
    .addTitle("credibility")
)

CREDIBILITY.build()

LOGIN = (
    Builder()
    .addPage("app/login.html")
    .addTitle("login")
    .addContext(
        {
            "title": "Login - Page",
            "obj_name": "login",
            "app_name": app_constants.SOFTWARE_NAME,
            "app_desc": app_constants.SOFTWARE_DESCRIPTION
        }
    )
)
LOGIN.build()
