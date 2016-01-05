$(function () {
    //index geolocation form
    $("#search_location").geocomplete({
        details: "form",
    });

    //search address
    $("button.find").click(function(){
      map.setCenter(new google.maps.LatLng( $("#find_lat").val(), $("#find_lng").val()));
      map.setZoom(16);
    });


    //add poit geolocation form
    $("#address").geocomplete({
        map: "#add_point_map",
        details: "form",
        location: [-30.037057, -51.219492],
        markerOptions: {
          draggable: false,
        }
    });

    //edit poit geolocation form
    $("#new_address").geocomplete({
        map: "#edit_point_map",
        details: "form",
        location: edit_address,
        markerOptions: {
          draggable: false,
        }
    });

})


//Marker window click
function bindInfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
    map.setCenter(marker.getPosition());
    $(".btn-map").css("margin-top","-10px");
    $(".form-map").css("margin-top","160px");
  });

  google.maps.event.addListener(infoWindow,'closeclick',function(){
      $(".btn-map").css("margin-top","0px");
      $(".form-map").css("margin-top","0px");
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
