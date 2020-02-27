from django.views.generic import TemplateView


class AgreementView(TemplateView):
    template_name = 'core/agreement.html'


class ApplicationView(TemplateView):
    template_name = 'core/application.html'


class IndexView(TemplateView):
    template_name = 'core/index.html'
