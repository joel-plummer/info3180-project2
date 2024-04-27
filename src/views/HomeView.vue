<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="home">
    <div class="container">
      <div class="left">
        <img src="https://images.pexels.com/photos/456710/pexels-photo-456710.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" alt="">
      </div>
      <div class="right">
        <div class="card">
            <h2>Photogram</h2>
          <hr>
          <div class="text">
            Share photos of your favourite moments with friends, family and the world.
          </div>
          <div class="btn">
            <RouterLink class="link btn-register" to="/register">Register</RouterLink>
            <RouterLink  class="link btn-login" to="/login">Login</RouterLink>
          </div>
        </div>
      </div>
    </div>
    </div>
</template>

<style>

  .home{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 120px;
  }
  .container {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: center;

  }
  .left {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 400px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    overflow: hidden;
    border-radius: 10px;
  }
  .left > img {
    width: 110%;
  }

  .card {
    display: flex;
    width: 400px;
    min-height: 300px;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;
    /* border: 1px solid rgb(252, 184, 184); */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
  }
  .card > .logo > img {
    object-fit: contain;
    width: 20px;
  }

  .logo {
    display: flex;
    margin-top: 10px;
    align-items: center;
    gap: 10px;
  }

  .text {
    margin: 0 10px;
  }

  h2{
    margin-top: 20px;
  }

  hr {
    width: 90%;
  }

  .btn {
    width: 90%;
    display: flex;
    gap: 10px;
  }

  .btn .link {
    flex: 1;
    text-decoration: none;
    color: #fff;
    padding: 10px;
    border-radius: 5px;
  }

  .btn-register{
    background: rgb(36, 139, 36);
  }

  .btn-login{
    background: rgb(64, 64, 205);
  }
</style>
