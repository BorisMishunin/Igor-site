# coding: utf-8

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.mail import send_mail

from models import Article, Album, Photo, Contacts
from forms import MailForm

def index(request):
     article_list = Article.objects.order_by('title')
     query_list = [(article, Photo.objects.filter(album = article.album)) for article in article_list]
     contacts_list = Contacts.objects.order_by('contact_type')
     form = MailForm(request.POST)
     context_dict = {'article_list':query_list, 'contacts_list':contacts_list, 'form':form}
     return render(request, 'web/index.html', context_dict)

@csrf_exempt
def show_img(request):
     if request.method == "POST":
          currpage = request.POST.get('current_page')
          curralbum = request.POST.get('current_album')
          currpage = int(currpage) if currpage != None else 1
          photos = Photo.objects.filter()#album = curralbum)
          page = Paginator(photos, 1).page(currpage)

          data = {}
          data['images'] = page
          html = render_to_string('web/show_img.html', data)
     else:
          html = 'no'

     return  HttpResponse(html, content_type="text/html")


def sent_mail(request):
     send_mail('Subject here', 'Here is the message.', 'from@example.com', ['mbaforever@gmail.com'], fail_silently=False)
     return render(request, 'web/index.html')




