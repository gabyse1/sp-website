document.addEventListener('DOMContentLoaded', function(){
    // navbar scroll
    window.addEventListener("scroll", function(){
    const headerHeight = document.querySelector(".head-container").offsetHeight;
        if(this.pageYOffset > headerHeight){
            document.querySelector(".head-container").classList.add("head-container-float");
        }
        else{
            document.querySelector(".head-container").classList.remove("head-container-float");
        }
    });

    // navbar submenu
    let navdropdowns = document.querySelectorAll('.nav-dropdown-toggle');

    navdropdowns.forEach(function(dropdown){

        dropdown.addEventListener('click', function(event){
            event.preventDefault();
            submenu = '#' + this.innerHTML.replace(/\s+/g,"").trim().toLowerCase();
            if(document.querySelector(submenu).classList.contains('hide-element')){
                document.querySelector(submenu).classList.remove('hide-element');
            }
            else{
                document.querySelector(submenu).classList.add('hide-element');
            }
        });
    });

    // set ckeditor width
    if(document.querySelector('.django-ckeditor-widget')){
        let ckeditors = document.querySelectorAll('.django-ckeditor-widget');
        ckeditors.forEach(function(ckedit){
            ckedit.style.width = "100%";
            ckedit.style.display= "flex";
        });
    }

    // change options of article origin from publication article
    if(document.querySelector('#id_article_origin')){
        document.querySelector('#id_media').removeAttribute("required");
        document.querySelector('#id_author').removeAttribute("required");
        document.querySelector('#id_source_web').removeAttribute("required");

        id_article_origin = document.querySelector('#id_article_origin');
        article_origin = id_article_origin.options[id_article_origin.selectedIndex].value;
        exchange_article_origin(article_origin);

        document.querySelector('#id_article_origin').addEventListener('change', function(){
            article_origin = this.options[this.selectedIndex].value;
            exchange_article_origin(article_origin);
        });
    }

    // retrieve selected media resource to display it as image or video
    if(document.querySelector('#id_media')){
        document.querySelector('#id_media').style.display = "none";
        id_media = document.querySelector('#id_media').value;
        // show media if it exists
        if (id_media > 0){
            fetch('/manage/retrieve/media/' + id_media)
            .then(response => response.json())
            .then(result => {
                display_media_in_main_form(result);
            })
            .catch(error => {
                console.error(error);
            });
        }
    }

    if(document.querySelector('#id_medias')){
        document.querySelector('#id_medias').style.display = "none";
        clean_html_element(document.querySelector('#form-content-media .row-grid'));
        let selectedOptions = getSelectedOptions(document.querySelector('#id_medias'));
        for(let i=0; i<selectedOptions.length; i++){
            fetch('/manage/retrieve/media/' + selectedOptions[i])
            .then(response => response.json())
            .then(result => {
                display_media_in_main_form(result);
            })
            .catch(error => {
                console.error(error);
            });
        }
    }

    if(document.querySelector('#id_list_icon')){
        document.querySelector('#id_list_icon').style.display = "none";
        id_media = document.querySelector('#id_list_icon').value;
        // show media if it exists
        if (id_media > 0){
            fetch('/manage/retrieve/media/' + id_media)
            .then(response => response.json())
            .then(result => {
                display_media_in_main_form(result,"tab-icon");
            })
            .catch(error => {
                console.error(error);
            });
        }
    }

    // retrieve selected medias from sliderElement to display them as images
    if(document.querySelector('#id_media_display_type')){

        if(document.querySelector('#id_media_display_type').value == "none"){
            clean_html_element(document.querySelector('#form-content-media .row-grid'));
            document.querySelector('#id_media_display_type [value="none"]').selected = true;
            document.querySelector('#select-media-link').style.display = "none";
            document.querySelector('#id_medias').parentElement.firstElementChild.style.display = "none";
        }

        document.querySelector('#id_media_display_type').addEventListener('change', function(){
            const selectedOptions = getSelectedOptions(document.querySelector('#id_medias'));

            if(document.querySelector('#id_media_display_type').value == "none"){
                // unselected all selected items
                for(let i=0; i<selectedOptions.length; i++){
                    document.querySelector('#id_medias [value="' + selectedOptions[i] + '"]').selected = false;
                }
                clean_html_element(document.querySelector('#form-content-media .row-grid'));
                document.querySelector('#id_media_display_type [value="none"]').selected = true;
                document.querySelector('#select-media-link').style.display = "none";
                document.querySelector('#id_medias').parentElement.firstElementChild.style.display = "none";
            }
            else{
                document.querySelector('#id_medias').parentElement.firstElementChild.style.display = "block";
                if(document.querySelector('#id_media_display_type').value == "simple"){
                    if(selectedOptions.length > 1){// multiple select.
                        let parent = document.querySelector('#form-content-media .row-grid');
                        for(let i=0; i<selectedOptions.length; i++){
                            if(i > 0){
                                document.querySelector('#id_medias [value="' + selectedOptions[i] + '"]').selected = false;
                                parent.removeChild(document.querySelector('#med-' + selectedOptions[i]));
                            }
                        }
                    }
                }
                document.querySelector('#select-media-link').style.display = "block";
            }
        });
    }

    // display DOM for choose element type
    if(document.querySelector('#new-record-element')){
        document.querySelector('#new-record-element').addEventListener('click', function(event){
            event.preventDefault();
            document.querySelector('#popup-container').classList.remove('hide-popup');
            document.querySelector('#popup-container').classList.add('float-popup');
            document.querySelector('#elementType-confirmation').classList.remove('hide-element');
        });

        document.querySelector('#elementType-confirmation #cancel-btn').addEventListener('click', function(event){
            event.preventDefault();
            document.querySelector('#popup-container').classList.add('hide-popup');
            document.querySelector('#popup-container').classList.remove('float-popup');
            document.querySelector('#elementType-confirmation').classList.add('hide-element');
        });
    }

    // create new section's element by type
    if(document.querySelectorAll('.select-elType')){
        domSelects = document.querySelectorAll('.select-elType');
        domSelects.forEach(function(domSelect){
            domSelect.addEventListener('change', function(){
                const template_name = domSelect.options[domSelect.selectedIndex].value;
                if (template_name != ""){
                    window.location.href = "/manage/add/" + template_name + "/" + this.id;
                    domSelect.value = "";

                    if(document.querySelector('#elementType-confirmation')){
                        document.querySelector('#popup-container').classList.add('hide-popup');
                        document.querySelector('#popup-container').classList.remove('float-popup');
                        document.querySelector('#elementType-confirmation').classList.add('hide-element');
                    }
                }
            });
        });
    }

    // create html name for section elements templates
    if(document.querySelector('#id_htmlName')){
        document.querySelector('#id_name').addEventListener('input', function(){
            type_name = document.querySelector('#id_name').value;
            type_name = type_name.charAt(0).toLowerCase() + type_name.slice(1);
            type_name = type_name.replace(/\s+/g,"").trim();
            document.querySelector('#id_htmlName').value = type_name;
        });
    }

    // create html file names for page's templates
    if(document.querySelector('#id_styleSheetName')){
        document.querySelector('#id_url_title_es').style.display = "none";
        document.querySelector('#id_url_title_en').style.display = "none";

        document.querySelector('#id_title_es').addEventListener('input', function(){
            htmlFile_name = document.querySelector('#id_title_es').value;
            words = htmlFile_name.split(" ");
            htmlFile = "";
            for(let i=0; i<words.length; i++){
                htmlFile += words[i].replace(/\s+/g,"").trim().toLowerCase();
            }
            document.querySelector('#id_styleSheetName').value = htmlFile;
            urlTitleEs = "";
            for(let i=0; i<words.length; i++){
                if(i > 0){
                    urlTitleEs += "-";
                }
                urlTitleEs += words[i].replace(/\s+/g,"").trim().toLowerCase();
            }
            document.querySelector("#id_url_title_es").value = urlTitleEs;
        });
        document.querySelector('#id_title_en').addEventListener('input', function(){
            htmlFile_name = document.querySelector('#id_title_en').value;
            words = htmlFile_name.split(" ");
            urlTitleEn = "";
            for(let i=0; i<words.length; i++){
                if(i > 0){
                    urlTitleEn += "-";
                }
                urlTitleEn += words[i].replace(/\s+/g,"").trim().toLowerCase();
            }
            document.querySelector("#id_url_title_en").value = urlTitleEn;
        });
    }

    // video form
    if (document.querySelector('#id_source')){
        id_source = document.querySelector('#id_source');
        video_source = id_source.options[id_source.selectedIndex].value;
        exchange_video_source(video_source);

        document.querySelector('#id_source').addEventListener('change', function(){
            video_source = this.options[this.selectedIndex].value;
            exchange_video_source(video_source);
        });
    }

    // delete records
    let deleteevents = document.querySelectorAll('.delete-record');
    deleteevents.forEach(function(deleteelement){
        deleteelement.addEventListener('click', function(event){
            event.preventDefault();
            const recordinfo = this.id.split('-');
            delete_record(recordinfo[1], recordinfo[2]);
        });
    });

    // set media or icon link
    let activeMediaIconLink = "media";

    // select media resource
    if (document.querySelector('#select-media-link')){
        document.querySelector('#select-media-link').addEventListener('click', function(event){
            event.preventDefault();
            activeMediaIconLink = "media";

            document.querySelector('#popup-container').classList.remove('hide-popup');
            document.querySelector('#popup-container').classList.add('float-popup');
            document.querySelector('#media-confirmation').classList.remove('hide-element');

            document.querySelector('#tab-image').classList.remove('hide-element');
            document.querySelector('#btn-tab-image').classList.add('active');

            if(document.querySelector('#btn-tab-video')){
                document.querySelector('#tab-video').classList.add('hide-element');
                document.querySelector('#btn-tab-video').classList.remove('active');
            }

            // initialize popup media
            set_media_gallery_height();
            initialize_image_form();
            retrieve_images_from_db("tab-image");

            //remove required attribute from media
            document.querySelector('#id_file_image').removeAttribute('required');

            if(document.querySelector('#btn-tab-video')){
                initialize_video_form();
                retrieve_videos_from_db();
                document.querySelector('#id_title').removeAttribute('required');
            }
        });
    }

    // select slider list icon
    if (document.querySelector('#select-icon-link')){
        document.querySelector('#select-icon-link').addEventListener('click', function(event){
            event.preventDefault();
            activeMediaIconLink = "icon";

            document.querySelector('#popup-container').classList.remove('hide-popup');
            document.querySelector('#popup-container').classList.add('float-popup');
            document.querySelector('#media-confirmation').classList.remove('hide-element');

            document.querySelector('#tab-image').classList.remove('hide-element');
            document.querySelector('#btn-tab-image').classList.add('active');

            // initialize popup media
            set_media_gallery_height();
            initialize_image_form();
            retrieve_images_from_db("tab-icon");

            //remove required attribute from media
            document.querySelector('#id_file_image').removeAttribute('required');
        });
    }

    // select html file
    if (document.querySelector('#select-htmlfile-link')){
        document.querySelector('#select-htmlfile-link').addEventListener('click', function(event){
            event.preventDefault();
            document.querySelector('#popup-container').classList.remove('hide-popup');
            document.querySelector('#popup-container').classList.add('float-popup');
            document.querySelector('#htmlfile-confirmation').classList.remove('hide-element');

            document.querySelector('#tab-htmlfile').classList.remove('hide-element');
            document.querySelector('#btn-tab-htmlfile').classList.add('active');

            document.querySelector("#id_file_html").value = "";

            //remove required attribute from html select
            document.querySelector('#id_file_html').removeAttribute('required');

        });
    }

    if (document.querySelector('#media-confirmation')){
        // media tabs click events
        document.querySelector('#btn-tab-image').addEventListener('click', function(){
            document.querySelector('#tab-image').classList.remove('hide-element');
            document.querySelector('#btn-tab-image').classList.add('active');

            if(document.querySelector('#btn-tab-video')){
                document.querySelector('#tab-video').classList.add('hide-element');
                document.querySelector('#btn-tab-video').classList.remove('active');
            }
        });

        if(document.querySelector('#btn-tab-video')){
            document.querySelector('#btn-tab-video').addEventListener('click', function(){
                document.querySelector('#tab-image').classList.add('hide-element');
                document.querySelector('#tab-video').classList.remove('hide-element');
                document.querySelector('#btn-tab-video').classList.add('active');
                document.querySelector('#btn-tab-image').classList.remove('active');
            });
        }

        document.querySelector('#btn-tab-close').addEventListener('click', function(){
            finish_media_popup();
        });

        // Insert new image media record
        document.querySelector('#save-image').addEventListener('click', function(event){
            event.preventDefault();
            let formElement = document.querySelector('#img-form');
            const data = new FormData(formElement);

            fetch('/manage/add/image/js', {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result["form_errors"]){
                    for (let key in result["form_errors"]){
                        ul = document.createElement("ul");
                        ul.setAttribute("class","errorlist");
                        li = document.createElement("li");
                        er = document.createTextNode(result["form_errors"][key]);
                        li.appendChild(er);
                        ul.appendChild(li);
                        parent = document.querySelector("#id_" + key).parentElement;
                        parent.removeChild(parent.lastChild);
                        parent.appendChild(ul);
                    }
                }
                else{
                    // remove last errores
                    if (document.querySelectorAll("#img-form .errorlist")){
                        elists = document.querySelectorAll("#img-form .errorlist");
                        elists.forEach(function(elist){
                            parent = elist.parentElement;
                            parent.removeChild(parent.lastChild);
                        });
                    }
                    // add last created media to media select element in mainform
                    elopt = document.createElement('option');
                    elopt.setAttribute("value", result["id"]);
                    eltxt = document.createTextNode(result["id"]);
                    elopt.appendChild(eltxt);

                    if(activeMediaIconLink == "icon"){
                        document.querySelector('#id_list_icon').appendChild(elopt);
                        document.querySelector('#id_list_icon [value="' + result["id"] + '"]').selected = true;
                        display_media_in_main_form(result,"tab-icon");
                    }
                    else{
                        if(document.querySelector('#id_media')){
                            document.querySelector('#id_media').appendChild(elopt);
                            document.querySelector('#id_media [value="' + result["id"] + '"]').selected = true;
                        }

                        if(document.querySelector('#id_medias')){
                            document.querySelector('#id_medias').appendChild(elopt);
                            if (document.querySelector('#id_media_display_type').value == "simple"){
                                let selectedOptions = getSelectedOptions(document.querySelector('#id_medias'));
                                for(let i=0; i<selectedOptions.length; i++){
                                    document.querySelector('#id_medias [value="' + selectedOptions[i] + '"]').selected = false;
                                    clean_html_element(document.querySelector('#form-content-media .row-grid'));
                                }
                                document.querySelector('#id_medias [value="' + result["id"] + '"]').selected = true;
                            }
                            else{
                                document.querySelector('#id_medias [value="' + result["id"] + '"]').selected = true;
                            }

                        }

                        display_media_in_main_form(result);
                    }
                    finish_media_popup();
                }
            })
            .catch(error => {
                alert(error);
            });
        });

        // Insert new video media record
        if(document.querySelector('#btn-tab-video')){
            document.querySelector('#save-video').addEventListener('click', function(event){
                event.preventDefault();
                let formElement = document.querySelector('#vid-form');
                const data = new FormData(formElement);

                fetch('/manage/add/video/js', {
                    method: 'POST',
                    body: data
                })
                .then(response => response.json())
                .then(result => {
                    if (result["form_errors"]){

                        for (let key in result["form_errors"]){
                            ul = document.createElement("ul");
                            ul.setAttribute("class","errorlist");
                            li = document.createElement("li");
                            er = document.createTextNode(result["form_errors"][key]);
                            li.appendChild(er);
                            ul.appendChild(li)
                            parent = document.querySelector("#id_" + key).parentElement;
                            next = document.querySelector("#id_" + key).nextSibling;
                            if (next){
                                parent.removeChild(parent.lastChild);
                            }
                            parent.appendChild(ul);
                        }
                    }
                    else{
                        // remove last errores
                        if (document.querySelectorAll("#vid-form .errorlist")){
                            elists = document.querySelectorAll("#vid-form .errorlist");
                            elists.forEach(function(elist){
                                parent = elist.parentElement;
                                parent.removeChild(parent.lastChild);
                            });
                        }
                        // add last media to media select in mainform
                        elopt = document.createElement('option');
                        elopt.setAttribute("value",result["id"]);
                        eltxt = document.createTextNode(result["id"]);
                        elopt.appendChild(eltxt);
                        document.querySelector('#id_media').appendChild(elopt);

                        // set and display new media
                        document.querySelector('#id_media [value="' + result["id"] + '"]').selected = true;
                        display_media_in_main_form(result);

                        finish_media_popup();
                    }
                })
                .catch(error => {
                    alert(error);
                });
            });
        }
    }

    if(document.querySelector('#htmlfile-confirmation')){
        // file tabs click events
        document.querySelector('#btn-tab-htmlfile').addEventListener('click', function(){
            document.querySelector('#tab-htmlfile').classList.remove('hide-element');
            document.querySelector('#btn-tab-htmlfile').classList.add('active');

        });

        document.querySelector('#btn-tab-close').addEventListener('click', function(){
            finish_htmlfile_popup();
        });

        // Insert new file record
        document.querySelector('#save-htmlfile').addEventListener('click', function(event){
            event.preventDefault();
            let formElement = document.querySelector('#htmlfile-form');
            const data = new FormData(formElement);

            fetch('/manage/add/htmlDesign/js', {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result["form_errors"]){

                    for (let key in result["form_errors"]){
                        ul = document.createElement("ul");
                        ul.setAttribute("class","errorlist");
                        li = document.createElement("li");
                        er = document.createTextNode(result["form_errors"][key]);
                        li.appendChild(er);
                        ul.appendChild(li)
                        parent = document.querySelector("#id_" + key).parentElement;
                        parent.removeChild(parent.lastChild);
                        parent.appendChild(ul);
                    }
                }
                else{
                    // remove last errores
                    if (document.querySelectorAll("#htmlfile-form .errorlist")){
                        elists = document.querySelectorAll("#htmlfile-form .errorlist");
                        elists.forEach(function(elist){
                            parent = elist.parentElement;
                            parent.removeChild(parent.lastChild);
                        });
                    }
                    // add last created html design to html design select element in mainform
                    elopt = document.createElement('option');
                    elopt.setAttribute("value", result["id"]);
                    eltxt = document.createTextNode(result["file_name"]);
                    elopt.appendChild(eltxt);

                    if(document.querySelector('#id_htmlDesign')){
                        document.querySelector('#id_htmlDesign').appendChild(elopt);
                        document.querySelector('#id_htmlDesign [value="' + result["id"] + '"]').selected = true;
                    }

                    finish_htmlfile_popup();
                }
            })
            .catch(error => {
                alert(error);
            });
        });
    }

    // select author record
    if(document.querySelector('#select-author-link')){
        document.querySelector('#select-author-link').addEventListener('click', function(event){
            event.preventDefault();
            document.querySelector('#popup-container').classList.remove('hide-popup');
            document.querySelector('#popup-container').classList.add('float-popup');
            document.querySelector('#author-confirmation').classList.remove('hide-element');
            document.querySelector('#tab-author').classList.remove('hide-element');
            document.querySelector('#tab-photo').classList.add('hide-element');
            document.querySelector('#btn-tab-author').classList.add('active');
            // hide id_photo
            document.querySelector('#id_photo').style.display = "none";
            // initialize author form
            set_author_form_height();
            initialize_author_form();
        });
    }

    if(document.querySelector('#author-confirmation')){
        // popup author photo
        if (document.querySelector('#select-photo-link')){
            document.querySelector('#select-photo-link').addEventListener('click', function(event){
                event.preventDefault();
                document.querySelector('#tab-author').classList.add('hide-element');
                document.querySelector('#tab-photo').classList.remove('hide-element');
                set_photo_gallery_height();
                // retrieve list of images from database
                document.querySelector("#id_file_photo").value = "";
                document.querySelector("#id_file_photo").removeAttribute("required");
                retrieve_images_from_db("tab-author");
            });
        }

        // set author photo field in popup-author
        if(document.querySelector('#id_photo')){
            document.querySelector('#id_photo').removeAttribute("required");
            // get author images
            fetch('/manage/retrieve/medias/images' )
            .then(response => response.json())
            .then(result => {
                let optList = `<option value="">---------</option>`;
                result.forEach(function(element){
                    optList += `<option value="` + element["id"] + `">` + element["file_url"] + `</option>`;

                });
                document.querySelector('#id_photo').innerHTML = optList;
            })
            .catch(error => {
                console.error(error);
            });
        }

        // Insert new author photograph record
        document.querySelector('#save-photo').addEventListener('click', function(event){
            event.preventDefault();
            let formElement = document.querySelector('#photo-form');
            const data = new FormData(formElement);
            const new_photo = data.get("file_photo");
            data.delete("file_photo");
            data.append("file_image",new_photo);
            debugger

            fetch('/manage/add/image/js', {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result["form_errors"]){

                    for (let key in result["form_errors"]){
                        ul = document.createElement("ul");
                        ul.setAttribute("class","errorlist");
                        li = document.createElement("li");
                        er = document.createTextNode(result["form_errors"][key]);
                        li.appendChild(er);
                        ul.appendChild(li)
                        parent = document.querySelector("#id_" + key).parentElement;
                        parent.removeChild(parent.lastChild);
                        parent.appendChild(ul);
                    }
                }
                else{
                    // remove last errores
                    if (document.querySelectorAll("#photo-form .errorlist")){
                        elists = document.querySelectorAll("#photo-form .errorlist");
                        elists.forEach(function(elist){
                            parent = elist.parentElement;
                            parent.removeChild(parent.lastChild);
                        });
                    }
                    // add last created photo to photo select in author form
                    elopt = document.createElement('option');
                    elopt.setAttribute("value", result["id"]);
                    eltxt = document.createTextNode(result["id"]);
                    elopt.appendChild(eltxt);

                    if(document.querySelector('#id_photo')){
                        document.querySelector('#id_photo').appendChild(elopt);
                        document.querySelector('#id_photo [value="' + result["id"] + '"]').selected = true;
                    }

                    display_media_in_main_form(result,"tab-author");

                    document.querySelector('#tab-author').classList.remove('hide-element');
                    document.querySelector('#tab-photo').classList.add('hide-element');
                }
            })
            .catch(error => {
                alert(error);
            });
        });

        // Insert new author record
        document.querySelector('#save-author').addEventListener('click', function(event){
            event.preventDefault();
            let formElement = document.querySelector('#author-form');
            const data = new FormData(formElement);
            const id_author_photo = data.get('photo');
            data.delete('photo');
            data.append('media',id_author_photo);

            fetch('/manage/add/author/js', {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result["form_errors"]){
                    for (let key in result["form_errors"]){
                        ul = document.createElement("ul");
                        ul.setAttribute("class","errorlist");
                        li = document.createElement("li");
                        er = document.createTextNode(result["form_errors"][key]);
                        li.appendChild(er);
                        ul.appendChild(li);
                        if(key == "media"){
                            key = "photo";
                        }
                        if(key != "all"){
                            parent = document.querySelector("#id_" + key).parentElement;
                            parent.removeChild(parent.lastChild);
                            parent.appendChild(ul);
                        }
                        else{
                            document.querySelector("#all-error-author").appendChild(ul);
                        }
                    }
                }
                else{
                    // remove last errores
                    if (document.querySelectorAll("#author-form .errorlist")){
                        elists = document.querySelectorAll("#author-form .errorlist");
                        elists.forEach(function(elist){
                            parent = elist.parentElement;
                            parent.removeChild(parent.lastChild);
                        });
                    }
                    // add last created author to author select in mainform
                    elopt = document.createElement('option');
                    elopt.setAttribute("value", result["id"]);
                    eltxt = document.createTextNode(result["name"]);
                    elopt.appendChild(eltxt);

                    if(document.querySelector('#id_author')){
                        document.querySelector('#id_author').appendChild(elopt);
                        document.querySelector('#id_author [value="' + result["id"] + '"]').selected = true;
                    }

                    document.querySelector('#btn-tab-author').classList.remove('active');
                    document.querySelector('#popup-container').classList.add('hide-popup');
                    document.querySelector('#popup-container').classList.remove('float-popup');
                    document.querySelector('#author-confirmation').classList.add('hide-element');
                }
            })
            .catch(error => {
                console.error(error);
            });
        });

        document.querySelector('#btn-tab-author-close').addEventListener('click', function(){
            document.querySelector('#btn-tab-author').classList.remove('active');
            document.querySelector('#popup-container').classList.add('hide-popup');
            document.querySelector('#popup-container').classList.remove('float-popup');
            document.querySelector('#author-confirmation').classList.add('hide-element');
        });
    }

    // set styles to password fields
    if(document.querySelector('#id_password1')){
        document.querySelector('#id_password1').classList.add("form-input-control");
    }
    if(document.querySelector('#id_password2')){
        document.querySelector('#id_password2').classList.add("form-input-control");
    }
    if(document.querySelector('#id_password')){
        document.querySelector('#id_password').classList.add("form-input-control");
    }

    // resize html files
    if(document.querySelectorAll('.insertfile')){
        let iframefiles = document.querySelectorAll(".insertfile");
        iframefiles.forEach(function(object){
            object.contentDocument.querySelector('body').style.height = object.parentElement.offsetHeight + "px";
            object.contentDocument.querySelector('body').style.width = "auto";
            object.style.height = object.parentElement.offsetHeight + "px";
            object.style.width = object.contentDocument.querySelector('body').offsetWidth + "px";
        });
    }
});

