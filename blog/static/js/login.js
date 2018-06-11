//登录
$('.login-btn').click(function () {
    $.ajax({
        url:'',
        type:'post',
        data:{
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            user: $('#user').val(),
            pwd: $('#pwd').val(),
            valid_code: $('#valid_code').val()
        },
        success:function (data) {
            if(data.state){
                location.href = data.next_url
            }else{
                $('.error').text(data.msg)
            }
        }
    })
});

//验证码刷新
$('#valid_img').click(function () {
    $(this)[0].src += '?'
});
