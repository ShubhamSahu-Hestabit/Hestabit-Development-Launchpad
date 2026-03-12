const API = "https://dummyjson.com/products?limit=200";

const grid = document.getElementById("productGrid");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const genderSelect = document.getElementById("genderSelect");

let allProducts = [];
let activeMain = "all";

const CATEGORY_MAP = {
  clothing: {
    men: ["mens-shirts"],
    women: ["tops", "womens-dresses"]
  },
  footwear: {
    men: ["mens-shoes"],
    women: ["womens-shoes"]
  },
  watches: {
    men: ["mens-watches"],
    women: ["womens-watches"]
  },
  sunglasses: {
    men: ["sunglasses"],
    women: ["sunglasses"]
  },
  bags: {
    women: ["womens-bags"]
  }
};

async function loadProducts() {
  const res = await fetch(API);
  const data = await res.json();
  allProducts = data.products;
  applyFilters();
}

function applyFilters() {
  const gender = genderSelect.value;

  let filtered = allProducts.filter(p => {
    if (activeMain === "all") {
      return Object.values(CATEGORY_MAP)
        .flatMap(c => Object.values(c).flat())
        .includes(p.category);
    }

    const map = CATEGORY_MAP[activeMain];
    if (!map) return false;

    if (gender === "all") {
      return Object.values(map).flat().includes(p.category);
    }

    return map[gender]?.includes(p.category);
  });

  // 🔍 Search filter
  const query = searchInput.value.toLowerCase();
  filtered = filtered.filter(p =>
    p.title.toLowerCase().includes(query)
  );

  // 🔃 Sorting
  switch (sortSelect.value) {
    case "high-low":
      filtered.sort((a, b) => b.price - a.price);
      break;

    case "low-high":
      filtered.sort((a, b) => a.price - b.price);
      break;

    case "az":
      filtered.sort((a, b) => a.title.localeCompare(b.title));
      break;

    case "za":
      filtered.sort((a, b) => b.title.localeCompare(a.title));
      break;

    case "rating-high":
      filtered.sort((a, b) => b.rating - a.rating);
      break;

    // default → no sorting
  }

  render(filtered);
}


function render(products) {
  grid.innerHTML = "";

  if (products.length === 0) {
    grid.innerHTML = "<p>No products found.</p>";
    return;
  }

  products.forEach(p => {
    const stars = "★".repeat(Math.round(p.rating));

    grid.innerHTML += `
      <div class="card">
        <img src="${p.thumbnail}" alt="${p.title}">
        <h4>${p.title}</h4>

        <div class="rating">
          ${stars}
          <span>${p.rating.toFixed(1)}</span>
        </div>

        <p class="price">$${p.price}</p>
      </div>
    `;
  });
}


document.querySelectorAll(".tabs button").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".tabs button")
      .forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    activeMain = btn.dataset.main;
    applyFilters();
  };
});

searchInput.oninput = applyFilters;
sortSelect.onchange = applyFilters;
genderSelect.onchange = applyFilters;

loadProducts();
