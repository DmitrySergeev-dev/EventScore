<script setup>
import { ref, onMounted } from 'vue'
import { fetchNews } from './api/news.js'
import EventsList  from './components/EventsList.vue'

const news = ref([]) // Инициализируем news как пустой массив

onMounted(async () => {
    news.value = await fetchNews() // Обновляем значение news после получения данных
})
</script>

<template>
  <EventsList :news=news />
</template>