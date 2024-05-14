document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const menubar = document.querySelector('.menu-bar');

    hamburger.addEventListener('click', () => {
        menubar.classList.toggle('active');
    });

    function clearInput() {
        document.getElementById('search').value = "";
        document.getElementById('food-list').innerHTML = "";
    }

    function searchRecipes(event) {
        // Check if the 'Enter' key was pressed
        if (event.key === "Enter") {
            let searchQuery = document.getElementById("search").value.trim();
            console.log("Search Query:", searchQuery);  // Debug: Log the search query

            if (searchQuery.length > 0) {
                $.ajax({
                    url: '/recommend',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ preferences: searchQuery }),
                    success: function(recipes) {
                        console.log("Recipes:", recipes);  // Debug: Log the recipes
                        displayRecipes(recipes);
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        console.log("AJAX Error:", textStatus, errorThrown);  // Debug: Log AJAX error details
                        console.log("Response:", xhr.responseText);  // Debug: Log response text
                        alert("Error searching recipes. Please check the console for more details.");
                    }
                });
            } else {
                document.getElementById('food-list').innerHTML = "";
            }
        }
    }

    function displayRecipes(recipes) {
        let foodList = document.getElementById('food-list');
        foodList.innerHTML = "";

        if (recipes.length === 0) {
            foodList.innerHTML = "<p>Sorry, no recipes found.</p>";
        } else {
            recipes.forEach((recipe, index) => {
                let recipeElement = `
                    <div class="card card-shadow">
                        <div class="card-header card-image">
                            <img src="${recipe.image_url}" alt="${recipe.name}">
                        </div>
                        <div class="card-body">
                            <h3>${recipe.name}</h3>
                            <p>${recipe.description}</p>
                        </div>
                        <div class="card-footer">
                            <button class="btn" onclick="showRecipeDetails(${index})">Get Recipe</button>
                        </div>
                    </div>
                `;
                foodList.innerHTML += recipeElement;
            });
        }
    }

    function showRecipeDetails(index) {
        let searchQuery = document.getElementById("search").value.trim();
        $.ajax({
            url: '/recommend',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ preferences: searchQuery }),
            success: function(recipes) {
                let recipe = recipes[index];
                document.getElementById('meal-name').textContent = recipe.name;
                document.getElementById('meal-descript-about').textContent = recipe.description;
                document.getElementById('meal-ingredients').textContent = recipe.ingredients;
                document.getElementById('meal-instruction').textContent = recipe.directions;
                document.getElementById('meal-img').src = recipe.image_url;
                document.getElementById('meal-detail').style.display = 'block';
            },
            error: function() {
                alert("Error loading recipe details.");
            }
        });
    }

    function closeBtn() {
        document.getElementById('meal-detail').style.display = 'none';
    }

    // Attach the searchRecipes function to the 'keyup' event of the search input
    document.getElementById("search").addEventListener("keyup", searchRecipes);
    document.getElementById("recipe-close-btn").addEventListener("click", closeBtn);
});
