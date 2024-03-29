function submit_message(message) {
        $.post( "/send_message/", {message: message}, handle_response);

        function handle_response(data) {
          // append the bot repsonse to the div

            console.log(data['message'][0].indexOf("song_request"))

            if (data['message'][0].indexOf("song_request") >= 0){
                console.log(data["message"][0].split(",")[1] )
                let music_url ="https://soundcloud.com/search?q="+data["message"][0].split(",")[1];
                  $('.chat-container').append(`

                
                <div class="chat-message col-md-5 offset-md-7 bot-message">
  
                    <a href="${music_url}" target="_blank">Music URL</a> 
                   
                </div>
                
          `)
                // remove the loading indicator
                $("#loading").remove();
            }

            else {

                for (i = 0; i < data.message.length; i++) {
                    $('.chat-container').append(`

                
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                
                    
                    ${data.message[i]} 
                   
                </div>
                
          `)
                    // remove the loading indicator
                    $("#loading").remove();
                }
            }
        }
    }






$('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        // return if the user does not enter any text
        if (!input_message) {
          return
        }
        $('.chat-container').append(`
            <div class="chat-message col-md-5 human-message">
                ${input_message}
            </div>
        `)

        // loading
        $('.chat-container').append(`
            <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
                <b>...</b>
            </div>
        `)

        // clear the text input
        $('#input_message').val('')

        // send the message
        submit_message(input_message)
    });