var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('youtube-player', {
	  height: '504',
	  width: '896',
	  videoId: initialVideoId,
    playerVars: { 'playsinline': 1 },
	  events: {
      'onReady' : onPlayerReady,
      'onStateChange': syncPlayingState
	  }
	});
}

function onPlayerReady(event) {
	controller = new PlayerController(event.target, songList); // ここグローバルなsongList使ってる
}

var playingState = "pause";
function syncPlayingState(event) {
	obj = document.getElementById("control-icon");
	if (event.data == YT.PlayerState.PLAYING) {
		obj.innerHTML = '<i class="far fa-pause-circle fa-8x fa-color-inui"></i>';
		playingState = "play";
		firstPlay = true;
	}
	if (event.data == YT.PlayerState.PAUSED) {
		obj.innerHTML = '<i class="far fa-play-circle fa-8x fa-color-inui"></i>';
		playingState = "pause";
	}
}
function changePlayingState() {
	obj = document.getElementById("control-icon");
	if (playingState == "play") {
		player.pauseVideo();
		obj.innerHTML = '<i class="far fa-play-circle fa-8x fa-color-inui"></i>';
		playingState = "pause";
		return;
	}
	if (playingState == "pause") {
		player.playVideo();
		obj.innerHTML = '<i class="far fa-pause-circle fa-8x fa-color-inui"></i>';
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

function playSong(video_id, start_at) {
  if (video_id !== currentVideoId) {
    loadVideo(video_id, start_at);
  } else {
    player.seekTo(start_at);
    player.playVideo();
  }
}

$(function(){
  $('a.song-title').click(function(event){
	  return false;
  });
});
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
}
