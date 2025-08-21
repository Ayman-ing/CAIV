<script setup lang="ts">
// Experience data and state
const experienceData = ref([])
const isExpanded = ref(false)
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const handleAddExperience = () => {
  // TODO: Navigate to add experience page or open modal
  console.log('Add work experience')
  navigateTo('/profile/experience/add')
}
</script>

<template>
  <CollapsibleSection
    title="Work Experience"
    description="Add your professional work history"
    icon="heroicons:briefcase"
    icon-color="text-blue-600 dark:text-blue-400"
    icon-bg-color="bg-blue-100 dark:bg-blue-900/30"
    button-color="bg-blue-600 dark:bg-blue-500 hover:bg-blue-700 dark:hover:bg-blue-600"
    :is-expanded="isExpanded"
    :is-empty="experienceData.length === 0"
    empty-message="No work experience added yet"
    add-button-text="Add Work Experience"
    @toggle="toggleSection"
    @add="handleAddExperience"
  >
    <!-- Experience List Content (when not empty) -->
    <div v-if="experienceData.length > 0" class="space-y-4">
      <!-- Experience items will go here -->
      <div v-for="(item, index) in experienceData" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <!-- Experience item content -->
      </div>
    </div>
  </CollapsibleSection>
</template>
