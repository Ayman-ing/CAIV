<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  initialTitle?: string
}>()

const emit = defineEmits<{
  confirm: [title: string]
  cancel: []
}>()

const title = ref(props.initialTitle || 'My Resume')
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
        Save Draft
      </h3>
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
        Give your draft a name so you can find it later.
      </p>
      <input
        v-model="title"
        placeholder="Draft name"
        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        @keydown.enter="title.trim() && emit('confirm', title.trim())"
      >
      <div class="flex justify-end space-x-3">
        <button
          class="px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:underline"
          @click="emit('cancel')"
        >
          Cancel
        </button>
        <button
          class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          :disabled="!title.trim()"
          @click="emit('confirm', title.trim())"
        >
          Save
        </button>
      </div>
    </div>
  </div>
</template>