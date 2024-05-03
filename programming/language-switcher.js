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
            var heroTitle = document.getElementById('hero-title');
            var heroMessage = document.getElementById('hero-message');
            
            // Update content based on loaded data
            heroTitle.textContent = content['hero-title'];
            heroMessage.textContent = content['hero-message'];
        })
        .catch(error => console.error('Error loading content:', error));
}

// Initial language switch
switchLanguage('en'); // Default to English