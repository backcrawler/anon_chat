from tornado.web import url

from . import views

urlpatterns = [
    url(r'/chat/', views.IndexView, name='main'),
    url(r'/link/', views.AjaxHandler, name='ajax'),
    url(r'/(\w+)/', views.MainWebsocket, name='ws'),
]