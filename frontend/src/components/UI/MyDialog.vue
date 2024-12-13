<script setup>
const props = defineProps(
    {
      show: {
        type: Boolean,
        required: true,
      default: false
      },
    }
)

const emit = defineEmits(["hideDialog"])


</script>

<template>
  <div class="dialog" v-if="show" @click.stop="$emit('hideDialog')">
    <div @click.stop class="dialog__content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.dialog {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  display: flex;
}

.dialog__content {
  margin: auto;
  background: white;
  border-radius: 12px;
  min-height: 50px;
  min-width: 300px;
  padding: 20px;
}
</style>
