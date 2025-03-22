import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Point } from 'ol/geom';
import { fromLonLat, toLonLat } from 'ol/proj';
import { Feature } from 'ol';
import Icon from 'ol/style/Icon';
import Style from 'ol/style/Style';

const map = new Map({
target: 'map',
layers: [
new TileLayer({
source: new OSM()
})
],
view: new View({
center: fromLonLat([23.5885, 46.7705]), // Cluj coordinates
zoom: 13
})
});

let selectedTextbox = null;
const coordinateInputs = document.querySelectorAll('.coordinate-input');

coordinateInputs.forEach(input => {
input.addEventListener('click', () => {
selectedTextbox = input;
});
});

map.on('singleclick', function (event) {
const coordinates = event.coordinate;
const lonLat = toLonLat(coordinates);

if (selectedTextbox) {
selectedTextbox.value = `${lonLat[0].toFixed(6)}, ${lonLat[1].toFixed(6)}`;
selectedTextbox = null;
}

const marker = new Feature({
geometry: new Point(fromLonLat(lonLat))
});

marker.setStyle(new Style({
image: new Icon({
anchor: [0.5, 1],
src: 'https://openlayers.org/en/latest/examples/data/icon.png'
})
}));

const vectorLayer = new VectorLayer({
source: new VectorSource({
features: [marker]
})
});

map.addLayer(vectorLayer);
});