document.addEventListener('DOMContentLoaded', function(){

	// INICIALIZACIÓN DE VARIABLES GLOBALES PARA TODAS LAS PÁGINAS
	let paginaWeb = document.querySelector('#body-container').dataset.pageorder;
	let activeLanguage = document.querySelector("html").getAttribute("lang");
	let id_seccion = 1;
	let nroSeccionesPW = $('#body-container').children('section').length;
	let nroSeccionDestino = 0;

	// INICIALIZACION DE VARIABLES PARA USO DEL EVENTO SCROLL
	let actualPosicionScrollTop = 0;
    let ultimaPosicionScrollTop = 0;
	let newActiveSection = 0;
	let newActiveSectionTop = 0;
	let activeStateScrollAnimation = false;
	let scrollActivado = false;

	// INICIALIZACION DE VARIABLES PARA SLIDER INTERACTIVO
	let nroItemsSliderInteractivoN1 = 0;
	let indPosActSliderInteractivoN1 = 0;
	let timeSliderInteractivoN1 = 0;

	// INICIALIZACION DE VARIABLES PARA SLIDERS AUTOMATICOS NIVEL 1
    let nroItemsSliderAutomaticoN1 = 0;
    let nroPosicionSliderAutomaticoN1 = 1;
    let ejecutarSliderAutomaticoN1 = 0;

    // INICIALIZACION DE VARIABLES PARA SLIDERS AUTOMATICOS NIVEL 2
    let nroItemsSliderAutomaticoN2 = 0;
   	let nroPosicionSliderAutomaticoN2 = 1;
   	let ejecutarSliderAutomaticoN2 = 0;

	// INICIALIZACION DE VARIABLES PARA REPRODUCCION DE VIDEOS
    let playProgressInterval = 0;
    let mouseclickMostrarControles = 0;
    let videoFullScreen = false;

    // INICIALIZACION DE FUNCIONES EN LA PRIMERA CARGA DE PÁGINA WEB
	func_aplicarAjustesEnElementos();
    func_actualizarNavegadorSecciones(1,1);
    func_inicializarSlidersInteractivosN1();
    func_inicializarSlidersAutomaticosN1();
    func_inicializarSlidersAutomaticosN2();
    func_addSocialNetworkIcons();
    func_inicializarElementosDeSeccionActual(id_seccion);

	// FUNCIONES PARA INICIALIZAR SLIDERS INTERACTIVOS DE LA PÁGINA
	function func_inicializarSlidersInteractivosN1(){

		let nroItemsSIN1 = 0;
		let numItemsSIN1 = 0;

		for(let i = 1; i <= nroSeccionesPW; i++){

			nroItemsSIN1 = $('#seccion_'+i+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1').length;

			if(nroItemsSIN1 > 1){
				if(nroItemsSIN1 > 2){
					$('#seccion_'+i+' .ul_slider_interactivo_nivel1').css('width',(nroItemsSIN1*100)+'%');
					$('#seccion_'+i+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('height',(nroItemsSIN1*100)+'%');

					$('#seccion_'+i+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child').insertBefore($('#seccion_'+i+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child'));
					$('#seccion_'+i+' .ul_slider_interactivo_nivel1').css('margin-left','-100%');

					$('#seccion_'+i+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child').insertBefore($('#seccion_'+i+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child'));
					$('#seccion_'+i+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');
				}
				else{
					$('#seccion_'+i+' .ul_slider_interactivo_nivel1').css('width',(nroItemsSIN1*100)+'%');
			    	$('#seccion_'+i+' .ul_slider_interactivo_nivel1').css('margin-left','0%');

					$('#seccion_'+i+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('height',(nroItemsSIN1*100)+'%');
					$('#seccion_'+i+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','0%');
				}

				$('#seccion_'+i+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',(100/nroItemsSIN1)+'%');
			}
		}
		func_updateActiveItemSliderFromList(0,0);

		$('#seccion_'+id_seccion+' .aside-slider-menu').css('left','0%');
	}

	function func_inicializarSlidersAutomaticosN1(){

		let nroItemsSAN1 = 0;

		for(let i = 1; i <= nroSeccionesPW; i++){

			nroItemsSAN1 = $('#seccion_'+i+' .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1').length;

			if(nroItemsSAN1 > 1){

		    	$('#seccion_'+i+' .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1').hide();
		    	$('#seccion_'+i+' .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:first-child').show();

		    	$('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden').css('height',(nroItemsSAN1*100)+'%');
			    $('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child').insertBefore($('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child'));
			    $('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');

			    if(paginaWeb == 1){
			    	if(i == 1){
			    		$('#seccion_1 .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+') img').css('left','0%');
			    		$('#seccion_1 .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+') img').animate({left: "-=4.5%"}, 8000, 'linear');

			    		$('#seccion_1 .slider_automatico_paginacion_nro .slider_paginacion_linea_animada').css('animation','paginacionLineaAnimadaAutomatica 4s linear infinite alternate');
			    	}
		    	}
			}
		}
	}

	function func_inicializarSlidersAutomaticosN2(){

		let nroItemsSAN2 = 0;

		for(let i = 1; i <= nroSeccionesPW; i++){

			nroItemsSAN2 = $('#seccion_'+i+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:nth-child(1) .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2').length;

			if(nroItemsSAN2 > 1){

		    	$('#seccion_'+i+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1 .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2').hide();
		    	$('#seccion_'+i+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1 .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2:first-child').show();

		    	$('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden').css('height',(nroItemsSAN2*100)+'%');
			    $('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child').insertBefore($('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child'));
			    $('#seccion_'+i+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');
			}
		}
	}

    // FUNCIONES SCROLL PARA VISUALIZACION DE SECCIONES A PANTALLA COMPLETA
		$(window).scroll(function(){

    	actualPosicionScrollTop = window.pageYOffset;

    	if(!scrollActivado){

	    	if(actualPosicionScrollTop > ultimaPosicionScrollTop){
    			id_seccion++;
    			id_seccion = id_seccion > nroSeccionesPW ? nroSeccionesPW : id_seccion;

		    	newActiveSection = document.getElementById('seccion_'+id_seccion);
		    	newActiveSectionTop = newActiveSection.getBoundingClientRect().top + actualPosicionScrollTop;
	    		$('html,body').animate({scrollTop: newActiveSectionTop},1000,function(){
	    			activeStateScrollAnimation = false;
	    		});
		    	func_restablecerElementosDeSeccionAnterior(id_seccion - 1);
		    	func_actualizarNavegadorSecciones(id_seccion - 1,id_seccion);
	    	}
	    	else{
	    		if(actualPosicionScrollTop < ultimaPosicionScrollTop){
	    			id_seccion--;
	    			id_seccion = id_seccion < 1 ? 1 : id_seccion;

			    	newActiveSection = document.getElementById('seccion_'+id_seccion);
			    	newActiveSectionTop = newActiveSection.getBoundingClientRect().top + actualPosicionScrollTop;
	    			$('html,body').animate({scrollTop: newActiveSectionTop},1000,function(){
		    			activeStateScrollAnimation = false;
		    		});
		    		func_restablecerElementosDeSeccionAnterior(id_seccion + 1);
		    		func_actualizarNavegadorSecciones(id_seccion + 1,id_seccion);
	    		}
	    	}

	    	func_inicializarElementosDeSeccionActual(id_seccion);
	    	scrollActivado = true;
	    	activeStateScrollAnimation = true;
	    }
	    else{

	    	if(!activeStateScrollAnimation){
	    		if(actualPosicionScrollTop > ultimaPosicionScrollTop){
		    		scrollActivado = false;
		    	}
		    	else{
		    		if(actualPosicionScrollTop < ultimaPosicionScrollTop){
		    			scrollActivado = false;
			    	}
		    	}
			}
	    }

	    ultimaPosicionScrollTop = actualPosicionScrollTop;
    });

    // FUNCIONES PARA RESTABLECER E INICIALIZAR ELEMENTOS DE SECCIONES
    function func_restablecerElementosDeSeccionAnterior(seccionAnterior){

    	// REINICIALIZAR SLIDER INTERACTIVO ANTERIOR
		if (nroItemsSliderInteractivoN1 == 2) {
	    	func_restSliderInteractivoN1C2(seccionAnterior,indPosActSliderInteractivoN1);
	    }
	    else{
	    	if(nroItemsSliderInteractivoN1 > 2) {
	    		func_restSliderInteractivoN1CX(seccionAnterior,indPosActSliderInteractivoN1);
	    	}
	    }

	    // REINICIALIZAR SLIDER AUTOMÁTICO ANTERIOR
	    if(nroItemsSliderAutomaticoN1 > 1){
	    	func_restSliderAutomaticoN1(seccionAnterior);
	    }

	    if(nroItemsSliderAutomaticoN2 > 1){
	    	func_restSliderAutomaticoN2(seccionAnterior);
	    }

	    // REPRODUCCION DE VIDEO
		func_pausarVideoAutomaticamente(seccionAnterior);
		func_fullScreenOffVideo(seccionAnterior);
    }

	function func_inicializarElementosDeSeccionActual(seccionActual){

		// INICIALIZAR SLIDER INTERACTIVO ACTUAL
		indPosActSliderInteractivoN1 = 0;
		nroItemsSliderInteractivoN1 = $('#seccion_'+seccionActual+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1').length;

		// INCIALIZAR EJECUCION DE SLIDER AUTOMATICO ACTUAL N1
		nroPosicionSliderAutomaticoN1 = 1;
		nroItemsSliderAutomaticoN1 = $('#seccion_'+seccionActual+' .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1').length;
		if(nroItemsSliderAutomaticoN1 > 1){
			func_executeSliderAutomaticoN1();
		}

		// INCIALIZAR EJECUCION DE SLIDER AUTOMATICO ACTUAL N2
		nroPosicionSliderAutomaticoN2 = 1;
		nroItemsSliderAutomaticoN2 = $('#seccion_'+seccionActual+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:nth-child(1) .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2').length;
		if(nroItemsSliderAutomaticoN2 > 1){
			func_executeSliderAutomaticoN2();
		}

		// REPRODUCCION DE VIDEO
		func_inicializarVideoAutomaticamente();
	}

	// FUNCIONES PARA ACTUALIZAR NAVEGADOR DE SECCIONES
	function func_actualizarNavegadorSecciones(seccionAnterior,seccionActual){


		let lastActiveSectionFont = document.getElementsByClassName('nav_secciones_fuente_'+seccionAnterior);
		if(lastActiveSectionFont.length > 0){
			lastActiveSectionFont[0].classList.remove('nav_secciones_fuente_activa');
		}

		let lastActiveSectionBar = document.getElementsByClassName('nav_secciones_barra_'+seccionAnterior);
		if(lastActiveSectionBar.length > 0){
			lastActiveSectionBar[0].classList.remove('nav_secciones_barra_activa');
		}

		let newActiveSectionFont = document.getElementsByClassName('nav_secciones_fuente_'+seccionActual);
		if(newActiveSectionFont.length > 0){
			newActiveSectionFont[0].classList.add('nav_secciones_fuente_activa');
		}

		let newActiveSectionBar = document.getElementsByClassName('nav_secciones_barra_'+seccionActual);
		if(newActiveSectionBar.length > 0){
			newActiveSectionBar[0].classList.add('nav_secciones_barra_activa');
		}
	}

	// FUNCIONES PARA EJECUCIÓN DE SLIDERS INTERACTIVOS

    function func_restSliderInteractivoN1C2(seccion,indPosicionActualSlider){

    	let contIteraciones = 1;

    	if(indPosicionActualSlider == 0){
    		timeSliderInteractivoN1 = 1000;
    	}
    	else{
    		timeSliderInteractivoN1 = 1000/indPosicionActualSlider;
    	}

    	while(contIteraciones <= indPosicionActualSlider){

	    	$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1').animate({marginLeft:'-100%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child').insertAfter($('#seccion_'+seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child'));
	    		$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1').css('margin-left','0%');
	    	});

	    	$('#seccion_'+seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'-100%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child').insertAfter( $('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child'));
	    		$('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','0%');
	    	});

    		contIteraciones++;
    	}

    	indPosActSliderInteractivoN1 = 0;

    	$('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',((100/nroItemsSliderInteractivoN1)*(indPosActSliderInteractivoN1+1))+'%');
    }

    function func_nextSliderInteractivoN1C2(indPosicionObjetivoSlider){

    	timeSliderInteractivoN1 = 1000;

    	$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').animate({marginLeft:'-100%'},timeSliderInteractivoN1, function(){
    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child').insertAfter($('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child'));
    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').css('margin-left','0%');
    	});

    	$('#seccion_'+id_seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'-100%'},timeSliderInteractivoN1, function(){
    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child').insertAfter( $('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child'));
    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','0%');
    	});

    	indPosActSliderInteractivoN1 = indPosicionObjetivoSlider;

    	$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',((100/nroItemsSliderInteractivoN1)*(indPosActSliderInteractivoN1+1))+'%');
    }

    function func_prevSliderInteractivoN1C2(indPosicionObjetivoSlider){

    	timeSliderInteractivoN1 = 1000;

    	$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').animate({marginLeft:'-100%'},timeSliderInteractivoN1, function(){
    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child').insertAfter($('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child'));
    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').css('margin-left','0%');
    	});

    	$('#seccion_'+id_seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'-100%'},timeSliderInteractivoN1, function(){
    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child').insertAfter( $('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child'));
    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','0%');
    	});

    	indPosActSliderInteractivoN1 = indPosicionObjetivoSlider;

    	$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',((100/nroItemsSliderInteractivoN1)*(indPosActSliderInteractivoN1+1))+'%');
    }

    function func_restSliderInteractivoN1CX(seccion,indPosicionActualSlider){

    	let contIteraciones = 1;

    	if(indPosicionActualSlider == 0){
    		timeSliderInteractivoN1 = 1000;
    	}
    	else{
    		timeSliderInteractivoN1 = 1000/indPosicionActualSlider;
    	}

    	while(contIteraciones <= indPosicionActualSlider){

    		$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1').animate({marginLeft:'0%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child').insertBefore($('#seccion_'+seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child'));
	    		$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1').css('margin-left','-100%');
	    	});

	    	$('#seccion_'+seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'0%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child').insertBefore( $('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child'));
	    		$('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');
	    	});

	    	contIteraciones++;
    	}

    	// REINICIALIZAR EL SLIDER ACTIVO EN LISTA DE ITEMS SLIDER
    	func_updateActiveItemSliderFromList(indPosicionActualSlider,0);

    	if($('#checkbox-slider-menu').prop('checked')){

    		$('.slider-menu-icon').click();

    		$('#seccion_'+seccion+' .seccion_titulo').css('display','flex');
            $('#seccion_'+seccion+' .aside-slider-menu').css('width','95%');
            $('#seccion_'+seccion+' .aside-slider-menu').css('left','5%');
            $('#seccion_'+seccion+' .aside-slider-menu').css('bottom','4%');
    	}

	    indPosActSliderInteractivoN1 = 0;

	    $('#seccion_'+seccion+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',((100/nroItemsSliderInteractivoN1)*(indPosActSliderInteractivoN1+1))+'%');
	}

    function func_nextSliderInteractivoN1CX(indPosicionObjetivoSlider, nroIteraciones){

    	let contIteraciones = 1;

    	if(nroIteraciones == 0){
    		timeSliderInteractivoN1 = 1000;
    	}
    	else{
    		timeSliderInteractivoN1 = 1000/nroIteraciones;
    	}

    	while(contIteraciones <= nroIteraciones){

	    	$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').animate({marginLeft:'-200%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child').insertAfter($('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child'));
	    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').css('margin-left','-100%');
	    	});

	    	$('#seccion_'+id_seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'-200%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child').insertAfter( $('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child'));
	    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');
	    	});

	    	contIteraciones++;
    	}

    	indPosActSliderInteractivoN1 = indPosicionObjetivoSlider;

    	$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',((100/nroItemsSliderInteractivoN1)*(indPosActSliderInteractivoN1+1))+'%');
    }

    function func_prevSliderInteractivoN1CX(indPosicionObjetivoSlider, nroIteraciones){

    	let contIteraciones = 1;

    	if(nroIteraciones == 0){
    		timeSliderInteractivoN1 = 1000;
    	}
    	else{
    		timeSliderInteractivoN1 = 1000/nroIteraciones;
    	}

    	while(contIteraciones <= nroIteraciones){

    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').animate({marginLeft:'0%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:last-child').insertBefore($('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:first-child'));
	    		$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1').css('margin-left','-100%');
	    	});


	    	$('#seccion_'+id_seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'0%'},timeSliderInteractivoN1, function(){
	    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child').insertBefore( $('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child'));
	    		$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');
	    	});

	    	contIteraciones++;
    	}

    	indPosActSliderInteractivoN1 = indPosicionObjetivoSlider;

    	$('#seccion_'+id_seccion+' .slider_interactivo_paginacion_nro .slider_paginacion_linea_animada').css('width',((100/nroItemsSliderInteractivoN1)*(indPosActSliderInteractivoN1+1))+'%');
	}

    $('.slider_next_button').click(function(){

		if((indPosActSliderInteractivoN1+1) > (nroItemsSliderInteractivoN1-1)){

			if(nroItemsSliderInteractivoN1 > 2){
				func_updateActiveItemSliderFromList(indPosActSliderInteractivoN1,0);
				func_nextSliderInteractivoN1CX(0,1);
			}
			else{
				func_nextSliderInteractivoN1C2(0);
			}
    	}
    	else{
    		if(nroItemsSliderInteractivoN1 > 2){
		    	func_updateActiveItemSliderFromList(indPosActSliderInteractivoN1,indPosActSliderInteractivoN1+1);
				func_nextSliderInteractivoN1CX(indPosActSliderInteractivoN1+1,1);
			}
			else{
				func_nextSliderInteractivoN1C2(indPosActSliderInteractivoN1+1);
			}
    	}

    	// SI EXISTIERA UN SLIDER AUTOMÁTICO DE NIVEL 2
    	func_restSliderAutomaticoN2();
    	func_executeSliderAutomaticoN2();
    });

    $('.slider_prev_button').click(function(){

    	if((indPosActSliderInteractivoN1-1) < 0){

    		if(nroItemsSliderInteractivoN1 > 2){
    			func_updateActiveItemSliderFromList(0,nroItemsSliderInteractivoN1-1);
				func_prevSliderInteractivoN1CX(nroItemsSliderInteractivoN1-1,1);
			}
			else{
				func_prevSliderInteractivoN1C2(nroItemsSliderInteractivoN1-1);
			}
    	}
    	else{
    		if(nroItemsSliderInteractivoN1 > 2){
    			func_updateActiveItemSliderFromList(indPosActSliderInteractivoN1,indPosActSliderInteractivoN1-1);
				func_prevSliderInteractivoN1CX(indPosActSliderInteractivoN1-1,1);
			}
			else{
				func_prevSliderInteractivoN1C2(indPosActSliderInteractivoN1-1);
			}
    	}

    	// SI EXISTIERA UN SLIDER AUTOMÁTICO DE NIVEL 2
    	func_restSliderAutomaticoN2();
    	func_executeSliderAutomaticoN2();
    });


    // FUNCIONES PARA EJECUCIÓN DE SLIDERS AUTOMATICOS NIVEL 1

    function func_executeSliderAutomaticoN1(){

    	clearInterval(ejecutarSliderAutomaticoN1);

	    if(paginaWeb == 1){
	    	if(id_seccion == 1){
	    		ejecutarSliderAutomaticoN1 = setInterval(function(){
	    			$('#seccion_1 .slider_automatico_paginacion_nro .slider_paginacion_linea_animada').css('animation','paginacionLineaAnimadaAutomatica 4s linear infinite alternate');
	            	func_nextSliderAutomaticoN1(8000);
	        	},8000);
	    	}
	    	else{
	    		ejecutarSliderAutomaticoN1 = setInterval(function(){
		            func_nextSliderAutomaticoN1(5000);
		        },5000);
	    	}
    	}
    	else{
    		ejecutarSliderAutomaticoN1 = setInterval(function(){
	            func_nextSliderAutomaticoN1(5000);
	        },5000);
    	}
    }

    function func_nextSliderAutomaticoN1(intervaloTiempo){

        nroPosicionSliderAutomaticoN1 = (nroPosicionSliderAutomaticoN1 >= nroItemsSliderAutomaticoN1) ? 1 : nroPosicionSliderAutomaticoN1 + 1;

        $('#seccion_'+id_seccion+' .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1').hide();
        $('#seccion_'+id_seccion+' .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+')').fadeIn(200,'linear');

        if(paginaWeb == 1){
	    	if(id_seccion == 1){
		        if((nroPosicionSliderAutomaticoN1 % 2) != 0){
		            $('#seccion_1 .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+') img').finish().css('left','0%');
		            $('#seccion_1 .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+') img').animate({left: "-=4.5%"}, intervaloTiempo, 'linear');
		        }
		        else{
		            $('#seccion_1 .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+') img').finish().css('left','-5%');
		            $('#seccion_1 .ul_slider_automatico_nivel1 .li_articuloSlider_nivel1:nth-child('+nroPosicionSliderAutomaticoN1+') img').animate({left: "+=4.5%"}, intervaloTiempo, 'linear');
		        }
		    }
	    }

	    $('#seccion_'+id_seccion+' .slider_paginacion_orden .ul_slider_paginacion_orden').animate({marginTop:'-200%'},200, function(){
    		$('#seccion_'+id_seccion+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:first-child').insertAfter( $('#seccion_'+id_seccion+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden .li_slider_paginacion_orden:last-child'));
    		$('#seccion_'+id_seccion+' .slider_automatico_paginacion_nro .ul_slider_paginacion_orden').css('margin-top','-100%');
    	});
    }

    function func_restSliderAutomaticoN1(seccion){

    	$('#seccion_'+seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1').hide();
        $('#seccion_'+seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:nth-child(1)').fadeIn(200,'linear');
    }

   	// FUNCIONES PARA EJECUCIÓN DE SLIDERS AUTOMATICOS NIVEL 2

    function func_executeSliderAutomaticoN2(){

    	clearInterval(ejecutarSliderAutomaticoN2);

    	ejecutarSliderAutomaticoN2 = setInterval(function(){
            func_nextSliderAutomaticoN2(5000);
        },5000);
    }

    function func_nextSliderAutomaticoN2(intervaloTiempo){

    	nroItemsSliderAutomaticoN2 = $('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1:nth-child(1) .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2').length;

    	nroPosicionSliderAutomaticoN2 = (nroPosicionSliderAutomaticoN2 >= nroItemsSliderAutomaticoN2) ? 1 : nroPosicionSliderAutomaticoN2 + 1;

        $('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1 .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2').hide();
        $('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1 .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2:nth-child('+nroPosicionSliderAutomaticoN2+')').fadeIn(200,'linear');
    }

    function func_restSliderAutomaticoN2(){

    	nroPosicionSliderAutomaticoN2 = 1;
    	$('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1 .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2').hide();
        $('#seccion_'+id_seccion+' .ul_slider_interactivo_nivel1 .li_articuloSlider_nivel1 .ul_slider_automatico_nivel2 .li_articuloSlider_nivel2:nth-child(1)').fadeIn(200,'linear');
    }

    // FUNCIONES PARA EJECUCION DE LISTA ITEMS SLIDER INTERACTIVO

    function func_updateActiveItemSliderFromList(indLastActiveItem, indNewActiveItem){

    	let lastActiveSlider = document.getElementsByClassName('li_nombre_item_'+(indLastActiveItem + 1));

    	if(lastActiveSlider.length > 0){
    		for (let j = 0; j < lastActiveSlider.length; j++) {
    			lastActiveSlider[j].classList.remove('active');
    		}
    	}

    	let newActiveSlider = document.getElementsByClassName('li_nombre_item_'+(indNewActiveItem + 1));

    	if(newActiveSlider.length > 0){
    		for(let i = 0; i < newActiveSlider.length; i++){
	        	newActiveSlider[i].classList.add('active');
	        }
    	}
    }

    // FUNCIONES PARA MODIFICAR ESTILOS DE ELEMENTOS HTML - CKEDITOR
    function func_addSocialNetworkIcons(){

    	let iconoFacebook = document.getElementById('link-icon-facebook');
    	if(iconoFacebook != null){
	    	iconoFacebook.innerHTML = '<a href="'+$('#link-icon-facebook a').attr('href')+'" target="_blank">'
		    							+'<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"'
					 						+'viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">'
											+'<path id="facebook" d="M42.4,33.6c0,1.4,0,7.9,0,7.9h-5.8v9.6h5.8v26.4h11.9V51.1h8c0,0,0.7-4.6,1.1-9.7c-1,0-9,0-9,0'
											+'s0-5.6,0-6.6s1.3-2.3,2.6-2.3s4,0,6.5,0c0-1.3,0-5.9,0-10c-3.3,0-7.1,0-8.8,0C42.1,22.5,42.4,32.1,42.4,33.6z"/>'
										+'</svg>'
									+'</a>';
		}

		let iconoTwitter = document.getElementById('link-icon-twitter');
		if(iconoTwitter != null){
	    	iconoTwitter.innerHTML = '<a href="'+$('#link-icon-twitter a').attr('href')+'" target="_blank">'
		    							+'<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"'
											+'viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">'
											+'<path id="twitter" d="M77.6,32.7c-2,1-4.2,1.5-6.7,1.8c2.4-1.4,4.2-3.7,5.1-6.4c-2.2,1.4-4.7,2.3-7.3,2.8'
											+'c-2.1-2.2-5.1-3.7-8.4-3.7c-6.4,0-11.6,5.2-11.6,11.6c0,0.9,0.1,1.7,0.3,2.6C39.5,41,31,36.4,25.3,29.4c-1,1.7-1.5,3.7-1.5,5.8'
											+'c0,4,2,7.5,5.1,9.6c-1.9-0.1-3.7-0.6-5.2-1.4c0,0.1,0,0.1,0,0.2c0,5.6,4,10.2,9.3,11.3c-1,0.3-2,0.4-3,0.4c-0.8,0-1.4-0.1-2.1-0.2'
											+'c1.4,4.5,5.7,7.9,10.8,8c-4,3.1-8.9,4.9-14.3,4.9c-1,0-1.8-0.1-2.7-0.2c5.1,3.3,11.2,5.2,17.7,5.2c21.2,0,32.8-17.6,32.8-32.8'
											+'c0-0.5,0-1,0-1.4C74.1,37.1,76.1,35,77.6,32.7L77.6,32.7z"/>'
										+'</svg>'
									+'</a>';
		}

		let iconoYoutube = document.getElementById('link-icon-youtube');
		if(iconoYoutube != null){
			iconoYoutube.innerHTML = '<a href="'+$('#link-icon-youtube a').attr('href')+'" target="_blank">'
		    							+'<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"'
											+'viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">'
											+'<path id="youtube" d="M68,27.8H32c-5.5,0-10,4.5-10,10v19c0,5.5,4.5,10,10,10h36c5.5,0,10-4.5,10-10v-19'
											+'C78,32.3,73.5,27.8,68,27.8z M43.9,56.8v-19l15,9.5L43.9,56.8z"/>'
										+'</svg>'
									+'</a>';
		}
    }

    // MODIFICACIONES AL CAMBIO DE TAMAÑO DE PANTALLA
    $(window).resize(function(){

        // AJUSTAR CINTILLO DE CONTROLES DE VIDEO
        let miVideo = $('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .contenedor_video video').attr('id');
    	if(miVideo != null){
    		if(videoFullScreen){
    			if($(window).outerWidth() > 768){
					$('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('width','90%');
				}
				else{
					$('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('width','100%');
				}
	    		let positionVideoControls = (($('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .contenedor_video').outerHeight() - $(window).outerHeight()) * 50) / $('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .contenedor_video').outerHeight();
	    		$('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('bottom',positionVideoControls+'%');
	    	}
    	}

    	// AUSTAR CINTILLO DE CONTROLES DE VIDEO FONDO DE SECCION
    	if($(window).outerWidth() > 768){
	    	$('#seccion_'+id_seccion+' .seccion_fondo_video .video_controles').css('width','90%');
	    }
	    else{
	    	$('#seccion_'+id_seccion+' .seccion_fondo_video .video_controles').css('width','100%');
	    }
    });

	function func_aplicarAjustesEnElementos(){
		/* set language button */
		if(activeLanguage == "es"){
			if (document.querySelectorAll(".lang-es")){
				const es_elements = document.querySelectorAll(".lang-es");
				es_elements.forEach(function(es_element){
					es_element.style.display = "inline-flex";
				});
			}

			if (document.querySelectorAll(".lang-en")){
				const en_elements = document.querySelectorAll(".lang-en");
				en_elements.forEach(function(en_element){
					en_element.style.display = "none";
				});
			}
		}
		else{
			if (document.querySelectorAll(".lang-en")){
				const en_elements = document.querySelectorAll(".lang-en");
				en_elements.forEach(function(en_element){
					en_element.style.display = "inline-flex";
				});
			}

			if (document.querySelectorAll(".lang-es")){
				const es_elements = document.querySelectorAll(".lang-es");
				es_elements.forEach(function(es_element){
					es_element.style.display = "none";
				});
			}
		}

		/* Add cero on left side of numbers */
		let sectionNumbers = document.querySelectorAll(".seccion_titulo_numeracion span");
		sectionNumbers.forEach(function(sectionNumber){
			let number = sectionNumber.innerHTML;
			sectionNumber.innerHTML = padLeft(number, 2);
		});

		let sectionNavNumbers = document.querySelectorAll(".nav_secciones_numero");
		sectionNavNumbers.forEach(function(sectionNavNumber){
			let number = sectionNavNumber.innerHTML;
			sectionNavNumber.innerHTML = padLeft(number, 2);
		});

		// cargar paises a selector de formulario
		if(document.querySelector("#id_country")){
			fetch('/retrieve/countries')
			.then(response => response.json())
			.then(result => {
				let optList = `<option value="">Select</option>`;
                result.forEach(function(element){
                    optList += `<option value="` + element["id"] + `">` + element["name_es"] + `</option>`;
                });
                document.querySelector('#id_country').innerHTML = optList;
			})
			.catch(error => {
				console.error(error);
			});
		}

		// inicializar eventos para mostrar el menu de slider
		let sectionSliderMenus = document.querySelectorAll(".slider-menu-icon");
		if(sectionSliderMenus){
			sectionSliderMenus.forEach(function(sectionSliderMenu){
				sectionSliderMenu.addEventListener("click", function(){
					let slidermenuid = this.getAttribute("data-slidermenuid");
					if(!document.querySelector("#checkbox-slider-menu-"+slidermenuid).checked){
						this.parentElement.style.width = "100%";
						this.parentElement.style.transition = "width 0s 0s";
						document.querySelector("#slider-menu-background-"+slidermenuid).classList.add("open-slider-menu-background");
						document.querySelector("#slider-menu-icon-"+slidermenuid).classList.add("open-slider-menu-icon");
						document.querySelector("#slider-menu-list-"+slidermenuid).classList.add("open-slider-menu-list");
					}
					else{
						document.querySelector("#slider-menu-background-"+slidermenuid).classList.remove("open-slider-menu-background");
						document.querySelector("#slider-menu-icon-"+slidermenuid).classList.remove("open-slider-menu-icon");
						document.querySelector("#slider-menu-list-"+slidermenuid).classList.remove("open-slider-menu-list");
						this.parentElement.style.width = "5%";
						this.parentElement.style.transition = "width 0s 2s";
					}
				});
			});
		}

		// eventos click de slider menu
		let sliderMenuClickEvents = document.querySelectorAll(".aside-slider-menu .article-link");
		if(sliderMenuClickEvents){
			sliderMenuClickEvents.forEach(function(sliderMenuClickEvent){
				sliderMenuClickEvent.addEventListener("click", function(event){
					event.preventDefault();

					let indPosObjSliderInteractivoN1 = this.getAttribute("data-slideindex") - 1;

					func_updateActiveItemSliderFromList(indPosActSliderInteractivoN1,indPosObjSliderInteractivoN1);

					if(indPosObjSliderInteractivoN1 > indPosActSliderInteractivoN1){

						if((indPosObjSliderInteractivoN1 - indPosActSliderInteractivoN1) <= (nroItemsSliderInteractivoN1 - indPosObjSliderInteractivoN1 + indPosActSliderInteractivoN1)){
							func_nextSliderInteractivoN1CX(indPosObjSliderInteractivoN1,indPosObjSliderInteractivoN1 - indPosActSliderInteractivoN1);
						}
						else{
							func_prevSliderInteractivoN1CX(indPosObjSliderInteractivoN1, nroItemsSliderInteractivoN1 - indPosObjSliderInteractivoN1 + indPosActSliderInteractivoN1);
						}
					}
					else{
						if(indPosObjSliderInteractivoN1 < indPosActSliderInteractivoN1){

							if((indPosActSliderInteractivoN1 - indPosObjSliderInteractivoN1) < (nroItemsSliderInteractivoN1 - indPosActSliderInteractivoN1 + indPosObjSliderInteractivoN1)){
								func_prevSliderInteractivoN1CX(indPosObjSliderInteractivoN1, indPosActSliderInteractivoN1 - indPosObjSliderInteractivoN1);
							}
							else{
								func_nextSliderInteractivoN1CX(indPosObjSliderInteractivoN1, nroItemsSliderInteractivoN1 - indPosActSliderInteractivoN1 + indPosObjSliderInteractivoN1);
							}
						}
					}

					document.querySelector("#slider-menu-icon-"+this.getAttribute("data-sectionorder")).click();

					// SI EXISTIERA UN SLIDER AUTOMÁTICO DE NIVEL 2
					func_restSliderAutomaticoN2();
					func_executeSliderAutomaticoN2();
				});
			});
		}

		// inicializar eventos para reproducción de videos
		let videoControlsButtons = document.querySelectorAll(".btn_mostrar_video_controles");
		if(videoControlsButtons){
			videoControlsButtons.forEach(function(videoControlsButton){
				videoControlsButton.addEventListener("click",function(){
					clearTimeout(mouseclickMostrarControles);
					let videomenuid = videoControlsButton.getAttribute("data-sectionorder");
					videoControlsButton.style.display = "none";
					document.querySelector("#video_controles_"+videomenuid).style.display = "flex";

					mouseclickMostrarControles = setTimeout(function() {
						document.querySelector("#video_controles_"+videomenuid).style.display = "none";
						videoControlsButton.style.display = "flex";
					},10000);
				});
			});
		}

		// let videoControls = document.querySelectorAll(".video_controles");
		// if(videoControls){
		// 	videoControls.forEach(function(videoControl){
		// 		let seccionOrden = videoControl.getAttribute("data-sectionorder");
		// 		videoControl.addEventListener("mouseover",function(){
		// 			document.querySelector("#video_controles_"+seccionOrden).style.display = "flex";
		// 		});
		// 		videoControl.addEventListener("mouseout",function(){
		// 			document.querySelector("#video_controles_"+seccionOrden).style.display = "none";
		// 		});
		// 	});
		// }

		let playVideoControls = document.querySelectorAll(".video_control_play");
		if(playVideoControls){
			playVideoControls.forEach(function(playVideoControl){
				playVideoControl.addEventListener("click",function(){
					func_playVideo(playVideoControl.parentElement.getAttribute("data-sectionorder"));
				});
			});
		}

		let pauseVideoControls = document.querySelectorAll(".video_control_pause");
		if(pauseVideoControls){
			pauseVideoControls.forEach(function(pauseVideoControl){
				pauseVideoControl.addEventListener("click",function(){
					func_pauseVideo(pauseVideoControl.parentElement.getAttribute("data-sectionorder"));
				});
			});
		}

		let mutedVideoControls = document.querySelectorAll(".video_control_muted");
		if(mutedVideoControls){
			mutedVideoControls.forEach(function(mutedVideoControl){
				mutedVideoControl.addEventListener("click",function(){
					func_mutedVideo(mutedVideoControl.parentElement.getAttribute("data-sectionorder"));
				});
			});
		}

		let soundVideoControls = document.querySelectorAll(".video_control_sound");
		if(soundVideoControls){
			soundVideoControls.forEach(function(soundVideoControl){
				soundVideoControl.addEventListener("click",function(){
					func_soundVideo(soundVideoControl.parentElement.getAttribute("data-sectionorder"));
				});
			});
		}

		let fullScreenOnVideoControls = document.querySelectorAll(".video_control_fullScreenOn");
		if(fullScreenOnVideoControls){
			fullScreenOnVideoControls.forEach(function(fullScreenOnVideoControl){
				fullScreenOnVideoControl.addEventListener("click",function(){
					func_fullScreenOnVideo(fullScreenOnVideoControl.parentElement.getAttribute("data-sectionorder"));
				});
			});
		}

		let fullScreenOffVideoControls = document.querySelectorAll(".video_control_fullScreenOff");
		if(fullScreenOffVideoControls){
			fullScreenOffVideoControls.forEach(function(fullScreenOffVideoControl){
				fullScreenOffVideoControl.addEventListener("click",function(){
					func_fullScreenOffVideo(fullScreenOffVideoControl.parentElement.getAttribute("data-sectionorder"));
				});
			});
		}

		let progressBoxVideoControls = document.querySelectorAll(".video_control_progress .progress_box");
		if(progressBoxVideoControls){
			progressBoxVideoControls.forEach(function(progressBoxVideoControl){
				progressBoxVideoControl.addEventListener("click",function(e){
					let videoControlProgress = progressBoxVideoControl.parentElement;
					let sectionid = videoControlProgress.parentElement.getAttribute("data-sectionorder");
					func_stopProgressTrackVideo();
					func_pauseVideo(sectionid);
					func_setPlayProgress(e.pageX,sectionid);
					func_playVideo(sectionid);
				});
			});
		}

		// eventos click para salto a sección específica
		let navegadorSecciones = document.querySelectorAll(".nav_secciones_fuente");
		if(navegadorSecciones){
			navegadorSecciones.forEach(function(navegadorSeccion){
				navegadorSeccion.addEventListener("click",function(){
					nroSeccionDestino = this.getAttribute('id');
					if(nroSeccionDestino > 0){
						if(nroSeccionDestino > id_seccion){
							funcClickFiresScroll(nroSeccionDestino,1);
						}
						else{
							if(nroSeccionDestino < id_seccion){
								funcClickFiresScroll(nroSeccionDestino,-1);
							}
						}
					}
				});
			});
		}
	}

	function padLeft(value, length) {
		return (value.toString().length < length) ? padLeft("0" + value, length) :
		value;
	}

	function func_inicializarVideoAutomaticamente(){

    	let miVideo = $('#seccion_'+id_seccion+' .contenedor_video video').attr('id');

    	if(miVideo != null){

    		document.getElementById(miVideo).removeAttribute('controls');

    		if(document.getElementById(miVideo).muted){
    			$('#seccion_'+id_seccion+' .contenedor_seccion .video_controles .video_control_sound').css('display','flex');
    			$('#seccion_'+id_seccion+' .contenedor_seccion .video_controles .video_control_muted').css('display','none');
    		}
    		else{
    			$('#seccion_'+id_seccion+' .contenedor_seccion .video_controles .video_control_sound').css('display','none');
    			$('#seccion_'+id_seccion+' .contenedor_seccion .video_controles .video_control_muted').css('display','flex');
    		}

    		$('#seccion_'+id_seccion+' .contenedor_seccion .video_controles .video_control_play').css('display','none');
	    	$('#seccion_'+id_seccion+' .contenedor_seccion .video_controles .video_control_pause').css('display','flex');

	    	$('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .video_controles .video_control_fullScreenOff').css('display','none');
	    	$('#seccion_'+id_seccion+' .sec_eld_articulo_multimedia .video_controles .video_control_fullScreenOn').css('display','flex');

	    	if($(window).outerWidth() > 768){
		    	$('#seccion_'+id_seccion+' .seccion_fondo_video .video_controles').css('width','90%');
		    }
		    else{
		    	$('#seccion_'+id_seccion+' .seccion_fondo_video .video_controles').css('width','100%');
		    }

	    	func_playVideo(id_seccion);

			// ocultar y mostrar controles de video
	    	clearTimeout(mouseclickMostrarControles);

	    	mouseclickMostrarControles = setTimeout(function() {
		        $('#seccion_'+id_seccion+' .seccion_fondo_video .video_controles').css('display','none');
		        $('#seccion_'+id_seccion+' .seccion_fondo_video .btn_mostrar_video_controles').css('display','flex');
		    },10000);
    	}
    }

    function func_pausarVideoAutomaticamente(seccion) {
    	func_pauseVideo(seccion);
    }

    function func_playVideo(seccion){
    	let miVideo = $('#seccion_'+seccion+' .contenedor_video video').attr('id');
    	if(miVideo != null){
    		document.getElementById(miVideo).play();
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_play').css('display','none');
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_pause').css('display','flex');

    		func_playProgressTrackVideo(seccion,miVideo);
    	}
    }

    function func_pauseVideo(seccion){
    	let miVideo = $('#seccion_'+seccion+' .contenedor_video video').attr('id');
    	if(miVideo != null){
    		document.getElementById(miVideo).pause();
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_pause').css('display','none');
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_play').css('display','flex');

    		func_stopProgressTrackVideo();
    	}
    }

    function func_mutedVideo(seccion){
    	let miVideo = $('#seccion_'+seccion+' .contenedor_video video').attr('id');
    	if(miVideo != null){
    		document.getElementById(miVideo).muted = true;
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_muted').css('display','none');
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_sound').css('display','flex');
    	}
    }

    function func_soundVideo(seccion){
    	let miVideo = $('#seccion_'+seccion+' .contenedor_video video').attr('id');
    	if(miVideo != null){
    		document.getElementById(miVideo).muted = false;
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_sound').css('display','none');
    		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_muted').css('display','flex');
    	}
    }

    function func_fullScreenOnVideo(seccion){
    	let miVideo = $('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video video').attr('id');
    	if(miVideo != null){
    		//poner a pantalla completa
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('height','100%');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('width','100%');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('position','fixed');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('top','50%');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('left','50%');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('transform','translateX(-50%) translateY(-50%)');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('overflow','hidden');

    		// reubicar nivel del título de sección
    		$('#seccion_'+seccion+' .contenedor_seccion .seccion_titulo').css('z-index','30');

    		// reubicar cintillo de controles
    		let positionVideoControls = (($('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').outerHeight() - $(window).outerHeight()) * 50) / $('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').outerHeight();
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('bottom',positionVideoControls+'%');

    		// actualizar botones fullscreen
    		if($(window).outerWidth() > 768){
				$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('width','90%');
			}
			else{
				$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('width','100%');
			}

    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .video_controles .video_control_fullScreenOn').css('display','none');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .video_controles .video_control_fullScreenOff').css('display','flex');

    		videoFullScreen = true;
    	}
    }

    function func_fullScreenOffVideo(seccion){
    	let miVideo = $('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video video').attr('id');
    	if(miVideo != null){
    		//poner a pantalla completa
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('position','relative');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('top','0%');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('left','0%');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video').css('transform','translateX(-0%) translateY(-0%)');

    		// reubicar nivel del título de sección
    		$('#seccion_'+seccion+' .contenedor_seccion .seccion_titulo').css('z-index','70');

    		// reubicar cintillo de controles
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('bottom','0%');

    		// actualizar botones fullscreen
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .contenedor_video .video_controles').css('width','100%');

    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .video_controles .video_control_fullScreenOn').css('display','flex');
    		$('#seccion_'+seccion+' .sec_eld_articulo_multimedia .video_controles .video_control_fullScreenOff').css('display','none');

    		videoFullScreen = false;
    	}
    }

    function func_playProgressTrackVideo(seccion,idVideo) {
    	func_updatePlayProgressVideo(seccion,idVideo);
		playProgressInterval = setTimeout(function(){func_playProgressTrackVideo(seccion,idVideo);}, 50);
	}

	function func_updatePlayProgressVideo(seccion,idVideo){
		let widthProgressBox = $('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_progress .progress_box').width();
		let widthProgressBar = (document.getElementById(idVideo).currentTime * widthProgressBox) / document.getElementById(idVideo).duration;
		$('#seccion_'+seccion+' .contenedor_seccion .video_controles .video_control_progress .progress_box .play_progress_bar').css('width',widthProgressBar+'px');
	}

	function func_stopProgressTrackVideo(){
		clearTimeout(playProgressInterval);
	}

	function func_setPlayProgress(posClickX, seccion){
		let videoProgressBox = document.querySelector("#video_controles_"+seccion+" .video_control_progress .progress_box");
		let widthProgressBox = videoProgressBox.offsetWidth;
		let widthProgressBar = posClickX - videoProgressBox.getBoundingClientRect().left;
		let videoActual = document.querySelector("#video_"+seccion);

		videoActual.currentTime = (videoActual.duration * widthProgressBar) / widthProgressBox;
		document.querySelector("#video_controles_"+seccion+" .video_control_progress .progress_box .play_progress_bar").style.width = widthProgressBar + "px";
    }

	function funcClickFiresScroll(nroSeccionDestino,direccion){

		actualPosicionScrollTop = window.pageYOffset + direccion;
		let nroSeccionOrigen = id_seccion;

		if(actualPosicionScrollTop > ultimaPosicionScrollTop){
			id_seccion = nroSeccionDestino > nroSeccionesPW ? nroSeccionesPW : nroSeccionDestino;

			newActiveSection = document.getElementById('seccion_'+nroSeccionDestino);
			newActiveSectionTop = newActiveSection.getBoundingClientRect().top + actualPosicionScrollTop;
			$('html,body').animate({scrollTop: newActiveSectionTop},1000,function(){
				activeStateScrollAnimation = false;
			});
			func_restablecerElementosDeSeccionAnterior(nroSeccionOrigen);
			func_actualizarNavegadorSecciones(nroSeccionOrigen,id_seccion);
		}
		else{
			if(actualPosicionScrollTop < ultimaPosicionScrollTop){
				id_seccion = nroSeccionDestino < 1 ? 1 : nroSeccionDestino;

				newActiveSection = document.getElementById('seccion_'+nroSeccionDestino);
				newActiveSectionTop = newActiveSection.getBoundingClientRect().top + actualPosicionScrollTop;
				$('html,body').animate({scrollTop: newActiveSectionTop},1000,function(){
					activeStateScrollAnimation = false;
				});
				func_restablecerElementosDeSeccionAnterior(nroSeccionOrigen);
				func_actualizarNavegadorSecciones(nroSeccionOrigen,id_seccion);
			}
		}

		func_inicializarElementosDeSeccionActual(id_seccion);
		scrollActivado = true;
		activeStateScrollAnimation = true;

		ultimaPosicionScrollTop = actualPosicionScrollTop;
	}

	window.addEventListener("orientationchange", function() {
		window.location.reload();
	});
});

function insertFile(object){
	// Diplay DOM elements depending on the language
	insertFileLanguage(object);
	// Resize SVG graphic depending on the window size
	let iframeDocument = object.contentDocument;
	if(window.outerWidth < 768){
		iframeDocument.body.style.width = object.parentElement.offsetWidth + "px"; 
		iframeDocument.body.style.height = iframeDocument.body.offsetHeight + "px";
		object.style.width = object.parentElement.offsetWidth + "px";
		object.style.height = iframeDocument.body.offsetHeight + "px";
	}
	else if(window.outerWidth < 966){
		iframeDocument.body.style.width = "396px";
		iframeDocument.body.style.height = iframeDocument.body.offsetHeight + "px";
		object.style.width = "400px";
		object.style.height = iframeDocument.body.offsetHeight + "px";
	}
	else{
		iframeDocument.body.style.height = object.parentElement.offsetHeight + "px";
		iframeDocument.body.style.width = "auto";
		object.style.height = object.parentElement.offsetHeight + "px";
		object.style.width = iframeDocument.body.offsetWidth + "px";
	}
}

function insertFileLanguage(object){
	let activeLanguage = document.querySelector("html").getAttribute("lang");
	let framehtml = object.contentDocument.body.parentElement;
	if(activeLanguage == "es"){
		framehtml.setAttribute("lang","es");

		if (object.contentDocument.querySelectorAll(".lang-es")){
			const es_elements = object.contentDocument.querySelectorAll(".lang-es");
			es_elements.forEach(function(es_element){
				es_element.style.display = "inline-flex";
			});
		}

		if (object.contentDocument.querySelectorAll(".lang-en")){
			const en_elements = object.contentDocument.querySelectorAll(".lang-en");
			en_elements.forEach(function(en_element){
				en_element.style.display = "none";
			});
		}
	}
	else{
		framehtml.setAttribute("lang","en");

		if (object.contentDocument.querySelectorAll(".lang-en")){
			const en_elements = object.contentDocument.querySelectorAll(".lang-en");
			en_elements.forEach(function(en_element){
				en_element.style.display = "inline-flex";
			});
		}

		if (object.contentDocument.querySelectorAll(".lang-es")){
			const es_elements = object.contentDocument.querySelectorAll(".lang-es");
			es_elements.forEach(function(es_element){
				es_element.style.display = "none";
			});
		}
	}
}
