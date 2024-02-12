$(function () {

    var reciever_id = $('.meta').first().attr('id');
    var chat_elm = $('#msg-list');
    // var request_counter = 1;
    var scrolling = false;
    var chatlist = document.getElementsByClassName('messages');
    $(".messages").scrollTop($('.messages')[0].scrollHeight);
    // $(".messages").animate({scrollTop: $(document).height()}, "fast");


    $('.meta').on('click', function () {

        reciever_id = $(this).attr('id');
        getChatMsgs(reciever_id);
        $(".messages").scrollTop($('.messages')[0].scrollHeight);
        // chatlist.scrollTop = $(document).height()
        // chatlist.scrollTop = chatlist.scrollHeight;


        // console.log(reciever_id)

    })
    // var chatlist = document.getElementById('msg-list');
    //                 chatlist.scrollTop = chatlist.scrollHeight;
    // $("#messages").scrollTop($("#messages")[0].scrollHeight);


    setInterval(function () {
        getChatMsgs(reciever_id);

    }, 5000);

    // console.log('was here')


    function getChatMsgs(rid) {

        // let chat_elm = $('#msg-list');

        // if (!scrolling) {


        if (reciever_id == 4) {


            // console.log("inside receiver id")
            $.get('/chatbot/getMessages/', {'reciever_id': rid})
                .then(function (data) {
                    // console.log("printing message list")
                    chat_elm.html('')
                    // console.log(data['message_list'])
                    let msg_class
                    for (i = 0; i < data['message_list'].length; i++) {
                        if (data['message_list'][i].sender_id == $('#logged_in_user_id').val()) {
                            msg_class = 'sent';
                        } else {
                            msg_class = 'replies';
                        }


                        // console.log('IDHAR MSG AYAI GA')

                        if (data['message_list'][i].message.indexOf("song_request") >= 0) {
                            // console.log(data['message_list'][i].message.indexOf("song_request"));
                            // console.log(data['message_list'][i].message.split(",")[1]);
                            var singer = data['message_list'][i].message.split(",")[1];

                            let music_url = "https://soundcloud.com/search?q=" + data['message_list'][i].message.split(",")[1];
                            // <a href="${music_url}" target="_blank">Music URL</a>
                            chat_elm.append('<li class="' + msg_class + '"><p><a href="' + music_url + '" target="_blank">Click Here For ' + singer + ' Music</a></p></li>')


                            // console.log('music check working');
                        } else if (data['message_list'][i].message.indexOf("event_request") >= 0) {

                            var event_string = data['message_list'][i].message.split("æ")[1];


                            // console.log(event_string)
                            let events_List = JSON.parse(event_string)
                            $.each(events_List, function (index, value) {
                                // console.log(index, value.name)

                                var description = value.description.text
                                var desc = description.substring(0, 20)

                                chat_elm.append('<li class="' + msg_class + '"> <div class="card" style="margin-left: 375px;">\n' +
                                    '  <img src="' + value.logo.url + '" alt="Avatar" style="width:230px;border-radius: 0px !important;">\n' +
                                    '  <div class="container" >\n' +
                                    '    <h4><b>' + value.name.text + '</b></h4>\n' +
                                    '    <p>' + desc + '</p>\n' +
                                    '     <a href="' + value.url + '" target="_blank">Click Here</a>\n' +
                                    '  </div>\n' +
                                    '</div></li>')

                            });
                            // console.log(events_List[0]['name']['text'])

                        } else if (data['message_list'][i].message_audio == 'empty') {
                            // if (data['message_list'][i].message_audio != 'empty') {
                            //     chat_elm.append('<li class="' + msg_class + '"><audio controls> <source src="http://127.0.0.1:8000/media/' + data['message_list'][i].message_audio + '" ' +
                            //         'type="audio/mpeg" ></audio><p>' + data['message_list'][i].message + '</p></li>')
                            //
                            //
                            // }
                            chat_elm.append('<li class="' + msg_class + '"><p>' + data['message_list'][i].message + '</p></li>')

                            // else{

                            //
                            // }
                            // chat_elm.append('<li class="' + msg_class + '"><audio> <source src="' +data['message_list'][i].message_audio + '" ></audio><p>' + data['message_list'][i].message + '</p></li>')

                        } else if (data['message_list'][i].message_audio != 'empty') {

                            chat_elm.append('<li class="' + msg_class + '"><audio controls> <source src="http://127.0.0.1:8000/media/' + data['message_list'][i].message_audio + '" ' +
                                'type="audio/mpeg" ></audio><p>' + data['message_list'][i].message + '</p></li>')
                        }


                    }

                    chatlist.scrollTop = chatlist.scrollHeight;

                })
            scrolling = false;
        } else {
            $.get('/chatbox/getMessages/', {'reciever_id': rid})
                .then(function (data) {
                    // console.log(data['message_list'])
                    let msg_class
                    chat_elm.html('')
                    for (let i = 0; i < data['message_list'].length; i++) {
                        if (data['message_list'][i].sender_id == $('#logged_in_user_id').val()) {
                            msg_class = 'sent';
                        } else {
                            msg_class = 'replies';
                        }
                        chat_elm.append('<li class="' + msg_class + '"><p>' + data['message_list'][i].sender_id + '</p><p>' + data['message_list'][i].message + '</p></li>')

                    }

                    chatlist.scrollTop = chatlist.scrollHeight;

                })
        }

        // }
        // scrolling condition end

        scrolling = false;
    }


    // $('.messages').scroll(function () {
    //     console.log('scrolling my dude')
    //     scrolling = true
    //     refreshTimer = setInterval(getChatMsgs(reciever_id), 500)
    //
    // })

    $('.messages').on('scroll', function () {
        scrolling = true;
    });
    refreshTimer = setInterval(getChatMsgs(reciever_id), 500)


    $('#chat-form').on('submit', (e) => {
        e.preventDefault();

        let msg = $('#chat-msg').val();
        $('#chat-msg').val('');
        let sender_id = $('#logged_in_user_id').val();

        let ajax_url
        if (reciever_id == 4) {
            ajax_url = '/chatbot/send_message/';
        } else {
            ajax_url = '/chatbox/saveMessage/';
        }

        let data_to_send = {
            'msg': msg,
            'sender': sender_id,
            'reciever': reciever_id
        };


        // if (reciever_id == 4) {
        //     let data_to_send = {
        //         'msg': msg,
        //         'sender': sender_id,
        //         'reciever': reciever_id
        //     };
        // } else {
        //     let data_to_send = {
        //         'msg': msg,
        //         'sender': sender_id,
        //         'reciever': reciever_id
        //     };
        // }


        $.post(ajax_url, data_to_send)
            .then((data) => {
                // console.log(data);
                // getChatMsgs(reciever_id)
                // $(".messages").scrollTop($('.messages')[0].scrollHeight);


            })
            .fail((err) => {
                console.log(err);
            });

    });


    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})


