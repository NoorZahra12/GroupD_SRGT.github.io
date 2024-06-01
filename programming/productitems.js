document.addEventListener('DOMContentLoaded', function () {
    let userCurrency = 'AED'; // Set default user currency
    let exchangeData = {};

    // Fetch exchange rates from the API
    fetch('https://api.exchangerate-api.com/v4/latest/USD')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            exchangeData = data;
            return fetch('../STOCK/stock.json');
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayProducts(data);
            populateBrandsFilter(data);
            setupCurrencyDropdown(data);
        })
        .catch(error => console.error('Error:', error));

    function displayProducts(data) {
        const productsDiv = document.getElementById('products');
        productsDiv.innerHTML = '';

        data.forEach(item => {
            const convertedPrice = (item.sellingPrice * exchangeData.rates[userCurrency]).toFixed(2);

            const productHTML = `
                <div class="product-item" data-brand="${item.brand}">
                    <p id="group">Category: ${item.group}</p>
                    <p id="name">Name: ${item.itemName}</p>
                    <p id="code">Code: ${item.itemCode}</p>
                    <p id="brand">Brand: ${item.brand}</p>
                    <p id="price">Price: ${convertedPrice} ${userCurrency}</p>
                    <button id="add_btn">Add to Cart</button>
                </div>
            `;

            productsDiv.innerHTML += productHTML;
        });
    }

    function populateBrandsFilter(data) {
        const brandFilter = document.getElementById('brand-filter');
        const brands = [...new Set(data.map(item => item.brand))];
    
        // Sort the brands array alphabetically
        brands.sort((a, b) => a.localeCompare(b));
    
        const allLi = document.createElement('li');
        allLi.textContent = 'All';
        allLi.addEventListener('click', () => filterByBrand('All'));
        brandFilter.appendChild(allLi);
    
        brands.forEach(brand => {
            const li = document.createElement('li');
            li.textContent = brand;
            li.addEventListener('click', () => filterByBrand(brand));
            brandFilter.appendChild(li);
        });
    }
    

    function filterByBrand(brand) {
        const products = document.querySelectorAll('.product-item');
        products.forEach(product => {
            if (brand === 'All' || product.dataset.brand === brand) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    }

    function setupCurrencyDropdown(data) {
        const currencySelect = document.getElementById('currency-select');
        currencySelect.addEventListener('change', (event) => {
            userCurrency = event.target.value;
            displayProducts(data);
    
        });
    }
    // Add event listener to "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll('#add_btn');
    addToCartButtons.forEach(button => {button.addEventListener('click', () => {addToCart(button.parentElement);});});
});

document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const openButton = document.getElementById('open-btn');
    const closeButton = document.getElementById('close-btn');

    openButton.addEventListener('click', () => {
        sidebar.classList.add('expanded');
        openButton.style.display = 'none';
    });

    closeButton.addEventListener('click', () => {
        sidebar.classList.remove('expanded');
        openButton.style.display = 'block';
    });
});
function addToCart(productElement) {
    const productName = productElement.querySelector('#name').textContent.split(': ')[1];
    const productPrice = parseFloat(productElement.querySelector('#price').textContent.split(': ')[1].split(' ')[0]);

    // Add the item to the cart
    const item = { name: productName, price: productPrice, quantity: 1 };
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push(item);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Item added to cart!');
}