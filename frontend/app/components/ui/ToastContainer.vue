<script setup lang="ts">
import Toast from '~/components/ui/Toast.vue'
import { useToast } from '~/composables/useToast'

const { toasts, removeToast } = useToast()
</script>

<template>
  <div class="fixed top-4 right-4 z-50 max-w-sm">
    <TransitionGroup name="toast-list">
      <Toast
        v-for="toast in toasts"
        :key="toast.id"
        :id="toast.id"
        :message="toast.message"
        :type="toast.type"
        :duration="toast.duration"
        @close="removeToast(toast.id)"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}

.toast-list-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.toast-list-leave-to {
  opacity: 0;
  transform: translateX(10px);
}

.toast-list-move {
  transition: transform 0.3s ease;
}
</style>