function retrieve_images_from_db(requesting_role){
    fetch('/manage/retrieve/medias/images')
    .then(response => response.json())
    .then(result => {
        listelements = `<div class="row-grid">`;
        result.forEach(function(element, index){
            listelements += `<div class="col-grid">
                                <div class="media-delimitator">
                                    <div class="media-container">
                                        <a id="` + element["id"] + `" class="media-object" href="#">
                                            <img src="` + element["file_url"] + `" alt="">
                                        </a>
                                    </div>
                                </div>
                            </div>`;
        });
        listelements += `</div>`;

        if(requesting_role == "tab-author"){
            clean_html_element(document.querySelector('#photo-gallery'));
            document.querySelector('#photo-gallery').innerHTML = listelements;
            set_select_event_to_media("tab-author");
        }

        if(requesting_role == "tab-icon"){
            clean_html_element(document.querySelector('#img-gallery'));
            document.querySelector('#img-gallery').innerHTML = listelements;
            set_select_event_to_media("tab-icon");
        }

        if(requesting_role == "tab-image"){
            clean_html_element(document.querySelector('#img-gallery'));
            document.querySelector('#img-gallery').innerHTML = listelements;
            set_select_event_to_media("tab-media");
        }
    })
    .catch(error => {
        console.error(error);
    });
}

