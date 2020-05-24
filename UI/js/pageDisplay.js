$(document).ready(function() {
    "use strict";
    $('ul.navbar-nav > li').click(function(e) {
        $('ul.navbar-nav > li').removeClass('active');
        $(this).addClass('active');
    });
    $(".nicebox").hide();
    $("#legend").hide();
    $("#map").hide();
    $("#barCard").hide();
    $("#scatterCard").hide();
    $("#mapButton").click(function(e) {
        $("#info").hide();
        $("#legend").show();
        $(".nicebox").show();
        $("#map").show();
        $("#barCard").hide();
        $("#scatterCard").hide();
    });
    $("#aboutButton").click(function(e) {
        $("#legend").hide();
        $(".nicebox").hide();
        $("#map").hide();
        $("#info").show();
        $("#barCard").hide();
        $("#scatterCard").hide();
    });
    $("#barButton").click(function(e) {
        $("#legend").hide();
        $(".nicebox").hide();
        $("#map").hide();
        $("#info").hide();
        $("#barCard").show();
        $("#scatterCard").hide();
    });
    $("#scatterButton").click(function(e) {
        $("#legend").hide();
        $(".nicebox").hide();
        $("#map").hide();
        $("#info").hide();
        $("#barCard").hide();
        $("#scatterCard").show();
    });

    //Create table from datastream
    var id=0;
    (function worker() {
        $.ajax({
            url: 'dummy_stream.json', 
            success: function(data) {
              var table = '<table border="1" id="tweetData"><thead><tr><th style="padding: 6px; text-align: center">Tweet</th></tr></thead><tbody>';
              for(var i = id; i<data.rows.length; i++){
                table+='<tr><td style="padding: 6px;">';
                table+=data.rows[i].value;
                table+='</td></tr>';
            }
            table+='</tbody></table>';
            $("#dataStream").html(table);
            },
            complete: function() {
              // Schedule the next request when the current one's complete
              setTimeout(worker, 10000);
            }
          });
        })();
});