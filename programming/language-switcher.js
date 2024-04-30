// Load content based on language
function loadContent(lang) {
    return fetch(`../content_lang_files/content-${lang}.json`)
        .then(response => response.json());
}

// Function to switch language
function switchLanguage(lang) {
    loadContent(lang)
        .then(content => {
            // Get elements with language-specific content
            var welcomeMessage = document.getElementById('welcome-message');
            var intro = document.getElementById('intro');
            
            // Update content based on loaded data
            welcomeMessage.textContent = content.welcomeMessage;
            intro.textContent = content.intro;
        })
        .catch(error => console.error('Error loading content:', error));
}

// Initial language switch
switchLanguage('en'); // Default to English