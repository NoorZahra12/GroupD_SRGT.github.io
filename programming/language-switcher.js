// Load content based on language
function loadContent(lang) {
    return fetch(`../content_lang_files/content-${lang}.json`)
        .then(response => response.json());
}

// Function created to switch language
function switchLanguage(lang) {
    loadContent(lang)
        .then(content => {
            // Iterate over the keys (variables) in the JSON object
            for (let key in content) {
                // Get elements with language-specific content
                var langswitch = document.getElementById(key);
                
                // Update content based on loaded data
                if (langswitch) {
                    langswitch.textContent = content[key];
                }
            }
        })
        .catch(error => console.error('Error loading content:', error));
}

// Initial language switch
switchLanguage('en'); // Default to English
