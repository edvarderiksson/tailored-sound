
/*$(function () {
    $('body').show();
}); */

/*var img = new Image();
    img.src = '/static/images/trees.png';

var int = setInterval(function() {
    if (img.complete) {
        clearInterval(int);
        document.getElementsByTagName('body')[0].style.backgroundImage = 'url(' + img.src + ')';
    }
}, 50);*/

function loading(){
            console.log("hello");
            $("#loading").show();
            $("#content").hide();       
}

$("iframe").hide();
$("iframe").ready(function() {
    $("iframe").show();
});


$(function() {
    $('body').hide();
    $('body').ready(function() { 
        $('body').show();
        //alert('ready');        
    });
});
/*
$('#mood').each(function() {
    if(this.selected) {
        $("#hidden-options").hide();
    }

});*/

//console.log($('#default-dropdown').val());

//console.log($("#default-dropdown option:selected").html());

$("#default-dropdown ").change(showDropdown);

function showDropdown() {
    var choice = $("#default-dropdown option:selected").html();    
    console.log(choice);
    
    if (choice == "Mood"){
        $("#hidden-options").css("display", "none");
        $("#default-button").css("display", "block");
        $("#search").css("border-radius", 0);
    }
    else {
        $("#hidden-options").css("display", "block");
        $("#default-button").css("display", "none");
        $("#search").css("border-radius", 4);
    }

}



/*if ($('#mood').selected) {
    console.log("mood");
    $("#hidden-options").css("display", "none");
    


}

if ($('#word').selected) {
    console.log("word");
    $("#hidden-options").css("display", "block");
    


}*/




/*$("#more-options").click(function(event) {
    event.preventDefault();
    if($("#more-options").text() == "More options"){
        $("#more-options").text("Fewer options");
    }
    else {
        $("#more-options").text("More options");
    }
    if ( $("#hidden-options").css("display") == "none"){
        $("#hidden-options").css("display", "block");
        $("#default-button").css("display", "none");
        console.log($("#more-options").text());
    }
    else {
        $("#hidden-options").css("display", "none");
        $("#default-button").css("display", "block");
        $("a#more-options").text("More options");
    }
    
});*/

/*$("#unchosen-dropdown").click(function(event) {
    event.preventDefault();
    var unchosen = $("#unchosen-dropdown").text();
    var def = $("#default-dropdown").text();
    $("#default-dropdown").text(unchosen);
    $("#unchosen-dropdown").text(def);
});*/

/*$("#unchosen-dropdown").click(function(event) {
    event.preventDefault();
    var unchosen = $("#unchosen-dropdown").value();
    var def = $("#default-dropdown").value();
    $("#default-dropdown").value(unchosen);
    $("#unchosen-dropdown").value(def);
});*/

