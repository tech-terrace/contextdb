<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <h1 @click="$router.push('/')">ContextDB</h1>
      <RouterLink to="/" active-class="active">Home</RouterLink>
      <RouterLink to="/about" active-class="active">About</RouterLink>
      <a href="/docs" active-class="active" target="_blank" rel="noopener noreferrer">Docs</a>
      <a href="https://forms.gle/RueGppsHpuvFVYkm7" target="_blank" rel="noopener noreferrer">Suggest Tool</a>
      <a href="https://github.com/tech-terrace/contextdb" target="_blank" rel="noopener noreferrer" class="github-link">
        <svg height="24" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="24" data-view-component="true">
          <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
        </svg>
      </a>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap');

h1 {
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
  flex-wrap: wrap;
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

nav a.github-link {
  padding: 0 8px;
  display: flex;
  align-items: center;
}

nav a.github-link svg {
  fill: var(--text-active-color);
  transition: fill 0.3s;
}

nav a.github-link:hover svg {
  fill: var(--active-link-color);
}

@media (max-width: 768px) {
  nav {
    flex-direction: column;
    align-items: flex-start;
  }

  h1 {
    margin-bottom: 10px;
  }

  nav a {
    width: 100%;
    padding: 10px 16px;
    margin-bottom: 5px;
  }

  nav a.github-link {
    padding: 10px 16px;
    justify-content: flex-start;
  }
}
</style>