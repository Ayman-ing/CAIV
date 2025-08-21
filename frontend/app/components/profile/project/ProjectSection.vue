<script setup lang="ts">
// Projects data and state
const projectsData = ref([])
const isExpanded = ref(false)
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const handleAddProject = () => {
  // TODO: Navigate to add project page or open modal
  console.log('Add project')
  navigateTo('/profile/projects/add')
}
</script>

<template>
  <CollapsibleSection
    title="Projects"
    description="Showcase your notable projects"
    icon="heroicons:code-bracket"
    icon-color="text-orange-600 dark:text-orange-400"
    icon-bg-color="bg-orange-100 dark:bg-orange-900/30"
    button-color="bg-orange-600 dark:bg-orange-500 hover:bg-orange-700 dark:hover:bg-orange-600"
    :is-expanded="isExpanded"
    :is-empty="projectsData.length === 0"
    empty-message="No projects added yet"
    add-button-text="Add Project"
    @toggle="toggleSection"
    @add="handleAddProject"
  >
    <!-- Projects List Content (when not empty) -->
    <div v-if="projectsData.length > 0" class="space-y-4">
      <!-- Project items will go here -->
      <div v-for="(item, index) in projectsData" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <!-- Project item content -->
      </div>
    </div>
  </CollapsibleSection>
</template>
