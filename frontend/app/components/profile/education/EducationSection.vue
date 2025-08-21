<script setup lang="ts">
// Education data and state
const educationData = ref([])
const isExpanded = ref(false)
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const handleAddEducation = () => {
  // TODO: Navigate to add education page or open modal
  console.log('Add education')
  navigateTo('/profile/education/add')
}
</script>

<template>
  <CollapsibleSection
    title="Education"
    description="Add your educational background"
    icon="heroicons:academic-cap"
    icon-color="text-green-600 dark:text-green-400"
    icon-bg-color="bg-green-100 dark:bg-green-900/30"
    button-color="bg-green-600 dark:bg-green-500 hover:bg-green-700 dark:hover:bg-green-600"
    :is-expanded="isExpanded"
    :is-empty="educationData.length === 0"
    empty-message="No education added yet"
    add-button-text="Add Education"
    @toggle="toggleSection"
    @add="handleAddEducation"
  >
    <!-- Education List Content (when not empty) -->
    <div v-if="educationData.length > 0" class="space-y-4">
      <!-- Education items will go here -->
      <div v-for="(item, index) in educationData" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <!-- Education item content -->
      </div>
    </div>
  </CollapsibleSection>
</template>
