var firebase = new Firebase("https://myirproject.firebaseio.com");
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 3,
    styles: [{
      featureType: 'poi',
      stylers: [{ visibility: 'on' }]  // Turn off points of interest.
    }, {
      featureType: 'transit.station',
      stylers: [{ visibility: 'on' }]  // Turn off bus stations, train stations, etc.
    }],
    disableDoubleClickZoom: true
  });
  map.addListener('click', function(e) {
    var marker = new google.maps.Marker({
      position: {lat: e.latLng.lat(), lng: e.latLng.lng()},
      map: map
    });
    firebase.push({lat: e.latLng.lat(), lng: e.latLng.lng()});
    var message = snapshot.val();
    var id = snapshot.key();
  });
}