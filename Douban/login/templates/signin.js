$(".in").eq(0).click(function(){
	$(".main1").css("display","block");
	$(".main2").css("display","none");
	$(".in").css("backgroundColor","white");
	$(".loginin").css("backgroundColor","#F7F7F7");
})
$(".loginin").eq(0).click(function(){
	$(".main1").css("display","none");
	$(".main2").css("display","block");
	$(".main3").css("display","none");
	$(".in").css("backgroundColor","#F7F7F7");
	$(".loginin").css("backgroundColor","white");
})
$(".forget").eq(0).click(function(){
	$(".main1").css("display","none");
	$(".main3").css("display","block")
})