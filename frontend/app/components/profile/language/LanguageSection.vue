<script setup lang="ts">
// Languages data and state
const languagesData = ref([])
const isExpanded = ref(false)
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const handleAddLanguage = () => {
  // TODO: Navigate to add language page or open modal
  console.log('Add language')
  navigateTo('/profile/languages/add')
}
</script>

<template>
  <CollapsibleSection
    title="Languages"
    description="Add languages you speak"
    icon="heroicons:language"
    icon-color="text-indigo-600 dark:text-indigo-400"
    icon-bg-color="bg-indigo-100 dark:bg-indigo-900/30"
    button-color="bg-indigo-600 dark:bg-indigo-500 hover:bg-indigo-700 dark:hover:bg-indigo-600"
    :is-expanded="isExpanded"
    :is-empty="languagesData.length === 0"
    empty-message="No languages added yet"
    add-button-text="Add Language"
    @toggle="toggleSection"
    @add="handleAddLanguage"
  >
    <!-- Languages List Content (when not empty) -->
    <div v-if="languagesData.length > 0" class="space-y-4">
      <!-- Language items will go here -->
      <div v-for="(item, index) in languagesData" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <!-- Language item content -->
      </div>
    </div>
  </CollapsibleSection>
</template>
