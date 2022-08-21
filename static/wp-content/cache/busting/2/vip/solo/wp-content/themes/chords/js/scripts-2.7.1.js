jQuery(window).on("load", function() {
	"use strict";

	/* -----------------------------------------
	 FlexSlider Init
	 ----------------------------------------- */
	var homeSlider = jQuery( '#home-slider' );
	if ( homeSlider.length ) {
		homeSlider.flexslider( {
			animation     : ThemeOption.slider_effect,
			direction     : ThemeOption.slider_direction,
			slideshow     : Boolean( ThemeOption.slider_autoslide ),
			slideshowSpeed: Number( ThemeOption.slider_speed ),
			animationSpeed: Number( ThemeOption.slider_duration ),
			prevText      : '',
			nextText      : '',
			directionNav  : false,
			controlNav    : true,
			start         : function( slider ) {
				slider.removeClass( 'loading' );
			},
			after: function( slider ) {
				var currentSlide = slider.slides.eq( slider.currentSlide );
				currentSlide.siblings().each( function() {
					var src = jQuery( this ).find( 'iframe' ).attr( 'src' );
					jQuery( this ).find( 'iframe' ).attr( 'src', src );
				} );
			}
		} );
	}

	/* -----------------------------------------
	Isotope / Masonry
	----------------------------------------- */
	var $container = jQuery('.list-masonry'),
			$filters = jQuery('.filters-nav');

	$container.each(function() {
		jQuery(this).isotope();
	});

	if ( $filters.length ) {
		$filters.each( function() {
			var $filterSet = jQuery( this ),
				$filterLinks = $filterSet.find( 'a' );

			$filterLinks.click( function(e) {
				var $that = jQuery(this),
					$selector = $that.attr('data-filter');

				if ( $that.parents('.event-list').length ) {

					$filterSet.find('.selected').removeClass('selected');
					$that.addClass('selected');

					$filterSet
						.parents('.event-list')
						.find('.list-masonry')
						.isotope({
							filter : $selector,
							animationOptions: {
								duration: 750,
								easing  : 'linear',
								queue   : false
							}
						});

				} else {
					var selector = jQuery(this).attr('data-filter');
					jQuery(this).parent().siblings().find('a').removeClass('selected');
					jQuery(this).addClass("selected");

					$container.isotope({
						filter: selector,
						animationOptions: {
							duration: 750,
							easing  : 'linear',
							queue   : false
						}
					});
				}

				e.preventDefault();
			});

		});
	}

	/* -----------------------------------------
	 Equalize Heights
	 ----------------------------------------- */
	jQuery(".item-list").find("div[class^='col']").matchHeight();

	/* -----------------------------------------
	 Homepage audio player autoplay
	 ----------------------------------------- */
	jQuery(".autoplay").find('.ci-soundplayer-play').trigger('click');
});

