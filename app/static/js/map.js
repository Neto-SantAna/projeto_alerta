/* Function to generate base for occurrences map
Source: https://www.w3schools.com/graphics/google_maps_intro.asp */
function myMap() {

    // Set properties for map object
    var mapProp = {
        center: new google.maps.LatLng(-8.0231617, -34.8732721),
        zoom: 11,
        mapTypeControl: false,
        streetViewControl: false
    };

    // Add map to related div
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    // Initialize variables for map contents
    var marker, position, icon, content, infowindow, pos;

    // Retrieve variable from html
    var occur = appConfig.occurrences;

    // Check user position and center map on it
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
            map.setZoom(16);

            occur.forEach(function(arrayItem) {
                // Check user position in relation to risk areas
                var dla = Math.abs((arrayItem.latitude - pos.lat) * 60 * 1852);
                var dlo = Math.abs((arrayItem.longitude - pos.lng) * 60 * 1852);
                var distance = Math.sqrt(Math.pow(dla, 2) + Math.pow(dlo, 2));

                if (distance < 100) {
                    // Check weather condition
                    var c = document.getElementById("condition").innerHTML;
                    if (c == 'Tempestade' || c == 'Chuvoso') {
                        // Alert user that is in a risk area and is raining
                        alert("Você está próximo a uma área de risco " + arrayItem.risk);
                    }
                }
            });
        });
    }

    // Iterate over selections from database
    occur.forEach(function(arrayItem) {
        // Set marker position
        position = new google.maps.LatLng(arrayItem.latitude, arrayItem.longitude);

        // Evaluate risk for marker design
        switch (arrayItem.risk) {
            case 'R1 Baixo':
                icon = 'green.png';
                break;
            case 'R2 Médio':
                icon = 'yellow.png';
                break;
            case 'R3 Alto':
                icon = 'orange.png';
                break;
            default:
                icon = 'red.png';
        }

        // Set the content of infowindow for each marker
        content = '<ul>' +
            '<li>Processo: ' + arrayItem.process + '</li>' +
            '<li>Risco: ' + arrayItem.risk + '</li>' +
            '<li>Lona: ' + arrayItem.lona + 'm</li>' +
            '<li>Latitude: ' + arrayItem.latitude + '</li>' +
            '<li>Longitude: ' + arrayItem.longitude + '</li>' +
            '</ul>';

        infowindow = new google.maps.InfoWindow({
            content: content
        });

        // Add marker to map
        marker = new google.maps.Marker({
            position: position,
            map: map,
            icon: '/static/images/' + icon,
            infowindow: infowindow
        });

        // Set center of the map to clicked marker and show its infowindow
        (function(marker, content) {
            google.maps.event.addListener(marker, 'click', function(event) {
                map.setZoom(17);
                map.setCenter(event.latLng);
                infowindow.setContent(content);
                infowindow.open(map, marker);
            });
        })(marker, content);
    });
}
