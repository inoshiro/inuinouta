var playingState = "pause";
function syncPlayingState(event) {
	obj = document.getElementById("control-icon");
	if (event.data == YT.PlayerState.PLAYING) {
    controller.changeState(STATE_PLAYING);
    obj.setAttribute("title", "停止する")
		obj.innerHTML = '<i class="far fa-pause-circle fa-4x fa-color-inui clickable-button"></i>';
		playingState = "play";
    propSongInfo();
	}
	if (event.data == YT.PlayerState.PAUSED) {
    controller.changeState(STATE_PAUSED);
    obj.setAttribute("title", "再生する")
		obj.innerHTML = '<i class="far fa-play-circle fa-4x fa-color-inui clickable-button"></i>';
		playingState = "pause";
	}
}
function changePlayingState() {
	obj = document.getElementById("control-icon");
	if (playingState == "play") {
    controller.playOrPause();
		obj.innerHTML = '<i class="far fa-play-circle fa-4x fa-color-inui clickable-button"></i>';
		playingState = "pause";
		return;
	}
	if (playingState == "pause") {
    controller.playOrPause();
		obj.innerHTML = '<i class="far fa-pause-circle fa-4x fa-color-inui clickable-button"></i>';
		playingState = "play";
		return;
	}
}

var isShuffle = false;
function changeShuffleMode(playlist) {
  obj = document.getElementById("control-button-shuffle");
  controller.pause();
  if (isShuffle) {
    controller.setPlaylist(playlist);
    controller.player.loadVideoById(playlist[0].video_id, playlist[0].start_at, 'large');
    obj.style.color = "#333";
    isShuffle = false;
  } else {
    let shuffled = shufflePlaylist(playlist);
    controller.setPlaylist(shuffled);
    controller.player.loadVideoById(playlist[0].video_id, playlist[0].start_at, 'large');
    obj.style.color = "green";
    isShuffle = true;
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

$(function() {
  $('a.song-title').click(function() {
    return false;
  });
});

function updateSongRowStyle(song=null) {
  $(".song-row").removeClass("selected");
  if (song) {
    $("#song-row-" + song.id).addClass("selected");
  }
}

function updateSongInfo(video_id, song_title, video_title) {
  var playingThumb = document.getElementById("playing-thumb");
  var playingSongTitle = document.getElementById("navigation-song-title");
  var playingVideoTitle = document.getElementById("navigation-video-title");
  playingThumb.src = "static/images/thumbs/" + video_id + ".jpg";
  playingSongTitle.textContent = song_title;
  playingVideoTitle.textContent = video_title;
}

function updateTweetData(song) {
  var intentUrl = "https://twitter.com/intent/tweet?";
  var text = "いぬいのうたで「" + song.title + "/" + song.artist + "」を再生中";
  var url = "https://uta.inui-dondon-sukininaru.net/?vid=" + song.video_id + "&sid=" + song.id;
  var hashtag = "いぬいのうた";

  var params = new URLSearchParams({
    "text": text,
    "url": url,
    "hashtags": hashtag
  });

  var obj = document.getElementById("twitter-share-link");
  obj.setAttribute("href", 
    intentUrl + params.toString()
  );
}

function propSongInfo()  {
  let song = controller.getPlayingScene();
  songPlaying = song;
  updateSongInfo(song.video_id, song.title  + " / " + song.artist, data_videos[song.video_id].title);
  updateTweetData(song);
  updateSongRowStyle(song);
}
