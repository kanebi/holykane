jQuery(document).ready(function($) {
	"use strict";

	var player       = $(".ci-soundplayer"),
			tracklisting = $(".ci-soundplayer-tracklist"),
			tracks       =  tracklisting.find('li');

	soundManager.setup({
		flashVersion: 9,
		preferFlash: false,
		onready: function() {

			tracks.each(function() {
				var that = $(this);

				soundManager.createSound({
					id: 'track_' + that.index(),
					url: that.find('a').attr('href'),
					onload: function() {

					},
					onplay: function() {
						player.addClass('playing');
						$('.track-title').text(that.text());

						if ( player.hasClass('ci-current-track') && player.hasClass('ci-streaming') ) {
							var uri = document.createElement('a');
							uri.href = this.url;

							$.SHOUTcast({
								host : uri.hostname,
								port : uri.port,
								interval : 10000,
								stats: function() {
									$('.track-title').text(this.get('songtitle'));
								}
							}).startStats();
						}
					},
					onresume: function() {
						player.addClass('playing');
					},
					onpause: function() {
						player.removeClass('playing');
					},
					onfinish: function() {
						nextTrack();
					},
					whileplaying: function() {
						$(".progress-bar").css('width', ((this.position/this.duration) * 100) + '%');
						var trackTime = getTime(this.position, true);
						$('.track-position').text(trackTime);
					},
					whileloading: function() {
						//$(".load-bar").css('width', ((this.bytesLoaded / this.bytesTotal) * 100) + '%');
					}
				});
			});

			// ## GUI Actions

			// Let's prevent default click action from all player links
			player.find('a').on('click', function(e) {
				e.preventDefault();
			});

			// Get the first track displayed in the track title
			$('.track-title').text(tracklisting.find('> :first-child').text());

			// Bind a click event to each track item in the list.
			// This basically handles all the play functionality,
			// the play button on the player controls actually triggers
			// a click in that specific item.
			tracks.on('click', function() {
				// find out if it's already playing *(set to active)*

				var that = $(this),
						isTrackPlaying = that.is('.active');

				if ( isTrackPlaying ) {
					// If it is playing: pause it.
					soundManager.pause('track_' + that.index());
				} else {
					// If it's not playing: stop all other sounds that might be playing and play the clicked sound.
					if ( that.siblings('li').hasClass('active') ) {
						soundManager.stopAll();
					}

					soundManager.play('track_' + that.index());
				}

				// Finally, toggle the *active* state of the clicked li and remove *active* from and other tracks.
				that.toggleClass('active').siblings('li').removeClass('active');

			});

		// Bind a click event to the play / pause button.
		$('.ci-soundplayer-play, .ci-soundplayer-pause').on('click', function() {

			if ( tracks.hasClass('active') == true ) {

				// If a track is active, play or pause it depending on current state.
				soundManager.togglePause( 'track_' + $('.ci-soundplayer-tracklist li.active').index() );
			} else {
				// If no tracks are active, just play the first one.
				tracklisting.find('li:first').click();
			}
		});

			// Previous + Next Track functionality follows

			$('.ci-soundplayer-next').on('click', function() {
				nextTrack();
			});

			$('.ci-soundplayer-prev').on('click', function() {
				prevTrack();
			});

			var nextTrack = function() {

				// Stop all sounds
				soundManager.stopAll();

				// Click the next list item after the current active one.
				// If it does not exist *(there is no next track)*, click the first list item.
				if ( tracklisting.find('li.active').next().click().length == 0 ) {
					tracklisting.find('li:first').click();
				}
			}; // nextTrack()

			var prevTrack = function(){

				// Stop all sounds
				soundManager.stopAll();

				// Click the previous list item after the current active one.
				// If it does not exist *(there is no previous track)*, click the last list item.
				if ( tracklisting.find('li.active').prev().click().length == 0 ) {
					tracklisting.find('li:last').click();
				}
			}; // prevTrack()

			// Progress Bar, make it clickable
			$('.track-bar').on('click', function(e) {
				var currentTrack = tracklisting.find('li.active');
				if ( currentTrack.length ) {

					// store the track
					var currentTrackID = currentTrack.index(),
							sound = soundManager.getSoundById('track_' + currentTrackID),
							trackbarWidth = $(this).width();

					// get X coordinates of where a user clicked
					var posX = e.pageX - $(this).offset().left,
							newPosition = ( posX / trackbarWidth );

					// make the magic
					if ( sound && sound.duration ) {
						sound.setPosition(sound.duration * newPosition );
					}

				}
			});

			// Track position (time) display
			function getTime(msec, useString) {
		    // convert milliseconds to hh:mm:ss, return as object literal or string
				var nSec = Math.floor(msec/1000),
						hh = Math.floor(nSec/3600),
						min = Math.floor(nSec/60) - Math.floor(hh * 60),
						sec = Math.floor(nSec -(hh*3600) -(min*60));

		    // if (min === 0 && sec === 0) return null; // return 0:00 as null
		    return (useString ? ((hh ? hh + ':' : '') + (hh && min < 10 ? '0' + min : min) + ':' + ( sec < 10 ? '0' + sec : sec ) ) : { 'min': min, 'sec': sec });
		  }
		}
	});
});
