jQuery(function($) {

	// Grab all fitvid instances. Bail on Elementor.
	var $ciVideos = $('.fluid-width-video-wrapper').not($('.elementor-page .fluid-width-video-wrapper'));
	
	if ($ciVideos.length) {
		$ciVideos.each(function () {
			
			var that = $(this);

			// Grab the iframe src
			var videoURL = that.find('iframe').attr('src');		
			
			// Youtube or Vimeo
			// Also bring back the video type, the ID and the thumb
			getVideoDetails(videoURL, function (data) {	

				var videoType = data[0];
				var videoID = data[1];
				var videoThumb = data[2];

				// Remove the iframe
				that.find('iframe').remove();				


				// If img width is < 640 something's wrong. In this case just don't set the bg image.
				getImgSize(videoThumb, function (imgData) {				
					if (imgData.width == 640) {
						that.css('background-image', 'url(' + videoThumb + ')');
					}					
				});

				// Add an extra class. We'll need it for styling
				that.addClass('fluid-width-video-preview');
				
				// An extra class won't hurt (Red or Blue button)
				if (videoType == 'youtube') {
					that.addClass('fluid-width-video-preview-youtube');
				}
				else if (videoType == 'vimeo') {
					that.addClass('fluid-width-video-preview-vimeo');
				}
				
				// Well, add the button
				var playButton = "<div class='play-button'></div>";
				that.append(playButton);

				// Click click
				// Pass the video type and id. Video type = vimeo or youtube? id = construct the full iframe tag.
				that.on('click', 
					{ 						
						videoType: videoType,
						videoID: videoID,
						
					}, function(e) {
						$(this).find('.play-button').fadeOut('fast');
						if (e.data.videoType == 'youtube') {							
							var iFrame = "<iframe src='https://www.youtube.com/embed/" + videoID + "?rel=0&showinfo=0&autoplay=1' frameborder='0' allowfullscreen='true'></iframe>";
							$(this).append(iFrame);
						}
						else if (e.data.videoType == 'vimeo') {														
							var iFrame = "<iframe src='https://player.vimeo.com/video/" + videoID + "?autoplay=1' frameborder='0' allowfullscreen='true' allow='autoplay; encrypted - media'1></iframe>";														
							$(this).append(iFrame);							
						}
				});
					
			});

		});
	}

	// Parse the video url and return an object help (type & video id)
	function parseVideo(url) {
		url.match(/(http:|https:|)\/\/(player.|www.)?(vimeo\.com|youtu(be\.com|\.be|be\.googleapis\.com))\/(video\/|embed\/|watch\?v=|v\/)?([A-Za-z0-9._%-]*)(\&\S+)?/);

		if (RegExp.$3.indexOf('youtu') > -1) {
			var type = 'youtube';
		} else if (RegExp.$3.indexOf('vimeo') > -1) {
			var type = 'vimeo';
		}

		return {
			type: type,
			ID: RegExp.$6
		};
	}

	// Grab the video image
	function getVideoDetails(url, cb) {
		var videoObj = parseVideo(url);
		if (videoObj.type == 'youtube') {
			cb(['youtube', videoObj.ID, '//img.youtube.com/vi/' + videoObj.ID + '/sddefault.jpg']);
		} else if (videoObj.type == 'vimeo') {
			$.get('https://vimeo.com/api/v2/video/' + videoObj.ID + '.json', function (data) {
				cb(['vimeo', videoObj.ID, data[0].thumbnail_large]);
			});
		}
	}
	
	// Check image size. 
	function getImgSize(imgSrc, cb) {
		var newImg = new Image();

		newImg.onload = function () {			
			cb({ width: newImg.width })			
		}

		return newImg.src = imgSrc;
	}

});