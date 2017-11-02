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
      $('div.left-side').load("template/block-left-sidebar-" + $(this).attr("data-index") + ".html");
    }else{
      //class two

    }
    //Todo: tooltip update
  });
});
