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

$('.delete').click(function(){
	$(this).parent().remove();
})

$(".first_one").click(function(){
	$(".first_one").css({"border":"none","color":"white","background":"#F7BDCA"});
	$(".first_two").css({"border":"2px solid #CCCCCC","color":"#CCCCCC","background":"white"});

})
$(".first_two").click(function(){
	$(".first_two").css({"border":"none","color":"white","background":"#F7BDCA"});
	$(".first_one").css({"border":"2px solid #CCCCCC","color":"#CCCCCC","background":"white"});

})

$(".second_one").click(function(){
	$(".second_one").css({"border":"none","color":"white","background":"#F7BDCA"});
	$(".second_two").css({"border":"2px solid #CCCCCC","color":"#CCCCCC","background":"white"});

})
$(".second_two").click(function(){
	$(".second_two").css({"border":"none","color":"white","background":"#F7BDCA"});
	$(".second_one").css({"border":"2px solid #CCCCCC","color":"#CCCCCC","background":"white"});

})

$(".third_one").click(function(){
	$(".third_one").css({"border":"none","color":"white","background":"#F7BDCA"});
	$(".third_two").css({"border":"2px solid #CCCCCC","color":"#CCCCCC","background":"white"});

})
$(".third_two").click(function(){
	$(".third_two").css({"border":"none","color":"white","background":"#F7BDCA"});
	$(".third_one").css({"border":"2px solid #CCCCCC","color":"#CCCCCC","background":"white"});

})

