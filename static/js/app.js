$(function () {
    //index geolocation form
    $("#search_location").geocomplete();

    //add poit geolocation form
    $("#address").geocomplete({
        map: "#add_point_map",
        details: "form"
    });
})


//Marker window click
function bindInfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
  });
}


//AJAX function to load map points
//TODO: Change it to jQuery - Sorry puritans :)
function downloadUrl(url,callback) {
 var request = window.ActiveXObject ?
     new ActiveXObject('Microsoft.XMLHTTP') :
     new XMLHttpRequest;

 request.onreadystatechange = function() {
   if (request.readyState == 4) {
     request.onreadystatechange = doNothing;
     callback(request, request.status);
   }
 };

 request.open('GET', url, true);
 request.send(null);
}

function doNothing() {}
