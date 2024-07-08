// Sample data for Home Solutions and Commercial Solutions
const solutions = [
    {
        solution_name: "Furnace Installation",
        category: "Heating",
        image_url: "https://example.com/images/furnace.jpg",
        solution_type: "Home",
    },
    {
        solution_name: "Air Conditioning Installation",
        category: "Cooling",
        image_url: "https://example.com/images/air-conditioning.jpg",
        solution_type: "Home",
    },
    {
        solution_name: "Ventilation System Installation",
        category: "Ventilation",
        image_url: "https://example.com/images/ventilation.jpg",
        solution_type: "Home",
    },
    {
        solution_name: "Commercial Boiler Installation",
        category: "Heating",
        image_url: "https://example.com/images/commercial-boiler.jpg",
        solution_type: "Commercial",
    },
    {
        solution_name: "Chiller System Installation",
        category: "Cooling",
        image_url: "https://example.com/images/chiller.jpg",
        solution_type: "Commercial",
    },
    {
        solution_name: "Commercial Ventilation System",
        category: "Ventilation",
        image_url: "https://example.com/images/commercial-ventilation.jpg",
        solution_type: "Commercial",
    },
];

// Function to display images based on selected categories and search input
function displayImages(selectedCategories, searchText) {
    const imageContainer = document.getElementById("imageContainer");
    imageContainer.innerHTML = ""; // Clear previous images

    solutions.forEach((solution) => {
        // Check if the solution matches selected categories and search input
        if (
            (selectedCategories.includes(solution.category) || selectedCategories.length === 0) &&
            (searchText === "" || solution.solution_name.toLowerCase().includes(searchText.toLowerCase()))
        ) {
            // Create an image card
            const card = document.createElement("div");
            card.classList.add("image-card");

            // Create an image element
            const imgElement = document.createElement("img");
            imgElement.src = solution.image_url;
            imgElement.alt = solution.solution_name;

            // Create a solution name element
            const solutionName = document.createElement("h3");
            solutionName.textContent = solution.solution_name;

            // Append elements to the card
            card.appendChild(imgElement);
            card.appendChild(solutionName);

            // Append the card to the image container
            imageContainer.appendChild(card);
        }
    });

    // Add grid layout class to the image container
    imageContainer.classList.add("image-grid");
}
