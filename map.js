console.log("hello");

var map = new maplibregl.Map({
    container: 'map',
    style: 'https://api.maptiler.com/maps/streets-v4/style.json?key=z42CYMIGsRqf1ginH8SF',
    center: [74.3587, 31.5204],
    zoom: 10
});

const months = ['January', 'February','March','April','May','June','July',
    'August','September','October','November', 'December'];

const years = ['2016', '2017','2018', '2019', '2020', '2021', '2022', 
    '2023', '2024', '2025']

// combine into one function
function filterBy(month, year){
    const filters = ['all', ['==', ['get', 'month'], month], ['==', ['get', 'year'], year]]
    map.setFilter('clusters', filters)
    document.getElementById('month-display').textContent = month

}

map.on('load', () =>{
    map.addSource('aqi_monitors', {
        type: 'geojson', 
        data: 'data/aqi_lhe_data.geojson'});

map.addLayer({
    id:'clusters',
    type: 'circle', 
    source: 'aqi_monitors', 
    paint: {
        'circle-radius': 12,
        'circle-color': [
            'match',
            ['downcase', ['get', 'aqi_cat']],
            'good', '#478c5c',
            'moderate', '#fede00',
            'unhealthy for sensitive groups', '#FF7E00',
            'unhealthy', '#e21b32',
            'very unhealthy', '#8F3F97',
            'hazardous', '#7E0023',
            '#bddee8']}});

// caled when the slider or the drop down is moved   
function monthYearHandler(){
    const month = document.getElementById('slider').value
    const monthName = months[month]
    const year = document.getElementById('pick-year').value
    filterBy(monthName, year)
}

// whenever there is an input event on the slider or drop down then call the function
document.getElementById('slider').addEventListener('input', monthYearHandler);

document.getElementById('pick-year').addEventListener('change', monthYearHandler)

// set a deafult value for initial map load
const defaultMonthIndex = 0;
const defaultYear = '2023';
document.getElementById('slider').value = defaultMonthIndex;
document.getElementById('pick-year').value = defaultYear;
filterBy(months[defaultMonthIndex], defaultYear);

// Create a popup, but don't add it to the map yet.
const popup = new maplibregl.Popup({
    closeButton: false,      // show a close “x” button
    closeOnClick: false      // clicking elsewhere will close the popup
    });

map.on('mouseenter', 'clusters', () => {
    map.getCanvas().style.cursor = 'pointer';
        });  
map.on('mouseleave', 'clusters', () => {
     map.getCanvas().style.cursor = '';
     popup.remove(); // hide popup when leaving the layer
     });      

// Show popup on click on the 'places' layer (your circle layer)
map.on('mousemove', 'clusters', (e) => {
// Take the first feature that was clicked
const feature = e.features[0];

// Copy the coordinates from the feature
const coordinates = feature.geometry.coordinates.slice();

// Read values from your GeoJSON properties
const stationName = feature.properties.station_name; 
const avgAqi = parseInt(feature.properties.avg_aqi);

// Build some simple HTML for the popup
const html = `
<div>
    <strong>${stationName}</strong><br/>
    Average AQI: ${avgAqi}
</div>
`;

// Set popup position + content and add it to the map
popup
.setLngLat(coordinates)
.setHTML(html)
.addTo(map);
});

});
