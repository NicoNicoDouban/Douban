$(".class1").click(function(){
	$(".book_cl_right").css({"position":"relative","top":"0px"})
	$(this).prevAll().hide();
	$(this).nextAll().hide();
	if($(this).css("marginTop")=="44px"){
		$(this).animate({marginTop:'0px'},10);
	}	
	$(".book_cl_right").css({"visibility":"visible","display":"block"});
})
$(".delete_right").click(function(){
	$(".book_cl_right").css({"position":"absolute","top":"-3000px"})
	$(".book_cl_right").css({"visibility":"hidden"});
	$(".class1").css("display","block");
	for(var i=0;i<8;i++){
		if($(".book_cl").children().eq(i).css("marginTop")=="0px"){
			$(".book_cl").children().eq(i).css("marginTop","44px")
		}
	}
	
})