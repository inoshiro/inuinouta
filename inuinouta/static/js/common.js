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
