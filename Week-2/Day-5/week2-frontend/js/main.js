import { fetchProducts } from "./api.js";
import { state } from "./state.js";
import { applyFilters } from "./filters.js";
import { renderProducts } from "./render.js";

const subBox = document.getElementById("subcategory");

function update() {
  renderProducts(applyFilters(state));
}

document.querySelectorAll(".category").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".category").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    state.mainCategory = btn.dataset.category;
    state.subCategory = null;

    subBox.classList.toggle("hidden", state.mainCategory !== "accessories");
    update();
  };
});

subBox?.querySelectorAll("button").forEach(btn => {
  btn.onclick = () => {
    state.subCategory = btn.dataset.sub;
    update();
  };
});

document.getElementById("search").oninput = e => {
  state.search = e.target.value.toLowerCase();
  update();
};

document.getElementById("sort").onchange = e => {
  state.sort = e.target.value;
  update();
};

(async function init() {
  state.products = await fetchProducts();
  update();
})();
