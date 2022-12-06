from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from .datavalidation import *
import os

# Create your models here.
def custom_media_path(instance, filename):
    return '{0}/{1}'.format(instance.mediaType, filename)

class User(AbstractUser):
    pass

    class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"
      db_table = "User"
      ordering = ["username"]

    def __str__(self):
      return f"{self.id}: {self.username}, {self.email}, {self.first_name}, {self.last_name}, {self.last_login}"

    def serialize(self):
      if self.last_login:
        lastlog = self.last_login.strftime("%b %d %Y, %I:%M %p")
      else:
        lastlog = None
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "last_login": lastlog
      }

class Country(models.Model):
    name_es = models.CharField(max_length=100, blank=False, unique=True)
    name_en = models.CharField(max_length=100, blank=False, unique=True)
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_countries")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "Country"
        ordering = ["id"]

    def clean(self):
        errors = {}
        errorlist = []
        if is_alphanumeric_space(self.name_es) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.name_es) > 50:
            errorlist.append("You must enter a maximum of 50 characters.")
        if errorlist:
            errors["name_es"] = errorlist
            errorlist = []

        if is_alphanumeric_space(self.name_en) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.name_en) > 50:
            errorlist.append("You must enter a maximum of 50 characters.")
        if errorlist:
            errors["name_en"] = errorlist

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.name_es}"

    def serialize(self):
        return {
            "id": self.id,
            "name_es": self.name_es,
            "name_en": self.name_en,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username
        }

class Region(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    scope = models.PositiveIntegerField(default=0, null=False, blank=False)
    country = models.ForeignKey("Country", null=False, blank=False, on_delete=models.CASCADE, related_name="country_regions")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_regions")

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        db_table = "Region"
        ordering = ["id"]

    def clean(self):
        errors = {}
        errorlist = []
        if is_alphanumeric_space(self.name) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.name) > 50:
            errorlist.append("You must enter a maximum of 100 characters.")
        if errorlist:
            errors["name"] = errorlist

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scope": self.scope,
            "country": self.country.id,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username
        }

class Province(models.Model):
    name = models.CharField(max_length=100, blank=False)
    region = models.ForeignKey("Region", null=False, blank=False, on_delete=models.CASCADE, related_name="region_provinces")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_provinces")

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        db_table = "Province"
        ordering = ["id"]

    def clean(self):
        errors = {}
        errorlist = []
        if is_alphanumeric_space(self.name) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.name) > 50:
            errorlist.append("You must enter a maximum of 100 characters.")
        if errorlist:
            errors["name"] = errorlist

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class District(models.Model):
    name = models.CharField(max_length=100, blank=False)
    altitude = models.IntegerField(default=0, null=False, blank=False)
    province = models.ForeignKey("Province", null=False, blank=False, on_delete=models.CASCADE, related_name="province_districts")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_districts")

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        db_table = "District"
        ordering = ["id"]

    def clean(self):
        errors = {}
        errorlist = []
        if is_alphanumeric_space(self.name) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.name) > 50:
            errorlist.append("You must enter a maximum of 100 characters.")
        if errorlist:
            errors["name"] = errorlist
            errorlist = []

        if is_positive_integer(self.altitude) is False:
            errorlist.append("You must enter a positive integer number.")
        if errorlist:
            errors["altitude"] = errorlist

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "altitude": self.altitude,
            "province": self.province,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class MediaResource(models.Model):
    media_type = [
        ("images","Image"),
        ("videos","Video")
    ]
    mediaType = models.CharField(max_length=6, blank=False, choices=media_type, default="images")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_mediaResources")

    class Meta:
        verbose_name = "MediaResource"
        verbose_name_plural = "MediaResources"
        db_table = "MediaResource"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.mediaType,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class Imagen(MediaResource):
    file_image = models.FileField(upload_to=custom_media_path, null=False, blank=False, unique=True, validators=[valid_image_extension, valid_image_file_size, valid_file_name])

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"
        db_table = "Imagen"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.file_image}, {self.modified}, {self.user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "file_name": self.file_image.name,
            "file_url": self.file_image.url,
            "mediaType": self.mediaType,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username
        }

    def delete(self):
        os.remove(settings.MEDIA_ROOT + self.file_image.name)
        return super(Imagen,self).delete()

