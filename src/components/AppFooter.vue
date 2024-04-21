<template>
  <div class="wrapper">
    <main>
      <!-- Your main content here -->
    </main>
    <footer>
      <div class="container">
        <p>Copyright &copy; {{ year }} Flask Inc.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
const year = new Date().getFullYear();
</script>

<style>
.wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}

footer {
  padding-top: 10px;
  background-color:#333 ;
  color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  position: sticky;
  bottom: 0;
}

.container {
  text-align: center;
}
</style>
