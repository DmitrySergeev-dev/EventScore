<script setup lang="ts">
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
  <div class="newsItem" v-for="item in news" :key="item.pk">
    <div>
      <strong>
        Описание:
      </strong>
      {{ item.description }}
    </div>

    <div>
      <strong>
        Статус:
      </strong>
      {{ item.status }}
    </div>

    <div>
      <strong>
        Дедлайн:
      </strong>
      {{ item.deadline }}
    </div>
  </div>

</template>

<style>
.newsItem {
  padding: 15px;
  border: 2px solid teal;
  margin-top: 15px;
}
</style>