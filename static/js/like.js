$(document).ready(function(){
    let display=false
    $('.like-form').submit(function(e){
        e.preventDefault()

        const post_id = $(this).attr('id')
        
        const LikeText = $(`.like-btn${post_id}`).text()
        const trim =$.trim(LikeText)

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
                console.log('good')
                if (trim ==='Unlike'){
                    $(`.like-btn${post_id}`).text('Like')
                    res =trimCount-1
                } else{
                    $(`.like-btn${post_id}`).text('Unlike')
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