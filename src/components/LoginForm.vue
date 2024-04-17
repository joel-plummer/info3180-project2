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
        <input name="username" type="text" class="form-control" />
      </div>
      <div class="form-group">
        <label for="password" class="form-label">password</label>
        <input name="password" type="password" class="form-control" />
      </div>
      <input type="submit" />
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
      console.log(csrf_token.value);
    });
};

onMounted(() => {
  getCsrfToken();
});

const loginUser = async () => {
  let loginForm = document.getElementById("loginForm");
  let form_data = new FormData(loginForm);
  console.log(...form_data.entries());
  console.log("CSRF Token:", csrf_token.value); // Log the CSRF token

  const loginResponse = await fetch("/api/v1/auth/login", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  });

  console.log("The Response", loginResponse);
  const data = await loginResponse.json();

  if (loginResponse.status === 200) {
    result.value = data;
    console.log(data);
    localStorage.setItem("token", data.token);
    localStorage.setItem("user_id", data.id);
    router.push({ name: "home" });
  } else {
    result.value = data.errors;
  }
};
</script>

<style>
.register {
  padding: 20px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
}
form {
  display: flex;
  flex-direction: column;
}
.form-group {
  display: flex;
  flex-direction: column;
  margin: 10px 0;
}

.form-group > label {
  font-weight: bold;
}

input[type="submit"] {
  margin-top: 20px;
  width: 100px;
  border: none;
  background: rgb(76, 120, 240);
  border-radius: 5%;
  color: #fff;
}

input[type="submit"]:hover {
  cursor: pointer;
  background: rgb(6, 24, 104);
}

.alert {
  padding-left: 50px;
}
</style>
