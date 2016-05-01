function initMap() {
        var myLatLng = {lat: 28.550100, lng: 77.249100};

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 18,
          center: myLatLng
        });

        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: 'Eros Hotel Managedaby Hilton'
        });
      }