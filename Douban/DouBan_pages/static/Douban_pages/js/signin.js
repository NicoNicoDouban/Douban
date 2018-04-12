
$(".in").eq(0).click(function(){
	/*$(".main1").css("display","block");
	$(".main2").css("display","none");*/
	var divID=0;

	$(".in").css("backgroundColor","white");
	$(".loginin").css("backgroundColor","#F7F7F7");
})
$(".loginin").eq(0).click(function(){
	/*$(".main1").css("display","none");
	$(".main2").css("display","block");
	$(".main3").css("display","none");*/

	$(".in").css("backgroundColor","#F7F7F7");
	$(".loginin").css("backgroundColor","white");
})
$(".forget").eq(0).click(function(){
	/*$(".main1").css("display","none");
	$(".main3").css("display","block")*/
	var divID = 2;

})
    $(function(){

        $('.captcha').click(function(){
        console.log('click');
         $.getJSON("/captcha/refresh/",
                  function(result){
             $('.captcha').attr('src', result['image_url']);
             $('#id_captcha_0').val(result['key'])
          });});

    $('#id_captcha_1').blur(function(){
  // #id_captcha_1为输入框的id，当该输入框失去焦点是触发函数
        json_data={
            'response':$('#id_captcha_1').val(), // 获取输入框和隐藏字段id_captcha_0的数值
            'hashkey':$('#id_captcha_0').val()
        }
        $.getJSON('/ajax_val', json_data, function(data){
 //ajax发送
            $('#captcha_status').remove()
            if(data['status']){ //status返回1为验证码正确， status返回0为验证码错误， 在输入框的后面写入提示信息
                $('#id_captcha_status').after('<span id="captcha_status" style="font-size: 14px;color: red;">验证码正确</span>')
            }else{
                 $('#id_captcha_status').after('<span id="captcha_status" style="font-size: 14px;color: red;">验证码错误</span>')
            }
        });
    });
    })