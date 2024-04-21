<template>
  <div class="register">
    <h1>Login</h1>
    <form @submit.prevent="loginUser" id="loginForm">
      <div v-if="result && result.length > 0">
        <ul class="alert alert-danger">
          <li v-for="error in result">{{ error }}</li>
        </ul>
      </div>
      <div v-if="result.message">
        <div class="alert alert-success">{{ result.message }}</div>
      </div>
      <div class="form-group">
        <label for="username" class="form-label">Username</label>
        <input
          name="username"
          type="text"
          class="form-control"
          placeholder="Enter your username"
        />
      </div>
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input
          name="password"
          type="password"
          class="form-control"
          placeholder="Enter your password"
        />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

let csrf_token = ref("");
let result = ref([]);

const getCsrfToken = () => {
  fetch("/api/v1/csrf-token")
    .then((res) => res.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
};

onMounted(() => {
  getCsrfToken();
});

const loginUser = async () => {
  let loginForm = document.getElementById("loginForm");
  let form_data = new FormData(loginForm);

  const loginResponse = await fetch("/api/v1/auth/login", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  });

  const data = await loginResponse.json();

  if (loginResponse.status === 200) {
    result.value = data;
    localStorage.setItem("token", data.token);
    localStorage.setItem(
      "name",
      JSON.stringify({ firstname: data.firstname, lastname: data.lastname })
    );
    router.push({ name: "home" });
  } else {
    result.value = data.errors;
  }
};
</script>

<style>
.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #ffffff;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group > label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-control {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.btn-primary {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: rgb(76, 120, 240);
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: rgb(6, 24, 104);
}

.alert {
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 4px;
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

.alert-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}
</style>
