<script setup lang="ts">
// Certifications data and state
const certificationsData = ref([])
const isExpanded = ref(false)
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const handleAddCertification = () => {
  // TODO: Navigate to add certification page or open modal
  console.log('Add certification')
  navigateTo('/profile/certifications/add')
}
</script>

<template>
  <CollapsibleSection
    title="Certifications"
    description="Add professional certifications"
    icon="heroicons:trophy"
    icon-color="text-yellow-600 dark:text-yellow-400"
    icon-bg-color="bg-yellow-100 dark:bg-yellow-900/30"
    button-color="bg-yellow-600 dark:bg-yellow-500 hover:bg-yellow-700 dark:hover:bg-yellow-600"
    :is-expanded="isExpanded"
    :is-empty="certificationsData.length === 0"
    empty-message="No certifications added yet"
    add-button-text="Add Certification"
    @toggle="toggleSection"
    @add="handleAddCertification"
  >
    <!-- Certifications List Content (when not empty) -->
    <div v-if="certificationsData.length > 0" class="space-y-4">
      <!-- Certification items will go here -->
      <div v-for="(item, index) in certificationsData" :key="index" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <!-- Certification item content -->
      </div>
    </div>
  </CollapsibleSection>
</template>
