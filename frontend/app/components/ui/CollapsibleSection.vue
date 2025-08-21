<script setup lang="ts">
interface Props {
  title: string
  description: string
  icon: string
  iconColor: string
  iconBgColor: string
  buttonColor: string
  isExpanded: boolean
  isEmpty?: boolean
  emptyMessage?: string
  addButtonText?: string
}

const props = withDefaults(defineProps<Props>(), {
  isEmpty: false,
  emptyMessage: 'No items added yet',
  addButtonText: 'Add Item'
})

const emit = defineEmits<{
  toggle: []
  add: []
}>()

const handleToggle = () => {
  emit('toggle')
}

const handleAdd = () => {
  emit('add')
}
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700">
    <!-- Header Button -->
    <button
      @click="handleToggle"
      class="w-full flex items-center justify-between p-6 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 rounded-lg"
    >
      <div class="flex items-center space-x-4">
        <div :class="`p-3 ${iconBgColor} rounded-lg`">
          <Icon :name="icon" :class="`w-6 h-6 ${iconColor}`" />
        </div>
        <div class="text-left">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ title }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ description }}</p>
        </div>
      </div>
      <Icon 
        name="heroicons:chevron-down" 
        class="w-5 h-5 text-gray-500 dark:text-gray-400 transition-transform"
        :class="{ 'rotate-180': isExpanded }"
      />
    </button>
    
    <!-- Expandable Content -->
    <div v-if="isExpanded" class="px-6 pb-6">
      <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
        <!-- Empty State -->
        <div v-if="isEmpty" class="text-center py-8">
          <p class="text-gray-500 dark:text-gray-400 mb-4">{{ emptyMessage }}</p>
          <button 
            @click="handleAdd"
            :class="`px-4 py-2 ${buttonColor} text-white rounded-lg hover:opacity-90 transition-colors`"
          >
            {{ addButtonText }}
          </button>
        </div>
        
        <!-- Content Slot -->
        <div v-else>
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>
