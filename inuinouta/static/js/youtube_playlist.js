// youtube_playlist.js
// YouTube動画のシーンの再生をプレイリストで制御するJS


// IFrame Player APIのスクリプトを埋め込む
// https://developers.google.com/youtube/iframe_api_reference?hl=ja
var onYouTubeIframeAPIReady;
var player;
var ytp_config;
var controller;
class YouTubePlayerConfig {
  constructor(height, width, video_id, player_tag) {
    ytp_config = {
      height: height,
      width: width,
      video_id: video_id,
      player_tag: player_tag
    }
  }
  player_init(scene_list, state_change_func) {
    let tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    let firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    onYouTubeIframeAPIReady = function() {
      player = new YT.Player(ytp_config.player_tag, {
        height: ytp_config.height,
        width: ytp_config.width,
        videoId: ytp_config.video_id,
        playerVars: {
          playsinline: 1,
          controls: 1 // シークバーと音量コントロールを実装後切り替える
        },
        events: {
          'onStateChange': state_change_func
        }
      });
      controller = new Controller();
      controller.setPlayer(player);
      controller.setPlaylist(scene_list);
    }
  }
}

function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING) {
    controller.changeState(STATE_PLAYING);
    return;
  }
  if (event.data == YT.PlayerState.PAUSED) {
    controller.changeState(STATE_PAUSED);
    return;
  }
}


const STATE_PAUSED = 0;
const STATE_PLAYING = 1;
class Controller {
  constructor() {
    this.player = null;
    this.playlist = null;
    this.sceneIndex = {};
    this.scenePointer = 0;
    this.state = STATE_PAUSED;
  }
  setPlayer(player) {
    this.player = player;
  }
  setPlaylist(playlist) {
    this.playlist = playlist;
    this.scenePointer = 0;
    this.sceneIndex = {};
    for (let i = 0; i < playlist.length; i++) {
      let scene = playlist[i];
      this.sceneIndex[scene.id] = i;
    }
  }
  getScene(scene_id) {
    let pointer = this.sceneIndex[scene_id];
    return this.playlist[pointer];
  }
  changeState(state) {
    this.state = state;
  }
  play() {
    this.player.playVideo();
  }
  pause() {
    this.player.pauseVideo();
  }
  playOrPause() {
    // 初期状態からは、一曲目を再生
    if (this.scenePointer == null) {
      let scene = this.playlist[0];
      this.player.loadVideoById(scene.video_id, scene.start_at, 'large');
      this.scenePointer = 0;
      return true;
    }
    // 再生済みの場合
    if (this.state == STATE_PLAYING) {
      this.player.pauseVideo();
      return true;
    }
    // 停止中の場合
    if (this.state == STATE_PAUSED) {
      this.player.playVideo();
      return true;
    }
  }
  playScene(scene_id) {
    let scene = this.getScene(scene_id);
    let pointer = this.sceneIndex[scene_id];
    if (this.scenePointer == pointer) {
      this.playOrPause();
      return true;
    }
    this.player.loadVideoById(scene.video_id, scene.start_at, 'large');
    this.scenePointer = pointer;
  }
  prev() {
    let playing_scene = this.playlist[this.scenePointer];
    let pointer = this.scenePointer - 1;
    let prev_scene = this.playlist[pointer];
    if (playing_scene.video_id == prev_scene.video_id) {
      this.player.seekTo(prev_scene.start_at, true)
    } else {
      this.player.loadVideoById(prev_scene.video_id, prev_scene.start_at, 'large');
    }
    this.scenePointer = pointer;
  }
  next() {
    let playing_scene = this.playlist[this.scenePointer];
    let pointer = this.scenePointer + 1;
    let next_scene = this.playlist[pointer];
    if (playing_scene.video_id == next_scene.video_id) {
      this.player.seekTo(next_scene.start_at, true)
    } else {
      this.player.loadVideoById(next_scene.video_id, next_scene.start_at, 'large');
    }
    this.scenePointer = pointer;
  }
  autoJump() {
    let scene = this.playlist[this.scenePointer];
    if (Math.ceil(this.player.getCurrentTime()) == scene.end_at) {
      this.next();
    }
  }
  getPlayingScene() {
    return this.playlist[this.scenePointer];
  }
}

// Fisher-Yates shuffle
function shufflePlaylist(playlist) {
  let shuffled = playlist.slice();
  for (let i = shuffled.length -1; i >= 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}
