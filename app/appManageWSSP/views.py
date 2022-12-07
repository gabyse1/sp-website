from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from .datavalidation import *
from .forms import *
from .models import *
import csv
import os
import smtplib, ssl

# Create your views here.
def index(request):
    # Authenticated users view their management site
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("pages"))
    else: # Everyone else is prompted to sign in
        return HttpResponseRedirect(reverse("login"))

def limitedAccess(request):
    # Authenticated users view their management site
    if request.user.is_authenticated:
        return render(request, "appManageWSSP/limitedAccess.html")

def retrieve_pages(request):
    recordlist = Page.objects.all().order_by("display_order")

    searchinput = request.GET.get("search")
    print(searchinput)

    if searchinput:
        recordlist = search_records("page", searchinput)
    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def pages(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_pages(request)

        return render(request, "appManageWSSP/pages.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "page",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_page(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_pages(request)
        
        if request.method == "POST":
            form = PageForm(request.POST)

            if form.is_valid():
                try:
                    page = form.save(commit=False)
                    page.user = request.user
                    page.save()

                    # create page's stylesheet
                    styleSheetName = form.cleaned_data["styleSheetName"]
                    existStyleSheet = StyleSheet.objects.filter(name=styleSheetName)
                    if not existStyleSheet:
                        # create style sheet in server
                        filename = open(f"./appDisplayWSSP/static/appDisplayWSSP/css/{styleSheetName}.scss","a", encoding="utf-8")
                        filename.write("/* ----- POSICIONAR ELEMENTOS DE DESCRIPCION ----- */" + os.linesep)
                        filename.close()
                        # create style sheet in database
                        newStyleSheet = StyleSheet(name=styleSheetName,content="/* ----- POSICIONAR ELEMENTOS DE DESCRIPCION ----- */",page=page,user=request.user)
                        newStyleSheet.save()

                    # load created record
                    return HttpResponseRedirect(reverse("adm_page", kwargs={"adm":"edit","id":page.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            order = Page.objects.all().count() + 1
            form = PageForm(initial={"display_order":order})

        return render(request, "appManageWSSP/pages.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "page",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_page(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        try:
            page = Page.objects.get(pk=int(id))
            # Retrieve page style sheet
            styleSheet = StyleSheet.objects.get(name=page.styleSheetName)
            lastStyleSheetName = styleSheet.name
            # Retrieve page sections
            pageSections = page.page_sections.all().order_by("display_order")
        except:
            raise Http404
        
        searchinput, paginator, page_obj = retrieve_pages(request)

        # Edit or delete record
        if request.method == "POST":
            form = PageForm(request.POST, instance=page)
            if form.is_valid():
                try:
                    # update record in database
                    page = form.save(commit=False)
                    page.user = request.user
                    page.save()
                    # update styleSheet record name
                    styleSheet.name = page.styleSheetName
                    styleSheet.save()
                    os.rename(f"./appDisplayWSSP/static/appDisplayWSSP/css/{lastStyleSheetName}.scss", f"./appDisplayWSSP/static/appDisplayWSSP/css/{styleSheet.name}.scss")
                    # load updated record
                    return HttpResponseRedirect(reverse("adm_page", kwargs={"adm":"edit","id":page.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = PageForm(instance=page)

            if adm == "delete":
                try:
                    # delete style sheet from server
                    os.remove(f"./appDisplayWSSP/static/appDisplayWSSP/css/{page.styleSheetName}.scss")
                    # delete style sheet from database
                    styleSheet.delete()
                    # delete record from database
                    page.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("pages"))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        return render(request, "appManageWSSP/pages.html", {
            "form": form,
            "webpage": page,
            "pageSections": pageSections,
            "styleSheetId": styleSheet.id,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "searchinput": searchinput,
            "modelname": "page",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_sections(request, id_page):
    # Get webpage
    try:
        webpage = Page.objects.get(pk=int(id_page))
    except:
        raise Http404

    # Record list
    recordlist = webpage.page_sections.all().order_by("display_order")

    # Search record
    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("section", searchinput, webpage)

    # Pagination
    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj, webpage

def sections(request, id_page):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, webpage = retrieve_sections(request, id_page)

        return render(request, "appManageWSSP/sections.html", {
            "webpage": webpage,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "section",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_section(request, id_page):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, webpage = retrieve_sections(request, id_page)

        # Create record
        if request.method == "POST":
            form = SectionForm(request.POST)

            if form.is_valid():
                try:
                    # create section record in database
                    section = form.save(commit=False)
                    section.page = webpage
                    section.user = request.user
                    section.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_page", kwargs={"adm":"edit","id":webpage.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            order = webpage.page_sections.all().count() + 1
            form = SectionForm(initial={"display_order":order, "page":webpage})

        formImage = ImagenForm()
        formVideo = VideoForm()

        return render(request, "appManageWSSP/sections.html", {
            "form": form,
            "webpage": webpage,
            "formImage": formImage,
            "formVideo": formVideo,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "section",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_section(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        media = None
        try:
            section = Section.objects.get(pk=int(id))
            # get media to delete if required
            if section.media:
                if section.media.mediaType == "video":
                    media = Video.objects.get(pk=int(section.media.id))
                elif section.media.mediaType == "image":
                    media = Imagen.objects.get(pk=int(section.media.id))
            # Retrieve page's sections
            sectionElements = section.section_elements.all().order_by("display_order")
        except:
            raise Http404

        searchinput, paginator, page_obj, webpage = retrieve_sections(request, section.page.id)

        # Create record
        if request.method == "POST":
            form = SectionForm(request.POST, instance=section)

            if form.is_valid():
                try:
                    # create section record in database
                    section = form.save(commit=False)
                    section.user = request.user
                    section.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_section", kwargs={"adm":"edit","id":section.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updation the record."])
                    raise
        else:
            form = SectionForm(instance=section)
            if adm == "delete":
                try:
                    # delete record from database
                    section.delete()
                    # remove photo from from database and server
                    if section.media.mediaType == "video":
                        if media and not is_video_related_to_model(media.id):
                            media.delete()
                    elif section.media.mediaType == "image":
                        if media and not is_image_related_to_model(media.id):
                            media.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("sections", kwargs={"id_page":section.page.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        formImage = ImagenForm()
        formVideo = VideoForm()

        elementTypeList = ElementType.objects.all()

        return render(request, "appManageWSSP/sections.html", {
            "form": form,
            "section": section,
            "sectionElements": sectionElements,
            "formImage": formImage,
            "formVideo": formVideo,
            "elementTypeList": elementTypeList,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "searchinput": searchinput,
            "modelname": "section",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_elements(request, id_section):
    try:
        section = Section.objects.get(pk=int(id_section))
    except:
        raise Http404

    recordlist = section.section_elements.all().order_by("display_order")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("element", searchinput, section)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj, section

def elements(request, id_section):
    if request.user.is_authenticated:

        searchinput, paginator, page_obj, section = retrieve_elements(request, id_section)

        elementTypeList = ElementType.objects.all()

        return render(request, "appManageWSSP/elements.html", {
            "section": section,
            "page_obj": page_obj,
            "paginator": paginator,
            "elementTypeList": elementTypeList,
            "searchinput": searchinput,
            "modelname": "element",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_descriptiveArticle(request, id_section):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, section = retrieve_elements(request, id_section)
        
        if request.method == "POST":
            form = DescriptiveArticleForm(request.POST)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.section = section
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_descriptiveArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            order = section.section_elements.all().count() + 1
            elementType = ElementType.objects.get(htmlName="descriptiveArticle")
            form = DescriptiveArticleForm(initial={"section":section,"elementType":elementType,"display_order":order})

        return render(request, "appManageWSSP/descriptiveArticle.html", {
            "form": form,
            "section": section,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "descriptionArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_descriptiveArticle(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        try:
            element = DescriptiveArticle.objects.get(pk=int(id))
        except:
            raise Http404

        searchinput, paginator, page_obj, section = retrieve_elements(request, element.section.id)

        # Create record
        if request.method == "POST":
            form = DescriptiveArticleForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_descriptiveArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = DescriptiveArticleForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("elements", kwargs={"id_section":element.section.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    raise

        elementTypeList = ElementType.objects.all()

        return render(request, "appManageWSSP/descriptiveArticle.html", {
            "form": form,
            "element": element,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "elementTypeList": elementTypeList,
            "searchinput": searchinput,
            "modelname": "descriptiveArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_graphicArticle(request, id_section):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, section = retrieve_elements(request, id_section)
        # Create record
        if request.method == "POST":
            form = GraphicArticleForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.section = section
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_graphicArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            order = section.section_elements.all().count() + 1
            elementType = ElementType.objects.get(htmlName="graphicArticle")
            form = GraphicArticleForm(initial={"section":section,"elementType":elementType,"display_order":order})

        formImage = ImagenForm()
        formVideo = VideoForm()

        return render(request, "appManageWSSP/graphicArticle.html", {
            "form": form,
            "formImage": formImage,
            "formVideo": formVideo,
            "section": section,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "graphicArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_graphicArticle(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        media = None
        try:
            element = GraphicArticle.objects.get(pk=int(id))
            media = Imagen.objects.get(pk=int(element.media.id))
        except:
            raise Http404

        searchinput, paginator, page_obj, section = retrieve_elements(request, element.section.id)
        # Create record
        if request.method == "POST":
            form = GraphicArticleForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_graphicArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = GraphicArticleForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # remove media from database and server
                    if media and not is_image_related_to_model(media.id):
                        media.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("elements", kwargs={"id_section":element.section.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    raise

        elementTypeList = ElementType.objects.all()
        formImage = ImagenForm()
        formVideo = VideoForm()

        return render(request, "appManageWSSP/graphicArticle.html", {
            "form": form,
            "formImage": formImage,
            "formVideo": formVideo,
            "element": element,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "elementTypeList": elementTypeList,
            "searchinput": searchinput,
            "modelname": "graphicArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_slider(request, id_section):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, section = retrieve_elements(request, id_section)
        # Create record
        if request.method == "POST":
            form = SliderForm(request.POST)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.section = section
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_slider", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            order = section.section_elements.all().count() + 1
            elementType = ElementType.objects.get(htmlName="slider")
            form = SliderForm(initial={"section":section,"elementType":elementType,"display_order":order})

        return render(request, "appManageWSSP/slider.html", {
            "form": form,
            "section": section,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "slider",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_outstanding(request, id_section):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, section = retrieve_elements(request, id_section)
        # Create record
        if request.method == "POST":
            form = OutstandingForm(request.POST)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.section = section
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_outstanding", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            elementType = ElementType.objects.get(htmlName="outstanding")
            form = OutstandingForm(initial={"section":section,"elementType":elementType})

        return render(request, "appManageWSSP/outstandings.html", {
            "form": form,
            "section": section,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "outstanding",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_outstanding(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        try:
            element = Outstanding.objects.get(pk=int(id))
            outstandingArticles = OutstandingArticle.objects.all().order_by("created")
        except:
            raise Http404
        
        searchinput, paginator, page_obj, section = retrieve_elements(request, element.section.id)
        
        if request.method == "POST":
            form = OutstandingForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_outstanding", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = OutstandingForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("elements", kwargs={"id_section":element.section.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    raise

        elementTypeList = ElementType.objects.all()

        return render(request, "appManageWSSP/outstandings.html", {
            "form": form,
            "element": element,
            "outstandingArticles": outstandingArticles,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "elementTypeList": elementTypeList,
            "searchinput": searchinput,
            "modelname": "outstanding",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_outstandingArticles(request, id_outstanding):
    try:
        outstanding = Outstanding.objects.get(pk=int(id_outstanding))
    except:
        raise Http404

    recordlist = outstanding.outstanding_outstandingArticles.all().order_by("-created")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("outstandingArticle", searchinput, outstanding)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj, outstanding

def outstandingArticles(request, id_outstanding):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, outstanding = retrieve_outstandingArticles(request, id_outstanding)

        formImage = ImagenForm()

        return render(request, "appManageWSSP/outstandingArticles.html", {
            "outstanding": outstanding,
            "formImage": formImage,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "outstandingArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_outstandingArticle(request, id_outstanding):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, outstanding = retrieve_outstandingArticles(request, id_outstanding)
        
        if request.method == "POST":
            form = OutstandingArticleForm(request.POST)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.outstanding = outstanding
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_outstandingArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = OutstandingArticleForm(initial={"outstanding":outstanding})

        formImage = ImagenForm()
        formVideo = VideoForm()
        formAuthor = AuthorForm()

        return render(request, "appManageWSSP/outstandingArticles.html", {
            "form": form,
            "formImage": formImage,
            "formVideo": formVideo,
            "formAuthor": formAuthor,
            "outstanding": outstanding,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "outstandingArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_outstandingArticle(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        media = None
        try:
            element = OutstandingArticle.objects.get(pk=int(id))
            # get media to delete if it requires
            if element.media.mediaType == "video":
                media = Video.objects.get(pk=int(element.media.id))
            elif element.media.mediaType == "image":
                media = Imagen.objects.get(pk=int(element.media.id))
        except:
            raise Http404
        
        searchinput, paginator, page_obj, outstanding = retrieve_outstandingArticles(request, element.outstanding.id)

        # Create record
        if request.method == "POST":
            form = OutstandingArticleForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_outstandingArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = OutstandingArticleForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # remove media from database and server
                    if element.media.mediaType == "video":
                        if media and not is_video_related_to_model(media.id):
                            media.delete()
                    elif element.media.mediaType == "image":
                        if media and not is_image_related_to_model(media.id):
                            media.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("outstandingArticles", kwargs={"id_outstanding":element.outstanding.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    raise

        formImage = ImagenForm()
        formVideo = VideoForm()
        formAuthor = AuthorForm()

        return render(request, "appManageWSSP/outstandingArticles.html", {
            "form": form,
            "formImage": formImage,
            "formVideo": formVideo,
            "formAuthor": formAuthor,
            "element": element,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "searchinput": searchinput,
            "modelname": "outstandingArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_htmlArticle(request, id_section):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, section = retrieve_elements(request, id_section)
        
        if request.method == "POST":
            form = HtmlArticleForm(request.POST)

            if form.is_valid():
                try:
                    # create record in database
                    element = form.save(commit=False)
                    element.section = section
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_htmlArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            order = section.section_elements.all().count() + 1
            elementType = ElementType.objects.get(htmlName="htmlArticle")
            form = HtmlArticleForm(initial={"section":section,"elementType":elementType,"display_order":order})

        formHtmlDesign = HtmlDesignForm()

        return render(request, "appManageWSSP/htmlArticle.html", {
            "form": form,
            "formHtmlDesign": formHtmlDesign,
            "section": section,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "htmlArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_htmlArticle(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        htmlFile = ""
        try:
            element = HtmlArticle.objects.get(pk=int(id))
            htmlFile = HtmlDesign.objects.get(pk=int(element.htmlDesign.id))
        except:
            raise Http404

        searchinput, paginator, page_obj, section = retrieve_elements(request, element.section.id)
        
        if request.method == "POST":
            form = HtmlArticleForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_htmlArticle", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = HtmlArticleForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # remove media from database and server
                    if htmlFile and not is_htmlfile_related_to_model(htmlFile.id):
                        htmlFile.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("elements", kwargs={"id_section":element.section.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        elementTypeList = ElementType.objects.all()
        formHtmlDesign = HtmlDesignForm()

        return render(request, "appManageWSSP/htmlArticle.html", {
            "form": form,
            "formHtmlDesign": formHtmlDesign,
            "element": element,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "elementTypeList": elementTypeList,
            "searchinput": searchinput,
            "modelname": "htmlArticle",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_slider(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        try:
            element = Slider.objects.get(pk=int(id))
            sliderElements = element.slider_sliderElements.all().order_by("display_order")
        except:
            raise Http404

        searchinput, paginator, page_obj, section = retrieve_elements(request, element.section.id)
        # Create record
        if request.method == "POST":
            form = SliderForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_slider", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = SliderForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("elements", kwargs={"id_section":element.section.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    raise

        elementTypeList = ElementType.objects.all()

        return render(request, "appManageWSSP/slider.html", {
            "form": form,
            "element": element,
            "sliderElements": sliderElements,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "elementTypeList": elementTypeList,
            "searchinput": searchinput,
            "modelname": "slider",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_sliderElements(request, id_slider):
    try:
        slider = Slider.objects.get(pk=int(id_slider))
    except:
        raise Http404

    recordlist = slider.slider_sliderElements.all().order_by("display_order")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("sliderElement", searchinput, slider)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj, slider

def sliderElements(request, id_slider):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, slider = retrieve_sliderElements(request, id_slider)

        formImage = ImagenForm()

        return render(request, "appManageWSSP/sliderElements.html", {
            "slider": slider,
            "formImage": formImage,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "sliderElement",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_sliderElement(request, id_slider):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj, slider = retrieve_sliderElements(request, id_slider)

        # Create record
        if request.method == "POST":
            form = SliderElementForm(request.POST)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.slider = slider
                    element.user = request.user
                    element.save()
                    element.medias.clear()
                    multiselect = form.cleaned_data.get("medias")
                    for ms in multiselect:
                        element.medias.add(ms.id)
                    # load created record
                    return HttpResponseRedirect(reverse("adm_sliderElement", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            order = slider.slider_sliderElements.all().count() + 1
            form = SliderElementForm(initial={"slider":slider,"display_order":order})

        formImage = ImagenForm()

        return render(request, "appManageWSSP/sliderElements.html", {
            "form": form,
            "formImage": formImage,
            "slider": slider,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "sliderElement",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_sliderElement(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404
        # Get section
        medias = None
        try:
            element = SliderElement.objects.get(pk=int(id))
            medias = element.medias.all()
        except:
            raise Http404

        searchinput, paginator, page_obj, slider = retrieve_sliderElements(request, element.slider.id)

        # Create record
        if request.method == "POST":
            form = SliderElementForm(request.POST, instance=element)

            if form.is_valid():
                try:
                    # create section record in database
                    element = form.save(commit=False)
                    element.user = request.user
                    element.save()
                    element.medias.clear()
                    multiselect = form.cleaned_data.get("medias")
                    if multiselect:
                        for ms in multiselect:
                            element.medias.add(ms)

                    # load created record
                    return HttpResponseRedirect(reverse("adm_sliderElement", kwargs={"adm":"edit","id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = SliderElementForm(instance=element)

            if adm == "delete":
                try:
                    # delete record from database
                    element.delete()
                    # remove media from database and server
                    if medias:
                        for media in medias:
                            if not is_image_related_to_model(media.id):
                                media.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("sliderElements", kwargs={"id_slider":element.slider.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    raise

        formImage = ImagenForm()

        return render(request, "appManageWSSP/sliderElements.html", {
            "form": form,
            "formImage": formImage,
            "element": element,
            "page_obj": page_obj,
            "paginator": paginator,
            "edit_record": True,
            "searchinput": searchinput,
            "modelname": "sliderElement",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_authors(request):
    recordlist = Author.objects.all().order_by("name")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("author", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def authors(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_authors(request)

        formImage = ImagenForm()

        return render(request, "appManageWSSP/authors.html", {
            "formImage": formImage,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "author",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_author(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_authors(request)
        
        if request.method == "POST":
            form = AuthorForm(request.POST)
            if form.is_valid():
                try:
                    # create record in database
                    author = form.save(commit=False)
                    author.user = request.user
                    author.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_author", kwargs={"adm":"edit","id":author.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = AuthorForm()

        formImage = ImagenForm()

        return render(request, "appManageWSSP/authors.html", {
            "form": form,
            "formImage": formImage,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "author",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_author(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        media = None
        try:
            author = Author.objects.get(pk=int(id))
            media = Imagen.objects.get(pk=int(author.media.id))
        except:
            raise Http404
        
        searchinput, paginator, page_obj = retrieve_authors(request)
        
        # Edit or delete record
        if request.method == "POST":
            form = AuthorForm(request.POST, instance=author)
            if form.is_valid():
                try:
                    # create record in database
                    author = form.save(commit=False)
                    author.user = request.user
                    author.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_author", kwargs={"adm":"edit","id":author.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = AuthorForm(instance=author)

            if adm == "delete":
                if author.author_outstandingArticles.all():
                    form.errors["__all__"] = form.error_class(["This author cannot be removed because it is related to a outstanding."])
                else:
                    # delete record from database
                    author.delete()
                    # remove media from database and server
                    if media and not is_image_related_to_model(media.id):
                        media.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("authors"))

        formImage = ImagenForm()

        return render(request, "appManageWSSP/authors.html", {
            "form": form,
            "formImage": formImage,
            "author": author,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "modelname": "author",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def contacts(request, id=None, adm=None):
    if request.user.is_authenticated:
        # Record list
        recordlist = Contact.objects.all().order_by("-created")

        # Search record
        searchinput = request.GET.get("search")
        if searchinput:
            recordlist = search_records("contact", searchinput)

        # Insert numbering
        recordlist = number_records(recordlist)

        # Pagination
        paginator,page_obj = paginate_records(request, recordlist)

        # Get html file name depending of user
        if request.user.is_superuser:
            htmlcontactfile = "contactsSuperuser"
        else:
            htmlcontactfile = "contacts"

        # Validate existence of the record
        if id:
            try:
                element = Contact.objects.get(pk=int(id))
                form = ContactForm(instance=element)

                if adm == "delete":
                    try:
                        # delete record from database
                        element.delete()
                        # load all records
                        return HttpResponseRedirect(reverse("contacts"))
                    except:
                        form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

                return render(request, f"appManageWSSP/{htmlcontactfile}.html", {
                    "form": form,
                    "element": element,
                    "page_obj": page_obj,
                    "paginator": paginator,
                    "edit_record": True,
                    "searchinput": searchinput,
                    "modelname": "contact",
                })
            except:
                raise Http404
        else:
            return render(request, f"appManageWSSP/{htmlcontactfile}.html", {
                "page_obj": page_obj,
                "paginator": paginator,
                "searchinput": searchinput,
                "modelname": "contact",
            })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_styleSheets(request):
        recordlist = StyleSheet.objects.all().order_by("name")

        searchinput = request.GET.get("search")
        if searchinput:
            recordlist = search_records("styleSheet", searchinput)

        recordlist = number_records(recordlist)

        paginator, page_obj = paginate_records(request, recordlist)

        return searchinput, paginator, page_obj

def styleSheets(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_styleSheets(request)

        return render(request, "appManageWSSP/styleSheets.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "styleSheet",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_styleSheet(request, id):
    if request.user.is_authenticated:
        # Get style sheet
        try:
            styleSheet = StyleSheet.objects.get(pk=int(id))
            filename = open(f"./appDisplayWSSP/static/appDisplayWSSP/css/{styleSheet.name}.scss", encoding='utf-8')
            lines = filename.read()
            styleSheet.content = lines
            filename.close()
        except:
            raise Http404

        searchinput, paginator, page_obj = retrieve_styleSheets(request)
        
        if request.method == "POST":
            form = StyleSheetForm(request.POST, instance=styleSheet)

            if form.is_valid():
                try:
                    # Save style sheet in server
                    filename = open(f"./appDisplayWSSP/static/appDisplayWSSP/css/{styleSheet.name}.scss", "w", encoding="utf-8")
                    filename.writelines(str(form.cleaned_data["content"]))
                    filename.close()
                    # create record in database
                    element = form.save(commit=False)
                    element.name = styleSheet.name
                    element.user = request.user
                    element.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_styleSheet", kwargs={"id":element.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = StyleSheetForm(instance=styleSheet)

        return render(request, "appManageWSSP/styleSheets.html", {
            "form": form,
            "styleSheet": styleSheet,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "modelname": "styleSheet",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_elementTypes(request):
    recordlist = ElementType.objects.all().order_by("name")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("elementType", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def elementTypes(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            searchinput, paginator, page_obj = retrieve_elementTypes(request)
            
            return render(request, "appManageWSSP/elementTypes.html", {
                "page_obj": page_obj,
                "paginator": paginator,
                "searchinput": searchinput,
                "modelname": "elementType",
            })
        else:
            return HttpResponseRedirect(reverse("limitedAccess"))
    else:
        return HttpResponseRedirect(reverse("login"))

def add_elementType(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            searchinput, paginator, page_obj = retrieve_elementTypes(request)
            
            if request.method == "POST":
                form = ElementTypeForm(request.POST)
                if form.is_valid():
                    try:
                        # create record in database
                        elementtype = form.save(commit=False)
                        elementtype.user = request.user
                        elementtype.save()
                        # load created record
                        return HttpResponseRedirect(reverse("adm_elementType", kwargs={"adm":"edit","id":elementtype.id}))
                    except:
                        form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
            else:
                form = ElementTypeForm()

            return render(request, "appManageWSSP/elementTypes.html", {
                "form": form,
                "page_obj": page_obj,
                "paginator": paginator,
                "searchinput": searchinput,
                "modelname": "elementType",
            })
        else:
            return HttpResponseRedirect(reverse("limitedAccess"))
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_elementType(request, adm, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # validate existence of the url
            if not adm == "edit" and not adm == "delete":
                raise Http404

            # Validate existence of the record
            try:
                elementtype = ElementType.objects.get(pk=int(id))
            except:
                raise Http404

            searchinput, paginator, page_obj = retrieve_elementTypes(request)
            
            if request.method == "POST":
                form = ElementTypeForm(request.POST, instance=elementtype)
                if form.is_valid():
                    try:
                        # update record in database
                        elementtype = form.save(commit=False)
                        elementtype.user = request.user
                        elementtype.save()
                        # load updated record
                        return HttpResponseRedirect(reverse("adm_elementType", kwargs={"adm":"edit","id":elementtype.id}))
                    except:
                        form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
            else:
                form = ElementTypeForm(instance=elementtype)

                if adm == "delete":
                    try:
                        # delete record from database
                        elementtype.delete()
                        # load all records
                        return HttpResponseRedirect(reverse("elementTypes"))
                    except:
                        form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

            return render(request, "appManageWSSP/elementTypes.html", {
                "form": form,
                "page_obj": page_obj,
                "paginator": paginator,
                "searchinput": searchinput,
                "edit_record": True,
                "id_record": id,
                "modelname": "elementType",
            })
        else:
            return HttpResponseRedirect(reverse("limitedAccess"))
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_countries(request):
    recordlist = Country.objects.all().order_by("name_es")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("country", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def countries(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_countries(request)

        return render(request, "appManageWSSP/countries.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "country",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_country(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_countries(request)
        
        if request.method == "POST":
            form = CountryForm(request.POST)
            if form.is_valid():
                try:
                    # create record in database
                    country = form.save(commit=False)
                    country.user = request.user
                    country.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_country", kwargs={"adm":"edit","id":country.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = CountryForm()

        return render(request, "appManageWSSP/countries.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "country",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_country(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        try:
            country = Country.objects.get(pk=int(id))
        except:
            raise Http404

        searchinput, paginator, page_obj = retrieve_countries(request)
        
        if request.method == "POST":
            form = CountryForm(request.POST, instance=country)
            if form.is_valid():
                try:
                    # update record in database
                    country = form.save(commit=False)
                    country.user = request.user
                    country.save()
                    # load updated record
                    return HttpResponseRedirect(reverse("adm_country", kwargs={"adm":"edit","id":country.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = CountryForm(instance=country)

            if adm == "delete":
                try:
                    regions = country.country_regions.all()
                    if not regions:
                        authors = country.country_authors.all()
                        if not authors:
                            contacts = country.country_contacts.all()
                            if not contacts:
                                # delete record from database
                                country.delete()
                                # load all records
                                return HttpResponseRedirect(reverse("countries"))
                            else:
                                form.errors["__all__"] = form.error_class(["This Country cannot be removed because it is related to a Contact."])
                        else:
                            form.errors["__all__"] = form.error_class(["This Country cannot be removed because it is related to an Author."])
                    else:
                        form.errors["__all__"] = form.error_class(["This Country cannot be removed because it is related to a Region."])
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        return render(request, "appManageWSSP/countries.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "id_record": id,
            "modelname": "country",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_regions(request):
    recordlist = Region.objects.all().order_by("name")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("region", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def regions(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_regions(request)

        return render(request, "appManageWSSP/regions.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "region",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_region(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_regions(request)
        
        if request.method == "POST":
            form = RegionForm(request.POST)
            if form.is_valid():
                try:
                    # create record in database
                    region = form.save(commit=False)
                    region.user = request.user
                    region.save()
                    # load created record
                    return HttpResponseRedirect(reverse("adm_region", kwargs={"adm":"edit","id":region.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = RegionForm()

        return render(request, "appManageWSSP/regions.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "region",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_region(request, adm, id):
    if request.user.is_authenticated:

        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        try:
            region = Region.objects.get(pk=int(id))
        except:
            raise Http404

        searchinput, paginator, page_obj = retrieve_regions(request)

        if request.method == "POST":
            form = RegionForm(request.POST, instance=region)
            if form.is_valid():
                try:
                    # update record in database
                    region = form.save(commit=False)
                    region.user = request.user
                    region.save()
                    # load updated record
                    return HttpResponseRedirect(reverse("adm_region", kwargs={"adm":"edit","id":region.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = RegionForm(instance=region)

            if adm == "delete":
                try:
                    regionProvinces = region.region_provinces.all()
                    if not regionProvinces:
                        # delete record from database
                        region.delete()
                        # load all records
                        return HttpResponseRedirect(reverse("regions"))
                    else:
                        form.errors["__all__"] = form.error_class(["This Region cannot be removed because it is related to a Province."])
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        return render(request, "appManageWSSP/regions.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "id_record": id,
            "modelname": "region",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_provinces(request):
    recordlist = Province.objects.all().order_by("name")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("province", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def provinces(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_provinces(request)

        return render(request, "appManageWSSP/provinces.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "province",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_province(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_provinces(request)

        if request.method == "POST":
            form = ProvinceForm(request.POST)
            if form.is_valid():
                try:
                    # validate existence of the record
                    existMatch = False
                    existProvinces = Province.objects.filter(name=form.cleaned_data["name"], region=form.cleaned_data["region"])
                    if existProvinces:
                        existMatch = True
                        form.errors["name"] = form.error_class(["There is already this province related to the " + str(form.cleaned_data["region"].name) + " region."])
                    if existMatch is False:
                        # create record in database
                        province = form.save(commit=False)
                        province.user = request.user
                        province.save()
                        # load created record
                        return HttpResponseRedirect(reverse("adm_province", kwargs={"adm":"edit","id":province.id}))
                except:
                    raise
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = ProvinceForm()

        return render(request, "appManageWSSP/provinces.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "province",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_province(request, adm, id):
    if request.user.is_authenticated:

        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        try:
            province = Province.objects.get(pk=int(id))
        except:
            raise Http404

        searchinput, paginator, page_obj = retrieve_provinces(request)

        if request.method == "POST":
            form = ProvinceForm(request.POST, instance=province)
            if form.is_valid():
                try:
                    # validate existence of the record
                    existMatch = False
                    existProvinces = Province.objects.filter(name=form.cleaned_data["name"], region=form.cleaned_data["region"])
                    if existProvinces:
                        existMatch = True
                        form.errors["name"] = form.error_class(["There is already this province related to the " + str(form.cleaned_data["region"].name) + " region."])
                    if existMatch is False:
                        # create record in database
                        province = form.save(commit=False)
                        province.user = request.user
                        province.save()
                        # load created record
                        return HttpResponseRedirect(reverse("adm_province", kwargs={"adm":"edit","id":province.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = ProvinceForm(instance=province)

            if adm == "delete":
                try:
                    provinceDistricts = province.province_districts.all()
                    if not provinceDistricts:
                        # delete record from database
                        province.delete()
                        # load all records
                        return HttpResponseRedirect(reverse("provinces"))
                    else:
                        form.errors["__all__"] = form.error_class(["This Province cannot be removed because it is related to a District."])
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        return render(request, "appManageWSSP/provinces.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "id_record": id,
            "modelname": "province",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_districts(request):
    recordlist = District.objects.all().order_by("name")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("district", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)
    
    return searchinput, paginator, page_obj

def districts(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_districts(request)

        return render(request, "appManageWSSP/districts.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "district",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_district(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_districts(request)
        
        if request.method == "POST":
            form = DistrictForm(request.POST)
            if form.is_valid():
                try:
                    # validate existence of the record
                    existMatch = False
                    existDistricts = District.objects.filter(name=form.cleaned_data["name"], province=form.cleaned_data["province"])
                    if existDistricts:
                        existMatch = True
                        form.errors["name"] = form.error_class(["There is already this district related to the " + str(form.cleaned_data["province"].name) + " province."])
                    if existMatch is False:
                        # create record in database
                        district = form.save(commit=False)
                        district.user = request.user
                        district.save()
                        # load created record
                        return HttpResponseRedirect(reverse("adm_district", kwargs={"adm":"edit","id":district.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = DistrictForm()

        return render(request, "appManageWSSP/districts.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "district",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_district(request, adm, id):
    if request.user.is_authenticated:

        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        try:
            district = District.objects.get(pk=int(id))
        except:
            raise Http404

        searchinput, paginator, page_obj = retrieve_districts(request)
        
        if request.method == "POST":
            form = DistrictForm(request.POST, instance=district)
            if form.is_valid():
                try:
                    # validate existence of the record
                    existMatch = False
                    existDistricts = District.objects.filter(name=form.cleaned_data["name"], province=form.cleaned_data["province"])
                    if existDistricts:
                        existMatch = True
                        form.errors["name"] = form.error_class(["There is already this district related to the " + str(form.cleaned_data["province"].name) + " province."])
                    if existMatch is False:
                        # update record in database
                        district = form.save(commit=False)
                        district.user = request.user
                        district.save()
                        # load updated record
                        return HttpResponseRedirect(reverse("adm_district", kwargs={"adm":"edit","id":district.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = DistrictForm(instance=district)

            if adm == "delete":
                try:
                    contacts = district.district_contacts.all()
                    if not contacts:
                        # delete record from database
                        district.delete()
                        # load all records
                        return HttpResponseRedirect(reverse("districts"))
                    else:
                        form.errors["__all__"] = form.error_class(["This District cannot be removed because it is related to a Contact."])
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])

        return render(request, "appManageWSSP/districts.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "id_record": id,
            "modelname": "district",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_images(request):
    recordlist = Imagen.objects.all().order_by("file_image")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("image", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def images(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_images(request)

        return render(request, "appManageWSSP/images.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "image",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_image(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_images(request)

        if request.method == "POST":
            form = ImagenForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    if "file_image" in request.FILES:
                        existImage = Imagen.objects.filter(file_image="images/" + str(form.cleaned_data["file_image"]))
                        if not existImage:
                            # create record in database
                            image = form.save(commit=False)
                            image.mediaType = "images"
                            image.user = request.user
                            image.save()
                            # load created record
                            return HttpResponseRedirect(reverse("adm_image", kwargs={"adm":"edit","id":image.id}))
                        else:
                            form.errors["__all__"] = form.error_class(["The image ( " + str(form.cleaned_data["file_image"]) + " ) already exists."])
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = ImagenForm()

        return render(request, "appManageWSSP/images.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "image",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_image(request, adm, id):
    if request.user.is_authenticated:

        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        old_image = ""
        try:
            image = Imagen.objects.get(pk=int(id))
            if image.file_image:
                old_image = image.file_image.name
        except:
            raise Http404
        
        searchinput, paginator, page_obj = retrieve_images(request)

        if request.method == "POST":
            form = ImagenForm(request.POST, request.FILES, instance=image)
            if form.is_valid():
                try:
                    existMatch = False
                    removeServerImage = False
                    if "file_image" in request.FILES:
                        existImage = Imagen.objects.filter(file_image="images/" + str(form.cleaned_data["file_image"]))
                        if existImage:
                            existMatch = True
                            form.errors["__all__"] = form.error_class(["The image ( " + str(form.cleaned_data["file_image"]) + " ) already exists."])
                        if old_image:
                            removeServerImage = True


                    if existMatch is False:
                        # create record in database
                        image = form.save(commit=False)
                        image.user = request.user
                        image.save()
                        # delete previous image from server only if it changed
                        if removeServerImage is True:
                            os.remove(settings.MEDIA_ROOT + old_image)
                        # load created record
                        return HttpResponseRedirect(reverse("adm_image", kwargs={"adm":"edit","id":image.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = ImagenForm(instance=image)

            if adm == "delete":
                isRelated = False
                if image.mediaResource_sections.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This image cannot be removed because it is related to a section."])
                elif image.mediaResource_graphicArticles.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This image cannot be removed because it is related to an article."])
                elif image.mediaResource_sliderElements.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This image cannot be removed because it is related to an article."])
                elif image.mediaResource_outstandingArticles.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This image cannot be removed because it is related to a outstanding."])
                elif image.mediaResource_authors.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This image cannot be removed because it is related to a author."])

                if isRelated is False:
                    # delete record from database
                    image.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("images"))

        return render(request, "appManageWSSP/images.html", {
            "form": form,
            "image": image,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "modelname": "image",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_videos(request):
    recordlist = Video.objects.all().order_by("title")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("video", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def videos(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_videos(request)

        return render(request, "appManageWSSP/videos.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "video",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_video(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_videos(request)
        
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    if form.cleaned_data["source"] == "server":
                        existVideo = Video.objects.filter(file_video="videos/" + str(form.cleaned_data["file_video"]))
                        if existVideo:
                            form.errors["file_video"] = form.error_class(["The video ( " + str(form.cleaned_data["file_video"]) + " ) already exists."])
                    else:
                        existVideo = Video.objects.filter(web_url=str(form.cleaned_data["web_url"]))
                        if existVideo:
                            form.errors["web_url"] = form.error_class(["A video with this url already exists."])
                    if not existVideo:
                        # create record in database
                        video = form.save(commit=False)
                        video.mediaType = "videos"
                        if form.cleaned_data["source"] == "server":
                            video.url = None
                        else:
                            video.file_video = None
                        video.user = request.user
                        video.save()
                        # load created record
                        return HttpResponseRedirect(reverse("adm_video", kwargs={"adm":"edit","id":video.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
                    raise
        else:
            form = VideoForm()

        return render(request, "appManageWSSP/videos.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "video",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_video(request, adm, id):
    if request.user.is_authenticated:

        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        old_video = ""
        # Validate existence of the record
        try:
            video = Video.objects.get(pk=int(id))
            if video.file_video:
                old_video = video.file_video.name
        except:
            raise Http404
        
        searchinput, paginator, page_obj = retrieve_videos(request)

        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES, instance=video)
            if form.is_valid():
                try:
                    existMatch = False
                    removeServerVideo = False
                    if form.cleaned_data["source"] == "server":
                        if "file_video" in request.FILES:
                            existVideo = Video.objects.filter(file_video="videos/" + str(form.cleaned_data["file_video"]))
                            if existVideo:
                                existMatch = True
                                form.errors["file_video"] = form.error_class(["The video ( " + str(form.cleaned_data["file_video"]) + " ) already exists."])
                            if old_video:
                                removeServerVideo = True
                    else:
                        existVideo = Video.objects.filter(web_url=str(form.cleaned_data["web_url"]))
                        if existVideo:
                            existMatch = True
                            form.errors["web_url"] = form.error_class(["A video with this url already exists."])
                        if old_video:
                            removeServerVideo = True

                    if existMatch is False:
                        # create record in database
                        video = form.save(commit=False)
                        if form.cleaned_data["source"] == "server":
                            video.web_url = None
                        else:
                            video.file_video = None
                        video.user = request.user
                        video.save()
                        # delete previous video from server only if it changed
                        if removeServerVideo is True:
                            os.remove(settings.MEDIA_ROOT + old_video)
                        # load created record
                        return HttpResponseRedirect(reverse("adm_video", kwargs={"adm":"edit","id":video.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = VideoForm(instance=video)

            if adm == "delete":
                isRelated = False
                if video.mediaResource_sections.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This video cannot be removed because it is related to a section."])
                elif video.mediaResource_graphicArticles.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This video cannot be removed because it is related to an article."])
                elif video.mediaResource_outstandingArticles.all():
                    isRelated = True
                    form.errors["__all__"] = form.error_class(["This video cannot be removed because it is related to a outstanding."])

                if isRelated is False:
                    # delete record from database
                    video.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("videos"))

        return render(request, "appManageWSSP/videos.html", {
            "form": form,
            "video": video,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "modelname": "video",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_htmlDesigns(request):
    recordlist = HtmlDesign.objects.all().order_by("file_html")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("htmlDesign", searchinput)

    recordlist = number_records(recordlist)

    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

@xframe_options_exempt
def htmlDesigns(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_htmlDesigns(request)

        return render(request, "appManageWSSP/htmlDesigns.html", {
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "htmlDesign",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

@xframe_options_exempt
def add_htmlDesign(request):
    if request.user.is_authenticated:
        searchinput, paginator, page_obj = retrieve_htmlDesigns(request)

        if request.method == "POST":
            form = HtmlDesignForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    if "file_html" in request.FILES:
                        existHtml = HtmlDesign.objects.filter(file_html="html/" + str(form.cleaned_data["file_html"]))
                        if not existHtml:
                            # create record in database
                            htmlDesign = form.save(commit=False)
                            htmlDesign.user = request.user
                            htmlDesign.save()
                            # load created record
                            return HttpResponseRedirect(reverse("adm_htmlDesign", kwargs={"adm":"edit","id":htmlDesign.id}))
                        else:
                            form.errors["__all__"] = form.error_class(["The html file ( " + str(form.cleaned_data["file_html"]) + " ) already exists."])
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
        else:
            form = HtmlDesignForm()

        return render(request, "appManageWSSP/htmlDesigns.html", {
            "form": form,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "modelname": "htmlDesign",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

@xframe_options_exempt
def adm_htmlDesign(request, adm, id):
    if request.user.is_authenticated:
        # validate existence of the url
        if not adm == "edit" and not adm == "delete":
            raise Http404

        # Validate existence of the record
        old_htmlDesign = ""
        try:
            htmlDesign = HtmlDesign.objects.get(pk=int(id))
            if htmlDesign.file_html:
                old_htmlDesign = htmlDesign.file_html.name
        except:
            raise Http404

        searchinput, paginator, page_obj = retrieve_htmlDesigns(request)

        if request.method == "POST":
            form = HtmlDesignForm(request.POST, request.FILES, instance=htmlDesign)
            if form.is_valid():
                try:
                    existMatch = False
                    removeServerHtmlDesign = False
                    if "file_html" in request.FILES:
                        existHtmlDesign = HtmlDesign.objects.filter(file_html="html/" + str(form.cleaned_data["file_html"]))
                        if existHtmlDesign:
                            existMatch = True
                            form.errors["__all__"] = form.error_class(["The html file ( " + str(form.cleaned_data["file_html"]) + " ) already exists."])
                        if old_htmlDesign:
                            removeServerHtmlDesign = True

                    if existMatch is False:
                        # create record in database
                        htmlDesign = form.save(commit=False)
                        htmlDesign.user = request.user
                        htmlDesign.save()
                        # delete previous image from server only if it changed
                        if removeServerHtmlDesign is True:
                            os.remove(settings.MEDIA_ROOT + old_htmlDesign)
                        # load created record
                        return HttpResponseRedirect(reverse("adm_htmlDesign", kwargs={"adm":"edit","id":htmlDesign.id}))
                except:
                    form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
        else:
            form = HtmlDesignForm(instance=htmlDesign)

            if adm == "delete":
                if not htmlDesign.htmlDesign_htmlArticles.all():
                    # delete record from database
                    htmlDesign.delete()
                    # load all records
                    return HttpResponseRedirect(reverse("htmlDesigns"))
                else:
                    form.errors["__all__"] = form.error_class(["This image cannot be removed because it is related to a section."])

        return render(request, "appManageWSSP/htmlDesigns.html", {
            "form": form,
            "htmlDesign": htmlDesign,
            "page_obj": page_obj,
            "paginator": paginator,
            "searchinput": searchinput,
            "edit_record": True,
            "modelname": "htmlDesign",
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def retrieve_users(request):
    recordlist = User.objects.all().order_by("username")

    searchinput = request.GET.get("search")
    if searchinput:
        recordlist = search_records("User", searchinput)
    recordlist = number_records(recordlist)
    paginator, page_obj = paginate_records(request, recordlist)

    return searchinput, paginator, page_obj

def users(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            searchinput, paginator, page_obj = retrieve_users(request)

            return render(request, "appManageWSSP/user.html", {
                "page_obj": page_obj,
                "paginator": paginator,
                "searchinput": searchinput,
                "modelname": "user"
            })
        else:
            return HttpResponseRedirect(reverse("limitedAccess"))
    else:
        return HttpResponseRedirect(reverse("login"))

def add_user(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # retrieve users
            searchinput, paginator, page_obj = retrieve_users()

            # Create a new user
            if request.method == "POST":
                form = UserForm(request.POST)

                if form.is_valid():
                    try:
                        record = form.save(commit=False)
                        record.user = request.user
                        record.save()

                        return HttpResponseRedirect(reverse("adm_user", kwargs={"adm":"edit","id":record.id}))
                    except:
                        form.errors["__all__"] = form.error_class(["There was a problem creating the record."])
            else:
                form = UserForm()

            return render(request, "appManageWSSP/users.html", {
                "form": form,
                "page_obj": page_obj,
                "paginator": paginator,
                "searchinput": searchinput,
                "modelname": "user",
            })
        else:
            return HttpResponseRedirect(reverse("limitedAccess"))
    else:
        return HttpResponseRedirect(reverse("login"))

def adm_user(request, adm, id):
    if request.user.is_authenticated:
        if (request.user.id == id) | (request.user.is_superuser):
            # validate existence of the url
            if not adm == "edit" and not adm == "delete":
                raise Http404

            # Validate existence of the record
            try:
                user = User.objects.get(pk=int(id))
            except:
                raise Http404

            # Retrieve users
            searchinput, paginator, page_obj = retrieve_users()

            # Edit or delete record
            if request.method == "POST":
                form = UserForm(request.POST, instance=user)
                if form.is_valid():
                    try:
                        # update record in database
                        record = form.save(commit=False)
                        record.user = request.user
                        record.save()

                        return HttpResponseRedirect(reverse("adm_user", kwargs={"adm":"edit","id":record.id}))
                    except:
                        form.errors["__all__"] = form.error_class(["There was a problem updating the record."])
            else:
                form = UserForm(instance=user)

                if adm == "delete":
                    if request.user.is_superuser:
                        try:
                            user.delete()
                            
                            return HttpResponseRedirect(reverse("users"))
                        except:
                            form.errors["__all__"] = form.error_class(["There was a problem deleting the record."])
                    else:
                        return HttpResponseRedirect(reverse("limitedAccess"))

            return render(request, "appManageWSSP/users.html", {
                "form": form,
                "element": user,
                "page_obj": page_obj,
                "paginator": paginator,
                "edit_record": True,
                "searchinput": searchinput,
                "modelname": "user",
            })
        else:
            return HttpResponseRedirect(reverse("limitedAccess"))
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "appManageWSSP/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "appManageWSSP/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Utilities
def search_records(model, searchinput, parent=None):

    searchinput_escaped = validate_text(searchinput)

    recordlist = []

    if model == "page":
        recordlist = Page.objects.filter(
            Q(title_es__icontains=searchinput_escaped) |
            Q(title_en__icontains=searchinput_escaped)
        ).distinct().order_by("display_order")
    elif model == "section":
        recordlist = parent.page_sections.filter(
            Q(title_es__icontains=searchinput_escaped) |
            Q(title_en__icontains=searchinput_escaped)
        ).distinct().order_by("display_order")
    elif model == "element":
        recordlist = parent.section_elements.filter(
            Q(title_es__icontains=searchinput_escaped) |
            Q(title_en__icontains=searchinput_escaped)
        ).distinct().order_by("title_es")
    elif model == "country":
        recordlist = Country.objects.filter(
            Q(name_es__icontains=searchinput_escaped) |
            Q(name_en__icontains=searchinput_escaped)
        ).distinct().order_by("name_es")
    elif model == "region":
        recordlist = Region.objects.filter(
            Q(name__icontains=searchinput_escaped)
        ).distinct().order_by("name")
    elif model == "province":
        recordlist = Province.objects.filter(
            Q(name__icontains=searchinput_escaped)
        ).distinct().order_by("name")
    elif model == "district":
        recordlist = District.objects.filter(
            Q(name__icontains=searchinput_escaped)
        ).distinct().order_by("name")
    elif model == "contact":
        recordlist = Contact.objects.filter(
            Q(name__icontains=searchinput_escaped) |
            Q(email__icontains=searchinput_escaped) |
            Q(message__icontains=searchinput_escaped)
        ).distinct().order_by("-created")
    elif model == "styleSheet":
        recordlist = StyleSheet.objects.filter(
            Q(name__icontains=searchinput_escaped)
        ).distinct().order_by("name")
    elif model == "author":
        recordlist = Author.objects.filter(
            Q(name__icontains=searchinput_escaped) |
            Q(profession__icontains=searchinput_escaped) |
            Q(work_company__icontains=searchinput_escaped)
        ).distinct().order_by("name")
    elif model == "user":
        recordlist = User.objects.filter(
            Q(username__icontains=searchinput_escaped) |
            Q(firs_name__icontains=searchinput_escaped) |
            Q(last_name__icontains=searchinput_escaped)
        ).distinct().order_by("username")

    return recordlist

def number_records(recordlist):
    numberingRecordlist = []
    number = 0

    for record in recordlist:
        number = number + 1
        record_dict = record.serialize()
        record_dict["number"] = number
        numberingRecordlist.append(record_dict)

    return numberingRecordlist

def paginate_records(request, modellist):
    page_number = request.GET.get("page", 1)

    try:
        paginator = Paginator(modellist, 10)
        page_obj = paginator.get_page(int(page_number))
    except:
        raise Http404

    return paginator, page_obj

def is_image_related_to_model(id):
    try:
        image = Imagen.objects.get(pk=int(id))
    except:
        return Http404

    if image.mediaResource_sections.all():
        return True
    elif image.mediaResource_graphicArticles.all():
        return True
    elif image.mediaResource_sliderElements.all():
        return True
    elif image.mediaResource_outstandingArticles.all():
        return True
    elif image.mediaResource_authors.all():
        return True
    else:
        return False

def is_video_related_to_model(id):
    try:
        video = Video.objects.get(pk=int(id))
    except:
        return Http404

    if video.mediaResource_sections.all():
        return True
    elif video.mediaResource_outstandingArticles.all():
        return True
    else:
        return False

def is_htmlfile_related_to_model(id):
    try:
        htmlFile = HtmlDesign.objects.get(pk=int(id))
    except:
        return Http404

    if htmlFile.htmlDesign_htmlArticles.all():
        return True
    else:
        return False

# Methods to retrieve data dynamically in Json format
# API Routes
def add_image_js(request):
    if request.user.is_authenticated:
        # Check request method
        if request.method == "POST":
            # Check media data
            form = ImagenForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    existImage = Imagen.objects.filter(file_image="images/" + form.cleaned_data["file_image"].name)
                    if not existImage:
                        # save file in server
                        # with open(settings.MEDIA_ROOT + 'images/' + upload_file.name, 'wb+') as destination:
                        #     for chunk in upload_file.chunks():
                        #         destination.write(chunk)
                        # save file in database
                        image = form.save(commit=False)
                        image.mediaType = "images"
                        image.user = request.user
                        image.save()
                        lastRecord = Imagen.objects.last()
                        # return last record
                        return JsonResponse(lastRecord.serialize())
                    else:
                        return JsonResponse({"form_errors":{"file_image":"The image ( " + form.cleaned_data["file_image"].name + " ) already exists, select it in the box bellow."}}, status=400)
                except:
                    return JsonResponse({"form_errors":{"all":"Failed to create the record."}}, status=400)
            else:
                return JsonResponse({"form_errors": form.errors}, status=400)
        else:
            return JsonResponse({"form_errors":{"all":"POST request required."}}, status=400)
    else:
        return render(request, "appManageWSSP/login.html")

def add_video_js(request):
    if request.user.is_authenticated:
        # Check request method
        if request.method == "POST":
            # Check media data
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    if form.cleaned_data["source"] == "server":
                        existVideo = Video.objects.filter(file_video="videos/" + form.cleaned_data["file_video"].name)
                        if existVideo:
                            return JsonResponse({"form_errors":{"file_video":"The video ( " + form.cleaned_data["file_video"].name + " ) already exists, select it in the box bellow."}}, status=400)
                    else:
                        existVideo = Video.objects.filter(web_url=form.cleaned_data["web_url"])
                        if existVideo:
                            return JsonResponse({"form_errors":{"web_url":"This video already exists, select it in the box bellow."}}, status=400)
                    if not existVideo:
                        # save file in database
                        video = form.save(commit=False)
                        video.mediaType = "videos"
                        if form.cleaned_data["source"] == "server":
                            video.url = None
                        else:
                            video.file_video = None
                        video.user = request.user
                        video.save()
                        lastRecord = Video.objects.last()
                        # return last record
                        return JsonResponse(lastRecord.serialize())
                except:
                    return JsonResponse({"form_errors":{"all":"Failed to create the record."}}, status=400)
            else:
                return JsonResponse({"form_errors": form.errors}, status=400)
        else:
            return JsonResponse({"form_errors":{"all":"POST request required."}}, status=400)
    else:
        return render(request, "appManageWSSP/login.html")

def add_htmlDesign_js(request):
    if request.user.is_authenticated:
        # Check request method
        if request.method == "POST":
            # Check media data
            form = HtmlDesignForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    existHtmlDesign = HtmlDesign.objects.filter(file_html="html/" + form.cleaned_data["file_html"].name)
                    if not existHtmlDesign:
                        # save file in database
                        htmlDesign = form.save(commit=False)
                        htmlDesign.user = request.user
                        htmlDesign.save()
                        lastRecord = HtmlDesign.objects.last()
                        # return last record
                        return JsonResponse(lastRecord.serialize())
                    else:
                        return JsonResponse({"form_errors":{"file_html":"The html design ( " + form.cleaned_data["file_html"].name + " ) already exists, select it in the main form."}}, status=400)
                except:
                    return JsonResponse({"form_errors":{"all":"Failed to create the record."}}, status=400)
            else:
                return JsonResponse({"form_errors": form.errors}, status=400)
        else:
            return JsonResponse({"form_errors":{"all":"POST request required."}}, status=400)
    else:
        return render(request, "appManageWSSP/login.html")

def retrieve_medias_js(request, type_media):
    if request.user.is_authenticated:
        try:
            if type_media == "images":
                # recover images
                images = Imagen.objects.all().order_by("file_image")
                # sent Json response
                return JsonResponse([image.serialize() for image in images], safe=False)
            elif type_media == "videos":
                # recover images
                videos = Video.objects.all().order_by("title")
                # sent Json response
                return JsonResponse([video.serialize() for video in videos], safe=False)
            else:
                return JsonResponse({"error": "Invalid media type."}, status=400)
        except:
            return JsonResponse({"error": "Failed retrieving records."}, status=404)
    else:
        return render(request, "appManageWSSP/login.html")

def retrieve_media_js(request, id_media):
    if request.user.is_authenticated:
        try:
            # recover media
            media = MediaResource.objects.get(pk=id_media)
            # recover media by type
            if media.mediaType == "images":
                media = Imagen.objects.get(pk=id_media)
            else:
                media = Video.objects.get(pk=id_media)
            # sent Json response
            return JsonResponse(media.serialize())
        except MediaResource.DoesNotExist:
            return JsonResponse({"error": "Media Resource not found."}, status=404)
    else:
        return render(request, "appManageWSSP/login.html")

def add_author_js(request):
    if request.user.is_authenticated:
        # Check request method
        if request.method == "POST":
            # Check media data
            form = AuthorForm(request.POST)
            if form.is_valid():
                try:
                    # save file in database
                    author = form.save(commit=False)
                    author.user = request.user
                    author.save()
                    lastRecord = Author.objects.last()
                    # return last record
                    return JsonResponse(lastRecord.serialize())
                except:
                    return JsonResponse({"form_errors":{"all":"Failed to create the record."}}, status=400)
            else:
                return JsonResponse({"form_errors": form.errors}, status=400)
        else:
            return JsonResponse({"form_errors":{"all":"POST request required."}}, status=400)
    else:
        return render(request, "appManageWSSP/login.html")

def retrieve_authors_js(request):
    if request.user.is_authenticated:
        try:
            # recover authors
            authors = Author.objects.all().order_by("name")
            # sent Json response
            return JsonResponse([author.serialize() for author in authors], safe=False)
        except:
            return JsonResponse({"error": "Failed retrieving records."}, status=404)
    else:
        return render(request, "appManageWSSP/login.html")

def retrieve_countries_js(request, lang):
    try:
        if lang == "es":
            countries = Country.objects.all().order_by("name_es")
        elif lang == "en":
            countries = Country.objects.all().order_by("name_en")
        else:
            return JsonResponse({"error": "Invalid language."}, status=400)

        return JsonResponse([country.serialize() for country in countries], safe=False)
    except:
        return JsonResponse({"error": "Failed retrieving records."}, status=404)

def retrieve_regions_js(request):
    try:
        country = Country.objects.get(name_en="PERU")
        regions = country.country_regions.all()

        return JsonResponse([region.serialize() for region in regions], safe=False)
    except:
        return JsonResponse({"error": "Failed retrieving records."}, status=404)

@csrf_exempt
def add_contact_js(request):
    # Check request method
    if request.method == "POST":
        # Check media data
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # save file in database
                contact = form.save(commit=False)
                contact.save()
                # creating a message (headers and text)
                header = 'From: {}\r\nTo: {}\r\nSubject: [IAA] - Contacto desde sitio web\r\n\r\n'.format(settings.EMAIL_SENDER_USER, settings.EMAIL_RECEIVER_USER)
                msg = header + """\
                Mensaje recibido desde el sitio web de Sierra Productiva.
                Se sugiere dar respuesta a este contacto cuyo email se encuentra listado lineas abajo.\n
                    Name:  {}
                    Email: {}
                    Mpvil: {}
                    Pais:  {}
                    Mensaje:\n
                    {}""".format(str(form.cleaned_data["name"]), str(form.cleaned_data["email"]), str(form.cleaned_data["telephone"]), str(form.cleaned_data["country"]), str(form.cleaned_data["message"]))
                print(msg)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(settings.EMAIL_HOST_SERVER, settings.EMAIL_PORT_SERVER, context=context) as server:
                    server.login(settings.EMAIL_SENDER_USER, settings.EMAIL_SENDER_PASSWORD)
                    server.sendmail(settings.EMAIL_SENDER_USER, settings.EMAIL_RECEIVER_USER, msg)
                # return successful answer
                return JsonResponse({"success": {"es":"Mensaje enviado satisfactoriamente", "en":"Message sent successfully."}})
            except Exception as error:
                return JsonResponse({"form_errors":{"all": {"es":"Error de envío. Por favor, intente nuevamente.", "en":"Email couldn't be sent. Please try again."}}}, status=400) 
        else:
            return JsonResponse({"form_errors": form.errors}, status=400)
    else:
        return JsonResponse({"form_errors":{"all":{"es":"Se requiere una solicitud POST", "en":"POST request required."}}}, status=400)

# Add location data dynamically.
def insert_country_data(request):
    user = User.objects.get(pk=1)
    with open('./insert_data/Paises.csv', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            register = Country(name_es=row[0], name_en=row[1], user=user)
            register.save()

    return HttpResponse("Country' registers were inserted to database successfully.")

def insert_region_data(request):
    user = User.objects.get(pk=1)
    pais = Country.objects.get(pk=1)

    with open("./insert_data/Regiones.csv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            registro = Region(name=row[0],scope=row[1],country=pais,user=user)
            registro.save()

    return HttpResponse("Region's registers were inserted to database successfully.")

def insert_province_data(request):
    user = User.objects.get(pk=1)

    with open("./insert_data/Provincias.csv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            region = Region.objects.get(pk=int(row[1]))
            registro = Province(name=row[0],region=region,user=user)
            registro.save()

    return HttpResponse("Province's registers were inserted to database successfully.")

def insert_district_data(request):
    user = User.objects.get(pk=1)

    with open("./insert_data/Distritos.csv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            province = Province.objects.get(pk=int(row[2]))
            registro = District(name=row[0],altitude=row[1],province=province,user=user)
            registro.save()

    return HttpResponse("District's registers were inserted to database successfully.")

def remove_district_data(request):
    for ide in range(1,125):
        remd = District.objects.get(pk=ide)
        remd.delete()

    return HttpResponse("District's registers were deleted from database successfully.")