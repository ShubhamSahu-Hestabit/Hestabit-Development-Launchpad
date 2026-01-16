export function renderProducts(products) {
  const container = document.getElementById("products");
  container.innerHTML = "";

  if (!products.length) {
    container.innerHTML = "<p>No products found.</p>";
    return;
  }

  products.forEach(p => {
    const card = document.createElement("div");
    card.className = "product-card";

    card.innerHTML = `
      <img src="${p.thumbnail}" alt="${p.title}" loading="lazy"/>
      <h3>${p.title}</h3>
      <p>$${p.price}</p>
    `;

    container.appendChild(card);
  });
}
