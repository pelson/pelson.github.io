$(function() {

   $(".settings-panel").height($(document).height()-70);

   $(".settings-panel #color-bluegreen").click(function(){
      $("link#theme-styles").attr("href", "css/styles-bluegreen.css");
      _gaq.push(['_trackEvent', 'Color Schemes', 'Switch', 'Blue Green']);
      return false;
   });

   $(".settings-panel #color-bluered").click(function(){
      $("link#theme-styles").attr("href", "css/styles-bluered.css");
      _gaq.push(['_trackEvent', 'Color Schemes', 'Switch', 'Blue Red']);
      return false;
   });

   $(".settings-panel #color-greyred").click(function(){
      $("link#theme-styles").attr("href", "css/styles-greyred.css");
      _gaq.push(['_trackEvent', 'Color Schemes', 'Switch', 'Grey Red']);
      return false;
   });

   $(".settings-toggle #toggle").click(function(){
      $(".settings-panel").fadeToggle({duration:400});
      
      if ($(".settings-toggle").hasClass('toggled') === false) {
         $(".settings-toggle").addClass("toggled").children(".glyphicons").removeClass("tint").addClass("remove_2");
         _gaq.push(['_trackEvent', 'Settings Panel', 'Open']);
      } else {
         $(".settings-toggle").removeClass("toggled").children(".glyphicons").addClass("tint").removeClass("remove_2");
         _gaq.push(['_trackEvent', 'Settings Panel', 'Close']);
      }

      return false;
   });
});


// $(document).mouseup(function (e)
// {
//     var container = $(".settings-panel");
//     var toggler = $(".settings-toggle #toggle");

//     if (!container.is(e.target) && !toggler.is(e.target) && container.has(e.target).length === 0)
//     {
//         container.hide();
//     }
// });