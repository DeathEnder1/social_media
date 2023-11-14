$(document).ready(function() {
    $('#comment-form').submit(function(e) {
        e.preventDefault();
        const post_id = $(this).attr('id')
        const formData = $(this).serialize();
        $.ajax({
            url: '/', 
            type: 'POST',
            data: ({
                formData,
                'post_id':post_id,
            }),
            success: function(response) {
                $('#comment-form input[name=body]').val(''); 

                $('#comments-list').append(
                    '<p> ${comment.user}: ${comment.body} </p>'
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});