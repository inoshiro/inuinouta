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
		let res = this.songs.filter(function(item, index){
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
    if (song) {
      playSong(song);
    }
	}
  playOrPause(song) {
    if (song) {
      if (song == this.getPlayingSong()) {
        changePlayingState();
      } else {
        playSong(song);
      }
    }
  }
	playPrevSong() {
		songPlaying = this.getPlayingSong();
		if (songPlaying) {
      if (this._isBegginingOfSong()) {
        this.play(songPlaying.prev);
      } else {
        this.play(songPlaying);
      }
		} else {
			let video = videoList.videos[this.player.getVideoData().video_id];
			let songStored = video.prev.lastSong;
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
			let video = videoList.videos[this.player.getVideoData().video_id];
			let played = false;
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
  autoJump() {
		songPlaying = this.getPlayingSong();
    if (songPlaying) {
      if (Math.ceil(this.player.getCurrentTime()) == songPlaying.end_at ) {
        this.playNextSong();
      }
    }
  }
	getPlayingSong() {
		return this.songList.searchSong(this.player.getVideoData().video_id, this.player.getCurrentTime());
	}
  _isBegginingOfSong() {
		let songPlaying = this.getPlayingSong();
		if (songPlaying) {
      let borderTime = songPlaying.start_at + 5;
      if (this.player.getCurrentTime() < borderTime) {
        return true;
      }
    }
    return false
  }
}


function deserialize_data(data) { 
  let video_list = new VideoList();
  let song_list = new SongList();
  let song_prev, video_prev;

  for (let i = 0, len_i = data.length; i < len_i; ++i) {

    item_v = data[i];
    obj_video = new Video(item_v['id'], item_v['title'])

    if (video_prev) {
      obj_video.prev = video_prev;
      video_prev.next = obj_video;
    }

    for (let j = 0, len_j = item_v['songs'].length; j < len_j; ++j) {

      item_s = item_v['songs'][j];
      obj_song = new Song(item_s['id'], obj_video, item_s['title'], item_s['artist'], item_s['start_at'], item_s['end_at']);

      if (song_prev) {
        obj_song.prev = song_prev;
        song_prev.next = obj_song;
      }

      obj_video.addSong(obj_song);
      song_list.addSong(obj_song);
      song_prev = obj_song;
    }

    video_list.addVideo(obj_video);
    video_prev = obj_video;
  }
  return {video_list, song_list}
}


// for google analytics
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-166010180-1');

<!-- Google Analytics -->
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-166010180-1', 'auto');
ga('send', 'pageview');
<!-- End Google Analytics -->

function sendPlaySongEvent(video_title, song_title) {
  ga('send', {
    hitType: 'event',
    eventCategory: 'Song',
    eventAction: 'play',
    eventLabel: song_title + ' / ' + video_title
  });
}
