<template>
  <div class="w-full">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-text-primary mb-2">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    
    <div class="relative">
      <Icon
        v-if="leftIcon"
        :name="leftIcon"
        :class="[
          'absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted pointer-events-none',
          iconSizeClasses
        ]"
      />
      
      <input
        :id="inputId"
        :value="modelValue"
        :class="inputClasses"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :autocomplete="autocomplete"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
      />
      
      <Icon
        v-if="rightIcon"
        :name="rightIcon"
        :class="[
          'absolute right-3 top-1/2 transform -translate-y-1/2 text-text-muted pointer-events-none',
          iconSizeClasses
        ]"
      />
    </div>
    
    <p v-if="error" class="mt-2 text-sm text-red-500">
      {{ error }}
    </p>
    
    <p v-else-if="hint" class="mt-2 text-sm text-text-muted">
      {{ hint }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface InputProps {
  modelValue?: string | number
  label?: string
  placeholder?: string
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search'
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  error?: string
  hint?: string
  leftIcon?: string
  rightIcon?: string
  size?: 'sm' | 'md' | 'lg'
  autocomplete?: string
}

interface InputEmits {
  (e: 'update:modelValue', value: string): void
  (e: 'focus', event: FocusEvent): void
  (e: 'blur', event: FocusEvent): void
}

const props = withDefaults(defineProps<InputProps>(), {
  type: 'text',
  size: 'md',
  disabled: false,
  readonly: false,
  required: false
})

const emit = defineEmits<InputEmits>()

// Generate unique ID for accessibility
const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

// Size classes
const sizeClasses = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-3 py-2 text-base',
  lg: 'px-4 py-3 text-lg'
}

// Icon size classes
const iconSizeMap = {
  sm: 'w-4 h-4',
  md: 'w-5 h-5',
  lg: 'w-6 h-6'
}

// Base input classes using Tailwind
const baseClasses = [
  'w-full border rounded-md shadow-sm transition-all duration-200 bg-white dark:bg-gray-800',
  'focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500',
  'placeholder:text-text-muted',
  'disabled:bg-muted-100 dark:disabled:bg-muted-800 disabled:text-text-muted disabled:cursor-not-allowed disabled:border-border',
  'readonly:bg-muted-50 dark:readonly:bg-muted-900 readonly:text-text-secondary'
]

// State-dependent classes
const stateClasses = computed(() => {
  if (props.error) {
    return [
      'border-red-300 text-red-900',
      'bg-red-50 dark:bg-red-950/10',
      'focus:border-red-500 focus:ring-red-500/20'
    ]
  }
  
  return [
    'border-border text-text-primary',
    'bg-white dark:bg-surface',
    'hover:border-border-hover'
  ]
})

// Padding adjustments for icons
const paddingClasses = computed(() => {
  const base = sizeClasses[props.size]
  
  if (props.leftIcon && props.rightIcon) {
    return base.replace('px-3', 'pl-10 pr-10').replace('px-4', 'pl-12 pr-12')
  } else if (props.leftIcon) {
    return base.replace('px-3', 'pl-10 pr-3').replace('px-4', 'pl-12 pr-4')
  } else if (props.rightIcon) {
    return base.replace('px-3', 'pl-3 pr-10').replace('px-4', 'pl-4 pr-12')
  }
  
  return base
})

// Computed classes
const inputClasses = computed(() => [
  ...baseClasses,
  ...stateClasses.value,
  paddingClasses.value
])

const iconSizeClasses = computed(() => iconSizeMap[props.size])

// Event handlers
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}
</script>
