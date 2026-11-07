'use strict';
const zoom = document.querySelector('#report-zoom');
const pages = document.querySelector('.report-pages');
if (zoom && pages) {
  zoom.addEventListener('change', () => {
    pages.classList.toggle('large', zoom.value === 'large');
  });
}
