from django.conf import settings
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render
from appManageWSSP.models import *
from PIL import Image

# Create your views here.
 
def get_page_es(request, pagename=None):
    if pagename == None:
        webPage = Page.objects.get(url_title_es="inicio")
    else:
        webPage = Page.objects.get(url_title_es=pagename)

    if webPage:
        # get page sections
        pageSections = webPage.page_sections.all().order_by("display_order")
        # get all page to display a dinamic menu on web site
        listPages = Page.objects.all().order_by("display_order")
        # set final list to store all informaciof of each section
        finalPageSections = []
        sectionCounter = 0

        for section in pageSections:
            sectionCounter += 1
            # get section serialize
            sectionDict = section.serialize()
            sectionDict["order"] = sectionCounter

            if section.media:
                if section.media.mediaType == "images":
                    image = Imagen.objects.get(pk=int(section.media.id))
                    imageSvg = image.file_image.name.endswith('.svg')
                    if imageSvg:
                        sectionDict["media_type"] = "imageSvg"
                    else:
                        sectionDict["media_type"] = "imageStandard"
                    sectionDict["media_url"] = image.file_image.url
                elif section.media.mediaType == "videos":
                    video = Video.objects.get(pk=int(section.media.id))
                    if video.source == "server":
                        sectionDict["media_type"] = "videoServer"
                        sectionDict["media_url"] = video.file_video.url
                    else:
                        sectionDict["media_type"] = "videoWeb"
                        sectionDict["media_url"] = video.web_url
            else:
                sectionDict["media_type"] = "none"

            # get section elements
            sectionElements = section.section_elements.all().order_by("display_order")
            
            sectionElementsList = []
            
            for element in sectionElements:
                sectionElementDict = {}
                sectionElementDict["elementType"] = element.elementType.htmlName
                sectionElementDict["title_es"] = element.title_es
                sectionElementDict["title_en"] = element.title_en
                sectionElementDict["show_title"] = element.show_title

                if element.elementType.htmlName == "descriptiveArticle":
                    descriptiveArticle = DescriptiveArticle.objects.get(pk=int(element.id))
                    sectionElementDict["description_es"] = descriptiveArticle.description_es
                    sectionElementDict["description_en"] = descriptiveArticle.description_en

                elif element.elementType.htmlName == "graphicArticle":
                    gArticle = GraphicArticle.objects.get(pk=int(element.id))
                    sectionElementDict["el_media_id"] = gArticle.media.id
                    if gArticle.media.mediaType == "images":
                        image = Imagen.objects.get(pk=int(gArticle.media.id))
                        imageSvg = image.file_image.name.endswith('.svg')
                        if imageSvg:
                            sectionElementDict["el_media_type"] = "imageSvg"
                        else:
                            sectionElementDict["el_media_type"] = "imageStandard"
                        sectionElementDict["el_media_url"] = image.file_image.url
                
                        imgsize = Image.open(settings.MEDIA_ROOT + image.file_image.name)
                        if imgsize.width > imgsize.height:
                            sectionElementDict["el_media_largeside"] = "largewidth"
                        else:
                            sectionElementDict["el_media_largeside"] = "largeheight"

                    elif gArticle.media.mediaType == "videos":
                        video = Video.objects.get(pk=int(gArticle.media.id))
                        if video.source == "server":
                            sectionElementDict["el_media_type"] = "videoServer"
                            sectionElementDict["el_media_url"] = video.file_video.url
                        else:
                            sectionElementDict["el_media_type"] = "videoWeb"
                            sectionElementDict["el_media_url"] = video.web_url

                elif element.elementType.htmlName == "slider":
                    slider = Slider.objects.get(pk=int(element.id))
                    sectionElementDict["sliderSize"] = slider.size
                    sectionElementDict["transitionType"] = slider.transitionType
                    sectionElementDict["display_sliderList"] = slider.display_sliderList
                    # get slider elements
                    sliderElements = slider.slider_sliderElements.all().order_by("display_order")
                    sliderElementsList = []
                    numberSliderElements = 0
                    for sliderElement in sliderElements:
                        numberSliderElements += 1
                        sliderElementDict = {}
                        sliderElementDict["slel_title_es"] = sliderElement.title_es
                        sliderElementDict["slel_title_en"] = sliderElement.title_en
                        sliderElementDict["slel_show_title"] = sliderElement.show_title
                        sliderElementDict["slel_description_es"] = sliderElement.description_es
                        sliderElementDict["slel_description_en"] = sliderElement.description_en

                        if slider.display_sliderList:
                            icon_image = Imagen.objects.get(pk=int(sliderElement.list_icon.id))
                            sliderElementDict["slel_list_icon_url"] = icon_image.file_image.url

                        sliderElementDict["slel_media_display_type"] = sliderElement.media_display_type

                        if sliderElement.media_display_type != "none":
                            sliderElementImagesList = []
        
                            medias = sliderElement.medias.all()
                            if medias:
                                for media in medias:
                                    sliderElementImagesDict = {}
                                    image = Imagen.objects.get(pk=int(media.id))
                                    if image.file_image.name.endswith('.svg'):
                                        sliderElementImagesDict["slel_media_type"] = "imageSvg"
                                    else:
                                        sliderElementImagesDict["slel_media_type"] = "imageStandard"
                                    sliderElementImagesDict["slel_media_url"] = image.file_image.url
                                    sliderElementImagesList.append(sliderElementImagesDict)
                            
                                sliderElementDict["slel_medias"] = sliderElementImagesList

                        sliderElementsList.append(sliderElementDict)
                    sectionElementDict["numberSliderElements"] = numberSliderElements
                    sectionElementDict["sliderElements"] = sliderElementsList

                elif element.elementType.htmlName == "outstanding":
                    outstanding = Outstanding.objects.get(pk=int(element.id))
                    # get outstanding's articles
                    outstandingArticles = outstanding.outstanding_outstandingArticles.all().order_by("-created")
                    outstandingArticlesList = []
                    
                    for outstandingArticle in outstandingArticles:
                        outstandingArticleDict = {}
                        outstandingArticleDict["outs_title_es"] = outstandingArticle.title_es
                        outstandingArticleDict["outs_title_en"] = outstandingArticle.title_en
                        outstandingArticleDict["outs_article_origin"] = outstandingArticle.article_origin
                        outstandingArticleDict["outs_source_web"] = outstandingArticle.source_web
                        outstandingArticleDict["outs_created"] = outstandingArticle.created

                        # get outstanding article media
                        if outstandingArticle.media.mediaType == "images":
                            image = Imagen.objects.get(pk=int(outstandingArticle.media.id))
                            outstandingArticleDict["outs_media_type"] = "imageStandard"
                            outstandingArticleDict["outs_media_url"] = image.file_image.url

                        elif outstandingArticle.media.mediaType == "videos":
                            video = Video.objects.get(pk=int(outstandingArticle.media.id))
                            if video.source == "server":
                                outstandingArticleDict["outs_media_type"] = "videoServer"
                                outstandingArticleDict["outs_media_url"] = video.file_video.url
                            else:
                                outstandingArticleDict["outs_media_type"] = "videoWeb"
                                outstandingArticleDict["outs_media_url"] = video.web_url
                        
                        # get outstanding author
                        outstandingArticleDict["outs_author_name"] = outstandingArticle.author.name
                        outstandingArticleDict["outs_author_profession_es"] = outstandingArticle.author.profession_es
                        outstandingArticleDict["outs_author_profession_en"] = outstandingArticle.author.profession_en
                        outstandingArticleDict["outs_author_country_es"] = outstandingArticle.author.country.name_es
                        outstandingArticleDict["outs_author_country_en"] = outstandingArticle.author.country.name_en

                        # get author media
                        if outstandingArticle.author.media.mediaType == "images":
                            image = Imagen.objects.get(pk=int(outstandingArticle.author.media.id))
                            outstandingArticleDict["outs_author_media_url"] = image.file_image.url

                        outstandingArticleDict["outs_description_es"] = outstandingArticle.description_es
                        outstandingArticleDict["outs_description_en"] = outstandingArticle.description_en
                        
                        outstandingArticlesList.append(outstandingArticleDict)
                    
                    sectionElementDict["outstandingArticles"] = outstandingArticlesList

                elif element.elementType.htmlName == "htmlArticle":
                    htmlArticle = HtmlArticle.objects.get(pk=int(element.id))
                    sectionElementDict["el_file_html_url"] = htmlArticle.htmlDesign.file_html.url
                
                sectionElementsList.append(sectionElementDict)

            sectionDict["numberElements"] = len(sectionElementsList)
            sectionDict["sectionElements"] = sectionElementsList
            finalPageSections.append(sectionDict)
    
        return render(request, f"appDisplayWSSP/pagemodeles.html", {
            "webPage": webPage,
            "listPages": listPages,
            "finalPageSections": finalPageSections,
        })
    else:
        raise Http404

