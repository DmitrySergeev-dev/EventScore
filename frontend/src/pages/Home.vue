<script setup>
import {ref, onMounted} from 'vue'
import {fetchNews, createNews, deleteNews} from '@/api/news.ts'
import NewsList from '@/components/NewsList.vue'
import NewsForm from '@/components/NewsForm.vue'

const news = ref([])

onMounted(async () => {
  news.value = await fetchNews()
})

const addNewsItem = async (newsItem) => {
  await createNews(newsItem)
  news.value = await fetchNews()
}

const removeNewsItem = async (newsItem) => {
  await deleteNews(newsItem.pk)
  news.value = await fetchNews()
}
</script>

<template>
  <NewsForm @newsCreated="addNewsItem"/>
  <NewsList :news="news" @removeNewsItem="removeNewsItem"/>
</template>
