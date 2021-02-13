// youtube_playlist.js
// YouTube動画のシーンの再生をプレイリストで制御するJS


// IFrame Player APIのスクリプトを埋め込む
// https://developers.google.com/youtube/iframe_api_reference?hl=ja
var onYouTubeIframeAPIReady;
var player;
var ytp_config;
var controller;
class YouTubePlayerConfig {
  constructor(height, width, player_tag) {
    ytp_config = {
      height: height,
      width: width,
      player_tag: player_tag
    }
  }
  player_init(controller, scene_list, video_id, start_at, state_change_func) {
    let tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    let firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    onYouTubeIframeAPIReady = function() {
      player = new YT.Player(ytp_config.player_tag, {
        height: ytp_config.height,
        width: ytp_config.width,
        videoId: video_id,
        playerVars: {
          start: start_at,
          playsinline: 1,
          controls: 1 // シークバーと音量コントロールを実装後切り替える
        },
        events: {
          'onStateChange': state_change_func
        }
      });
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
  constructor(hook_functions) {
    this.player = null;
    this.playlist = null;
    this.sceneIndex = {};
    this.scenePointer = 0;
    this.state = STATE_PAUSED;
    this.hook_functions = hook_functions;
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
      this.player.loadVideoById(scene.video_id, scene.start_at);
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
      this.player.seekTo(scene.start_at, true);
      this.play();
      return true;
    }
    let scene_playing = this.getPlayingScene();
    if (scene.video_id == scene_playing.video_id) {
      this.player.seekTo(scene.start_at, true)
      this.play();
    } else {
      this.player.loadVideoById(scene.video_id, scene.start_at);
    }
    sendPlaySongEvent(scene.title, data_videos[scene.video_id].title);  // FIXME あとで切り離す
    this.scenePointer = pointer;
  }
  prev() {
    let scene = this.getPlayingScene();
    if (Math.ceil(this.player.getCurrentTime()) > (scene.start_at + 5) ) {
      this.playScene(scene.id);
      return;
    }

    let prev_scene = this.getPrevScene();
    this.playScene(prev_scene.id);
  }
  next() {
    let next_scene = this.getNextScene();
    this.playScene(next_scene.id);
  }
  autoJump() {
    let scene = this.getPlayingScene();
    if (Math.ceil(this.player.getCurrentTime()) == scene.end_at) {
      this.next();
    }
  }
  getPlayingScene() {
    return this.playlist[this.scenePointer];
  }
  getPrevScene() {
    return this.playlist[this.scenePointer-1];
  }
  getNextScene() {
    return this.playlist[this.scenePointer+1];
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
