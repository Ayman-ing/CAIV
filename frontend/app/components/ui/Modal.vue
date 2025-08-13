<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
        @click="handleOverlayClick"
      >
        <div
          :class="modalClasses"
          @click.stop
        >
          <!-- Header -->
          <div v-if="$slots.header || title" class="flex items-center justify-between px-6 py-4 border-b border-border">
            <slot name="header">
              <h2 v-if="title" class="text-xl font-semibold text-text-primary dark:text-white">{{ title }}</h2>
            </slot>
            
            <button
              v-if="closable"
              class="flex items-center justify-center w-8 h-8 text-text-muted  dark:text-white hover:text-text-primary hover:bg-muted-100 dark:hover:bg-muted-800 rounded-md transition-all duration-200"
              @click="close"
            >
              <Icon name="lucide:x" class="w-5 h-5" />
            </button>
          </div>
          
          <!-- Content -->
          <div class="px-6 py-4 text-text-primary dark:text-white">
            <slot />
          </div>
          
          <!-- Footer -->
          <div v-if="$slots.footer" class="flex gap-3 justify-end px-6 py-4 border-t border-border bg-muted-50 dark:bg-muted-900/50">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
interface ModalProps {
  modelValue: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  closable?: boolean
  closeOnOverlay?: boolean
}

interface ModalEmits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'close'): void
}

const props = withDefaults(defineProps<ModalProps>(), {
  size: 'md',
  closable: true,
  closeOnOverlay: true
})

const emit = defineEmits<ModalEmits>()

// Size classes using Tailwind
const sizeClasses = {
  sm: 'max-w-sm w-full',
  md: 'max-w-md w-full',
  lg: 'max-w-lg w-full',
  xl: 'max-w-2xl w-full',
  full: 'max-w-4xl w-full'
}

// Base modal classes
const baseClasses = [
  'bg-white dark:bg-gray-900',
  'rounded-lg',
  'shadow-xl',
  'max-h-[90vh]',
  'overflow-auto',
  'border',
  'border-border'
]

const modalClasses = computed(() => [
  ...baseClasses,
  sizeClasses[props.size]
])

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    close()
  }
}

// Handle escape key
onMounted(() => {
  const handleEscape = (event: KeyboardEvent) => {
    if (event.key === 'Escape' && props.modelValue && props.closable) {
      close()
    }
  }
  
  document.addEventListener('keydown', handleEscape)
  
  onUnmounted(() => {
    document.removeEventListener('keydown', handleEscape)
  })
})

// Lock body scroll when modal is open
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active > div,
.modal-leave-active > div {
  transition: transform 0.3s ease;
}

.modal-enter-from > div,
.modal-leave-to > div {
  transform: scale(0.9);
}
</style>
