// sliding-images.js

// Get all of the sliding images
const slidingImages = document.querySelectorAll('.tm-portfolio');

// Add a click event listener to each sliding image
slidingImages.forEach(slidingImage => {
  slidingImage.addEventListener('click', () => {
    // Get the project ID of the sliding image
    const projectID = slidingImage.getAttribute('data-project-id');

    // Get the project description section
    const projectDescriptionSection = document.querySelector('section[data-project-id="' + projectID + '"]');

    // Hide the current content section
    const currentContentSection = document.querySelector('.container > section');
    currentContentSection.style.display = 'none';

    // Display the project description section
    projectDescriptionSection.style.display = 'block';
  });
});
