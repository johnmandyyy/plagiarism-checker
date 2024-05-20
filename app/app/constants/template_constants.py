from app.builder.template_builder import Builder
from app.constants import app_constants

HOME = (
    Builder()
    .addPage("app/home.html")
    .addTitle("home")
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
