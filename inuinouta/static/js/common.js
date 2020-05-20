
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var controller;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('youtube-player', {
	  height: '405',
	  width: '720',
	  videoId: initialVideoId,
	  playerVars: { 'start': initialVideoStart },
	  events: {
		'onReady' : onPlayerReady,
		'onStateChange': syncPlayingState
	  }
	});
  }

function onPlayerReady(event) {
	controller = new PlayerController(event.target, songList);
}

var playingState = "pause";
function syncPlayingState(event) {
	obj = document.getElementById("control-icon");
	if (event.data == YT.PlayerState.PLAYING) {
		obj.innerHTML = '<i class="far fa-pause-circle fa-4x fa-color-inui"></i>';
		playingState = "play";
		firstPlay = true;
	}
	if (event.data == YT.PlayerState.PAUSED) {
		obj.innerHTML = '<i class="far fa-play-circle fa-4x fa-color-inui"></i>';
		playingState = "pause";
	}
}
function changePlayingState() {
	obj = document.getElementById("control-icon");
	if (playingState == "play") {
		player.pauseVideo();
		obj.innerHTML = '<i class="far fa-play-circle fa-4x fa-color-inui"></i>';
		playingState = "pause";
		return;
	}
	if (playingState == "pause") {
		player.playVideo();
		obj.innerHTML = '<i class="far fa-pause-circle fa-4x fa-color-inui"></i>';
		playingState = "play";
		firstPlay = true;
		return;
	}
}

var currentVideoId;

function loadVideo(video_id, seek_to=0) {
  player.loadVideoById(video_id, seek_to);
  currentVideoId = video_id;
}

function playSong(song) {
  if (song.video.id !== currentVideoId) {
    loadVideo(song.video.id, song.start_at);
  } else {
    player.seekTo(song.start_at);
    player.playVideo();
  }
  sendPlaySongEvent(song);
  updateSongInfo(song.video.id, song.title + " / " + song.artist, song.video.title);
  updateSongRowStyle(song);
}

function updateSongRowStyle(song=null) {
  $(".song-row").removeClass("selected");
  if (song) {
    $("#song-row-" + song.id).addClass("selected");
  }
}

var controller;
$(function(){
  $('a.song-title').click(function(event){
	  return false;
  });
  controller = new PlayerController(player, songList);
});

function updateSongInfo(video_id, song_title, video_title) {
  var playingThumb = document.getElementById("playing-thumb");
  var playingSongTitle = document.getElementById("navigation-song-title");
  var playingVideoTitle = document.getElementById("navigation-video-title");
  playingThumb.src = "http://img.youtube.com/vi/" + video_id + "/mqdefault.jpg";
  playingSongTitle.textContent = song_title;
  playingVideoTitle.textContent = video_title;
}

class Video {
	constructor(id, title) {
		this.id = id;
		this.title = title;
		this.songs = [];
		this.firstSong = null;
		this.lastSong = null;
		this.prev = null;
		this.next = null;
	}
	addSong(song) {
		this.songs.push(song);
		if (!this.firstSong) {
			this.firstSong = song;
		}
		this.lastSong = song;
	}
}

class VideoList {
	constructor() {
		this.videos = {};
	}
	addVideo(video) {
		this.videos[video.id] = video;
	}
	
}

class Song {
	constructor(id, video, title, artist, start_at, end_at) {
		this.id = id;
		this.video = video;
		this.title = title;
		this.artist = artist;
		this.start_at = start_at;
		this.end_at = end_at;
		this.prev = null;
		this.next = null;
	}
	isPlaying(video_id, time) {
		if (this.video.id != video_id) {
			return false
		}
		if (this.start_at <= time && time <= this.end_at) {
			return true;
		}
		return false;
	}

}
class SongList {
	constructor() {
		this.songs = new Array();
	}
	addSong(obj_song) {
		this.songs[obj_song.id] = obj_song;
	}
	searchSong(video_id, current_time) {
		var res = this.songs.filter(function(item, index){
			if (item.isPlaying(video_id, current_time)) return true;
		});
		return res[0];
	}
}

class PlayerController {
	constructor(player, songlist) {
		this.player = player
		this.songList = songlist;
	}
	play(song) {
    playSong(song);
	}
	playPrevSong() {
		songPlaying = this.getPlayingSong();
		if (songPlaying) {
			this.play(songPlaying.prev);
		} else {
			video = videoList.videos[this.player.getVideoData().video_id];
			var songStored = video.prev.lastSong;
			video.songs.forEach(song => {
				if (this.player.getCurrentTime() < song.start_at) {
					this.play(songStored);
					return;
				}
				songStored = song;
			});
		}
	}
	playNextSong() {
		songPlaying = this.getPlayingSong();
		if (songPlaying) {
			this.play(songPlaying.next);
		} else {
			video = videoList.videos[this.player.getVideoData().video_id];
			var played = false;
			video.songs.forEach(song => {
        if (!played) {
          if (this.player.getCurrentTime() < song.start_at) {
            this.play(song);
            played = true;
            return;
          }
        }
			});
			if (!played) {
				this.play(video.next.firstSong);
			}
		}
	}
	getPlayingSong() {
		return this.songList.searchSong(this.player.getVideoData().video_id, this.player.getCurrentTime());
	}
}
