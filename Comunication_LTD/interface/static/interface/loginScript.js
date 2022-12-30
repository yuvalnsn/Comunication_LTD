var form = document.getElementById("myForm");  // Use Django template language to render a new HTML template
var login= document.getElementById("loginButton")
var background2=document.getElementById("background")
var fieldHigh = form.elements.id_sec_level_0;
var fieldLow = form.elements.id_sec_level_1;

fieldHigh.onclick= function (){
  background2.style.backgroundColor="#E14D2A"
  console.log(fieldHigh.value);}

fieldLow.onclick= function (){
  console.log(fieldLow.value);}


