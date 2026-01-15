let todos = loadTodos();

const input = document.getElementById("todo-input");
const addBtn = document.getElementById("add-btn");
const list = document.getElementById("todo-list");

function renderTodos() {
  list.innerHTML = "";

  todos.forEach(todo => {
    const li = document.createElement("li");
    if (todo.completed) li.classList.add("completed");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = todo.completed;
    checkbox.addEventListener("change", () => toggleCompleted(todo.id));

    const span = document.createElement("span");
    span.textContent = todo.text;

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.addEventListener("click", () => editTodo(todo.id));

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.addEventListener("click", () => deleteTodo(todo.id));

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(editBtn);
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

function addTodo() {
  try {
    const text = input.value.trim();
    if (!text) return;

    todos.push({
      id: Date.now(),
      text,
      completed: false
    });

    saveTodos(todos);
    renderTodos();
    input.value = "";
  } catch (error) {
    console.error("Error adding todo", error);
  }
}

function editTodo(id) {
  try {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    const newText = prompt("Edit task", todo.text);
    if (!newText) return;

    todo.text = newText;
    saveTodos(todos);
    renderTodos();
  } catch (error) {
    console.error("Error editing todo", error);
  }
}

function deleteTodo(id) {
  try {
    todos = todos.filter(t => t.id !== id);
    saveTodos(todos);
    renderTodos();
  } catch (error) {
    console.error("Error deleting todo", error);
  }
}

function toggleCompleted(id) {
  try {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    todo.completed = !todo.completed;
    saveTodos(todos);
    renderTodos();
  } catch (error) {
    console.error("Error toggling todo", error);
  }
}

addBtn.addEventListener("click", addTodo);
document.addEventListener("DOMContentLoaded", renderTodos);
