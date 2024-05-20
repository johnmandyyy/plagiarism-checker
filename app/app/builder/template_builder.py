from django.shortcuts import render
from datetime import datetime


class TemplateBuilder:
    """A template builder class."""

    def __init__(self):

        self.__Page = None
        self.__Title = None

    def setPage(self, page: str) -> None:
        """A method used to set page location"""
        self.__Page = page

    def setTitle(self, title: str) -> None:
        """A method used to set title"""
        self.__Title = title

    def getProps(self):
        return {"page": self.__Page, "title": self.__Title}


class Builder:

    def __init__(self):
        self.instance = TemplateBuilder()
        self.Page = None
        self.Context = None
        self.initialize()

    def addPage(self, ingridients) -> TemplateBuilder:
        self.instance.setPage(ingridients)
        return self

    def addTitle(self, ingridients) -> TemplateBuilder:
        self.instance.setTitle(ingridients)
        return self

    def addContext(self, context={}) -> TemplateBuilder:
        if len(context) < 1:
            context = self.Context
        else:
            self.Context = context

        self.Context = context
        return self

    def initialize(self):
        self.Context = {
            "title": self.instance.getProps()["title"],
            "date": str(datetime.now()),
            "obj_name": str(self.instance.getProps()["title"]).lower(),
        }

    def build(self) -> TemplateBuilder:
        """A method used to build the object."""
        self.Page = self.instance.getProps()["page"]
        return self.instance

    def render_page(self, request):
        """A method to render when there is an error in the page."""
        try:
            return render(request, self.Page, self.Context)
        except Exception as e:
            # Render an Error Page
            return render(
                request,
                "app/constants/error.html",
                {
                    "title": "Maintenance Page",
                    "date": str(datetime.now()),
                    "message": str(e),
                },
            )
