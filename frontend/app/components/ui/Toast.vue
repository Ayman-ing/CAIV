<script setup lang="ts">
import { computed, onMounted } from 'vue'

interface ToastProps {
  id: string
  message: string
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

const props = withDefaults(defineProps<ToastProps>(), {
  type: 'info',
  duration: 4000
})

const emit = defineEmits<{
  (e: 'close'): void
}>()

// Get icon and colors based on type
const typeConfig = computed(() => {
  const configs = {
    success: {
      icon: 'mdi:check-circle',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      borderColor: 'border-green-200 dark:border-green-800',
      textColor: 'text-green-800 dark:text-green-200',
      iconColor: 'text-green-600 dark:text-green-400'
    },
    error: {
      icon: 'mdi:alert-circle',
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      borderColor: 'border-red-200 dark:border-red-800',
      textColor: 'text-red-800 dark:text-red-200',
      iconColor: 'text-red-600 dark:text-red-400'
    },
    warning: {
      icon: 'mdi:alert',
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
      borderColor: 'border-yellow-200 dark:border-yellow-800',
      textColor: 'text-yellow-800 dark:text-yellow-200',
      iconColor: 'text-yellow-600 dark:text-yellow-400'
    },
    info: {
      icon: 'mdi:information',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      borderColor: 'border-blue-200 dark:border-blue-800',
      textColor: 'text-blue-800 dark:text-blue-200',
      iconColor: 'text-blue-600 dark:text-blue-400'
    }
  }
  return configs[props.type]
})

// Auto close after duration
onMounted(() => {
  if (props.duration > 0) {
    setTimeout(() => {
      emit('close')
    }, props.duration)
  }
})
</script>

<template>
  <Transition
    name="toast"
    @enter="(el) => { (el as HTMLElement).style.opacity = '0' }"
    @after-enter="(el) => { (el as HTMLElement).style.opacity = '1' }"
  >
    <div
      :class="[
        'flex items-start gap-3 px-4 py-3 rounded-lg border mb-3 last:mb-0',
        typeConfig.bgColor,
        typeConfig.borderColor,
        typeConfig.textColor
      ]"
    >
      <Icon :name="typeConfig.icon" :class="['w-5 h-5 flex-shrink-0 mt-0.5', typeConfig.iconColor]" />
      <p class="flex-grow text-sm font-medium">{{ message }}</p>
      <button
        @click="emit('close')"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
      >
        <Icon name="mdi:close" class="w-4 h-4" />
      </button>
    </div>
  </Transition>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(10px);
}
</style>