def get_page_en(request, pagename=None):
    if pagename == None:
        webPage = Page.objects.get(url_title_en="home")
    else:
        webPage = Page.objects.get(url_title_en=pagename)

    if webPage:
        pageSections = webPage.page_sections.all().order_by("display_order")

        listPages = Page.objects.all().order_by("display_order")

        finalPageSections = []
        sectionCounter = 0

        for section in pageSections:
            sectionCounter += 1
            # get section serialize
            sectionDict = section.serialize()
            sectionDict["order"] = sectionCounter

            if section.media:
                if section.media.mediaType == "images":
                    image = Imagen.objects.get(pk=int(section.media.id))
                    imageSvg = image.file_image.name.endswith('.svg')
                    if imageSvg:
                        sectionDict["media_type"] = "imageSvg"
                    else:
                        sectionDict["media_type"] = "imageStandard"
                    sectionDict["media_url"] = image.file_image.url

                elif section.media.mediaType == "videos":
                    video = Video.objects.get(pk=int(section.media.id))
                    if video.source == "server":
                        sectionDict["media_type"] = "videoServer"
                        sectionDict["media_url"] = video.file_video.url
                    else:
                        sectionDict["media_type"] = "videoWeb"
                        sectionDict["media_url"] = video.web_url
                    
            else:
                sectionDict["media_type"] = "none"

            # get section's elements
            sectionElements = section.section_elements.all().order_by("display_order")
            
            sectionElementsList = []
            
            for element in sectionElements:
                sectionElementDict = {}
                sectionElementDict["elementType"] = element.elementType.htmlName
                sectionElementDict["title_es"] = element.title_es
                sectionElementDict["title_en"] = element.title_en
                sectionElementDict["show_title"] = element.show_title

                if element.elementType.htmlName == "descriptiveArticle":
                    descriptiveArticle = DescriptiveArticle.objects.get(pk=int(element.id))
                    sectionElementDict["description_es"] = descriptiveArticle.description_es
                    sectionElementDict["description_en"] = descriptiveArticle.description_en

                elif element.elementType.htmlName == "graphicArticle":
                    gArticle = GraphicArticle.objects.get(pk=int(element.id))
                    sectionElementDict["el_media_id"] = gArticle.media.id
                    if gArticle.media.mediaType == "images":
                        image = Imagen.objects.get(pk=int(gArticle.media.id))
                        imageSvg = image.file_image.name.endswith('.svg')
                        if imageSvg:
                            sectionElementDict["el_media_type"] = "imageSvg"
                        else:
                            sectionElementDict["el_media_type"] = "imageStandard"
                        sectionElementDict["el_media_url"] = image.file_image.url
                
                        imgsize = Image.open(settings.MEDIA_ROOT + image.file_image.name)
                        if imgsize.width > imgsize.height:
                            sectionElementDict["el_media_largeside"] = "largewidth"
                        else:
                            sectionElementDict["el_media_largeside"] = "largeheight"

                    elif gArticle.media.mediaType == "videos":
                        video = Video.objects.get(pk=int(gArticle.media.id))
                        if video.source == "server":
                            sectionElementDict["el_media_type"] = "videoServer"
                            sectionElementDict["el_media_url"] = video.file_video.url
                        else:
                            sectionElementDict["el_media_type"] = "videoWeb"
                            sectionElementDict["el_media_url"] = video.web_url

                elif element.elementType.htmlName == "slider":
                    slider = Slider.objects.get(pk=int(element.id))
                    sectionElementDict["sliderSize"] = slider.size
                    sectionElementDict["transitionType"] = slider.transitionType
                    sectionElementDict["display_sliderList"] = slider.display_sliderList
                    # get slider elements
                    sliderElements = slider.slider_sliderElements.all().order_by("display_order")
                    sliderElementsList = []
                    numberSliderElements = 0
                    for sliderElement in sliderElements:
                        numberSliderElements += 1
                        sliderElementDict = {}
                        sliderElementDict["slel_title_es"] = sliderElement.title_es
                        sliderElementDict["slel_title_en"] = sliderElement.title_en
                        sliderElementDict["slel_show_title"] = sliderElement.show_title
                        sliderElementDict["slel_description_es"] = sliderElement.description_es
                        sliderElementDict["slel_description_en"] = sliderElement.description_en

                        if slider.display_sliderList:
                            icon_image = Imagen.objects.get(pk=int(sliderElement.list_icon.id))
                            sliderElementDict["slel_list_icon_url"] = icon_image.file_image.url

                        sliderElementDict["slel_media_display_type"] = sliderElement.media_display_type

                        if sliderElement.media_display_type != "none":
                            sliderElementImagesList = []
        
                            medias = sliderElement.medias.all()
                            if medias:
                                for media in medias:
                                    sliderElementImagesDict = {}
                                    image = Imagen.objects.get(pk=int(media.id))
                                    if image.file_image.name.endswith('.svg'):
                                        sliderElementImagesDict["slel_media_type"] = "imageSvg"
                                    else:
                                        sliderElementImagesDict["slel_media_type"] = "imageStandard"
                                    sliderElementImagesDict["slel_media_url"] = image.file_image.url
                                    sliderElementImagesList.append(sliderElementImagesDict)
                            
                                sliderElementDict["slel_medias"] = sliderElementImagesList

                        sliderElementsList.append(sliderElementDict)
                    sectionElementDict["numberSliderElements"] = numberSliderElements
                    sectionElementDict["sliderElements"] = sliderElementsList

                elif element.elementType.htmlName == "outstanding":
                    outstanding = Outstanding.objects.get(pk=int(element.id))
                    # get outstanding's articles
                    outstandingArticles = outstanding.outstanding_outstandingArticles.all().order_by("-created")
                    outstandingArticlesList = []
                    
                    for outstandingArticle in outstandingArticles:
                        outstandingArticleDict = {}
                        outstandingArticleDict["outs_title_es"] = outstandingArticle.title_es
                        outstandingArticleDict["outs_title_en"] = outstandingArticle.title_en
                        outstandingArticleDict["outs_article_origin"] = outstandingArticle.article_origin
                        outstandingArticleDict["outs_source_web"] = outstandingArticle.source_web
                        outstandingArticleDict["outs_created"] = outstandingArticle.created

                        # get outstanding article media
                        if outstandingArticle.media.mediaType == "images":
                            image = Imagen.objects.get(pk=int(outstandingArticle.media.id))
                            outstandingArticleDict["outs_media_type"] = "imageStandard"
                            outstandingArticleDict["outs_media_url"] = image.file_image.url

                        elif outstandingArticle.media.mediaType == "videos":
                            video = Video.objects.get(pk=int(outstandingArticle.media.id))
                            if video.source == "server":
                                outstandingArticleDict["outs_media_type"] = "videoServer"
                                outstandingArticleDict["outs_media_url"] = video.file_video.url
                            else:
                                outstandingArticleDict["outs_media_type"] = "videoWeb"
                                outstandingArticleDict["outs_media_url"] = video.web_url
                        
                        # get outstanding author
                        outstandingArticleDict["outs_author_name"] = outstandingArticle.author.name
                        outstandingArticleDict["outs_author_profession_es"] = outstandingArticle.author.profession_es
                        outstandingArticleDict["outs_author_profession_en"] = outstandingArticle.author.profession_en
                        outstandingArticleDict["outs_author_country_es"] = outstandingArticle.author.country.name_es
                        outstandingArticleDict["outs_author_country_en"] = outstandingArticle.author.country.name_en

                        # get author media
                        if outstandingArticle.author.media.mediaType == "images":
                            image = Imagen.objects.get(pk=int(outstandingArticle.author.media.id))
                            outstandingArticleDict["outs_author_media_url"] = image.file_image.url

                        outstandingArticleDict["outs_description_es"] = outstandingArticle.description_es
                        outstandingArticleDict["outs_description_en"] = outstandingArticle.description_en
                        
                        outstandingArticlesList.append(outstandingArticleDict)
                    
                    sectionElementDict["outstandingArticles"] = outstandingArticlesList

                elif element.elementType.htmlName == "htmlArticle":
                    htmlArticle = HtmlArticle.objects.get(pk=int(element.id))
                    sectionElementDict["el_file_html_url"] = htmlArticle.htmlDesign.file_html.url
                
                sectionElementsList.append(sectionElementDict)

            sectionDict["numberElements"] = len(sectionElementsList)
            sectionDict["sectionElements"] = sectionElementsList
            finalPageSections.append(sectionDict)
    
        return render(request, f"appDisplayWSSP/pagemodelen.html", {
            "webPage": webPage,
            "listPages": listPages,
            "finalPageSections": finalPageSections,
        })
    else:
        raise Http404


# API Routes
def retrieve_countries(request):
    try:
        # recover images
        countries = Country.objects.all().order_by("name_es")
        # sent Json response
        return JsonResponse([country.serialize() for country in countries], safe=False)
    except:
        return JsonResponse({"error": "Failed retrieving records."}, status=404)