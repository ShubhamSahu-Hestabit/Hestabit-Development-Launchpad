const menuBtn = document.getElementById("menuBtn");
const dropdownBtn = document.getElementById("dropdownBtn");
const dropdown = document.getElementById("dropdown");

menuBtn.addEventListener("click", () => {
  dropdown.classList.add("hidden");
});

dropdownBtn.addEventListener("click", () => {
  dropdown.classList.toggle("hidden");
});

const openModal = document.getElementById("openModal");
const closeModal = document.getElementById("closeModal");
const modalOverlay = document.getElementById("modalOverlay");

openModal.addEventListener("click", () => {
  modalOverlay.classList.remove("hidden");
});

closeModal.addEventListener("click", () => {
  modalOverlay.classList.add("hidden");
});

modalOverlay.addEventListener("click", e => {
  if (e.target === modalOverlay) {
    modalOverlay.classList.add("hidden");
  }
});

let count = 0;
const countEl = document.getElementById("count");

document.getElementById("increase").addEventListener("click", () => {
  count++;
  countEl.textContent = count;
});

document.getElementById("decrease").addEventListener("click", () => {
  if (count > 0) count--;
  countEl.textContent = count;
});

const faqs = [
  {
    q: "How do I choose the right clothing size?",
    a: "Refer to the brand size chart and measure your chest, waist, and hips accurately."
  },
  {
    q: "Which fabric is best for everyday wear?",
    a: "Cotton and cotton blends are breathable, soft, and comfortable for daily use."
  },
  {
    q: "How should I wash delicate garments?",
    a: "Use cold water, mild detergent, and avoid high spin cycles."
  },
  {
    q: "What is the difference between slim fit and regular fit?",
    a: "Slim fit is more tailored, while regular fit offers a relaxed and comfortable feel."
  },
  {
    q: "How can I make clothes last longer?",
    a: "Wash inside out, avoid excessive heat, and store garments properly."
  },
  {
    q: "Are sustainable fabrics better for the environment?",
    a: "Yes, they reduce water consumption and environmental impact."
  }
];

const faqHTML = faqs
  .map(faq => `
    <div class="faq-item">
      <div class="faq-question">${faq.q}</div>
      <div class="faq-answer">${faq.a}</div>
    </div>
  `)
  .reduce((acc, item) => acc + item, "");

document.getElementById("faq").innerHTML = faqHTML;

document.querySelectorAll(".faq-question").forEach(q => {
  q.addEventListener("click", () => {
    q.parentElement.classList.toggle("active");
  });
});
