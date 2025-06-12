document.addEventListener("DOMContentLoaded", function () {
    const dropdownToggle = document.getElementById("dropdown-toggle");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    // Toggle dropdown on click
    dropdownToggle?.addEventListener("click", function (event) {
        event.stopPropagation(); // Prevent click from closing immediately
        dropdownMenu.classList.toggle("show");
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (event) {
        if (!dropdownMenu.contains(event.target) && event.target !== dropdownToggle) {
            dropdownMenu.classList.remove("show");
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Handle Add to Cart button clicks dynamically
    document.querySelectorAll(".add-to-cart-form").forEach(form => {
        form.addEventListener("submit", async function(event) {
            event.preventDefault();

            let medicineId = this.getAttribute("data-medicine-id");

            try {
                // Fetch the correct price before adding to the cart
                let response = await fetch(`/medicine/price/${medicineId}`);
                let data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Create a hidden input for price and append it
                let priceInput = document.createElement("input");
                priceInput.type = "hidden";
                priceInput.name = "price";
                priceInput.value = data.price;
                this.appendChild(priceInput);

                // Submit the form with the correct price
                this.submit();
            } catch (error) {
                console.error("Error fetching price:", error);
                alert("Failed to fetch price. Please try again.");
            }
        });
    });
});



