from django.apps import AppConfig


class BakeryDemoBaseAppConfig(AppConfig):
    label = "base"
    name = "bakerydemo.base"
    verbose_name = "Bakerydemo Base"

    def ready(self):
        from . import index  # noqa: F401
