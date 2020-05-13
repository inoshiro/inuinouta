var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('youtube-player', {
	  height: '450',
	  width: '800',
	  videoId: initialVideoId
	});
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
