$(".white1").click(function(){
	$(".sign").removeAttr("readonly");
	
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

$(".delete2").click(function(){
	$(this).prev().css("display","block");
})
$(".confirm").click(function(){
	$(this).parent().parent().css("display","none");
})
$(".cancle").click(function(){
	$(this).parent().css("display","none");
})

$(".add").click(function(){
	$(".article").css("display","none");
	$(".form").css("display","block");
})
$(".edit").click(function(){
	$(".article").css("display","none");
	$(".form").css("display","block");
})