$(".white1").click(function(){
	$(".sign").removeAttr("readonly");
	$(".save").css("display","block");
})
$(document).click(function(){
    $(".sign").attr("readonly","readonly");
});
$(".sign").click(function(event){
    event.stopPropagation();
});
$(".white1").click(function(event){
    event.stopPropagation();
});


$(".white2").click(function(){
	$(".name_input").removeAttr("readonly");
	$(".save").css("display","block");
})
$(document).click(function(){
    $(".name_input").attr("readonly","readonly");
});
$(".name_input").click(function(event){
    event.stopPropagation();
});
$(".white2").click(function(event){
    event.stopPropagation();
});


$(".white3").click(function(){
	$(".gender_input").removeAttr("readonly");
	$(".save").css("display","block");
})
$(document).click(function(){
    $(".gender_input").attr("readonly","readonly");
});
$(".gender_input").click(function(event){
    event.stopPropagation();
});
$(".white3").click(function(event){
    event.stopPropagation();
});


$(".white4").click(function(){
	$(".date_input").removeAttr("readonly");
	$(".save").css("display","block");
})
$(document).click(function(){
    $(".date_input").attr("readonly","readonly");
});
$(".date_input").click(function(event){
    event.stopPropagation();
});
$(".white4").click(function(event){
    event.stopPropagation();
});


$(".portrait").click(function(){
	$(".pop").css("display","block")
})
$(document).click(function(){
    $(".pop").css("display","none")
});
$(".portrait").click(function(event){
    event.stopPropagation();
});
$(".pop").click(function(event){
    event.stopPropagation();
});