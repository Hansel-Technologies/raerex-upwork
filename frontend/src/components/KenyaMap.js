import React, { useState, useEffect } from 'react';
import { ComposableMap, Geographies, Geography, Marker, ZoomableGroup } from "react-simple-maps";
import { scaleQuantile } from "d3-scale";

const KenyaMap = ({ orders }) => {
  const [dimensions, setDimensions] = useState({ width: 600, height: 400 });
  const [mapData, setMapData] = useState([]);

  useEffect(() => {
    const updateDimensions = () => {
      const container = document.getElementById('kenya-map');
      if (container) {
        setDimensions({
          width: container.offsetWidth,
          height: container.offsetHeight
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);

    // Parse orders data if it's a string
    if (typeof orders === 'string') {
      try {
        setMapData(JSON.parse(orders));
      } catch (error) {
        console.error('Error parsing orders data:', error);
      }
    } else {
      setMapData(orders);
    }

    return () => window.removeEventListener('resize', updateDimensions);
  }, [orders]);

  const maxOrders = Math.max(...mapData.map(o => o.count), 1);
  const sizeScale = scaleQuantile().domain([0, maxOrders]).range([4, 8, 12, 16, 20]);

  return (
    <ComposableMap
      projection="geoMercator"
      projectionConfig={{
        scale: 2500,
        center: [37.9062, 0.0236]
      }}
      width={dimensions.width}
      height={dimensions.height}
    >
      <ZoomableGroup>
        <Geographies geography="/static/data/kenya-counties.json">
          {({ geographies }) =>
            geographies.map(geo => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#EAEAEC"
                stroke="#D6D6DA"
              />
            ))
          }
        </Geographies>
        {mapData.map(({ name, coordinates, count }) => (
          <Marker key={name} coordinates={coordinates}>
            <circle r={sizeScale(count)} fill="#FF5533" stroke="#FFFFFF" strokeWidth={2} />
            <text
              textAnchor="middle"
              y={-10}
              style={{ fontFamily: "system-ui", fill: "#5D5A6D", fontSize: "8px" }}
            >
              {name}
            </text>
          </Marker>
        ))}
      </ZoomableGroup>
    </ComposableMap>
  );
};

export default KenyaMap;