from django.views.generic import TemplateView

# Create your views here.
class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'    

class HomePageView(TemplateView):
    template_name = 'index.html'