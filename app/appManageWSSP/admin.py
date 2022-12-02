from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "last_login")

class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_es", "name_en", "modified", "user")

class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "modified", "user")

admin.site.register(User, UserAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Contact)
admin.site.register(MediaResource)
admin.site.register(Video)
admin.site.register(Imagen)
admin.site.register(HtmlDesign)
admin.site.register(Page)
admin.site.register(Section)
admin.site.register(ElementType)
admin.site.register(Element)
admin.site.register(DescriptiveArticle)
admin.site.register(GraphicArticle)
admin.site.register(HtmlArticle)
admin.site.register(Slider)
admin.site.register(SliderElement)
admin.site.register(Author)
admin.site.register(Publication)
admin.site.register(PublicationArticle)
admin.site.register(StyleSheet)