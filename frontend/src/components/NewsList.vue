<script setup lang="ts">
import NewsItem from "@/components/NewsItem.vue";

interface News {
  pk: string;
  description: string;
  status: string;
  deadline: string;
}

const props = defineProps<{
  news: [News];
}>();
</script>

<template>
  <div v-if="news.length > 0">
    <h3>Список новостей</h3>
    <transition-group name="user-list">
      <NewsItem
        v-for="item in news"
        :newsItem="item"
        :key="item.pk"
        @remove="$emit('removeNewsItem', item);"
      />
    </transition-group>
  </div>
  <h2 v-else style="color: red">
    Список новостей пуст
  </h2>
</template>

<style scoped>
.user-list-item {
  display: inline-block;
  margin-right: 10px;
}
.user-list-enter-active,
.user-list-leave-active {
  transition: all 0.4s ease;
}
.user-list-enter-from,
.user-list-leave-to {
  opacity: 0;
  transform: translateX(130px);
}
.user-list-move {
  transition: transform 0.4s ease;
}
</style>
