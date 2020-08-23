
  $('.editTweet').click(function(e){
    var html = $(this).closest('div .new-post-container').find(".tweet-body p").html();

    $(this).closest('div .new-post-container').find(".tweet-body p").replaceWith('<textarea>'+html + '\r\n</textarea>').html();
    $(this).closest('div .new-post-container').find(".tweet-footer button").css("display", "block");
  });


  $('.tweet-footer button').click(function(e){
    var new_text = $(this).closest('div .new-post-container').find(".tweet-body textarea").val();

    $(this).closest('div .new-post-container').find(".tweet-body textarea").replaceWith('<p class="tweetComment">'+new_text + '\r\n</p>');
    $(this).closest('div .new-post-container').find(".tweet-footer button").css("display", "none");

    var tweet_id = $(this).closest('div .new-post-container').attr("id");

    $.ajax({
        url: '/edit/tweet',
        data: {'new_text': new_text, 'tweet_id': tweet_id},
        dataType: 'json',
        success: function (data) {
        }
    });
});



$('.like-button').click(function(e){

    var tweet_id = $(this).closest('div .new-post-container').attr("id");
    var the_heart = $(this);

    if($(this).hasClass("is-liked")){
        unlikeTweet(tweet_id, the_heart);
    }else{
        
        $.ajax({
            url: '/like/tweet',
            data: {'tweet_id': tweet_id},
            dataType: 'json',
            success: function (data) {
                the_heart.addClass("is-liked");
                var likes = the_heart.closest(".tweet-footer").find(".likes-number").html();
                new_likes = likes + 1;
                the_heart.closest(".tweet-footer").find(".likes-number").empty();
                the_heart.closest(".tweet-footer").find(".likes-number").html(new_likes);
            }
        });
    }    
});



$('.is-liked').click(function(e){

    var tweet_id = $(this).closest('div .new-post-container').attr("id");
    var the_heart = $(this);

    unlikeTweet(tweet_id, the_heart);

});


function unlikeTweet(tweet_id, the_heart){

    console.log(tweet_id);

    $.ajax({
        url: '/unlike/tweet',
        data: {'tweet_id': tweet_id},
        dataType: 'json',
        success: function (data) {
            the_heart.removeClass("is-liked");
            var likes = the_heart.closest(".tweet-footer").find(".likes-number").html();
            new_likes = likes - 1;
            the_heart.closest(".tweet-footer").find(".likes-number").html(new_likes);

        }
    });
}
