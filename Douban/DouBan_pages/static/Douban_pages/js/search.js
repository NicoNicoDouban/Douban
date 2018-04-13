$(".list_normal").click(function(){
	var s=$(this).text();
	$(".detail_head").text(s);
	$(".list_normal").css({"borderLeft":"0px solid #F2F2F2","paddingLeft":"30px","backgroundColor":"#F2F2F2"});
	$(".list_special").css({"borderLeft":"0px solid #71CDD8","paddingLeft":"30px","backgroundColor":"#71CDD8"});
	$(this).css({"borderLeft":"2px solid #71CDD8","paddingLeft":"28px","backgroundColor":"white"});
})
$(".list_special").click(function(){
	var s=$(this).text();
	$(".detail_head").text(s);
	$(".list_normal").css({"borderLeft":"0px solid #F2F2F2","paddingLeft":"30px","backgroundColor":"#F2F2F2"});
	$(".list_special").css({"borderLeft":"0px solid #71CDD8","paddingLeft":"30px","backgroundColor":"#71CDD8"});
	$(this).css({"borderLeft":"2px solid black","paddingLeft":"28px","backgroundColor":"rgb(153,217,234)"});
})
/*$(".list_book").click(function(){
	$(".detail_main_text").css("display","none");
	$(".book_cl_right").css("display","block");
})
$(".list_text").click(function(){
	$(".detail_main_text").css("display","block");
	$(".book_cl_right").css("display","none");
})*/
$(".list_book").click(function(){
	$(".book_").css("display","block");
	$(".book_author").css("display","none");
	$(".t_").css("display","none");
	$(".te_author").css("display","none");
	$(".te_content").css("display","none");
})

$(".list_author").click(function(){
	$(".book_").css("display","none");
	$(".book_author").css("display","block");
	$(".t_").css("display","none");
	$(".te_author").css("display","none");
	$(".te_content").css("display","none");
})

$(".t_article").click(function(){
	$(".book_").css("display","none");
	$(".book_author").css("display","none");
	$(".t_").css("display","block");
	$(".te_author").css("display","none");
	$(".te_content").css("display","none");
})
$(".t_author").click(function(){
	$(".book_").css("display","none");
	$(".book_author").css("display","none");
	$(".t_").css("display","none");
	$(".te_author").css("display","block");
	$(".te_content").css("display","none");
})
$(".t_text").click(function(){
	$(".book_").css("display","none");
	$(".book_author").css("display","none");
	$(".t_").css("display","none");
	$(".te_author").css("display","none");
	$(".te_content").css("display","block");
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
/*.detail_main_text book_cl_right*/