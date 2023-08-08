var parent = document.querySelector("#parent-form")
var table = document.querySelector("#table-form")
var addButton = document.querySelector("#add-form")
var totalForms = document.querySelector("#id_senderdoc_rworder-TOTAL_FORMS")
var totalForms_rd_order = document.querySelector("#id_recipientdoc_rworder-TOTAL_FORMS")
var status_rw_order = document.querySelector("#status_rw_order")


addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let itemForm = document.querySelectorAll(".item-form")
    let newForm = itemForm[itemForm.length-1].cloneNode(true) 
    let formRegex = RegExp(`rworder-(\\d){1}-`,'g') 

    let formNum = itemForm.length-1 
    formNum++ 
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `rworder-${formNum}-`) 
    parent.insertBefore(newForm, itemForm[itemForm.length-1].nextSibling)

    if (status_rw_order == 'r') {
        totalForms_rd_order.setAttribute('value', `${formNum+1}`)
    } else {
        totalForms.setAttribute('value', `${formNum+1}`)
    }
}

function showEditPopup(url) {
    var win = window.open(url, "Edit", 
        'height=500,width=800,resizable=yes,scrollbars=yes');
    return false;
}
function showAddPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    href = triggeringLink.href;
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
function closePopup(win, newID, newRepr, id) {
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
    win.close();
}

$("#edit_address").click(function(){
	address_name = $("#id_address option:selected").text();
    var data = {"address_name":address_name};
    $.ajax({
        type : 'GET',
        url :  'railway-order-address/ajax/get_address_id',
        data : data,
        success : function(data){
        	var url = "railway-order-address/" + data['address_id'] + "/edit/";
        	showEditPopup(url);
        },
        error: function(data) {
          alert("Something Went Wrong"); 
        }
  	});
})

$("#edit_shipper").click(function(){
	shipper_name = $("#id_shipper option:selected").text();
    var data = {"shipper_name":shipper_name};
    $.ajax({
        type : 'GET',
        url :  'railway-order-shipper/ajax/get_shipper_id',
        data : data,
        success : function(data){
        	var url = "railway-order-shipper/" + data['shipper_id'] + "/edit/";
        	showEditPopup(url);
        },
        error: function(data) {
          alert("Something Went Wrong"); 
        }
  	});
})
