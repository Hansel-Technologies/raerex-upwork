import React from 'react';
import ReactDOM from 'react-dom';
import KenyaMap from './components/KenyaMap';

document.addEventListener('DOMContentLoaded', () => {
  const mapContainer = document.getElementById('kenya-map');
  if (mapContainer) {
    const ordersData = JSON.parse(mapContainer.dataset.orders || '[]');
    ReactDOM.render(<KenyaMap orders={ordersData} />, mapContainer);
  }
});