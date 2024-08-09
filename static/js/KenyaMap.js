// static/js/KenyaMap.js
function createKenyaMap(containerId, orders) {
  console.log('Creating Kenya Map');
  console.log('Container ID:', containerId);
  console.log('Orders data:', orders);

  if (typeof ReactSimpleMaps === 'undefined') {
    console.error('ReactSimpleMaps is not defined. Make sure the library is loaded correctly.');
    return;
  }

  const { ComposableMap, Geographies, Geography, Marker, ZoomableGroup } = ReactSimpleMaps;

  if (!ComposableMap || !Geographies || !Geography || !Marker || !ZoomableGroup) {
    console.error('One or more ReactSimpleMaps components are not available.');
    return;
  }

  const width = 600;
  const height = 600;

  const maxOrders = Math.max(...orders.map(o => o.count));
  const sizeScale = d3.scaleQuantile()
    .domain([0, maxOrders])
    .range([4, 8, 12, 16, 20]);

  const Map = React.createElement(ComposableMap, {
    projection: "geoMercator",
    projectionConfig: {
      scale: 2500,
      center: [37.9062, 0.0236] // Coordinates for Kenya
    },
    width: width,
    height: height
  }, 
    React.createElement(ZoomableGroup, {},
      React.createElement(Geographies, { geography: "/static/data/kenya-counties.json" },
        ({ geographies }) =>
          geographies.map(geo => React.createElement(Geography, {
            key: geo.rsmKey,
            geography: geo,
            fill: "#EAEAEC",
            stroke: "#D6D6DA"
          }))
      ),
      orders.map(({ name, coordinates, count }) =>
        React.createElement(Marker, { key: name, coordinates: coordinates },
          React.createElement('circle', {
            r: sizeScale(count),
            fill: "#FF5533",
            stroke: "#FFFFFF",
            strokeWidth: 2
          }),
          React.createElement('text', {
            textAnchor: "middle",
            y: -10,
            style: { fontFamily: "system-ui", fill: "#5D5A6D", fontSize: "8px" }
          }, name)
        )
      )
    )
  );

  ReactDOM.render(Map, document.getElementById(containerId));
}