$(function(){
  'use script'

  feather.replace();

  const sb = new PerfectScrollbar('.sidebar-body', {
    suppressScrollX: true
  });

  $('.sidebar').on('mouseenter mouseleave', function(e) {
    var isHover = (e.type === 'mouseenter')? true : false;

    if($('.sidebar').hasClass('minimized')) {
      if(isHover) {
        setTimeout(function(){
          $('.sidebar').addClass('expand');
          sb.update();
        }, 300);
      } else {
        $('.sidebar').removeClass('expand');
        $('.sidebar-body').scrollTop(0);
        sb.update();
      }
    }
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

  // for demo only
  $('#navigationSkins a').on('click', function(e){
    e.preventDefault();

    var s = $(this).attr('data-skin');
    localStorage.setItem('skin', s);

    location.reload();
  });

  $('#navigationStyles a').on('click', function(e){
    e.preventDefault();

    var s = $(this).attr('data-style');
    localStorage.setItem('style', s);

    location.reload();
  });

  //on page load
  var sk = (localStorage.getItem('skin'))? localStorage.getItem('skin') : 'base';
  var st = (localStorage.getItem('style'))? localStorage.getItem('style') : 'base';

  // skin
  $('body').attr('class', function(i, c){
    return c.replace(/(^|\s)skin-\S+/g, '');
  });

  $('body').addClass('skin-'+sk);
  $('#navigationSkins a[data-skin='+sk+']').addClass('active').siblings().removeClass('active');

  //sidebar nav style
  $('.nav-sidebar').attr('class', function(i, c){
    return c.replace(/(^|\s)style-\S+/g, '');
  });

  if(st !== 'base') {
    $('.nav-sidebar').addClass('style-'+st);
  }

  $('#navigationStyles a[data-style='+st+']').addClass('active').siblings().removeClass('active');

});