function retrieve_videos_from_db(){
    fetch('/manage/retrieve/medias/videos')
    .then(response => response.json())
    .then(result => {
        listelements = `<div class="row-grid">`;
        result.forEach(function(element, index){
            listelements += `<div class="col-grid">
                                <div class="media-delimitator">
                                    <div class="media-container">
                                        <a id="` + element["id"] + `" class="media-object media-object-video" href="#">`;

            if (element["source"] == "server"){
                listelements += `<video controls>
                                    <source src="` + element["file_url"] + `" type="video/mp4">
                                </video>`;
            }
            else{
                listelements += `<iframe src="` + element["web_url"] + `"></iframe>`;
            }

            listelements += `<div class="button-select"><span>&#10003;</span></div>
                            </a>
                        </div>
                    </div>
                </div>`;
        });
        listelements += `</div>`;

        clean_html_element(document.querySelector('#vid-gallery'));
        document.querySelector('#vid-gallery').innerHTML = listelements;
        set_select_event_to_media("tab-media");
    })
    .catch(error => {
        console.error(error);
    });
}

function set_select_event_to_media(requesting_role){
    let mediaobjectevents = document.querySelectorAll('.media-object');
    mediaobjectevents.forEach(function(mediaobject){
        mediaobject.addEventListener('click', function(event){
            event.preventDefault();
            let isSelected = false;

            if(requesting_role == "tab-author"){
                fetch('/manage/retrieve/media/' + this.id)
                .then(response => response.json())
                .then(result => {
                    document.querySelector('#tab-photo').classList.add('hide-element');
                    document.querySelector('#tab-author').classList.remove('hide-element');
                    document.querySelector('#id_photo [value="' + this.id + '"]').selected = true;
                    display_media_in_main_form(result,"tab-author");
                })
                .catch(error => {
                    console.error(error);
                });
            }
            else{
                if(requesting_role == "tab-icon"){
                    if(document.querySelector('#id_list_icon [value="' + this.id + '"]').selected == true){
                        isSelected = true;
                    }
                    else{
                        document.querySelector('#id_list_icon [value="' + this.id + '"]').selected = true;
                    }
                }
                else{
                    if(document.querySelector('#id_media')){
                        if(document.querySelector('#id_media [value="' + this.id + '"]').selected == true){
                            isSelected = true;
                        }
                        else{
                            document.querySelector('#id_media [value="' + this.id + '"]').selected = true;
                        }
                    }

                    if(document.querySelector('#id_medias')){

                        if (document.querySelector('#id_media_display_type').value == "simple"){
                            if(document.querySelector('#id_medias [value="' + this.id + '"]').selected == false){
                                let selectedOptions = getSelectedOptions(document.querySelector('#id_medias'));
                                for(let i=0; i<selectedOptions.length; i++){
                                    document.querySelector('#id_medias [value="' + selectedOptions[i] + '"]').selected = false;
                                    clean_html_element(document.querySelector('#form-content-media .row-grid'));
                                }
                                document.querySelector('#id_medias [value="' + this.id + '"]').selected = true;
                            }
                            else{
                                isSelected = true;
                            }
                        }
                        else{
                            if (document.querySelector('#id_media_display_type').value == "multiple"){
                                if(document.querySelector('#id_medias [value="' + this.id + '"]').selected == true){
                                    isSelected = true;
                                }
                                else{
                                    document.querySelector('#id_medias [value="' + this.id + '"]').selected = true;
                                }
                            }
                        }
                    }
                }

                // retrieve media url
                if(isSelected == false){
                    fetch('/manage/retrieve/media/' + this.id)
                    .then(response => response.json())
                    .then(result => {
                        if(requesting_role == "tab-icon"){
                            display_media_in_main_form(result,"tab-icon");
                        }
                        else{
                            display_media_in_main_form(result,"tab-media");
                        }
                        document.querySelector('#popup-container').classList.add('hide-popup');
                        document.querySelector('#popup-container').classList.remove('float-popup');
                        document.querySelector('#media-confirmation').classList.add('hide-element');
                    })
                    .catch(error => {
                        console.error(error);
                    });
                }
                else{
                    document.querySelector('#popup-container').classList.add('hide-popup');
                    document.querySelector('#popup-container').classList.remove('float-popup');
                    document.querySelector('#media-confirmation').classList.add('hide-element');
                }
            }
        });
    });
}

