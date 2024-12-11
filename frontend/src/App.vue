<script setup>
import { ref, onMounted } from 'vue'
import { fetchNews } from './api/news.js'

const news = ref([]) // Инициализируем news как пустой массив

onMounted(async () => {
    news.value = await fetchNews() // Обновляем значение news после получения данных
})
</script>

<template>
    <ul>
        <li v-for="item in news" :key="item.pk">
            {{ item.description }}: {{ item.status }}
        </li>
    </ul>
</template>