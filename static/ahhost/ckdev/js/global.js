$(function(){
  // enable bootstrap 3 tooltip
  $('[data-toggle="tooltip"]').tooltip();

  //set openlayer map dynamically
  var height = $(window).height() - $("section.banner").outerHeight() - $(".footer").outerHeight();
  var width = $(window).width() - $(".left-side").outerWidth();
  $('#map').css('height', height.toString() + 'px');
  $('#map').css('width', width.toString() + 'px');

  //main menu loading dynamically
  $('.nav li').click(function(){
    $('.nav li').removeClass("active");
    $(this).addClass("active");
    if($(this).hasClass("one")){
      //class one
      $('div.left-side').load(
        "template/block-left-sidebar-" + $(this).attr("data-index") + ".html",
        function (){
          $('[data-toggle="tooltip"]').tooltip();
        }
      );

    }else{
      //class two
      switch ($(this).attr("data-index")) {
        case "5":
          $('#help_modal').modal();
          break;
        case "6":
          $('#about_modal').modal();
          break;
        default:
          alert("Global.js Error:未找到modal");
      }
    }
  });


});
