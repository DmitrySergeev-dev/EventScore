<script setup>
import {ref, onMounted} from 'vue'
import {fetchNews, createNews, deleteNews} from '@/api/news.ts'
import NewsList from '@/components/NewsList.vue'
import NewsForm from '@/components/NewsForm.vue'
import MyButton from '@/components/UI/MyButton.vue'
import MyDialog from '@/components/UI/MyDialog.vue'

const news = ref([])
const dialogVisible = ref(false)

onMounted(async () => {
  news.value = await fetchNews()
})

const addNewsItem = async (newsItem) => {
  await createNews(newsItem)
  dialogVisible.value = false
  news.value = await fetchNews()
}

const removeNewsItem = async (newsItem) => {
  await deleteNews(newsItem.pk)
  news.value = await fetchNews()
}

const showDialog = async () => {
  dialogVisible.value = true
  console.log(`dialogVisible: ${dialogVisible.value}`)
}

function hideDialog() {
  dialogVisible.value = false
}

</script>

<template>
  <my-button @click="showDialog">Добавить новость</my-button>
  <my-dialog :show="dialogVisible" @hideDialog="hideDialog">
    <news-form @newsCreated="addNewsItem" />
  </my-dialog>
  <NewsList :news="news" @removeNewsItem="removeNewsItem" />
</template>

