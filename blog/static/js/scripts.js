$(document).ready(function(){

    //increments or decrements votes on list page
    voteChangeList();

    //increments and decrements votes on details page
    voteChangeDetail();

    //user adding suggestion
    addSuggestion();

    //checks search string
    checkQueryString();

    //gives details of poem
    giveDetail();

});


//allows users to add their own suggestions for a particular poem
function addSuggestion() {
    el = document.getElementById('add');
    if (el) {
        el.addEventListener("click", function () {
            // Get the input's content
            var input = document.getElementById('new-suggestion');
            var text = input.value;

            toAdd = $(`<div class = "suggestion">
        <a href = "#" class = "btn"><button type = "button" class = "upvote"> Upvote</button></a>
         <a href = "#" class = "btn"><button type = "button" class = "downvote"> Downvote</button></a>
        <div class = "votes">0</div>
        <p> ${text} </p>
        </div>`);

            var contentDiv = $(this).parent().siblings('div#suggestions'); //gets div for suggestions
            $(toAdd).appendTo(contentDiv);

            var msg = $('<p class="msg">Suggestion successfully added!</p>');
            $(msg).appendTo(contentDiv).fadeOut(3000, function () {
                this.remove();
            });
        });
    }
}


//allows users to check if a poem is popular or not by detecting a focus event
function giveDetail() {
    $("#all-poems").on('focus', "a", function (event) {
        event.preventDefault();
        var elem = $(this).parent().parent();  //get poem div
        var voteDiv = $(this).parent().siblings('div.votes'); //get votes
         var votesNum = parseInt( $(voteDiv).text() );
        if (votesNum <= 0) {
            var msg = $('<p class="msg">Help make this poem better!</p>');
            $(msg).appendTo(elem).fadeOut(3000, function () {
                this.remove();
            });
        } else {
            var msg = $('<p class = "msg"> This poem seems to be popular! </p>');
            $(msg).appendTo(elem).fadeOut(3000, function () {
            });
        }
    });
}


//parses the search query and displays results accordingly
function checkQueryString(){
    var querystring = window.location.search;
    console.log(querystring);
    var urlParams = new URLSearchParams(querystring);
    if (urlParams.has('search-poems')){
        var keyword = urlParams.get("search-poems");
        if (keyword == "bush pooper"){
            var result = $(`<h2 class = "poem-title"><a href = "Humor/3"> The Bush Pooper </a> </h2>
                <p class = "poem-description">There once was a man from Nantucket, <br> Who liked to poop in a bucket, <br> He ate a worm and saw a fern, <br> And thought to himself, <br> Screw it!</p>`)
            $("#search-results").append(result);

        } else{
            var result_text = "No results found for \""+ keyword + "\"";
            $("#search-results").append(result_text);

        }
    }

}



 //up vote and down vote button event handler on list page
function voteChangeList(){
    $("#all-poems").on('click', "a.btn", function (event) {
        event.preventDefault();
        var voteDiv = $(this).siblings('div.votes'); //get votes
         var votesNum = parseInt( $(voteDiv).text() );

         if ($(this).children().hasClass("upvote")){
             votesNum++;
              $(voteDiv).text(votesNum);
         }
         else if  ($(this).children().hasClass("downvote")){
             votesNum--;
              $(voteDiv).text(votesNum);
         }
     });
}


 //up vote and down vote button event handler on details page
function voteChangeDetail(){
     $("#suggestions").on('click', "a.btn",function (event) {
        event.preventDefault();
        var voteDiv = $(this).siblings('div.votes'); //get votes
         var votesNum = parseInt( $(voteDiv).text() );
         console.log(votesNum);

         if ($(this).children().hasClass("upvote")){
             votesNum++;
              $(voteDiv).text(votesNum);
         }
         else if  ($(this).children().hasClass("downvote")){
             votesNum--;
              $(voteDiv).text(votesNum);
         }
     });

}