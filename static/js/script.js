/* script file for tailored-sound */


// handling for displaying load bar

function loading(){
            console.log("hello");
            $("#loading").show();
            $("#content").hide();       
}

$("iframe").hide();
$("iframe").ready(function() {
    $("iframe").show();
});



// attempt at loading page only when all elements ready
// intended to produce cleaner image loading

$(function() {
    $('body').hide();
    $('body').ready(function() { 
        $('body').show();       
    });
});



// handling for dropdown menu

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


