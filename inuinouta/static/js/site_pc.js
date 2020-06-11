
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var controller;
function onYouTubeIframeAPIReady() {
  loadPlayer();
}

function loadPlayer() {
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
    obj.setAttribute("title", "停止する")
		obj.innerHTML = '<i class="far fa-pause-circle fa-4x fa-color-inui"></i>';
		playingState = "play";
		firstPlay = true;
	}
	if (event.data == YT.PlayerState.PAUSED) {
    obj.setAttribute("title", "再生する")
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
