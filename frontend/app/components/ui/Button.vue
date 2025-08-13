<template>
  <component
    :is="as"
    :href="as === 'a' ? href : undefined"
    :type="as === 'button' ? type : undefined"
    :disabled="disabled || loading"
    :class="buttonClasses"
    v-bind="$attrs"
    @click="handleClick"
  >
    <Icon
      v-if="loading"
      name="lucide:loader-2"
      class="animate-spin"
      :class="iconSizeClasses"
    />
    <Icon
      v-else-if="icon && iconPosition === 'left'"
      :name="icon"
      :class="[iconSizeClasses, { 'mr-2': $slots.default }]"
    />
    
    <slot />
    
    <Icon
      v-if="!loading && icon && iconPosition === 'right'"
      :name="icon"
      :class="[iconSizeClasses, { 'ml-2': $slots.default }]"
    />
  </component>
</template>

<script setup lang="ts">
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  as?: 'button' | 'a'
  type?: 'button' | 'submit' | 'reset'
  href?: string
  disabled?: boolean
  loading?: boolean
  icon?: string
  iconPosition?: 'left' | 'right'
  block?: boolean
}

interface ButtonEmits {
  (e: 'click', event: Event): void
}

const props = withDefaults(defineProps<ButtonProps>(), {
  variant: 'primary',
  size: 'md',
  as: 'button',
  type: 'button',
  iconPosition: 'left',
  disabled: false,
  loading: false,
  block: false
})

const emit = defineEmits<ButtonEmits>()

// Base classes using Tailwind
const baseClasses = [
  'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
  'border rounded-md'
]

// Variant classes
const variantClasses = {
  primary: [
    'bg-primary-600 text-white border-primary-600',
    'hover:bg-primary-700 hover:border-primary-700',
    'focus:ring-primary-500',
    'active:bg-primary-800'
  ],
  secondary: [
    'bg-muted-600 text-black dark:text-white border-secondary-500',
    'hover:bg-muted-700 hover:border-secondary-900',
    'focus:ring-muted-500',
    'active:bg-muted-800'
  ],
  outline: [
    'bg-transparent text-primary-600 border-border',
    'hover:bg-primary-600 hover:text-white hover:border-primary-600',
    'focus:ring-primary-500'
  ],
  ghost: [
    'bg-transparent text-text-primary border-transparent',
    'hover:bg-surface hover:text-text-primary',
    'focus:ring-primary-500'
  ],
  destructive: [
    'bg-red-600 text-white border-red-600',
    'hover:bg-red-700 hover:border-red-700',
    'focus:ring-red-500',
    'active:bg-red-800'
  ]
}

// Size classes
const sizeClasses = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
  xl: 'px-8 py-4 text-xl'
}

// Icon size classes
const iconSizeMap = {
  sm: 'w-4 h-4',
  md: 'w-5 h-5',
  lg: 'w-6 h-6',
  xl: 'w-7 h-7'
}

// Computed classes
const buttonClasses = computed(() => [
  ...baseClasses,
  ...variantClasses[props.variant],
  sizeClasses[props.size],
  {
    'w-full': props.block,
    'cursor-not-allowed': props.disabled || props.loading
  }
])

const iconSizeClasses = computed(() => iconSizeMap[props.size])

// Handle click events
const handleClick = (event: Event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>
