// $(window).scroll(function() {

scrollBottom = function () {
   return $(document).height() - $(window).height() - $(window).scrollTop();
}


function resizer(event) {
  $('#navbar-spacer').height($('nav').height() + 50);
}

$(window).ready(resizer);
$(window).resize(resizer);

$(window).scroll(function() {
  // Reduce the navbar once we have scrolled a little, but make it bigger again once we are near the bottom.
  elems = $('nav').find('*')
  if (navbar_toggled !== null) {
    elems = elems.not($('.actual-navbar'));
  }
  if ($(document).scrollTop() > 90 && scrollBottom() > 40) {
    elems.addClass('shrink');
  } else {
    elems.removeClass('shrink');
  }
});

function toggle_nav() {
  $('nav').find('*').not($('.actual-navbar')).toggleClass('shrink');
}

$('.nav-toggle').click(function () {
  nav_currently_visible = ! $('.actual-navbar').hasClass('shrink');
  console.log('Current status visible:', nav_currently_visible, navbar_toggled);
  if (navbar_toggled === null) {
    navbar_toggled = nav_currently_visible;
  }
  navbar_toggled = !navbar_toggled;
  if (!navbar_toggled) {
    $('.actual-navbar').find('*').addClass('shrink')
    $('.actual-navbar').addClass('shrink')
  } else {
    $('.actual-navbar').find('*').removeClass('shrink')
    $('.actual-navbar').removeClass('shrink')
  }
  
});


$(document).keydown(function(e){
    console.log(e.keyCode)
    if (e.keyCode == 83) { 
       toggle_nav();
    }
});

var navbar_toggled = null;

