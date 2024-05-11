<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <h2 @click="$router.push('/')">ContextDB</h2>
        <RouterLink to="/" active-class="active">Home</RouterLink>
        <RouterLink to="/about" active-class="active">About</RouterLink>
      </nav>
  </header>

  <RouterView />
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap');

h2 {
  font-family: 'Poppins', sans-serif;
  margin-right: 10px;
  cursor: pointer;
}

header {
  background-color: var(--header-bg-color);
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

nav {
  display: flex;
  justify-content: start;
  align-items: center;
}

nav a {
  text-decoration: none;
  color: var(--text-active-color);
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

nav a:hover {
  background-color: var(--link-hover-bg-color);
}

.active {
  color: var(--active-link-color);
}
</style>