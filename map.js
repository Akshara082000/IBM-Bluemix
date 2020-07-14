
var map=L.map('map').setView([22.910502,75.989501],5);
L.tileLayer("https://api.maptiler.com/maps/hybrid/256/{z}/{x}/{y}.jpg?key=Gb2ovo1WytzyxeUcRP7b",{
    /*attribution:'<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'*/
}).addTo(map);

L.marker([22.910502,75.989501],15).addTo(map)
    .bindPopup('Click on the states <br>of the country<br>to get accurate results.')
    .openPopup();

map.on('click', function(e) {
console.log("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng);
document.getElementById("lang").value=e.latlng.lng;
document.getElementById("lat").value=e.latlng.lat;
});




