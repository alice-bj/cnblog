// 点赞 踩灭
$('#div_digg .digg').click(function () {

    var username = $('#hid_username').val();
    if(username){
        var is_up = $(this).hasClass('diggit');
        var article_id = $('#hid_article_pk').val();
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url:'/blog/poll/',
            type:'post',
            data:{
                is_up:is_up,
                article_id:article_id,
                csrfmiddlewaretoken:csrfmiddlewaretoken
            },
            success:function (data) {
                if(data.state){
                    // 赞或者灭 成功
                    if(is_up){
                        var val = parseInt($('#digg_count').text())+1;
                        $('#digg_count').text(val)

                    }else{
                        var val = parseInt($('#bury_count').text())+1;
                        $('#bury_count').text(val)
                    }

                }else{
                    // 重复操作 失败
                    if(data.first_operate){
                        $('#digg_word').html('您已经推荐过').css({"color":"red","margin-right":"26px",'margin-top':"10px"})
                    }else{
                        $('#digg_word').html('您已经反对过').css({"color":"red","margin-right":"26px",'margin-top':"10px"})
                    }
                }
            }
        })
    }else{
        location.href = '/login/'
    }

});


//评论 提交评论事件
var pid = '';  // 空为根评论

$('.comment-btn').click(function () {
    var username = $('#hid_username').val();
    if(username){  // 登录 后操作
        var article_id = $('#hid_article_pk').val();

        if($('#comment-text').val()[0] !== "@"){
            pid = ""
        }

        //@alex\n567
        // 获取子评论内容
        if(pid){
            var index = $('#comment-text').val().indexOf('\n');
            var content = $('#comment-text').val().slice(index+1)
        }else{
            var content = $('#comment-text').val();
        }

        $.ajax({
            url:'/blog/comment/',
            type:'post',
            data:{
                article_id:article_id,
                content:content,
                pid:pid,
                csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
            },
            success:function (data) {
                if(data.state){  // 提交成功
                    // 根评论 显示
                    var floor = $('.comment_list .comment_item').length+1;
                    var ctime = data.time;
                    var username = $('#hid_username').val();
                    var content =  data.content;
                    var pname = data.pidname;
                    if(data.pid){  // 子评论
                        var s ='<li class="list-group-item comment_item"><div><a href="">#'+floor+'楼</a>&nbsp;&nbsp;&nbsp; ' +
                            '<span>'+ ctime+ ' </span>&nbsp;&nbsp;<a href="">'+ username +'</a> </div> <div> ' +
                            ' <div class="parent_comment_info well">\n' +
                            ' <a href="">@'+pname+'</a>&nbsp;&nbsp;\n' +
                            ' </div><p>'+content+'</p> </div> </li>';
                    }else{
                        // 应该有 2 套 s
                        var s ='<li class="list-group-item comment_item"><div><a href="">#'+floor+'楼</a>&nbsp;&nbsp;&nbsp; ' +
                            '<span>'+ ctime+ ' </span>&nbsp;&nbsp;<a href="">'+ username +'</a> </div> <div> <p>'+content+'</p> </div> </li>';
                    }

                    $('.comment_list').append(s);

                    //清空数据
                    $('#comment-text').val("");
                    //清空pid
                    pid = "";
                }
            }
        })

    }else{  // 未登录
        location.href = "/login/"
    }
});

// 绑定回复 按钮事件
$('.comment_item .replay').click(function () {
    // 获取焦点
    $('#comment-text').focus();
    var val ="@" + $(this).attr('username')+ '\n';  // 回复得人得名字
    $('#comment-text').val(val);

    pid = $(this).attr("pk")
});
