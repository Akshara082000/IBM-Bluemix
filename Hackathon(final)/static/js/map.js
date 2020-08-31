
var map=L.map('map').setView([22.910502,75.989501],5);
L.tileLayer("https://api.maptiler.com/maps/hybrid/256/{z}/{x}/{y}.jpg?key=Gb2ovo1WytzyxeUcRP7b",{
    /*attribution:'<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'*/
}).addTo(map);

L.marker([22.910502,75.989501],15).addTo(map)
    .bindPopup('Click on the states <br>of the country<br>to get accurate results.')
    .openPopup();

map.on('click', function(e) {
    $.ajax({ url:'https://www.mapquestapi.com/geocoding/v1/reverse?key=cJ7E9WnLGHbfVncS0U3InQGKRAESPRyA&location='+e.latlng.lat+','+e.latlng.lng+'&outFormat=json&thumbMaps=false',
    success: function(data){
        var state = data.results[0].locations[0].adminArea3;
        var country=data.results[0].locations[0].adminArea1;
        console.log(state+","+country);
    document.getElementById("lang").value=e.latlng.lng;
    document.getElementById("lat").value=e.latlng.lat;
    document.getElementById("Country").value=state+","+country;
    }
    });


});


/*$.ajax({ url:'https://maps.googleapis.com/maps/api/geocode/json?latlng='+e.latlng.lat+','+e.latlng.lng+'&key=AIzaSyCGjarWOlgZdwQKqRMkd65-Y8EJ1XH4uM0',
success: function(data){
   
    console.log(data);
    
document.getElementById("lang").value=e.latlng.lng;
document.getElementById("lat").value=e.latlng.lat;
document.getElementById("Country").value=state;
}



*/