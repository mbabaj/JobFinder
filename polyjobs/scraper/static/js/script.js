// Job Filtering Script
document.addEventListener("DOMContentLoaded", () => {
  const searchTitle = document.getElementById("search-title");
  const searchLocation = document.getElementById("search-location");
  const categoryFilter = document.getElementById("category-filter");
  const jobCards = document.querySelectorAll(".job-card");

  function filterJobs() {
    const titleValue = searchTitle.value.toLowerCase();
    const locationValue = searchLocation.value.toLowerCase();
    const categoryValue = categoryFilter.value;

    jobCards.forEach(card => {
      const title = card.dataset.title.toLowerCase();
      const location = card.dataset.location.toLowerCase();
      const category = card.dataset.category;

      const matchesTitle = title.includes(titleValue);
      const matchesLocation = location.includes(locationValue);
      const matchesCategory = categoryValue === "all" || category === categoryValue;

      if (matchesTitle && matchesLocation && matchesCategory) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

  searchTitle.addEventListener("input", filterJobs);
  searchLocation.addEventListener("input", filterJobs);
  categoryFilter.addEventListener("change", filterJobs);
});
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".favorite-btn").forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();   // 🚀 stop form submission or link navigation

            const url = this.dataset.url;
            const jobId = this.dataset.jobId;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_favorited) {
                    this.textContent = "★ Unfavorite";
                } else {
                    this.textContent = "☆ Favorite";
                }
            })
            .catch(err => console.error("Error:", err));
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Account dropdown toggle
document.addEventListener("DOMContentLoaded", () => {
  const accountBtn = document.getElementById("account-btn");
  const dropdown = document.querySelector(".dropdown");

  if (accountBtn) {
    accountBtn.addEventListener("click", () => {
      dropdown.classList.toggle("active");
    });

    // Close dropdown if clicked outside
    document.addEventListener("click", (event) => {
      if (!dropdown.contains(event.target)) {
        dropdown.classList.remove("active");
      }
    });
  }
});