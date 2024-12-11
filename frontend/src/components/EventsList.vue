<script setup>
  const props = defineProps(['news'])
  console.log(props.news)
</script>

<template>
  <ul>
        <li v-for="item in props.news" :key="item.pk">
            {{ item.description }}: {{ item.status }}
        </li>
  </ul>
</template>