class Video(MediaResource):
    title = models.CharField(max_length=100, blank=False, unique=True)
    video_source = [
        ("server","Server"),
        ("web","Web")
    ]
    source = models.CharField(max_length=10, blank=False, choices=video_source, default="server")
    web_url = models.URLField(null=True, blank=True, unique=False)
    file_video = models.FileField(upload_to=custom_media_path, null=True, blank=True, unique=False, validators=[valid_video_extension, valid_video_file_size, valid_file_name])

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        db_table = "Video"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title}, {self.web_url}, {self.file_video.name}, {self.modified}, {self.user.username}"

    def serialize(self):
        file_name = None
        file_url = None

        if self.file_video:
            file_name = self.file_video.name
            file_url = self.file_video.url

        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "web_url": self.web_url,
            "file_name": file_name,
            "file_url": file_url,
            "mediaType": self.mediaType,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username
        }

    def clean(self):
        errors = {}
        errorlist = []
        if self.title:
            if is_alphanumeric_space(self.title) is False:
                errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
            if len(self.title) > 50:
                errorlist.append("You must enter a maximum of 100 characters.")
            if errorlist:
                errors["title"] = errorlist

        if errors:
            raise ValidationError(errors)

    def delete(self):
        if self.file_video:
            os.remove(settings.MEDIA_ROOT + self.file_video.name)
        return super(Video,self).delete()

class HtmlDesign(models.Model):
    file_html = models.FileField(upload_to="html", null=False, blank=False, unique=True, validators=[valid_html_extension, valid_html_file_size, valid_file_name])
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_htmlDesigns")

    class Meta:
        verbose_name = "HtmlDesign"
        verbose_name_plural = "HtmlDesign"
        db_table = "HtmlDesign"
        ordering = ["id"]

    def __str__(self):
        return f"{self.file_html}"

    def serialize(self):
        return {
            "id": self.id,
            "file_name": self.file_html.name,
            "file_url": self.file_html.url,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username
        }

    def delete(self):
        os.remove(settings.MEDIA_ROOT + self.file_html.name)
        return super(HtmlDesign,self).delete()

class Author(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True)
    profession_es = models.CharField(max_length=250, blank=False)
    profession_en = models.CharField(max_length=250, blank=False)
    media = models.ForeignKey("MediaResource", null=False, blank=False, on_delete=models.CASCADE, related_name="mediaResource_authors")
    country = models.ForeignKey("Country", null=False, blank=False, on_delete=models.CASCADE, related_name="country_authors")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_authors")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "Author"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "profession_es": self.profession_es,
            "profession_es": self.profession_en,
            "media": self.media.id,
            "country": self.country.name_es,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username
        }