function getSelectedOptions(select){
    let options = select.options;
    let opt;
    let selectedOptions = [];

    for (let i=0, iLen=options.length; i<iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            selectedOptions.push(opt.value);
        }
    }
    return selectedOptions;
}

function delete_record(modelname, identifier){

    document.querySelector('#popup-container').classList.remove('hide-popup');
    document.querySelector('#popup-container').classList.add('float-popup');
    document.querySelector('#delete-confirmation').classList.remove('hide-element');

    document.querySelector('#delete-confirmation #delete-btn').addEventListener('click', function(event){
        event.preventDefault();
        document.querySelector('#popup-container').classList.add('hide-popup');
        document.querySelector('#popup-container').classList.remove('float-popup');
        document.querySelector('#delete-confirmation').classList.add('hide-element');
        window.location.href = "/manage/delete/" + modelname + "/" + identifier;
    });

    document.querySelector('#delete-confirmation #cancel-btn').addEventListener('click', function(event){
        event.preventDefault();
        document.querySelector('#popup-container').classList.add('hide-popup');
        document.querySelector('#popup-container').classList.remove('float-popup');
        document.querySelector('#delete-confirmation').classList.add('hide-element');
    });
}

function display_media_in_main_form(result, requesting_role){

    if(requesting_role == "tab-author"){
        clean_html_element(document.querySelector('#form-content-photo .row-grid'));
    }
    else{
        if(requesting_role == "tab-icon"){
            clean_html_element(document.querySelector('#form-content-icon .row-grid'));
        }
        else{
            if(document.querySelector('#id_media')){
                clean_html_element(document.querySelector('#form-content-media .row-grid'));
            }
        }
    }

    elcol = document.createElement("div");
    elcol.setAttribute("class","col-grid");
    elcol.setAttribute("id","med-" + result['id']);
    elmde = document.createElement("div");
    elmde.setAttribute("class","media-delimitator");
    elmco = document.createElement("div");
    elmco.setAttribute("class","media-container");

    if (result['mediaType'] == 'images'){
        elmed = document.createElement('img');
        elmed.setAttribute("src", result['file_url']);
    }
    else{
        if (result['source'] == "server"){
            elmed = document.createElement('video');
            elmed.setAttribute("controls",true);
            elsrc = document.createElement('source');
            elsrc.setAttribute('src',result['file_url']);
            elmed.appendChild(elsrc);
        }
        else{
            elmed = document.createElement("iframe");
            elmed.setAttribute("src", result['web_url']);
        }
    }
    elmco.appendChild(elmed);

    elbtn = document.createElement("div");
    elbtn.setAttribute("class","button-close media-button-close");
    elspn = document.createElement("span");
    eltxt = document.createTextNode("X"); // &#9747;
    elspn.appendChild(eltxt);
    elbtn.appendChild(elspn);

    elbtn.addEventListener('click', function(){
        if(requesting_role == "tab-author"){
            document.querySelector('#id_photo [value=""]').selected = true;
            document.querySelector('#form-content-photo .row-grid').removeChild(document.querySelector('#med-' + result['id']));
        }
        else{
            if(requesting_role == "tab-icon"){
                document.querySelector('#id_list_icon [value=""]').selected = true;
                document.querySelector('#form-content-icon .row-grid').removeChild(document.querySelector('#med-' + result['id']));
            }
            else{
                if(document.querySelector('#id_media')){
                    document.querySelector('#id_media [value=""]').selected = true;
                }

                if(document.querySelector('#id_medias')){
                    document.querySelector('#id_medias [value="' + result['id'] + '"]').selected = false;
                }
                document.querySelector('#form-content-media .row-grid').removeChild(document.querySelector('#med-' + result['id']));
            }
        }
    });

    elmco.appendChild(elbtn);
    elmde.appendChild(elmco);
    elcol.appendChild(elmde);

    if(requesting_role == "tab-author"){
        document.querySelector('#form-content-photo .row-grid').appendChild(elcol);
    }
    else{
        if(requesting_role == "tab-icon"){
            document.querySelector('#form-content-icon .row-grid').appendChild(elcol);
        }
        else{
            document.querySelector('#form-content-media .row-grid').appendChild(elcol);
        }
    }
}

