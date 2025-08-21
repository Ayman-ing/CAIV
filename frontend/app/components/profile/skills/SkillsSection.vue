<script setup lang="ts">
// Skills data and state
const skillsData = ref([])
const isExpanded = ref(false)
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const handleAddSkills = () => {
  // TODO: Navigate to add skills page or open modal
  console.log('Add skills')
  navigateTo('/profile/skills/add')
}
</script>

<template>
  <CollapsibleSection
    title="Skills"
    description="Add your technical and soft skills"
    icon="heroicons:star"
    icon-color="text-purple-600 dark:text-purple-400"
    icon-bg-color="bg-purple-100 dark:bg-purple-900/30"
    button-color="bg-purple-600 dark:bg-purple-500 hover:bg-purple-700 dark:hover:bg-purple-600"
    :is-expanded="isExpanded"
    :is-empty="skillsData.length === 0"
    empty-message="No skills added yet"
    add-button-text="Add Skills"
    @toggle="toggleSection"
    @add="handleAddSkills"
  >
    <!-- Skills List Content (when not empty) -->
    <div v-if="skillsData.length > 0" class="space-y-4">
      <!-- Skills items will go here -->
      <div v-for="(item, index) in skillsData" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <!-- Skills item content -->
      </div>
    </div>
  </CollapsibleSection>
</template>
