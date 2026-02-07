
function init() {
    if (typeof google === 'undefined' || !google.maps) {
        console.error('Google Maps JavaScript API not loaded');
        return;
    }

    // Center coordinates
    var myLatlng = new google.maps.LatLng(40.69847032728747, -73.9514422416687);

    var mapOptions = {
        zoom: 12,
        center: myLatlng,
        scrollwheel: false,
        styles: [
            {
                "featureType": "administrative.country",
                "elementType": "geometry",
                "stylers": [
                    { "visibility": "simplified" },
                    { "hue": "#ff0000" }
                ]
            }
        ]
    };

    var mapElement = document.getElementById('map');
    if (!mapElement) {
        console.warn('Map element with id=\"map\" not found');
        return;
    }

    var map = new google.maps.Map(mapElement, mapOptions);

    // Single marker at the center
    new google.maps.Marker({
        position: myLatlng,
        map: map
    });
}