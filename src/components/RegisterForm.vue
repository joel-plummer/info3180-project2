<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="registerUser" id="registerForm">
      <div v-if="result.errors">
        <ul class="alert alert-danger">
          <li v-for="error in result.errors">{{ error }}</li>
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
      <div class="form-group">
        <label for="firstname" class="form-label">First Name</label>
        <input
          name="firstname"
          type="text"
          class="form-control"
          placeholder="Enter your first name"
        />
      </div>
      <div class="form-group">
        <label for="lastname" class="form-label">Last Name</label>
        <input
          name="lastname"
          type="text"
          class="form-control"
          placeholder="Enter your last name"
        />
      </div>
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          name="email"
          type="email"
          class="form-control"
          placeholder="Enter your email"
        />
      </div>
      <div class="form-group">
        <label for="location" class="form-label">Location</label>
        <input
          name="location"
          type="text"
          class="form-control"
          placeholder="Enter your location"
        />
      </div>
      <div class="form-group">
        <label for="biography" class="form-label">Biography</label>
        <textarea
          row="10"
          name="biography"
          class="form-control"
          placeholder="Enter your biography"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="profile_photo" class="form-label">Profile Photo</label>
        <input type="file" name="profile_photo" class="form-control-file" />
      </div>
      <input type="submit" class="btn btn-primary" value="Register" />
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
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

const registerUser = () => {
  let registerForm = document.getElementById("registerForm");
  let form_data = new FormData(registerForm);

  fetch("/api/v1/register", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      result.value = data;
    })
    .catch((err) => {
      console.error("There was a problem with the fetch operation: ", err);
      result.value = err;
    });
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
