// project.js

document.addEventListener('DOMContentLoaded', function () {
    // Add an event listener to all project items
    document.querySelectorAll('.tm-portfolio').forEach(function(project) {
      project.addEventListener('click', function() {
        // Get the project ID from the data-project-id attribute
        var projectId = this.getAttribute('data-project-id');
        
        // Replace the content in the left column with the content for the clicked project
        var projectContent = getProjectContent(projectId); // Define a function to get project content
        document.querySelector('.col-md-4 .description-list').innerHTML = projectContent;
      });
    });
  
    // Define a function to get project content based on project ID
    function getProjectContent(projectId) {
      // Replace this with your logic to fetch the content for each project
      // For this example, I'm using static content
      switch (projectId) {
        case '1':
          return `
            <dt>Client:</dt>
            <dd>Project 1 Client</dd>
            <dt>Location:</dt>
            <dd>Project 1 Location</dd>
            <!-- Add more content here for Project 1 -->
          `;
        case '2':
          return `
            <dt>Client:</dt>
            <dd>Project 2 Client</dd>
            <dt>Location:</dt>
            <dd>Project 2 Location</dd>
            <!-- Add more content here for Project 2 -->
          `;
        // Add more cases for other projects as needed
        default:
          return '';
      }
    }
  });
  