class Page(models.Model):
    title_es = models.CharField(max_length=50, blank=False, unique=True)
    title_en = models.CharField(max_length=50, blank=False, unique=True)
    styleSheetName = models.CharField(max_length=50, blank=False, unique=True)
    url_title_es = models.CharField(max_length=50, blank=False, unique=True)
    url_title_en = models.CharField(max_length=50, blank=False, unique=True)
    display_order = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_pages")

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        db_table = "Page"
        ordering = ["id"]

    def clean(self):
        errors = {}
        errorlist = []
        if is_alphanumeric_space(self.title_es) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.title_es) > 50:
            errorlist.append("You must enter a maximum of 50 characters.")
        if errorlist:
            errors["title_es"] = errorlist
            errorlist = []

        if is_alphanumeric_space(self.title_en) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.title_en) > 50:
            errorlist.append("You must enter a maximum of 50 characters.")
        if errorlist:
            errors["title_en"] = errorlist
            errorlist = []

        if is_positive_integer(self.display_order) is False:
            errorlist.append("You must enter a positive integer number.")
        if errorlist:
            errors["display_order"] = errorlist

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.title_es}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "styleSheetName": self.styleSheetName,
            "url_title_es": self.url_title_es,
            "url_title_en": self.url_title_en,
            "display_order": self.display_order,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class Section(models.Model):
    title_es = models.CharField(max_length=250, blank=False, unique=True)
    title_en = models.CharField(max_length=250, blank=False, unique=True)
    show_title = models.BooleanField(default=True, null=False, blank=False)
    display_order = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    media = models.ForeignKey("MediaResource", null=True, blank=True, on_delete=models.CASCADE, related_name="mediaResource_sections")
    page = models.ForeignKey("Page", null=False, blank=False, on_delete=models.CASCADE, related_name="page_sections")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_sections")

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        db_table = "Section"
        ordering = ["id"]

    def __str__(self):
        return f"{self.title_es}"

    def serialize(self):
        media_resource = None
        if self.media:
            media_resource = self.media.id

        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "display_order": self.display_order,
            "media_resource": media_resource,
            "page": self.page.id,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class ElementType(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    htmlName = models.CharField(max_length=100, blank=False, unique=True)
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_elementTypes")

    class Meta:
        verbose_name = "ElementType"
        verbose_name_plural = "ElementTypes"
        db_table = "ElementType"
        ordering = ["id"]

    def clean(self):
        errors = {}
        errorlist = []
        if is_alphanumeric_space(self.name) is False:
            errorlist.append("You must enter alphanumeric characters, spaces, hyphens and underscores.")
        if len(self.name) > 50:
            errorlist.append("You must enter a maximum of 50 characters.")
        if errorlist:
            errors["name"] = errorlist

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class Element(models.Model):
    title_es = models.CharField(max_length=250, blank=False, unique=True)
    title_en = models.CharField(max_length=250, blank=False, unique=True)
    show_title = models.BooleanField(default=True, null=False, blank=False)
    elementType = models.ForeignKey("ElementType", null=False, blank=False, on_delete=models.CASCADE, related_name="elemenType_elements")
    display_order = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    section = models.ForeignKey("Section", null=False, blank=False, on_delete=models.CASCADE, related_name="section_elements")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_elements")

    class Meta:
        verbose_name = "Element"
        verbose_name_plural = "Elements"
        db_table = "Element"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title_es}, {self.show_title}, {self.elementType.name}, {self.section.display_order}, {self.section.title_es}, {self.modified}, {self.user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "elementType": self.elementType,
            "display_order": self.display_order,
            "section": self.section.id,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class DescriptiveArticle(Element):
    description_es = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "DescriptiveArticle"
        verbose_name_plural = "DescriptiveArticles"
        db_table = "DescriptiveArticle"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.description_es}, {self.description_en}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "description_es": self.description_es,
            "description_en": self.description_en,
            "elementType": self.elementType.name,
            "display_order": self.display_order,
            "section": self.section.id,
        }

class GraphicArticle(Element):
    media = models.ForeignKey("MediaResource", null=False, blank=False, on_delete=models.CASCADE, related_name="mediaResource_graphicArticles")

    class Meta:
        verbose_name = "GraphicArticle"
        verbose_name_plural = "GraphicArticles"
        db_table = "GraphicArticle"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title_es}, {self.media}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "media": self.media.id,
            "elementType": self.elementType.name,
            "display_order": self.display_order,
            "section": self.section.id,
        }

class HtmlArticle(Element):
    htmlDesign = models.ForeignKey("HtmlDesign", null=False, blank=False, on_delete=models.CASCADE, related_name="htmlDesign_htmlArticles")

    class Meta:
        verbose_name = "htmlArticle"
        verbose_name_plural = "htmlArticles"
        db_table = "htmlArticle"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.htmlDesign}, {self.section.title_es}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "htmlDesign": self.htmlDesign.id,
            "elementType": self.elementType.name,
            "display_order": self.display_order,
            "section": self.section.id,
        }

class Slider(Element):
    sizes = [("fullscreen","Full Screen"), ("dinamic","Dinamic")]
    size = models.CharField(max_length=20, choices=sizes, default="fullscreen", blank=False)
    transition = [("interactive","Interactive"), ("automatic","Automatic")]
    transitionType = models.CharField(max_length=20, choices=transition, default="interactive", blank=False)
    display_sliderList = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        db_table = "Slider"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title_es}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "size": self.size,
            "transitionType": self.transitionType,
            "display_sliderList": self.display_sliderList,
            "elementType": self.elementType.name,
            "display_order": self.display_order,
            "section": self.section.id,
        }

