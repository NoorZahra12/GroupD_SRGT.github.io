document.addEventListener('DOMContentLoaded', function () {
    let userCurrency = 'AED'; // Set default user currency
    let exchangeData = {};
    let cart = [];

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

        data.forEach((item, index) => {
            const convertedPrice = (item.sellingPrice * exchangeData.rates[userCurrency]).toFixed(2);

            const productHTML = `
                <div class="product-item" data-brand="${item.brand}">
                    <p id="group">الفئة: ${item.group}</p>
                    <p id="name">الاسم: ${item.itemName}</p>
                    <p id="code">الكود: ${item.itemCode}</p>
                    <p id="brand">العلامة التجارية: ${item.brand}</p>
                    <p id="stock">المخزون: ${item.quantity}</p>
                    <p id="price">السعر: ${convertedPrice} ${userCurrency}</p>
                    <button class="add_btn" data-index="${index}">أضف إلى السلة</button>
                </div>
            `;

            productsDiv.innerHTML += productHTML;
        });

        // Attach event listeners for "Add to Cart" buttons
        const addToCartButtons = document.querySelectorAll('.add_btn');
        addToCartButtons.forEach(button => {
            button.addEventListener('click', () => {
                addToCart(data[button.dataset.index]);
            });
        });
    }

    function populateBrandsFilter(data) {
        const brandFilter = document.getElementById('brand-filter');
        const brands = [...new Set(data.map(item => item.brand))];

        // Sort the brands array alphabetically
        brands.sort((a, b) => a.localeCompare(b));

        const allLi = document.createElement('li');
        allLi.textContent = 'الكل';
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

    function addToCart(item) {
        const existingItemIndex = cart.findIndex(cartItem => cartItem.itemCode === item.itemCode);

        if (existingItemIndex > -1) {
            cart[existingItemIndex].quantity++;
        } else {
            cart.push({...item, quantity: 1});
        }

        displayCart();
    }

    function displayCart() {
        const cartList = document.querySelector('.cart_list');
        const totalPriceElement = document.getElementById('total-price');
        cartList.innerHTML = '';

        let totalPrice = 0;

        cart.forEach((item, index) => {
            const convertedPrice = (item.sellingPrice * exchangeData.rates[userCurrency]).toFixed(2);
            totalPrice += item.quantity * item.sellingPrice * exchangeData.rates[userCurrency];

            const cartItemHTML = `
                <div class="product-item" data-brand="${item.brand}">
                    <p id="group">الفئة: ${item.group}</p>
                    <p id="name">الاسم: ${item.itemName}</p>
                    <p id="code">الكود: ${item.itemCode}</p>
                    <p id="brand">العلامة التجارية: ${item.brand}</p>
                    <p id="stock">المخزون: ${item.quantity}</p>
                    <div>
                        <div class="plus_btn" data-index="${index}" data-action="increment">+</div>
                        <div class="customer_quantity">${item.quantity}</div>
                        <div class="minus_btn" data-index="${index}" data-action="decrement">-</div>
                    </div>
                    <p id="price">السعر: ${convertedPrice} ${userCurrency}</p>
                    <button data-index="${index}" data-action="remove">إزالة من السلة</button>
                </div>
            `;

            cartList.innerHTML += cartItemHTML;
        });

        totalPriceElement.textContent = `السعر الإجمالي: ${totalPrice.toFixed(2)} ${userCurrency}`;

        // Attach event listeners for cart buttons
        cartList.querySelectorAll('.plus_btn').forEach(button => {
            button.addEventListener('click', () => updateCartItemQuantity(button.dataset.index, 'increment'));
        });

        cartList.querySelectorAll('.minus_btn').forEach(button => {
            button.addEventListener('click', () => updateCartItemQuantity(button.dataset.index, 'decrement'));
        });

        cartList.querySelectorAll('[data-action="remove"]').forEach(button => {
            button.addEventListener('click', () => removeCartItem(button.dataset.index));
        });
    }

    function updateCartItemQuantity(index, action) {
        if (action === 'increment') {
            cart[index].quantity++;
        } else if (action === 'decrement' && cart[index].quantity > 1) {
            cart[index].quantity--;
        } else if (action === 'decrement' && cart[index].quantity === 1) {
            removeCartItem(index);
        }

        displayCart();
    }

    function removeCartItem(index) {
        cart.splice(index, 1);
        displayCart();
    }
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