function exchange_video_source(video_source){
    if (video_source == "server"){
        // exchange video source
        url_parent = document.querySelector("#id_web_url").parentElement;
        url_parent.classList.add("hide-form-item");
        file_video_parent = document.querySelector("#id_file_video").parentElement;
        file_video_parent.classList.remove("hide-form-item");
    }
    else{
        url_parent = document.querySelector("#id_web_url").parentElement;
        url_parent.classList.remove("hide-form-item");
        file_video_parent = document.querySelector("#id_file_video").parentElement;
        file_video_parent.classList.add("hide-form-item");
    }

    if(document.querySelector('#btn-tab-video')){
        document.querySelector("#id_file_video").value = "";
        document.querySelector("#id_web_url").value = "";
    }
}

function exchange_article_origin(article_origin){
    if(article_origin == "web"){
        document.querySelector('#id_source_web').parentElement.classList.remove("hide-form-item");
    }
    else{
        document.querySelector('#id_source_web').value = "www.sierraproductiva.org";
        document.querySelector('#id_source_web').parentElement.classList.add("hide-form-item");
    }
}

function set_media_gallery_height(){
    // fix media gallery height
    popupcontenth = document.querySelector("#media-confirmation .popup-content").offsetHeight;
    headerh = document.querySelector("#tab-header").offsetHeight;
    titleh = document.querySelector('#tab-title').offsetHeight;
    formhi = document.querySelector('#img-form').offsetHeight;
    galleryhi = popupcontenth - headerh - titleh - formhi;
    document.querySelector('#img-gallery').style.height = galleryhi + "px";

    if(document.querySelector('#btn-tab-video')){
        formhv = document.querySelector('#vid-form').offsetHeight;
        galleryhv = popupcontenth - headerh - titleh - formhv;
        document.querySelector('#vid-gallery').style.height = galleryhv + "px";
    }
}

