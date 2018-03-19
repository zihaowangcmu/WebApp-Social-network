function getList() {
    $.ajax({
        url: "/socialnetwork/get_list_json",
        dataType : "json",
        success: function(items) {
            update_post_list(items);
            update_comment_list(items);
            update_following_List(items);
        }
    });
}

function update_comment_list(items) {
    var comments = JSON.parse(items['comments']);
    // console.log(pk_comment);
    var updated_pk_comment = comments.length-1;
    // console.log(updated_pk_comment);
    // console.log("#########################");
    for (var i = pk_comment; i <= updated_pk_comment; ++i)
    {
        this_comment = comments[i];
        $(".comments_for_post_"+this_comment.fields.post).append(
            "<li class='comment_bullet'>" + 
            sanitize(this_comment.fields.content) + "<br/>" + 
            "By" + "\xa0\xa0\xa0\xa0\xa0" + ":" +
            "<a href=\'/socialnetwork/someone_profile?created_by=" + 
            sanitize(this_comment.fields.created_by_username) + "\'>" + 
            sanitize(this_comment.fields.created_by_username) + "<br/>" + "</a>" +
            "When:" + this_comment.fields.creation_time + "</li>"
        );
    }
    pk_comment = updated_pk_comment + 1;
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function addItem(postID) {
    var itemTextElement = $("#item."+postID);
    var itemTextValue   = itemTextElement.val();
    var last_update_time = new Date().getTime()/1000;

    // Clear input box and old error message (if any)
    itemTextElement.val('');
    displayError('');

    // data-->url-->success
    $.ajax({
        url: "/socialnetwork/add_comment",
        type: "POST",
        data: { this_post:           itemTextValue, 
                current_post_id:     postID,
                last_update_time:    last_update_time,
                csrfmiddlewaretoken: getCSRFToken() },
        dataType : "json",
        success: function(response) {
            if ('error' in response){
                displayError(response.error);
            } else {
                update_comment_list(response);
            }
        }
    });
}

function update_post_list(items) {
    var posts = JSON.parse(items['posts']);
    var comments = JSON.parse(items['comments']);
    var updated_pk_post = posts.length-1;
    for (var i = pk_post; i <= updated_pk_post; ++i)
    {
        this_post = posts[i];
        // console.log(this_post);
        $(".poster").prepend(
            "<div class='poster_bullet'>" + "Publisher:" + 
            "<a href=\'/socialnetwork/someone_profile?created_by=" + 
            sanitize(this_post.fields.created_by_username) + 
            "\'>" + sanitize(this_post.fields.created_by_username) + "<br/></a>" +  
            "Contents:" + sanitize(this_post.fields.content) + "<br/>" + 
            "Published Time:" + sanitize(this_post.fields.creation_time) + 
            "<br/>" + "<div>" + "<label>Comments:</label>" + 
            "<input id='item' type='text' name='item' class='" + 
            sanitize(this_post.fields.created_by_identity) + "'>" + 
            "<button onclick=\"addItem(\'" + 
            sanitize(this_post.fields.created_by_identity) + "\')\">Add item</button>" + 
            "<span id=\"error\" class=\"error\"></span>" + 
            "</div>" + "<ol class=\"comments_for_post_" + 
            sanitize(this_post.fields.created_by_identity) + "\"></ol>" + 
            "</div>" 
        );
    }
    pk_post = updated_pk_post + 1;
}

function update_following_List(items) {
    console.log(items);
    var following_posts    = JSON.parse(items['following_posts']);
    var following_comments = JSON.parse(items['following_comments']);
    // console.log(following_comments);
    var updated_pk_following_post    = following_posts.length-1;
    var updated_pk_following_comment = following_comments.length-1;
    console.log(following_posts);
    console.log(pk_following_post);
    console.log(updated_pk_following_post);
    console.log("#########################");
    for (var i = pk_following_post; i <= updated_pk_following_post; ++i)
    {
        this_post = following_posts[i];
        console.log(this_post);
        console.log(this_post.fields.created_by_identity);
        $(".following_poster").prepend(
            "<div class='following_poster_bullet'>" + "Publisher:" + 
            "<a href=\'/socialnetwork/someone_profile?created_by=" + 
            sanitize(this_post.fields.created_by_username) + 
            "\'>" + sanitize(this_post.fields.created_by_username) + "<br/></a>" +  
            "Contents:" + sanitize(this_post.fields.content) + "<br/>" + 
            "Published Time:" + sanitize(this_post.fields.creation_time) + 
            "<br/>" + "<div>" + "<label>Comments:</label>" + 
            "<input id='item' type='text' name='item' class='" + 
            sanitize(this_post.fields.created_by_identity) + "'>" + 
            "<button onclick=\"addItem(\'" + 
            sanitize(this_post.fields.created_by_identity) + "\')\">Add item</button>" + 
            "<span id=\"error\" class=\"error\"></span>" + 
            "</div>" + "<ol class=\"comments_for_post_" + 
            sanitize(this_post.fields.created_by_identity) + "\"></ol>" + 
            "</div>"
        );
    }
    pk_following_post = updated_pk_following_post + 1;

    // for (var j = pk_following_comment; j <= updated_pk_following_comment; ++j)
    // {
    //     this_comment = following_comments[j];
    //     $(".comments_for_post_"+this_comment.fields.post).append(
    //         "<li class='comment_bullet'>" + 
    //         sanitize(this_comment.fields.content) + "<br/>" + 
    //         "By" + "\xa0\xa0\xa0\xa0\xa0" + ":" +
    //         "<a href=\'/socialnetwork/someone_profile?created_by=" + 
    //         sanitize(this_comment.fields.created_by_username) + "\'>" + 
    //         sanitize(this_comment.fields.created_by_username) + "<br/>" + "</a>" +
    //         "When:" + this_comment.fields.creation_time + "</li>"
    //     );
    // }
    // pk_following_comment = updated_pk_following_comment + 1;
}

window.onload = function(){
    getList();
    pk_post = 0;
    pk_comment = 0;
    pk_following_post = 0;
    pk_following_comment = 0;
}

// need pk here too!
window.setInterval(getList, 5000);