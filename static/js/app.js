$(function () {
    //index geolocation form
    $("#search_location").geocomplete();

    //add poit geolocation form
    $("#address").geocomplete({
        map: "#add_point_map",
        details: "form"
    });



})