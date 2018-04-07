$(".phone").click(function(){
	$(".pop_window").animate({
		top:'110px'},600);
	$(".pop_window").css("display","block");
})
$(".close").click(function(){
	$(".pop_window").css({"display":"block","top":"-310px"});
})