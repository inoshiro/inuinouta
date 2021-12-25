var playingState = "pause";
function syncPlayingState(event) {
  obj = document.getElementById("control-icon");
  if (event.data == YT.PlayerState.PLAYING) {
    controller.changeState(STATE_PLAYING);
    obj.setAttribute("title", "停止する");
    obj.innerHTML =
      '<i class="far fa-pause-circle fa-4x fa-color-inui clickable-button"></i>';
    playingState = "play";
    propSongInfo();
  }
  if (event.data == YT.PlayerState.PAUSED) {
    controller.changeState(STATE_PAUSED);
    obj.setAttribute("title", "再生する");
    obj.innerHTML =
      '<i class="far fa-play-circle fa-4x fa-color-inui clickable-button"></i>';
    playingState = "pause";
  }
}
function changePlayingState() {
  obj = document.getElementById("control-icon");
  if (playingState == "play") {
    controller.playOrPause();
    obj.innerHTML =
      '<i class="far fa-play-circle fa-4x fa-color-inui clickable-button"></i>';
    playingState = "pause";
    return;
  }
  if (playingState == "pause") {
    controller.playOrPause();
    obj.innerHTML =
      '<i class="far fa-pause-circle fa-4x fa-color-inui clickable-button"></i>';
    playingState = "play";
    return;
  }
}

var isShuffle = false;
function changeShuffleMode(playlist) {
  obj = document.getElementById("control-button-shuffle");
  controller.pause();
  if (isShuffle) {
    window.dispatchEvent(
      new CustomEvent("playScene", { detail: { id: playlist[0].id } })
    );
    controller.setPlaylist(playlist);
    controller.player.loadVideoById(
      playlist[0].video_id,
      playlist[0].start_at,
      "large"
    );
    obj.style.color = "#333";
    isShuffle = false;
  } else {
    let shuffled = shufflePlaylist(playlist);
    controller.setPlaylist(shuffled);
    let skip = true;
    let pointer = 0;
    while (skip) {
      skip = shuffled[pointer].unplayable;
      if (skip) {
        pointer++;
      }
    }
    window.dispatchEvent(
      new CustomEvent("playScene", { detail: { id: shuffled[pointer].id } })
    );
    controller.player.loadVideoById(
      shuffled[pointer].video_id,
      shuffled[pointer].start_at,
      "large"
    );
    obj.style.color = "green";
    isShuffle = true;
  }
}

var currentVideoId;

function loadVideo(video_id, seek_to = 0) {
  player.loadVideoById(video_id, seek_to);
  currentVideoId = video_id;
}

$(function () {
  $("a.song-title").click(function () {
    return false;
  });
});

function updateSongRowStyle() {
  let song = controller.getPlayingScene();
  $(".song-row").removeClass("selected");
  if (song) {
    $("#song-row-" + song.id).addClass("selected");
  }
}

function updateSongInfo(video_id, song_title, video_title) {
  let song = controller.getPlayingScene();
  let video = data_videos[song.video_id];

  let playingThumb = document.getElementById("playing-thumb");
  let playingSongTitle = document.getElementById("navigation-song-title");
  let playingVideoTitle = document.getElementById("navigation-video-title");

  playingThumb.src = "https://inuinouta.s3.ap-northeast-1.amazonaws.com/images/thumbs/" + song.video_id + ".jpg";
  playingSongTitle.textContent = song.title;
  playingVideoTitle.textContent = video.title;
}

function updateTweetData() {
  let song = controller.getPlayingScene();

  let intentUrl = "https://twitter.com/intent/tweet?";
  let text = "いぬいのうたで「" + song.title + "/" + song.artist + "」を再生中";
  let url = "https://uta.inui-dondon-sukininaru.net/?sid=" + song.id;
  let hashtag = "いぬいのうた";

  let params = new URLSearchParams({
    text: text,
    url: url,
    hashtags: hashtag,
  });

  let obj = document.getElementById("twitter-share-link");
  obj.setAttribute("href", intentUrl + params.toString());
}

function propSongInfo() {
  updateSongInfo();
  updateTweetData();
  updateSongRowStyle();
}

function applyFilter(text) {
  songTable.search(text).draw();
}

window.addEventListener("playScene", (event) => {
  const tag_id = "song-row-" + event.detail.id;
  const element = document.getElementById(tag_id);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "center" });
  }
});
