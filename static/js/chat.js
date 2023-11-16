const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log(e)
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `
        <tr>
        <td style="border-right: 1px solid black;">
            <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded" style="word-wrap: break-word; width: 300px;">
                ${data.message}
            </p>
        </td>
        </tr>`
    }
    else{
        document.querySelector('#chat-body').innerHTML += `
        <tr>
        <td style="border-right: 1px solid black;">
            <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded" style="word-wrap: break-word; width: 300px;">
                ${data.message}
            </p>
        </td>
        </tr>`
    }
}
// socket.onmessage = function(e){
//     const data = JSON.parse(e.data);
//     let messageText = data.message;
    
//     // Split the message into chunks of 40 characters each
//     const chunks = [];
//     while (messageText.length > 40) {
//         chunks.push(messageText.substr(0, 40));
//         messageText = messageText.substr(40);
//     }
//     chunks.push(messageText);
    
//     // Construct the HTML for each chunk
//     chunks.forEach(chunk => {
//         if (data.username === message_username) {
//             document.querySelector('#chat-body').innerHTML += `
//                 <tr>
//                     <td>
//                         <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
//                             ${chunk}
//                         </p>
//                     </td>
//                 </tr>`;
//         } else {
//             document.querySelector('#chat-body').innerHTML += `
//                 <tr>
//                     <td>
//                         <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
//                             ${chunk}
//                         </p>
//                     </td>
//                 </tr>`;
//         }
//     });
// }
document.querySelector('#message_input').addEventListener('keydown', function(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        const message_input = document.querySelector('#message_input');
        const message = message_input.value;
        if (message.trim() === ''){
            return false;
        }
        else {
            socket.send(JSON.stringify({
                'message': message,
                'username': message_username
            }));
        }
        message_input.value = '';
    }
});

document.querySelector('#chat-message-submit').onclick = function(e){

    const message_input = document.querySelector('#message_input');
    const message = message_input.value;
    // var chunks = [];
    // var currentIndex = 0;
    if (message.trim() === ''){
        return false
    }
    else{
        // if (message.length > 40) {    
        //     while (currentIndex < message.length) {
        //       chunks.push(message.substr(currentIndex, 40));
        //       currentIndex += 40;
        //     }      
        // }
        // message = chunks.join('\n');
        // console.log(message)
        socket.send(JSON.stringify({
            'message': message,
            'username': message_username
        }));
    }
    message_input.value = '';
}