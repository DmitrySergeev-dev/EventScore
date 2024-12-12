<script setup>
import { ref, computed } from 'vue'
import Home from './pages/Home.vue'
import About from './pages/About.vue'
import NotFound from './pages/NotFound.vue'
import Navbar from './components/Navbar.vue'

const routes = {
  '/': Home,
  '/about': About,
  '/notFound': NotFound
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/']
})
</script>

<template>
  <div class="app-container"> <!-- Добавьте контейнер -->
    <Navbar />
    <component :is="currentView" />
  </div>
</template>







