$(document).ready(function(){

    //increments or decrements votes on list page
    voteChangeList();

    //increments and decrements votes on details page
    voteChangeDetail();

    // //user adding suggestion
     addSuggestion();

    // //checks search string
    checkQueryString();
    //
    //gives details of poem
    giveDetail();

    //shows detail of poem
    showPoem();

});


//allows users to add their own suggestions for a particular poem
function addSuggestion() {

    $("#content #suggestion-form #cancel").click(function() {
        $("#suggestion-form")[0].reset();
    });

    $("#content #suggestion-form #add").click(function() {
        var poem_id = $(this).attr('data-poem-id');
        var ajax_url = $(this).attr('data-ajax-url');
        var form_data = JSON.stringify($('form').serialize());
        var suggestion;

         var urlParams = new URLSearchParams(form_data);
         if (urlParams.has('new-suggestion')){
             suggestion = urlParams.get("new-suggestion");
             suggestion = suggestion.slice(0, -1);
         }

        // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                poem_id: poem_id,
                suggestion: suggestion,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:  {'X-CSRFToken': csrftoken},

            context: this


        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {


              toAdd = $(`<div class = "suggestion">
                         <a href = "#" class = "btn"><button type = "button" class = "upvote"> Upvote</button></a>
                        <a href = "#" class = "btn"><button type = "button" class = "downvote"> Downvote</button></a>
                        <div class = "votes">0</div>
                        <p> ${json.suggestion} </p>
                        </div>`);

              var contentDiv = $(this).parent().siblings('div#suggestions'); //gets div for suggestions
              $(toAdd).appendTo(contentDiv);

              var msg = $('<p class="msg">Suggestion successfully added!</p>');
              $(msg).appendTo(contentDiv).fadeOut(3000, function () {
                  this.remove();
            });
              $("#suggestion-form")[0].reset();

          })
          // Code to run if the request fails;
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
        });
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

// allows users to view entire poem by hovering over it

function showPoem(){
    $("#all-poems .poem .show-poem").click(function() {
        var poem_id = $(this).attr('data-poem-id');
        var ajax_url = $(this).attr('data-ajax-url');

        // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                poem_id: poem_id,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:  {'X-CSRFToken': csrftoken},

            context: this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              var details = json.details;
              details = details;
              targetDiv = $(this).siblings('p.poem-description');
              var obj = $(targetDiv).text(details);
              obj.html(obj.html().replace(/\n/g,'<br/>'));
          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
          });


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
     $("#all-poems a button").click(function() {

         var poem_id = $(this).attr('data-poem-id');
         var action = $(this).attr('data-action');
         var ajax_url = $(this).attr('data-ajax-url');

         // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                poem_id: poem_id,
                action: action,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:  {'X-CSRFToken': csrftoken},

            context: this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              var voteDiv = $(this).parent().siblings('div.votes'); //get votes
              if (json.success == 'success'){
                  var newScore = json.score;
                  $(voteDiv).text(newScore);
              }
              else{
                  alert("Error: "+ json.error);
              }


          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
          });


     });
}


 //up vote and down vote button event handler on details page
function voteChangeDetail(){
      $("#suggestions a button").click(function() {
          // var poem_id = $(this).attr('data-poem-id');
          var suggestion_id = $(this).attr('data-suggestion-id');
          var action = $(this).attr('data-action');
          var ajax_url = $(this).attr('data-ajax-url');

         // Using the core $.ajax() method
          $.ajax({

          // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
               // poem_id: poem_id,
                suggestion_id: suggestion_id,
                action: action,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:  {'X-CSRFToken': csrftoken},

            context: this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              var voteDiv = $(this).parent().siblings('div.votes'); //get votes
              if (json.success == 'success'){
                  var newScore = json.score;
                  $(voteDiv).text(newScore);
              }
              else{
                  alert("Error: "+ json.error);
              }


          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
          });
     });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');