let btn = document.querySelector("button");
let input = document.querySelector("input");
let ul = document.querySelector("ul");

// Hide the "Clear All" button when there are no tasks
function toggleClearAllButton() {
  let clearAllButton = document.getElementById("clearAll");
  if (ul.children.length === 0) {
    clearAllButton.style.display = "none";
  } else {
    clearAllButton.style.display = "block";
  }
}

btn.addEventListener("click", function () {
  if (input.value.trim() !== "") {
    // Check if input is not empty
    let items = document.createElement("li");
    items.innerText = input.value;
    ul.appendChild(items);
    input.value = "";

    let delBtm = document.createElement("button");
    delBtm.innerText = "Remove";
    delBtm.classList.add("delete");
    items.appendChild(delBtm);
  } else {
    alert("Please enter a task!");
  }

  // Toggle the visibility of "Clear All" button when a task is added
  toggleClearAllButton();
});

input.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    if (input.value.trim() !== "") {
      // Check if input is not empty
      let items = document.createElement("li");

      items.innerText = input.value;
      ul.appendChild(items);
      input.value = "";

      let delBtm = document.createElement("button");
      delBtm.innerText = "Remove";
      delBtm.classList.add("delete");
      items.appendChild(delBtm);
    } else {
      alert("Please enter a task!");
    }
  }

  // Toggle the visibility of "Clear All" button when a task is added
  toggleClearAllButton();
});

ul.addEventListener("click", function (event) {
  if (event.target.nodeName == "BUTTON") {
    let listItem = event.target.parentElement;
    listItem.remove();
    console.log(`Task: ${listItem.innerText} deleted!`);

    // Hide the "Clear All" button after clearing tasks
    toggleClearAllButton();
  }
});

// Mark task as completed
ul.addEventListener("click", function (event) {
  if (event.target.tagName === "LI") {
    event.target.classList.toggle("completed");
  }
});

// Clear all tasks logic
document.getElementById("clearAll").addEventListener("click", function () {
  ul.innerHTML = "";
  // Hide the "Clear All" button after clearing tasks
  toggleClearAllButton();
});

// Initially check the button visibility
toggleClearAllButton();
