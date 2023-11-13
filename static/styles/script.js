// 
var settingmenu = document.querySelector(".setting_menu");

function settingsMenuToggle() {
    settingmenu.classList.toggle("setting_menu_height");
}

// 
const createPostButton = document.getElementById('create-post-button');
const popupContainer = document.getElementById('popup-container');
const closePopupButton = document.querySelector('.close-button');

createPostButton.addEventListener('click', () => {
    popupContainer.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
    popupContainer.style.display = 'none';
});

document.addEventListener('click', (event) => {
    if (event.target === popupContainer) {
        popupContainer.style.display = 'none';
    }
});


// 
$(document).ready(function(){
    let display=false
    $('.like-form').submit(function(e){
        e.preventDefault()

        const post_id = $(this).attr('id')

        const LikeText = $(`.like-btn${post_id}`).html()
        const trim =$.trim(LikeText)
        console.log(trim)

        const url = $(this).attr('action')

        let res;
        const like= $(`.like-count${post_id}`).text()
        const trimCount = parseInt(like)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id':post_id,
            },
            success: function(response){
                if (trim =='<i><ion-icon name="heart-dislike-outline" role="img" class="md hydrated"></ion-icon></i>'){
                    $(`.like-btn${post_id}`).html('<i><ion-icon name="heart-outline"></ion-icon></ion-icon></i>')
                    res =trimCount-1
                } else{
                    $(`.like-btn${post_id}`).html('<i><ion-icon name="heart-dislike-outline"></i>')
                    res =trimCount+1
                }
                const like= $(`.like-count${post_id}`).text(res)
            },
            error: function(response){
                console.log('error',response)
            }        
        })

    });
});