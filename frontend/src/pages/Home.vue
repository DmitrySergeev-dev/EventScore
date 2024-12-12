<script setup>
import {ref, onMounted} from 'vue'
import {fetchNews} from '@/api/news.js'
import NewsList from '@/components/NewsList.vue'
import NewsForm from '@/components/NewsForm.vue'

const news = ref([]) // Инициализируем news как пустой массив

onMounted(async () => {
  news.value = await fetchNews() // Обновляем значение news после получения данных
})

function addNewsItem(newsItem){
  news.value.push(newsItem)
}
</script>

<template>
  <NewsForm @newsCreated="addNewsItem" />
  <NewsList :news=news />
</template>
