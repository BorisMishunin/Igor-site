#! coding: utf-8
from django.db import models
from django.conf import settings
from PIL import Image
import os


TYPE_OF_ARTICLES = ((0,'HTML'), (1,'ALBUM'))

def get_mini(path):
    file_path, filename = os.path.split(path)
    name, type = filename.split('.')
    return os.path.join(file_path, '%s_mini.%s' %(name,type))

def _add_mini(url):
    parts = url.split('.')
    parts.insert(-1, 'mini')
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)


def _del_mini(path):
    miniPath = _add_mini(path)
    if os.path.exists(miniPath):
        os.remove(miniPath)

class ContactTypes(models.Model):
    name = models.CharField("Вид контактной информации", max_length=100)
    icon = models.ImageField("Иконка", upload_to = 'images')
    class Meta:
        ordering = ['name']
        verbose_name = 'Вид контактной информации'
        verbose_name_plural = 'Виды контактной информации'

    def __unicode__(self):
        return self.name

class Contacts(models.Model):
    contact_type = models.ForeignKey(ContactTypes, verbose_name='Вид контакта')
    contact_info = models.TextField(verbose_name='Значение')
    clickable = models.BooleanField(verbose_name='Это ссылка')

    @property
    def icon(self):
        img_url = self.contact_type.icon.url
        return '<img class = "contact_icon" src = "%s" height = 30px width = 30px>'% img_url

    class Meta:
        ordering = ['contact_type']
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контакты'

    def __unicode__(self):
        return '%s: %s' %(str(self.contact_type.name), str(self.contact_info))



class Album(models.Model):
    title = models.CharField("Название альбома", max_length=100)
    #img = models.ImageField("Изображение альбома", upload_to='images', help_text='Размер изображения 200px на 200px')
    class Meta:
        ordering = ['title']
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __unicode__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=128)
    type = models.IntegerField(choices=TYPE_OF_ARTICLES, default=0)
    body = models.TextField()
    album = models.ForeignKey(Album, verbose_name='Альбом')

    def __unicode__(self):
        return self.title

    #def __str__(self):
    #    return 'str: %s' % repr(self.title.encode("UTF-8"))

class Photo(models.Model):
    title = models.CharField("Название фотографии", max_length=100)
    album = models.ForeignKey(Album, verbose_name='Альбом')
    img = models.ImageField("Фото", upload_to = 'images', help_text='Желательно, чтоб фото было не большого размера')
    class Meta:
        ordering = ['title']
        verbose_name = 'Фото'
        verbose_name_plural = "Фотографии"

    @property
    def mini_path(self):
        return get_mini(self.img.path)

    @property
    def mini_url(self):
        img_url = self.img.url
        return get_mini(img_url) if os.path.exists(get_mini(self.img.path)) else img_url

    def img_html(self):
        img_url = self.img.url
        return '<a href= "%s"><img src = "%s" width = 214 heigth=161></a>'%(img_url, get_mini(img_url) if os.path.exists(get_mini(self.img.path)) else img_url)

    img_html.allow_tags = True

    @property
    def big_img(self):
        img_url = self.img.url
        return '<img class = "big_img" src = "%s">'% img_url

    @property
    def small_img(self):
        img_url = self.img.url
        return '<a href= "%s"><img src = "%s" width = %s heigth=%s></a>'%(img_url, get_mini(img_url) if os.path.exists(get_mini(self.img.path)) else img_url,'10%', '10%')

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        try:
            obj =  Photo.objects.get(id=self.id)
            if obj.img.path != self.img.path:
                _del_mini(obj.img.path)
                obj.img.delete()
        except:
            pass
        super(Photo, self).save()
        try:
            img = Image.open(self.img.path)
            img.thumbnail(
                (128, 200),
                Image.ANTIALIAS
            )
            img.save(self.mini_path, 'JPEG')
        except:
            pass


    def delete(self, using=None):
        try:
            obj = Photo.objects.get(id=self.id)
            _del_mini(obj.img.path)
            obj.img.delete()
        except (Photo.DoesNotExist, ValueError):
            pass
        super(Photo, self).delete()

    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})
