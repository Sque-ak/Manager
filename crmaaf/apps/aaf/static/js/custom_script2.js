/* Toggle between adding and removing the "responsive" class to nav menu when the user clicks on the icon */

function navigationMenu(){
    $(".nav-button").click(function() {
      $('.nav-menu').toggleClass('responsive');
    });
  };

  /* Toggle between adding and removing the "open" class to nav menu when the user clicks on the icon */
function menu(){
  $(".nav-menu").toggleClass('open');
  $(".nav-button").toggleClass('col--close')
  $(".nav-button").toggleClass('col--bars')
};

  function scrollToPage(numberPage) {
    scrollTo($(".page-to-" + numberPage).position());
  }

  function changePage(numberPage) {
    $(".selected-page").fadeOut(600);
    $(".selected-page").toggleClass("selected-page");
    $(".page-to-"+numberPage).toggleClass("selected-page");
    $(".page-to-"+numberPage).fadeIn(1200);
  }

  function customSelector() {
    $(".shareholder-selector").each(function() {
      var classes = $(this).attr("class");
      var template = '<div class="' + classes + '">';
      template += '<span class="custom-select-trigger">' + $(this).attr("placeholder") + "</span>";
      template += '<div class="custom-options">';
      $(this).find("option").each(function() {
        template += '<span class="custom-option ' + $(this).attr("class") + '" data-value="' + $(this).attr("value")+'">' + $(this).html() + "</span>";
      });
      template += "</div></div>";
      $(this).wrap('<div class="custom-select-wrapper"> </div>');
      $(this).hide();
      $(this).after(template);
    });

    $(".custom-option:first-of-type").hover(
      function() {
        $(this)
          .parents(".custom-options")
          .addClass("option-hover");
      },
      function() {
        $(this)
          .parents(".custom-options")
          .removeClass("option-hover");
      }
    );
    $(".custom-select-trigger").on("click", function() {
      $("html").one("click", function() {
        $(".shareholder-selector").removeClass("opened");
      });
      $(this)
        .parents(".shareholder-selector")
        .toggleClass("opened");
      event.stopPropagation();
    });
    $(".custom-option").on("click", function() {
      changePage($(this).data("value"));
      $(this).parents(".custom-select-wrapper").find("select").val($(this).data("value"));
      $(this).parents(".custom-options").find(".custom-option").removeClass("selection");
      $(this).addClass("selection");
      $(this).parents(".shareholder-selector").removeClass("opened");
      $(this).parents(".shareholder-selector").find(".custom-select-trigger").text($(this).text());
    });
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

    $(".nav-button").click(function() {  
      menu();
    });

    $(window).scrollTop(0);
    $('.col--arrow-up').show();

    const swiperGroups = document.querySelector('.swiper-groups')
    Object.assign(swiperGroups, {
      slidesPerView: 1,
      spaceBetween: 10,
      breakpoints: {
        640: {
          slidesPerView: 2,
          spaceBetween: 20,
          navigation: true,
        },
        768: {
          slidesPerView: 4,
          spaceBetween: 20,
        },
        1024: {
          slidesPerView: 6,
          spaceBetween: 30,
        },
      },
    });

    swiperGroups.initialize();
    navigationMenu();
    customSelector();
  });