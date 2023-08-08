var p_slide = 1;

/* Toggle between adding and removing the "open" class to nav menu when the user clicks on the icon */
function menu(){
    $(".nav-menu").toggleClass('open');
    $(".nav-button").toggleClass('col--close')
    $(".nav-button").toggleClass('col--bars')
};


/*get values of screen height*/
function parralaxEffect() {
  $(".page-n1").css("height", $(window).height() + "px"); 
}

function changeActiveNavItem(numberPage) {
  $('.item-nav-menu').removeClass('active-nav-menu')
  $('.page-' + numberPage).addClass("active-nav-menu")
}

function scrollToPage(numberPage, closemenu) {
  scrollTo($(".page-n" + numberPage).position());
  changeActiveNavItem(numberPage);
  if (closemenu == 1) { 
     menu();
  }

}

function currentSlide(n, slider) {
  slideChange(p_slide = n, slider);
}

function nextSlide(maxSlide, slider) {
  if (p_slide < maxSlide) {
    slideChange(p_slide += 1, slider);   
  } else {
    slideChange(p_slide = 1, slider);
  }
}

function prevSlide(maxSlide, slider) {
  if (p_slide > 1) {
    slideChange(p_slide -= 1, slider);
  } else {
    slideChange(p_slide = maxSlide, slider);
  }
}

function slideChange(n, slider) {
  let dots = document.getElementsByClassName("dot-"+slider);
  $('.pack').css({'opacity': '0', 'max-width': '0', 'max-height': '0', 'overflow': 'hidden'});
  $('.'+ slider +'-pack-'+ n).css({'opacity': '', 'max-width': '', 'max-height': '', 'overflow': ''});  
  $('.dot-'+slider).removeClass('dot-active');
  dots[n-1].className  += ' dot-active';
}

function orderProductShow(nameOrder) {
  $('.overlay-site').fadeIn(300);
  $('#order_product').val(nameOrder);
  $('.popup-order').fadeIn(300);
}

function orderProductHide() {
  $('.overlay-site').fadeOut(300);
  $('.popup-order').fadeOut(300);
  $('.popup-order').val();
}

function thanksHide(){
  $('.overlay-site').fadeOut(300);
  $('.popup-thanks').fadeOut(300);
}

function thanksShow(f){
  $('.overlay-site').fadeIn(300);
  $('.popup-thanks').fadeIn(300);
  $('#close-popup').click(function(){thanksHide(); f.submit();})
}

function whatIsPage(scroll) {

  if (scroll >= $(".page-n1").position().top - 150){
    changeActiveNavItem(1);
  }
  if (scroll >= $(".page-n2").position().top - 150) {
    changeActiveNavItem(2);
  }
  if (scroll >= $(".page-n3").position().top - 150) {
    changeActiveNavItem(3);
  }
  if (scroll >= $(".page-n4").position().top - 450) {
    changeActiveNavItem(4);
  }
}

$(document).ready(function(){

  $("body").fadeIn(250);

  $("a.link-to-page").click(function(event){
    event.preventDefault();
    linkLocation = this.href;
    $("body").fadeOut(250, redirectPage);
  });

  function redirectPage() {
    window.location = linkLocation;
  }

  $(window).scrollTop(0);
  parralaxEffect();
  $(".nav-button").click(function() {  
    menu();
  });
  orderProductHide();
});

$(window).bind('resize',function(){
  parralaxEffect();
});  

$(window).scroll(function (event) {
  let scroll = $(window).scrollTop();
  if (scroll > 0){
    $('header').addClass('active-header');
    $('.col--arrow-up').fadeIn(400);
    $('.logo').removeClass('logo-change-size');
    $('#logo-txt').fadeIn(1);
    if ($(window).height() > 540) {
      $(".page-n1").css("height", "540px"); 
    } else {
      $(".page-n1").css("height", "380px"); 
    }

  }
  else {
    $('header').removeClass('active-header');
    $('.col--arrow-up').fadeOut(400);
    $('.logo').addClass('logo-change-size');
    $('#logo-txt').fadeOut(1);
    parralaxEffect();
  }
  whatIsPage(scroll);
});