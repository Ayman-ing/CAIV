<template>
  <div :class="cardClasses" @click="handleClick">
    <div v-if="title || subtitle || $slots.header" class="px-6 py-4 border-b border-border">
      <slot name="header">
        <h3 v-if="title" class="text-lg font-semibold text-text-primary dark:text-white">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="text-sm text-text-secondary mt-1 dark:text-white">
          {{ subtitle }}
        </p>
      </slot>
    </div>
    
    <div v-if="$slots.default" class="px-6 py-4 dark:text-white">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="px-6 py-4 border-t border-border bg-surface ">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface CardProps {
  title?: string
  subtitle?: string
  variant?: 'default' | 'outline' | 'ghost'
  shadow?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  hover?: boolean
  clickable?: boolean
}

interface CardEmits {
  (e: 'click', event: Event): void
}

const props = withDefaults(defineProps<CardProps>(), {
  variant: 'default',
  shadow: 'sm',
  hover: false,
  clickable: false
})

const emit = defineEmits<CardEmits>()

// Base classes
const baseClasses = [
  'rounded-lg transition-all duration-200 overflow-hidden'
]

// Variant classes
const variantClasses = {
  default: 'bg-surface border border-border',
  outline: 'bg-transparent border border-border',
  ghost: 'bg-transparent border-0'
}

// Shadow classes
const shadowClasses = {
  none: '',
  sm: 'shadow-sm',
  md: 'shadow-md',
  lg: 'shadow-lg',
  xl: 'shadow-xl'
}

// Hover and clickable classes
const interactiveClasses = computed(() => {
  const classes = []
  
  if (props.hover || props.clickable) {
    classes.push('hover:shadow-md', 'hover:border-border-hover')
  }
  
  if (props.clickable) {
    classes.push('cursor-pointer', 'hover:bg-surface-hover')
  }
  
  return classes
})

// Computed classes
const cardClasses = computed(() => [
  ...baseClasses,
  variantClasses[props.variant],
  shadowClasses[props.shadow],
  ...interactiveClasses.value
])

// Handle click events
const handleClick = (event: Event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>
