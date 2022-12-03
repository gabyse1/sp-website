from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# create python classes to represent forms
class UserForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            'password1',
            'password2',
            "first_name",
            "last_name",
        ]

        labels = {
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
            "first_name": "First Name",
            "last_name": "Last Name"
        }

        help_text = {
            "username": _("Input alphabet characters"),
        }

        widgets = {
            "username": forms.TextInput(attrs={"class":"form-input-control"}),
            "email": forms.EmailInput(attrs={"class":"form-input-control"}),
            "password1": forms.PasswordInput(attrs={"class":"form-input-control"}),
            "password2": forms.PasswordInput(attrs={"class":"form-input-control"}),
            "first_name": forms.TextInput(attrs={"class":"form-input-control"}),
            "last_name": forms.TextInput(attrs={"class":"form-input-control"}),
        }

class CountryForm(forms.ModelForm):

    class Meta:
        model = Country

        fields = [
            "name_es",
            "name_en",
        ]

        labels = {
            "name_es": "Country Name (Spanish)",
            "name_en": "Country Name (English)",
        }

        widgets = {
            "name_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "name_en": forms.TextInput(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "name_es": {
                "unique": _("A Country with this name already exists."),
                "required": _("Country name is required."),
            },
            "name_en": {
                "unique": _("A Country with this name already exists."),
                "required": _("Country name is required."),
            },
        }

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region

        fields = [
            "name",
            "scope",
            "country",
        ]

        labels = {
            "name": "Region Name",
            "scope": "Scope (Number of Families)",
            "country": "Country",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-input-control"}),
            "scope": forms.NumberInput(attrs={"class":"form-input-control"}),
            "country": forms.Select(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "name": {
                "unique": _("A Region with this name already exists."),
                "required": _("Region name is required."),
            },
            "scope": {
                "required": _("Territorial Scope is required."),
            },
            "country": {
                "required": _("Country is required."),
            },
        }

class ProvinceForm(forms.ModelForm):

    class Meta:
        model = Province

        fields = [
            "name",
            "region",
        ]

        labels = {
            "name": "Province Name",
            "region": "Region",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-input-control"}),
            "region": forms.Select(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "name": {
                "unique": _("A Province with this name already exists."),
                "required": _("Province name is required."),
            },
            "region": {
                "required": _("Region is required."),
            },
        }

class DistrictForm(forms.ModelForm):

    class Meta:
        model = District

        fields = [
            "name",
            "altitude",
            "province",
        ]

        labels = {
            "name": "District Name",
            "altitude": "District Altitude (m.a.s.l.)",
            "province": "Province",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-input-control"}),
            "altitude": forms.NumberInput(attrs={"class":"form-input-control"}),
            "province": forms.Select(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "name": {
                "unique": _("A District with this name already exists."),
                "required": _("District name is required."),
            },
            "altitude": {
                "required": _("Altitude name is required."),
            },
            "province": {
                "required": _("Province is required."),
            },
        }

class ImagenForm(forms.ModelForm):

    class Meta:
        model = Imagen

        fields = [
            "file_image",
        ]

        labels = {
            "file_image": "Image File",
        }

        widgets = {
            "file_image": forms.ClearableFileInput(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "file_image": {
                "unique": _("An image with this name already exists."),
                "required": _("Image is required."),
            },
        }

class HtmlDesignForm(forms.ModelForm):

    class Meta:
        model = HtmlDesign

        fields = [
            "file_html",
        ]

        labels = {
            "file_html": "Html File",
        }

        widgets = {
            "file_html": forms.ClearableFileInput(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "file_html": {
                "unique": _("An html file with this name already exists."),
                "required": _("Html file is required."),
            },
        }

class VideoForm(forms.ModelForm):

    class Meta:
        model = Video

        fields = [
            "title",
            "source",
            "web_url",
            "file_video",
        ]

        labels = {
            "title": "Video Title",
            "source": "Video Source",
            "web_url": "Video Embedded url",
            "file_video": "Video File",
        }

        widgets = {
            "title": forms.TextInput(attrs={"class":"form-input-control"}),
            "source": forms.Select(attrs={"class":"form-input-control"}),
            "web_url": forms.URLInput(attrs={"class":"form-input-control"}),
            "file_video": forms.ClearableFileInput(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "title": {
                "unique": _("A video with this title already exists."),
                "required": _("Video title is required."),
            },
            "source": {
                "required": _("Video source is required."),
            },
            "web_url": {
                "unique": _("A video with this url already exists."),
            },
            "file_video": {
                "unique": _("A video with this name already exists."),
            },
        }

class PageForm(forms.ModelForm):

    class Meta:
        model = Page

        fields = [
            "title_es",
            "title_en",
            "styleSheetName",
            "url_title_es",
            "url_title_en",
            "display_order",
        ]

        labels = {
            "title_es": "Page Title (Spanish)",
            "title_en": "Page Title (English)",
            "styleSheetName": "Page Style Sheet Name",
            "url_title_es": "Url Page Title (Spanish)",
            "url_title_en": "Url Page Title (English)",
            "display_order": "Display Order",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "styleSheetName": forms.TextInput(attrs={"readonly":"readonly", "class":"form-input-control"}),
            "url_title_es": forms.TextInput(attrs={"readonly":"readonly", "class":"form-input-control"}),
            "url_title_en": forms.TextInput(attrs={"readonly":"readonly", "class":"form-input-control"}),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "display_order",
            "media",
            "page",
        ]

        labels = {
            "title_es": "Section Title (Spanish)",
            "title_en": "Section Title (English)",
            "show_title": "Show Title",
            "display_order": "Display Order",
            "media": "Media Resource as Background",
            "page": "Page",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "media": forms.Select(attrs={"class":"form-input-control"}),
            "page": forms.Select(attrs={"class":"form-input-control"}),
        }

class ElementTypeForm(forms.ModelForm):

    class Meta:
        model = ElementType

        fields = [
            "name",
            "htmlName",
        ]

        labels = {
            "name": "Element Type Name",
            "htmlName": "HTML name of the element type",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-input-control"}),
            "htmlName": forms.TextInput(attrs={"class":"form-input-control","readonly":"readonly"}),
        }

        error_messages = {
            "name": {
                "unique": _("An Element Type with this name already exists."),
                "required": _("Element Type name is required."),
            },
            "htmlName": {
                "unique": _("An HTML Name with this name already exists."),
                "required": _("HTML name is required."),
            },
        }

class DescriptiveArticleForm(forms.ModelForm):
    description_es = forms.CharField(widget=CKEditorUploadingWidget())
    description_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = DescriptiveArticle

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "description_es",
            "description_en",
            "display_order",
            "section",
            "elementType",
        ]

        labels = {
            "title_es": "Descriptive Article Title (Spanish)",
            "title_en": "Descriptive Article Title (English)",
            "show_title": "Show Title",
            "description_es": "Description (Spanish)",
            "description_en": "Description (English)",
            "display_order": "Display Order",
            "section": "Section",
            "elementType": "Element Type",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "description_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "description_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "section": forms.Select(attrs={"class":"form-input-control"}),
            "elementType": forms.HiddenInput(),
        }

class GraphicArticleForm(forms.ModelForm):
    class Meta:
        model = GraphicArticle

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "media",
            "display_order",
            "section",
            "elementType",
        ]

        labels = {
            "title_es": "Graphic Article Title (Spanish)",
            "title_en": "Graphic Article Title (English)",
            "show_title": "Show Title",
            "media": "Media Resource",
            "display_order": "Display Order",
            "section": "Section",
            "elementType": "Element Type",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "media": forms.Select(attrs={"class":"form-input-control"}),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "section": forms.Select(attrs={"class":"form-input-control"}),
            "elementType": forms.HiddenInput(),
        }

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "size",
            "transitionType",
            "display_sliderList",
            "display_order",
            "section",
            "elementType",
        ]

        labels = {
            "title_es": "Slider Title (Spanish)",
            "title_en": "Slider Title (English)",
            "show_title": "Show Title",
            "size": "Slider Size",
            "transitionType": "Transition Type",
            "display_sliderList": "Display Slider List",
            "display_order": "Display Order",
            "section": "Section",
            "elementType": "Element Type",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "size": forms.Select(attrs={"class":"form-input-control"}),
            "transitionType": forms.Select(attrs={"class":"form-input-control"}),
            "display_sliderList": forms.CheckboxInput(),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "section": forms.Select(attrs={"class":"form-input-control"}),
            "elementType": forms.HiddenInput(),
        }

class SliderElementForm(forms.ModelForm):
    description_es = forms.CharField(widget=CKEditorUploadingWidget())
    description_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = SliderElement

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "description_es",
            "description_en",
            "media_display_type",
            "medias",
            "list_icon",
            "display_order",
            "slider",
        ]

        labels = {
            "title_es": "Slide Element Title (Spanish)",
            "title_en": "Slide Element Title (English)",
            "show_title": "Show Title",
            "description_es": "Description (Spanish)",
            "description_en": "Description (English)",
            "media_display_type": "Image display Type",
            "medias": "Images",
            "list_icon": "Icon to show on list",
            "display_order": "Display Order",
            "slider": "Slider",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "description_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "description_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "media_display_type": forms.Select(attrs={"class":"form-input-control"}),
            "medias": forms.SelectMultiple(attrs={"class":"form-input-control-auto"}),
            "list_icon": forms.Select(attrs={"class":"form-input-control"}),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "slider": forms.Select(attrs={"class":"form-input-control"}),
        }

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author

        fields = [
            "name",
            "profession_es",
            "profession_en",
            "media",
            "country",
        ]

        labels = {
            "name":"Author Name",
            "profession_es":"Profession (Spanish)",
            "profession_en":"Profession (English)",
            "media":"media",
            "country":"Country",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-input-control"}),
            "profession_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "profession_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "media": forms.Select(attrs={"required":True,"class":"form-input-control"}),
            "country": forms.Select(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "name": {
                "unique": _("An author with this name already exists."),
                "required": _("Author name is required."),
            },
            "profession_es": {
                "required": _("Profession is required."),
            },
            "profession_en": {
                "required": _("Profession is required."),
            },
            "media": {
                "unique": _("An author with this photograph already exists. Change it."),
                "required": _("Author's photograph is required."),
            },
            "country": {
                "required": _("Country is required."),
            },
        }

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "display_order",
            "section",
            "elementType",
        ]

        labels = {
            "title_es": "Publication Title (Spanish)",
            "title_en": "Publication Title (English)",
            "show_title":"Display Title",
            "display_order": "Display Order",
            "section": "Section",
            "elementType": "Element Type",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "section": forms.Select(attrs={"class":"form-input-control"}),
            "elementType": forms.HiddenInput(),
        }

        error_messages = {
            "title_es": {
                "unique": _("A publication with this name already exists."),
                "required": _("Publication name is required."),
            },
            "title_en": {
                "unique": _("A publication with this name already exists."),
                "required": _("Publication name is required."),
            },
            "elementType": {
                "required": _("Element type is required."),
            },
            "section": {
                "required": _("Section is required."),
            },
        }

class PublicationArticleForm(forms.ModelForm):
    description_es = forms.CharField(widget=CKEditorUploadingWidget())
    description_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = PublicationArticle

        fields = [
            "title_es",
            "title_en",
            "article_origin",
            "source_web",
            "author",
            "media",
            "description_es",
            "description_en",
            "publication",

        ]

        labels = {
            "title_es": "Publication Article Title (Spanish)",
            "title_en": "Publication Article Title (English)",
            "article_origin": "Article Origin",
            "source_web": "Web Source",
            "author": "Author",
            "media": "Image or Video for Article",
            "description_es": "Description (Spanish)",
            "description_en": "Description (English)",
            "publicacion": "Publicacion",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "article_origin": forms.Select(attrs={"class":"form-input-control"}),
            "source_web": forms.TextInput(attrs={"class":"form-input-control"}),
            "author": forms.Select(attrs={"class":"form-input-control"}),
            "media": forms.Select(attrs={"class":"form-input-control"}),
            "description_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "description_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "publication": forms.Select(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "title_es": {
                "unique": _("An article with this title already exists."),
                "required": _("Article's title is required."),
            },
            "title_en": {
                "unique": _("An article with this title already exists."),
                "required": _("Article's title is required."),
            },
            "article_origin": {
                "required": _("Article origin is required."),
            },
            "source_web": {
                "required": _("Source's web is required."),
            },
            "author": {
                "required": _("An article author is required."),
            },
            "media": {
                "required": _("A media resource is required."),
            },
            "publication": {
                "required": _("Publication is required."),
            },
        }

class HtmlArticleForm(forms.ModelForm):

    class Meta:
        model = HtmlArticle

        fields = [
            "title_es",
            "title_en",
            "show_title",
            "htmlDesign",
            "display_order",
            "section",
            "elementType",
        ]

        labels = {
            "title_es": "Html Article Title (Spanish)",
            "title_en": "Html Article Title (English)",
            "show_title": "Display Title",
            "htmlDesign": "Html File Name",
            "display_order": "Display Order",
            "section": "Section",
            "elementType": "Element Type",
        }

        widgets = {
            "title_es": forms.TextInput(attrs={"class":"form-input-control"}),
            "title_en": forms.TextInput(attrs={"class":"form-input-control"}),
            "show_title": forms.CheckboxInput(),
            "htmlDesign": forms.Select(attrs={"class":"form-input-control"}),
            "display_order": forms.NumberInput(attrs={"class":"form-input-control"}),
            "section": forms.Select(attrs={"class":"form-input-control"}),
            "elementType": forms.HiddenInput(),
        }

        error_messages = {
            "title_es": {
                "unique": _("An html article with this title already exists."),
                "required": _("Html article title is required."),
            },
            "title_en": {
                "unique": _("A html article with this title already exists."),
                "required": _("Html article title is required."),
            },
            "htmlDesign": {
                "unique": _("A html file with this name already exists."),
                "required": _("Html file is required."),
            },
            "elementType": {
                "required": _("Element type is required."),
            },
            "section": {
                "required": _("Section is required."),
            },
        }

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = [
            "name",
            "email",
            "telephone",
            "country",
            "message",
        ]

        labels = {
            "name":"Contact Name",
            "email":"Email",
            "telephone":"Telephone",
            "country":"Country",
            "message":"Message",
        }

        widgets = {
            "name": forms.TextInput(attrs={"disabled":True,"class":"form-input-control"}),
            "email": forms.TextInput(attrs={"disabled":True,"class":"form-input-control"}),
            "telephone": forms.TextInput(attrs={"disabled":True,"class":"form-input-control"}),
            "country": forms.Select(attrs={"disabled":True,"class":"form-input-control"}),
            "message": forms.Textarea(attrs={"disabled":True,"class":"form-input-control-auto"}),
        }

        error_messages = {
            "name": {
                "required": _("Name is required."),
            },
            "email": {
                "required": _("Email is required."),
            },
            "country": {
                "required": _("Country is required."),
            },
            "message": {
                "required": _("Message is required."),
            },
        }

class StyleSheetForm(forms.ModelForm):
    class Meta:
        model = StyleSheet

        fields = [
            "name",
            "content",
            "page",
        ]

        labels = {
            "name":"Css File Name",
            "content":"Content",
            "page":"Page",
        }

        widgets = {
            "name": forms.TextInput(attrs={"readonly":"readonly", "class":"form-input-control"}),
            "content": forms.Textarea(attrs={"class":"form-input-control-auto"}),
            "page": forms.Select(attrs={"class":"form-input-control"}),
        }

        error_messages = {
            "name": {
                "unique": _("A style sheet with this name already exists."),
                "required": _("Name is required."),
            },
            "content": {
                "required": _("Content is required."),
            },
            "page": {
                "required": _("Page is required."),
            },
        }
