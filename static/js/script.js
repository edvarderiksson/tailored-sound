$("#more-options").click(function(event) {
    event.preventDefault();
    if ( $("#hidden-options").css("display") == "none"){
        $("#hidden-options").css("display", "block");
        $("#default-button").css("display", "none");
    }
    else {
        $("#hidden-options").css("display", "none");
        $("#default-button").css("display", "block");
    }
    
});

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