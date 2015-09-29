#! coding: utf-8
from django.contrib import admin
from web.models import  Album, Photo, Article, ContactTypes, Contacts

class AlbumInLine(admin.StackedInline):
    model = Photo
    extra = 5

class AdminAlbum(admin.ModelAdmin):
    inlines = [AlbumInLine, ]

class AdminFoto(admin.ModelAdmin):
    admin.site.disable_action('delete_selected')
    def full_delete_selected(self, request, obj):
        for o in obj.all():
            o.delete()
    full_delete_selected.short_description = 'Удалить выбранные иллюстрации'
    actions = ['full_delete_selected']
    list_display = ('title', 'album', 'img', 'img_html', )

admin.site.register(Article)
admin.site.register(Album, AdminAlbum)
admin.site.register(Photo, AdminFoto)
admin.site.register(ContactTypes)
admin.site.register(Contacts)

