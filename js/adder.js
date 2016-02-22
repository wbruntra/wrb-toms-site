$('#example-1').click(function() {
  $('input[name="title"]').val('In Your Arms');
  $('input[name="code"]').val('IOu0DuxFAT0');
  $('input[name="year"]').val('2012');
});

$('#example-2').click(function() {
  $('input[name="title"]').val('Losing A Whole Year');
  $('input[name="code"]').val('MwlqymYLCb4');
  $('input[name="year"]').val('1998');
});

$('#example-3').click(function() {
  $('input[name="title"]').val('So Sorry');
  $('input[name="code"]').val('wfEPvebGGJM');
  $('input[name="year"]').val('2007');
});

function YouTubeGetID(url){
  var ID = '';
  url = url.replace(/(>|<)/gi,'').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
  if(url[2] !== undefined) {
    ID = url[2].split(/[^0-9a-z_\-]/i);
    ID = ID[0];
  }
  else {
    ID = url;
  }
    return ID;
}

$('#ajaxer').click(function() {
    var vid_id = $('input[name="code"]').val();
    if (vid_id.length == 11) {
        console.log(vid_id);
        requestYoutube(vid_id);
    }
});

$('#parse').click(function(e) {
    e.preventDefault();
    url = $('#my-url').val();
    var parsedCode = YouTubeGetID(url)
    $('input[name="code"]').val(parsedCode);
    $('#ajaxer').click();
});


API_KEY = "AIzaSyDlq1ibZttSj5wjHmSXn3EDrUQs-GjojNk";
URL = "https://www.googleapis.com/youtube/v3/videos";

function requestYoutube(vid_id) {
    var API_KEY = "AIzaSyDlq1ibZttSj5wjHmSXn3EDrUQs-GjojNk";
    var URL = "https://www.googleapis.com/youtube/v3/videos";
    $.ajax({
      dataType:"json",
      url:URL,
      data: {
        key:API_KEY,
        id:vid_id,
        part:'snippet'
      },
      success:function(data) {
        d = data;
        v = d['items'][0]['snippet'];
        vTitle = v['title'];
        $('input[name="title"]').val(vTitle);
        vYear = v['publishedAt'].slice(0,4);
        $('input[name="year"]').val(vYear);
    },
    error:function(e) {
      console.log(e);
    }
    });
};

function validateYoutube(vid_id) {
  $.ajax({
    dataType:"json",
    url:URL,
    data: {
      key:API_KEY,
      id:vid_id,
      part:'snippet'
    },
    success: function(data) {
      if (data['items'].length != 0) {
        console.log('Valid id');
        $('#add-form').submit();
      } else {
        console.log('Invalid id');
        $('.error').html('Video ID not valid');
        $('.error').show();
      }
    },
    error: function(data) {
      console.log(data);
    }
    });
}

$('#add-form input[type="submit"]').click(function(e) {
  e.preventDefault();
  var vid_id = $('input[name="code"]').val();
  validateYoutube(vid_id);
}
);
