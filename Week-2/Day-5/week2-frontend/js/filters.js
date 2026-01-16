import { CATEGORY_MAP } from "./constants.js";

export function applyFilters(state) {
  let list = [...state.products];

  if (state.mainCategory !== "all") {
    list = list.filter(p =>
      CATEGORY_MAP[state.mainCategory].includes(p.category)
    );
  }

  if (state.subCategory) {
    list = list.filter(p => p.category === state.subCategory);
  }

  if (state.search) {
    list = list.filter(p =>
      p.title.toLowerCase().includes(state.search)
    );
  }

  if (state.sort === "high") {
    list.sort((a, b) => b.price - a.price);
  }

  return list;
}