jQuery(document).ready(function($) {
	"use strict";

	/* -----------------------------------------
	 Responsive Menus Init with mmenu
	 ----------------------------------------- */
	var mainNav = $("#navigation"),
		mobileNav = $("#mobilemenu");

	mainNav.clone().removeAttr('id').removeClass().appendTo(mobileNav);
	mobileNav.find('li').removeAttr('id');

	mobileNav.mmenu({
		offCanvas: {
			position : 'top',
			zposition: 'front'
		},
		autoHeight: true,
		navbars: [
			{
				position: 'top',
				content: [
					'prev',
					'title',
					'close'
				]
			}
		],
		extensions: ['theme-dark']
	});

	/* -----------------------------------------
	 Main Navigation Init
	 ----------------------------------------- */
	$('#navigation').superfish({
		delay      : 300,
		animation  : { opacity: 'show', height: 'show' },
		speed      : 'fast',
		dropShadows: false
	});

	/* -----------------------------------------
	 Responsive Videos with fitVids
	 ----------------------------------------- */
	$('#main').fitVids();

	/* -----------------------------------------
	 Lightbox
	 ----------------------------------------- */
	var pp_images = $("a[data-rel^='prettyPhoto']");
	if (pp_images.length) {
		pp_images.prettyPhoto({
			show_title        : false,
			hook              : 'data-rel',
			social_tools      : false,
			theme             : 'pp_woocommerce',
			horizontal_padding: 20,
			opacity           : 0.8,
			deeplinking       : false
		});
	}

	/* -----------------------------------------
	 Event Map Init
	 ----------------------------------------- */
	var event_map = $("#event_map");
	if ( event_map.length ) {
		var lat = event_map.data( 'lat' ), lng = event_map.data( 'lng' ), tipText = event_map.data( 'tooltip-txt' ), titleText = event_map.attr( 'title' );

		map_init( lat, lng, tipText, titleText );
	}

	/* -----------------------------------------
	 SoundManager2 Init
	 ----------------------------------------- */
	soundManager.setup({
		url: ThemeOption.swfPath
	});

	/* -----------------------------------------
	 SoundCloud Trigger
	 ----------------------------------------- */
	if ($('.soundcloud-wrap').length) {
		$('.sc-play').click(function(e){
			var target = $(this).parent().find('.soundcloud-wrap');
			target.slideToggle('fast');
			e.preventDefault();
		});
	}

	var $buttons = $(".track-buttons");

	function addTallClasstoTrack() {
		if ( $(window).width() < 1032 && $buttons.length ) {
			$('.track').each(function() {
				if ( $(this).find(".track-buttons").length ) {
					$(this).addClass('tall');
				}
			});
		} else {
			$(".track").removeClass('tall');
		}
	}

	addTallClasstoTrack();

	$(window).on('resize', function(e) {
		addTallClasstoTrack();
	});

	/* -----------------------------------------
	 Galleries (stapel.js)
	 ----------------------------------------- */
	var tpclose = $('.tp-close');

	var stapel = $( '#tp-grid' ).stapel( {
		gutter    : 30,
		pileAngles: 2,
		onAfterOpen: function(pileName) {
			tpclose.fadeIn();
			var pp_images = $("a[data-rel^='prettyPhoto']");
			pp_images.prettyPhoto({
				show_title        : false,
				hook              : 'data-rel',
				social_tools      : false,
				theme             : 'pp_woocommerce',
				horizontal_padding: 20,
				opacity           : 0.8,
				deeplinking       : false
			});
		},
		onAfterClose: function(pileName) {
			var pp_images = $("a[data-rel^='prettyPhoto']");
			pp_images.off('click');
		}
	} );

	tpclose.on('click', function(e) {
		$(this).hide();
		stapel.closePile();

		e.preventDefault();
	});

});

function map_init(lat, lng, tipText, titleText) {
	'use strict';
	if ( typeof google === 'object' && typeof google.maps === 'object' ) {
		var myLatlng = new google.maps.LatLng( lat, lng );
		var mapOptions = {
			zoom     : 8,
			center   : myLatlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			styles   : [
				{"stylers": [{"saturation": -100}, {"gamma": 1}]},
				{
					"elementType": "labels.text.stroke",
					"stylers"    : [{"visibility": "off"}]
				},
				{
					"featureType": "poi.business",
					"elementType": "labels.text",
					"stylers"    : [{"visibility": "off"}]
				},
				{
					"featureType": "poi.business",
					"elementType": "labels.icon",
					"stylers"    : [{"visibility": "off"}]
				},
				{
					"featureType": "poi.place_of_worship",
					"elementType": "labels.text",
					"stylers"    : [{"visibility": "off"}]
				},
				{
					"featureType": "poi.place_of_worship",
					"elementType": "labels.icon",
					"stylers"    : [{"visibility": "off"}]
				},
				{
					"featureType": "road",
					"elementType": "geometry",
					"stylers"    : [{"visibility": "simplified"}]
				},
				{
					"featureType": "water",
					"stylers"    : [{"visibility": "on"}, {"saturation": 50}, {"gamma": 0}, {"hue": "#50a5d1"}]
				},
				{
					"featureType": "administrative.neighborhood",
					"elementType": "labels.text.fill",
					"stylers"    : [{"color": "#333333"}]
				},
				{
					"featureType": "road.local",
					"elementType": "labels.text",
					"stylers"    : [{"weight": 0.5}, {"color": "#333333"}]
				},
				{
					"featureType": "transit.station",
					"elementType": "labels.icon",
					"stylers"    : [{"gamma": 1}, {"saturation": 50}]
				}
			]
		};

		var map = new google.maps.Map( document.getElementById( 'event_map' ), mapOptions );

		var contentString = '<div class="tip-content">' + tipText + '</div>';

		var infowindow = new google.maps.InfoWindow( {
			content: contentString
		} );

		var marker = new google.maps.Marker( {
			position: myLatlng, map: map, title: titleText
		} );

		google.maps.event.addListener( marker, 'click', function() {
			infowindow.open( map, marker );
		} );
	}
}
