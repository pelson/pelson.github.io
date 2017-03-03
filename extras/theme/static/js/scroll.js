scrollBottom = function () {
   return $(document).height() - $(window).height() - $(window).scrollTop();
}

$(window).scroll(function() {
  // Reduce the navbar once we have scrolled a little, but make it bigger again once we are near the bottom.
  elems = $('nav').find('*')
  if (navbar_toggled !== null) {
    elems = elems.not($('.actual-navbar').find('*'));
    elems = elems.not($('.actual-navbar'));
  }
  if ($(document).scrollTop() > 90) {
    elems.addClass('shrink');
  } else {
    elems.removeClass('shrink');
  }
});

function toggle_nav() {
  $('nav').find('*').not($('.actual-navbar')).not($('.actual-navbar').find('*')).toggleClass('shrink');
}

function real_nav() {
  nav_currently_visible = ! $('.actual-navbar').hasClass('shrink');
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
}

$('.nav-toggle').click(real_nav);


$(document).keydown(function(e){
    /* console.log(e.keyCode) */
    if (e.keyCode == 83) { 
       toggle_nav();
    }
    if (e.keyCode == 78) {
      real_nav();
    }
});

if (navbar_toggled === undefined) {
  /* TODO: Use a data attribute on the object. */
  var navbar_toggled = null;
}

