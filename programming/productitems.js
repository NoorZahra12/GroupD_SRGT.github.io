document.addEventListener('DOMContentLoaded', function () {
    // Fetch exchange rates from the API
    fetch('https://api.exchangerate-api.com/v4/latest/USD')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(exchangeData => {
            // Fetch product data
            fetch('../stock.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    const productsDiv = document.getElementById('products');
                    data.forEach(item => {
                        // Convert selling price to user's currency
                        const userCurrency = 'EUR'; // You can replace 'EUR' with user's currency code
                        const convertedPrice = (item.sellingPrice * exchangeData.rates[userCurrency]).toFixed(2);
                        
                        // Create product item HTML
                        const productHTML = `
                            <div>
                                <p id="group">Category: ${item.group}</p>
                                <p id="name">Name: ${item.itemName}</p>
                                <p id="code">Code: ${item.itemCode}</p>
                                <div>
                                    <p id="price">Price: ${convertedPrice} ${userCurrency}</p>
                                    <button id="add_btn">Add to Cart</button>
                                </div>
                            </div>
                        `;
                        
                        // Append product item to productsDiv
                        productsDiv.innerHTML += productHTML;
                    });
                })
                .catch(error => console.error('Error fetching products:', error));
        })
        .catch(error => console.error('Error fetching exchange rates:', error));
});
