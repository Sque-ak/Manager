
$(document).ready(function() {

  // Modal button when user click on button it call the modal form.
  $(".modal-form").each(function() {$(this).modalForm({
    formURL: $(this).data("form-url") 
  }); });

  $(".move_to_detail_page").click(function(e) {
    if ($(e.target).hasClass('action') || $(e.target).is('button') || $(e.target).is('img')) {
      return false;
    }
    else {
    document.location=$(this).data("form-url");
    }
  });

  $("#dateperiod_button").click(function(){
    $(this).text(function(i, text){
      return text === "Период ▽" ? "Период ▷" : "Период ▽";
    })
    $("#dateperiod").toggle();
  }); 
  
  $("#dateperiod").hide();  
  

});

