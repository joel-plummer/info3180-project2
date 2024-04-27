<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">📷 Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <!-- <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li> -->
            <!-- <li class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li> -->
            <li class="nav-item">
              <RouterLink class="nav-link" :to="`/users/${userId}/`"
                >My Profile</RouterLink
              >
            </li>
            <li>
              <RouterLink class="nav-link" to="/posts/new">New Post</RouterLink>
            </li>
            <li>
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li>
              <RouterLink class="nav-link" to="/logout" @click="logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { jwtDecode } from "jwt-decode";
import { useRouter } from "vue-router";

const router = useRouter();

let token = localStorage.getItem("token");

if (!token) {
  router.push({ name: "login" });
}

let decodedToken = jwtDecode(token);

const userId = decodedToken.sub;

if (!userId) {
  router.push({ name: "login" });
}

const logout = () => {
  localStorage.removeItem("token");
  router.push({ name: "login" });
};
</script>

<style>
.navbar-brand {
  font-size: 1.5rem;
  font-weight: bolder;
}
</style>