function set_photo_gallery_height(){
    popupcontenth = document.querySelector("#author-confirmation .popup-content").offsetHeight;
    headerh = document.querySelector("#tab-author-header").offsetHeight;
    titleh = document.querySelector('#tab-photo-title').offsetHeight;
    formhi = document.querySelector('#photo-form').offsetHeight;
    galleryhi = popupcontenth - headerh - titleh - formhi;
    document.querySelector('#photo-gallery').style.height = galleryhi + "px";
}

function set_author_form_height(){
    popupcontenth = document.querySelector("#author-confirmation .popup-content").offsetHeight;
    headerh = document.querySelector("#tab-author-header").offsetHeight;
    titleh = document.querySelector('#tab-author-title').offsetHeight;
    authorformh = popupcontenth - headerh - titleh;
    document.querySelector('#tab-author-form').style.height = authorformh + "px";
}

function initialize_image_form(){
    document.querySelector("#id_file_image").value = "";
}

function initialize_video_form(){
    document.querySelector("#id_title").value = "";
    document.querySelector('#id_source [value="server"]').selected = true;
    document.querySelector("#id_web_url").value = "";
    document.querySelector("#id_file_video").value = "";
}

function initialize_author_form(){
    document.querySelector("#id_name").value = "";
    document.querySelector("#id_profession_es").value = "";
    document.querySelector("#id_profession_en").value = "";
    document.querySelector('#id_photo [value=""]').selected = true;
    document.querySelector('#form-content-photo .row-grid').innerHTML = "";
    document.querySelector('#id_country [value=""]').selected = true;
}

function finish_media_popup(){
    if(document.querySelector('#btn-tab-video')){
        document.querySelector('#btn-tab-video').classList.remove('active');
    }
    if(document.querySelector('#btn-tab-image')){
        document.querySelector('#btn-tab-image').classList.remove('active');
    }

    document.querySelector('#popup-container').classList.add('hide-popup');
    document.querySelector('#popup-container').classList.remove('float-popup');
    document.querySelector('#media-confirmation').classList.add('hide-element');
}

function finish_htmlfile_popup(){
    if(document.querySelector('#btn-tab-htmlfile')){
        document.querySelector('#btn-tab-htmlfile').classList.remove('active');
    }

    document.querySelector('#popup-container').classList.add('hide-popup');
    document.querySelector('#popup-container').classList.remove('float-popup');
    document.querySelector('#htmlfile-confirmation').classList.add('hide-element');
}

function clean_html_element(parent){
    while(parent.firstElementChild){
        parent.removeChild(parent.firstElementChild);
    }
}

