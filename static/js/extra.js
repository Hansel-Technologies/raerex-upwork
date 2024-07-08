// custom.js

// Function to open the modal popup with the clicked image
function openModal(imageSrc) {
    var modal = document.getElementById('imageModal');
    var modalImage = document.getElementById('modalImage');
    modal.style.display = "block";
    modalImage.src = imageSrc;
  }
  
  // Function to close the modal popup
  function closeModal() {
    var modal = document.getElementById('imageModal');
    modal.style.display = "none";
  }
  
  // Add click event listeners to the clickable images
  var clickableImages = document.querySelectorAll('.image-clickable');
  clickableImages.forEach(function(image) {
    image.addEventListener('click', function() {
      openModal(image.src);
    });
  });
  