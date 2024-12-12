<script setup>
import {ref} from 'vue'

let newsItem = ref(
    {
      description: "",
      deadline: ""
    }
)
const emit = defineEmits(['newsCreated',])

function createNewsItem() {
  emit('newsCreated', newsItem.value)
  newsItem.value = {
    description: "",
    deadline: ""
  }
}

</script>

<template>
  <form @submit.prevent>
    <h4>Добавление новости</h4>
    <my-input
        v-focus
        v-model="newsItem.description"
        type="text"
        placeholder="Описание"
    />
    <my-input
        v-model="newsItem.deadline"
        type="text"
        placeholder="Дедлайн"
    />
    <my-button
        style="align-self: flex-end; margin-top: 15px"
        @click="createNewsItem"
    >
      Создать
    </my-button>
  </form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
}

</style>