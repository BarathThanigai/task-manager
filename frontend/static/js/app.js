const state = {
  token: localStorage.getItem("taskManagerToken") || "",
  username: localStorage.getItem("taskManagerUsername") || "",
  skip: 0,
  limit: 5,
  total: 0,
  filterCompleted: "",
};

const messageBox = document.getElementById("message-box");
const taskList = document.getElementById("task-list");
const pageLabel = document.getElementById("page-label");
const filterSelect = document.getElementById("filter-completed");

function showMessage(message, isError = false) {
  if (!messageBox) {
    console.warn(message);
    return;
  }
  messageBox.textContent = message;
  messageBox.style.color = isError ? "#b42318" : "#115e59";
}

function formatError(data) {
  if (!data || data.detail === undefined) {
    return "Request failed";
  }

  if (Array.isArray(data.detail)) {
    return data.detail
      .map((item) => {
        if (typeof item === "string") return item;
        if (item.msg) return item.msg;
        return JSON.stringify(item);
      })
      .join(" ");
  }

  if (typeof data.detail === "object") {
    return Object.values(data.detail)
      .flat()
      .map((value) => (typeof value === "string" ? value : JSON.stringify(value)))
      .join(" ");
  }

  return String(data.detail);
}

async function apiRequest(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }

  const response = await fetch(path, { ...options, headers });
  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(formatError(data));
  }
  return data;
}

function saveSession(token, username) {
  state.token = token;
  state.username = username;
  localStorage.setItem("taskManagerToken", token);
  localStorage.setItem("taskManagerUsername", username);
}

function clearSession() {
  state.token = "";
  state.username = "";
  localStorage.removeItem("taskManagerToken");
  localStorage.removeItem("taskManagerUsername");
}

function renderTasks(items) {
  if (!taskList) return;

  if (!items.length) {
    taskList.innerHTML = "<p>No tasks found for this page/filter.</p>";
    return;
  }

  taskList.innerHTML = items
    .map(
      (task) => `
        <article class="task-item ${task.completed ? "completed" : ""}">
          <div>
            <h3>${task.title}</h3>
            <p>${task.description || "No description"}</p>
            <small>Status: ${task.completed ? "Completed" : "Pending"}</small>
          </div>
          <div class="task-actions">
            <button type="button" data-action="toggle" data-id="${task.id}">
              ${task.completed ? "Mark pending" : "Mark complete"}
            </button>
            <button type="button" class="delete" data-action="delete" data-id="${task.id}">
              Delete
            </button>
          </div>
        </article>
      `
    )
    .join("");
}

async function loadTasks() {
  if (!state.token) {
    return;
  }

  const params = new URLSearchParams({
    skip: String(state.skip),
    limit: String(state.limit),
  });
  if (state.filterCompleted !== "") {
    params.set("completed", state.filterCompleted);
  }

  try {
    const data = await apiRequest(`/tasks?${params.toString()}`);
    state.total = data.total;
    renderTasks(data.items);
    if (pageLabel) {
      const currentPage = Math.floor(state.skip / state.limit) + 1;
      const totalPages = Math.max(1, Math.ceil(state.total / state.limit));
      pageLabel.textContent = `Page ${currentPage} of ${totalPages}`;
    }
  } catch (error) {
    showMessage(error.message, true);
  }
}

function redirectToTasks() {
  window.location.href = "/static/tasks.html";
}

function redirectToLogin() {
  window.location.href = "/";
}

function updateWelcomeText() {
  const userNameElement = document.getElementById("user-name");
  if (userNameElement) {
    userNameElement.textContent = state.username || "friend";
  }
}

function initLoginPage() {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
  });

  const loginButton = document.getElementById("login-button");
  if (!loginButton) return;

  loginButton.addEventListener("click", async () => {
    const formData = new FormData(loginForm);
    const payload = Object.fromEntries(formData.entries());

    if (!payload.username || !payload.password) {
      showMessage("Username and password are required.", true);
      return;
    }

    try {
      const data = await apiRequest("/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      saveSession(data.access_token, payload.username);
      showMessage("Login successful.");
      redirectToTasks();
    } catch (error) {
      showMessage(error.message, true);
    }
  });
}

function initRegisterPage() {
  const registerForm = document.getElementById("register-form");
  if (!registerForm) return;

  registerForm.addEventListener("submit", (event) => {
    event.preventDefault();
  });

  const registerButton = document.getElementById("register-button");
  if (!registerButton) return;

  registerButton.addEventListener("click", async () => {
    const formData = new FormData(registerForm);
    const payload = Object.fromEntries(formData.entries());

    if (!payload.username || !payload.email || !payload.password) {
      showMessage("All fields are required.", true);
      return;
    }

    if (payload.password.length < 6) {
      showMessage("Password must be at least 6 characters.", true);
      return;
    }

    try {
      await apiRequest("/register", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showMessage("Registration successful. Redirecting to login...");
      registerForm.reset();
      setTimeout(() => redirectToLogin(), 1200);
    } catch (error) {
      showMessage(error.message, true);
    }
  });
}

function initTasksPage() {
  if (!window.location.pathname.endsWith("tasks.html")) return;

  if (!state.token) {
    redirectToLogin();
    return;
  }

  updateWelcomeText();

  const taskForm = document.getElementById("task-form");
  if (taskForm) {
    taskForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(taskForm);
      const payload = Object.fromEntries(formData.entries());

      if (!payload.title) {
        showMessage("Task title is required.", true);
        return;
      }

      try {
        await apiRequest("/tasks", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        showMessage("Task created.");
        taskForm.reset();
        state.skip = 0;
        await loadTasks();
      } catch (error) {
        showMessage(error.message, true);
      }
    });
  }

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      clearSession();
      showMessage("Logged out.");
      redirectToLogin();
    });
  }

  if (filterSelect) {
    filterSelect.addEventListener("change", async (event) => {
      state.filterCompleted = event.target.value;
      state.skip = 0;
      await loadTasks();
    });
  }

  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");

  if (prevBtn) {
    prevBtn.addEventListener("click", async () => {
      state.skip = Math.max(0, state.skip - state.limit);
      await loadTasks();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", async () => {
      if (state.skip + state.limit < state.total) {
        state.skip += state.limit;
        await loadTasks();
      }
    });
  }

  if (taskList) {
    taskList.addEventListener("click", async (event) => {
      const button = event.target.closest("button");
      if (!button) return;

      const taskId = button.dataset.id;
      const action = button.dataset.action;

      try {
        if (action === "toggle") {
          const task = await apiRequest(`/tasks/${taskId}`);
          await apiRequest(`/tasks/${taskId}`, {
            method: "PUT",
            body: JSON.stringify({ completed: !task.completed }),
          });
          showMessage("Task updated.");
        }

        if (action === "delete") {
          await apiRequest(`/tasks/${taskId}`, { method: "DELETE" });
          showMessage("Task deleted.");
        }

        await loadTasks();
      } catch (error) {
        showMessage(error.message, true);
      }
    });
  }

  loadTasks();
}

document.addEventListener("DOMContentLoaded", () => {
  initLoginPage();
  initRegisterPage();
  initTasksPage();
});