class SliderElement(models.Model):
    title_es = models.CharField(max_length=250, blank=False, unique=True)
    title_en = models.CharField(max_length=250, blank=False, unique=True)
    show_title = models.BooleanField(default=True, null=False, blank=False)
    description_es = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    media_display_types = [("none","None"), ("simple","Simple"), ("multiple","Multiple")]
    media_display_type = models.CharField(max_length=20, choices=media_display_types, default="simple", blank=False)
    medias = models.ManyToManyField("MediaResource", null=True, blank=True, related_name="mediaResource_sliderElements")
    list_icon = models.ForeignKey("MediaResource", null=True, blank=True, on_delete=models.CASCADE, related_name="listIcon_slideElements")
    display_order = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    slider = models.ForeignKey("Slider", null=False, blank=False, on_delete=models.CASCADE, related_name="slider_sliderElements")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_sliderElements")

    class Meta:
        verbose_name = "SliderElement"
        verbose_name_plural = "SliderElements"
        db_table = "SliderElement"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title_es}, {self.media_display_type}, {self.display_order}, {self.slider.title_es}, {self.modified}, {self.user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "show_title": self.show_title,
            "description_es": self.description_es,
            "description_en": self.description_en,
            "media_display_type": self.media_display_type,
            "medias": self.medias.id,
            "list_icon": self.list_icon.id,
            "display_order": self.display_order,
            "slider": self.slider.id,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class Outstanding(Element):

    class Meta:
        verbose_name = "Outstanding"
        verbose_name_plural = "Outstandings"
        db_table = "Outstanding"
        ordering = ["id"]

    def __str__(self):
        return f"{self.title_es}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "elementType": self.elementType.name,
            "display_order": self.display_order,
            "section": self.section.id,
        }

class OutstandingArticle(models.Model):
    title_es = models.CharField(max_length=100, blank=False, unique=True)
    title_en = models.CharField(max_length=100, blank=False, unique=True)
    article_origins = [("web","Web"), ("local","Local")]
    article_origin = models.CharField(max_length=10, choices=article_origins, default="web", blank=False)
    source_web = models.URLField(max_length=250, null=False, blank=False)
    author = models.ForeignKey("Author", null=False, blank=False, on_delete=models.CASCADE, related_name="author_outstandingArticles")
    media = models.ForeignKey("MediaResource", null=False, blank=False, on_delete=models.CASCADE, related_name="mediaResource_outstandingArticles")
    description_es = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    outstanding = models.ForeignKey("Outstanding", null=False, blank=False, on_delete=models.CASCADE, related_name="outstanding_outstandingArticles")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=False, blank=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_outstandingArticles")

    class Meta:
        verbose_name = "OutstandingArticle"
        verbose_name_plural = "OutstandingArticles"
        db_table = "OutstandingArticle"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title_es}, {self.article_origin}, {self.modified}, {self.user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "title_es": self.title_es,
            "title_en": self.title_en,
            "article_origin": self.article_origin,
            "source_web": self.source_web,
            "author": self.author.name,
            "media": self.media.id,
            "description_es": self.description_es,
            "description_en": self.description_en,
            "outstanding": self.outstanding.id,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }

class Contact(models.Model):
    name = models.CharField(max_length=250, blank=False)
    email = models.EmailField(null=False, blank=False)
    telephone= models.CharField(max_length=15, blank=True)
    message = models.TextField(blank=False)
    country = models.ForeignKey("Country", null=False, blank=False, on_delete=models.CASCADE, related_name="country_contacts")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=False, blank=False)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        db_table = "Contact"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.name}, {self.email}, {self.telephone}, {self.country.name_es}, {self.created}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "telephone": self.telephone,
            "message": self.message,
            "country": self.country.name_es,
            "created": self.created.strftime("%b %d %Y, %I:%M %p")
        }

class StyleSheet(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    content = models.TextField(blank=False)
    page = models.ForeignKey("Page", null=False, blank=False, on_delete=models.CASCADE, related_name="page_styleSheets")
    modified = models.DateTimeField(auto_now=True, null=False, blank=False)
    user = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE, related_name="user_styleSheets")

    class Meta:
        verbose_name = "StyleSheet"
        verbose_name_plural = "StyleSheets"
        db_table = "StyleSheet"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.name}, {self.modified}, {self.user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "page": self.page.id,
            "modified": self.modified.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user
        }