// START: Chatbot Functionality
const chatIcon = document.getElementById("chat-icon");
const chatbotContainer = document.getElementById("chatbot-container");
const closeChatbot = document.querySelector(".close-chatbot");
const sendButton = document.getElementById("send-button");
const chatInput = document.getElementById("chat-input");
const chatbotBody = document.getElementById("chatbot-body");

// Show or hide the chatbot on icon click
chatIcon.addEventListener("click", () => {
    chatbotContainer.classList.toggle("show");
    chatbotContainer.style.opacity = chatbotContainer.classList.contains("show") ? "1" : "0";
});

// Close the chatbot when the close button is clicked
closeChatbot.addEventListener("click", () => {
    chatbotContainer.classList.remove("show");
});

// Send a message when the send button is clicked or Enter is pressed
sendButton.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Function to send a message and display a bot response
function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Display the user message
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatbotBody.appendChild(userMessage);

    chatInput.value = "";  // Clear input
    chatbotBody.scrollTop = chatbotBody.scrollHeight;  // Scroll to the bottom

    // Simulate a bot response (you can replace this with an API call)
    setTimeout(() => {
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = "I'm here to help!"; // Placeholder response
        chatbotBody.appendChild(botMessage);
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }, 1000);
}
// END: Chatbot Functionality

// START: Dropdown Menu Toggle
const dropdownBtn = document.querySelector(".dropdown-btn");
const dropdownContent = document.querySelector(".dropdown-content");

dropdownBtn.addEventListener("click", () => {
    dropdownContent.classList.toggle("show");
});
// END: Dropdown Menu Toggle

// START: Fetch Categories on Page Load (list_category)
async function loadCategories() {
    try {
        const response = await fetch("/list_category", { method: "GET" });
        if (response.ok) {
            const categories = await response.json();
            renderResults(categories);  // Display categories by default
        } else {
            console.error("Failed to load categories");
        }
    } catch (error) {
        console.error("Error loading categories:", error);
    }
}
document.addEventListener("DOMContentLoaded", loadCategories);
// END: Fetch Categories on Page Load

// START: Modal Functionality for Adding Category
const addButton = document.getElementById("add-button");
const addModal = document.getElementById("add-modal");
const closeButton = document.querySelector(".close-button");

// Show modal when Add button is clicked
addButton.addEventListener("click", () => addModal.classList.add("show-modal"));

// Hide modal when close button or area outside modal content is clicked
closeButton.addEventListener("click", () => addModal.classList.remove("show-modal"));
addModal.addEventListener("click", (event) => {
    if (event.target === addModal) addModal.classList.remove("show-modal");
});
// END: Modal Functionality for Adding Category

// START: Form Submission for Adding New Category
document.getElementById("add-category-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        favicon: document.getElementById("favicon").value,
        examples: {
            title: document.getElementById("example-title").value,
            code: document.getElementById("example-code").value
        }
    };

    try {
        const response = await fetch("/add_category", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("Category added successfully!");
            addModal.classList.remove("show-modal");
            document.getElementById("add-category-form").reset();
            loadCategories(); // Reload categories after adding
        } else {
            console.error("Failed to add category. Status:", response.status);
        }
    } catch (error) {
        console.error("Error adding category:", error);
    }
});
// END: Form Submission for Adding New Category

// START: Search Functionality (search_by_category)
async function performSearch() {
    const query = document.getElementById("search-input").value.trim();
    if (!query) {
        loadCategories();  // If no search term, reload all categories
        return;
    }

    try {
        const response = await fetch("/search_by_category", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        if (response.ok) {
            const data = await response.json();
            renderResults(data);  // Render search results
        } else {
            console.error("Failed to perform search");
        }
    } catch (error) {
        console.error("Error loading search data:", error);
    }
}

// Attach search function to search button
document.getElementById("search-button").addEventListener("click", performSearch);
// END: Search Functionality

// START: Render Search Results with Dropdown and Collapsible Examples
function renderResults(results) {
    const searchResults = document.getElementById("search-results");
    searchResults.innerHTML = "";  
    searchResults.classList.add("show");

    results.forEach(result => {
        const resultItem = document.createElement("div");
        resultItem.className = "result-item";

        // Icon
        const icon = document.createElement("img");
        icon.className = "result-icon";
        icon.src = result.favicon || "default-icon-path"; // Use a default icon if none provided
        icon.alt = `${result.name} icon`;

        // Content container
        const content = document.createElement("div");

        // Header
        const header = document.createElement("div");
        header.className = "result-header";
        header.textContent = result.name;

        // Description
        const description = document.createElement("div");
        description.className = "result-description";
        description.textContent = result.description;

        // Examples (collapsible)
        const examples = document.createElement("div");
        examples.className = "result-examples";
        
        const exampleTitle = document.createElement("p");
        exampleTitle.textContent = result.examples.title;

        const exampleCode = document.createElement("pre");
        exampleCode.textContent = result.examples.code;

        examples.appendChild(exampleTitle);
        examples.appendChild(exampleCode);

        // Toggle button for examples
        const toggleButton = document.createElement("span");
        toggleButton.className = "example-toggle";
        toggleButton.textContent = "Show Examples";
        toggleButton.addEventListener("click", () => {
            examples.classList.toggle("show");
            toggleButton.textContent = examples.classList.contains("show") ? "Hide Examples" : "Show Examples";
        });

        // Dropdown for Edit/Delete options
        const dropdown = document.createElement("div");
        dropdown.className = "result-dropdown";
        
        const dropdownIcon = document.createElement("i");
        dropdownIcon.className = "fas fa-ellipsis-v"; // FontAwesome icon for dropdown
        dropdown.appendChild(dropdownIcon);
        
        const dropdownContent = document.createElement("div");
        dropdownContent.className = "result-dropdown-content";
        
        const editOption = document.createElement("a");
        editOption.href = "#";
        editOption.innerHTML = `<i class="fas fa-edit"></i> Edit`; // FontAwesome edit icon
        
        const deleteOption = document.createElement("a");
        deleteOption.href = "#";
        deleteOption.innerHTML = `<i class="fas fa-trash-alt"></i> Delete`; // FontAwesome delete icon
        
        dropdownContent.appendChild(editOption);
        dropdownContent.appendChild(deleteOption);
        dropdown.appendChild(dropdownContent);

        // Append all parts to content container
        content.appendChild(header);
        content.appendChild(description);
        content.appendChild(toggleButton);
        content.appendChild(examples);

        // Append icon, content, and dropdown to result item
        resultItem.appendChild(icon);
        resultItem.appendChild(content);
        resultItem.appendChild(dropdown);

        // Append result item to search results container
        searchResults.appendChild(resultItem);
    });
}
// END: Render Search Results with Dropdown and Collapsible Examples
