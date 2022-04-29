$(function(){
  'use script'

  feather.replace();

  const sb = new PerfectScrollbar('.sidebar-body', {
    suppressScrollX: true
  });

  // content menu
  $('#contentMenu').on('click', function(e){
    e.preventDefault();
    $('.sidebar').toggleClass('minimized');

    $('.sidebar-body').scrollTop(0);
    sb.update();
  });

  // mobile menu
  $('#mobileMenu').on('click', function(e){
    e.preventDefault();
    $('body').toggleClass('sidebar-show');
  });
  $('#closeMenu').on('click', function(e){
    e.preventDefault();
    $('body').toggleClass('sidebar-show');
  });
});
