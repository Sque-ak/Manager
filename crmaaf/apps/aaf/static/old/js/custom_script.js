function slider() {
  /**
   * Function for scrolling sliders on the main sector;
   */

  let indexSlide = 0;
  var slids = document.querySelectorAll(".slick-slide");
  let mainImg = document.querySelector(".main-section-1__img");
  let mainDesc = document.querySelectorAll(".main-section-1__littledesc");

  function change() { // Change a slide on the board.

      for (let i = 0; i < slids.length; i++) {
        slids[i].classList.remove("slick-current"); //Clear a slide tags;
        mainDesc[i].classList.remove("show_desc");
      }

      slids[indexSlide].classList.add("slick-current"); //Set the active slick;
      mainDesc[indexSlide].classList.add("show_desc");  //Set the active description;
      mainImg.style.opacity = "0"; //For animation;
      setTimeout(function() { 
        mainImg.src = slids[indexSlide].src; //Set the active image;
        mainImg.style.opacity = "1"; 
      }, 500);
  }
  
  let Next = document.querySelector(".slick-next");
  Next.addEventListener('click', function() {
    if (indexSlide >= slids.length-1) indexSlide = 0; // Reset counter;
    else indexSlide += 1;

    change(); //change slide.
  });

  let Prev = document.querySelector(".slick-prev")
  Prev.addEventListener('click', function() {
    if (indexSlide <= 0) indexSlide = slids.length-1; // Resever the reset counter;
    else indexSlide -= 1;

    change(); //change slide
  });

  for (let i = 0; i < slids.length; i++) {
    slids[i].addEventListener('click', function(){ //The slids buttons on bottom;
      indexSlide = i;
      change(); //change slide
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  slider();
});
