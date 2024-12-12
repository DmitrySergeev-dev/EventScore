<script setup>
import formatDatetime from '@/utils/datetimeHelpers.ts'

const props = defineProps(
    {
      newsItem: {
        type: Object,
        required: true,
      }
    }
)

</script>

<template>
  <div class="newsItem">
    <div>
      <div>
      <strong>Описание: </strong>{{ newsItem.description }}
      </div>

      <div>
        <strong>Статус: </strong>{{ newsItem.status }}
      </div>

      <div>
        <strong>Дедлайн: </strong>{{ formatDatetime(newsItem.deadline) }}
      </div>
    </div>

  <div class="news_item__btns">
    <my-button
        @click="$emit('remove', newsItem)"
    >
      Удалить
    </my-button>
  </div>
  </div>
</template>


<style scoped>
.newsItem {
  padding: 15px;
  border: 2px solid teal;
  margin-top: 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.news_item__btns {
  display: flex;
}
</style>