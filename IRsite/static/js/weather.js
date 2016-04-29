if("geolocation" in navigator){
	navigator.geolocation.getCurrentPosition(function(position){
		loadWeather(position.coords.latitude + ',' + position.coords.longitude);
	});
} else {
	loadWeather("Delhi, IN", "");
}

$(document).ready(function() {
	setInterval(getWeather, 10000);
});

function loadWeather(location, woeid) {
	console.log("a");
	$.simpleWeather({
		location: location,
		woeid: woeid,
		unit: 'c',
		sucess: function(weather) {
			city = weather.city;
			temp = weather.temp+'&deg';
			wcode = '<img class="weathericon" src="images/weathericons/' + weather.code + '.svg">';
			wind = '<p>' + weather.wind.speed + '</p><p>' + weather.units.speed + '</p>';
			humidity = weather.humidity + ' %';
			console.log("b");
			$(".location").text(city);
			$(".tempreture").html(temp);
			$(".climate_bg").html(wcode);
			$(".windspeed").html(wind);
			$(".humidity").text(humidity);

			// console.log("reached here");
			console.log(city);
			console.log(temp);

		},
		error: function(error) {
			$(".error").html('<p>' + error + '</p>');

		}
	});
}