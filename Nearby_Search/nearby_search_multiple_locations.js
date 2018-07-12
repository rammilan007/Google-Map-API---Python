// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
////--- FINAL WORKING CODE FOR MULTIPLE LOCATIONS---------------------
var map;
var infowindow;
var name_list=[];
var cd_list=[];
var list_latlng=[{lat: 18.536091, lng: 73.896983},{lat: 18.6530366, lng: 73.7824141},{lat :28.4322217 , lng : 77.03476320000004}]

function initMap() {
  var pyrmont ={lat: 18.536091, lng: 73.896983};
  map = new google.maps.Map(document.getElementById('map'), {
    center: pyrmont,
    zoom: 15
  });

  infowindow = new google.maps.InfoWindow();
  var service = new google.maps.places.PlacesService(map);
  for(var i=0;i<list_latlng.length;i++){
  	service.nearbySearch({
    	location: list_latlng[i],
    	radius: 500,
    	type: ['lodging']
  		}, callback);
  }
}

function callback(results, status) {

  if (status === google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      createMarker(results[i]);
/*       var obj = [
             results[i].name,
      results[i].geometry.location.lat(),
      results[i].geometry.location.lng()
      ] */
    //  name_list.push(results[i].name);
      cd_list.push( [
     	results[i].name,
      results[i].geometry.location.lat(),
      results[i].geometry.location.lng()
      ]);
    }
    
  }
      var csvContent = "data:text/csv;charset=utf-8,";

 	let rows=cd_list;
      rows.forEach(function(rowArray){
     let row = rowArray.join(",");
   csvContent += rowArray + "\r\n";
   
   });
   
  /*  cd_list.forEach(function(obj){
     let row = obj.latitude +","+ obj.longitude +","+ obj.name;
    csvContent += row +"\r\n"
   });
    */

var encodedUri = encodeURI(csvContent);
var link = document.createElement("a");
link.setAttribute("href", encodedUri);
link.setAttribute("download", "my_data.csv");
link.innerHTML= "Click Here to download";
document.body.appendChild(link); // Required for FF

link.click(); // This will download the data file named "my_data.csv".
}

function createMarker(place) {
  var placeLoc = place.geometry.location;
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(place.name);
    infowindow.open(map, this);
  });
}