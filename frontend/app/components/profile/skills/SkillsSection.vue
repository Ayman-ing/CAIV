<script setup lang="ts">
// filepath: frontend/app/components/profile/skills/SkillsSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { useToast } from '~/composables/useToast'
import type { Skill, SkillFormData, SkillGroup } from './types'
import { SKILL_CATEGORIES, PROFICIENCY_LEVELS } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()

// Skills Data
const skills = ref<Skill[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingSkill = ref<Skill | null>(null)

// Delete confirmation modal state
const isDeleteModalOpen = ref(false)
const skillToDelete = ref<Skill | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<SkillFormData>({
  category: '',
  name: '',
  proficiency: ''
})

onMounted(async () => {
  await fetchSkills()
})

const fetchSkills = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllSkills(activeProfile.value.uuid)
    skills.value = data
  } catch (error) {
    console.error('Failed to fetch skills:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingSkill.value = null
  formData.value = {
    category: '',
    name: '',
    proficiency: ''
  }
  isModalOpen.value = true
}

const openEditModal = (skill: Skill) => {
  isEditing.value = true
  editingSkill.value = skill
  formData.value = {
    category: skill.category || '',
    name: skill.name,
    proficiency: skill.proficiency || ''
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  const payload: Omit<Skill, 'uuid'> = {
    name: formData.value.name.trim(),
    category: formData.value.category.trim() || null,
    proficiency: formData.value.proficiency || null
  }

  try {
    if (isEditing.value && editingSkill.value) {
      await profileSectionsService.updateSkill(
        activeProfile.value.uuid,
        editingSkill.value.uuid,
        payload
      )
      success('Skill updated successfully!')
    } else {
      await profileSectionsService.createSkill(activeProfile.value.uuid, payload)
      success('Skill added successfully!')
    }
    await fetchSkills()
    closeModal()
  } catch (err) {
    console.error('Failed to save skill:', err)
    error(`Failed to save skill: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingSkill.value = null
}

const openDeleteModal = (skill: Skill) => {
  skillToDelete.value = skill
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  skillToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !skillToDelete.value) {
    console.error('Delete aborted: profile or skill missing', { 
      profileUuid: activeProfile.value?.uuid, 
      skill: skillToDelete.value 
    })
    return
  }
  
  isDeleting.value = true
  try {
    console.log(`Deleting skill ${skillToDelete.value.uuid} for profile ${activeProfile.value.uuid}`)
    const result = await profileSectionsService.deleteSkill(activeProfile.value.uuid, skillToDelete.value.uuid)
    console.log('Delete result:', result)
    await fetchSkills()
    closeDeleteModal()
    success('Skill deleted successfully!')
  } catch (err) {
    console.error('Failed to delete skill:', err)
    error(`Failed to delete skill: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' && formData.value.category.trim() !== ''
})

const hasSkills = computed(() => {
  return skills.value.length > 0
})

// Group skills by category for better display
const groupedSkills = computed((): SkillGroup[] => {
  const groups = new Map<string, Skill[]>()
  
  skills.value.forEach(skill => {
    const category = skill.category || 'Other'
    if (!groups.has(category)) {
      groups.set(category, [])
    }
    groups.get(category)?.push(skill)
  })
  
  return Array.from(groups.entries()).map(([category, categorySkills]) => ({
    category,
    skills: categorySkills.sort((a, b) => a.name.localeCompare(b.name)),
    count: categorySkills.length
  })).sort((a, b) => a.category.localeCompare(b.category))
})

const getProficiencyColor = (proficiency: string | null) => {
  if (!proficiency) return 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
  const colors = {
    'Beginner': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800',
    'Intermediate': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800',
    'Advanced': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800',
    'Expert': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800'
  }
  return colors[proficiency as keyof typeof colors] || 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600'
}

const getProficiencyLabel = (proficiency: string | null) => {
  if (!proficiency) return 'Not specified'
  return PROFICIENCY_LEVELS.find(level => level.value === proficiency)?.label || proficiency
}
</script>

<template>
  <CollapsibleSection
    title="Skills"
    description="Your technical and professional skills"
    icon="mdi:star"
    icon-color="text-purple-600 dark:text-purple-400"
    icon-bg-color="bg-purple-100 dark:bg-purple-900/30"
    button-color="bg-purple-600 dark:bg-purple-500 hover:bg-purple-700 dark:hover:bg-purple-600"
    :is-expanded="isExpanded"
    :is-empty="!isLoading && !hasSkills"
    empty-message="Add your skills"
    add-button-text="Add Skill"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-purple-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasSkills" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:star-check" class="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <div>
              <p class="text-sm font-medium text-purple-700 dark:text-purple-300">Total Skills</p>
              <p class="text-xs text-purple-600 dark:text-purple-400">{{ skills.length }} skill{{ skills.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <Icon name="mdi:shape" class="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <div>
              <p class="text-sm font-medium text-purple-700 dark:text-purple-300">Categories</p>
              <p class="text-xs text-purple-600 dark:text-purple-400">{{ groupedSkills.length }} categor{{ groupedSkills.length !== 1 ? 'ies' : 'y' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Skill
        </button>
      </div>

      <!-- Skills by Category -->
      <div class="space-y-6">
        <div v-for="group in groupedSkills" :key="group.category" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <!-- Category Header -->
          <div class="flex items-center justify-between mb-4 pb-2 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
              <Icon name="mdi:folder-outline" class="w-5 h-5 mr-2 text-purple-600 dark:text-purple-400" />
              {{ group.category }}
            </h3>
            <span class="px-2 py-1 text-xs font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800 rounded-full">
              {{ group.count }} skill{{ group.count !== 1 ? 's' : '' }}
            </span>
          </div>
          
          <!-- Skills Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div v-for="skill in group.skills" :key="skill.uuid" class="relative p-4 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg hover:shadow-sm transition-shadow group">
              <!-- Skill Name -->
              <div class="mb-2">
                <h4 class="font-medium text-gray-900 dark:text-gray-100">{{ skill.name }}</h4>
              </div>
              
              <!-- Proficiency Badge -->
              <div class="mb-3">
                <span :class="getProficiencyColor(skill.proficiency)" class="px-2 py-1 text-xs font-medium border rounded-full">
                  {{ getProficiencyLabel(skill.proficiency) }}
                </span>
              </div>
              
              <!-- Actions -->
              <div class="flex items-center justify-end space-x-1 group-hover:opacity-100 transition-opacity">
                <button
                  @click="openEditModal(skill)"
                  class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  title="Edit skill"
                >
                  <Icon name="mdi:pencil" class="w-4 h-4" />
                </button>
                
                <button
                  @click="openDeleteModal(skill)"
                  class="p-1.5 text-gray-400 hover:text-red-500 transition-colors"
                  title="Remove skill"
                >
                  <Icon name="mdi:delete" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Skill' : 'Add Skill'"
    size="lg"
    @close="closeModal"
  >
    <div class="space-y-6">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Skill Name *
        </label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          placeholder="e.g. JavaScript"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div>
        <label for="category" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Category
        </label>
        <select
          id="category"
          v-model="formData.category"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option value="" disabled>Select a category *</option>
          <option v-for="cat in SKILL_CATEGORIES" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
      </div>

      <div>
        <label for="proficiency" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Proficiency Level
        </label>
        <select
          id="proficiency"
          v-model="formData.proficiency"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        >
          <option value="">Not specified</option>
          <option v-for="level in PROFICIENCY_LEVELS" :key="level.value" :value="level.value">
            {{ level.label }}
          </option>
        </select>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeModal"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Cancel
        </button>
        <button
          @click="handleSave"
          :disabled="!isFormValid"
          class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Skill"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Skill?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ skillToDelete?.name }}</span>? This action cannot be undone.
          </p>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeDeleteModal"
          :disabled="isDeleting"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button
          @click="confirmDelete"
          :disabled="isDeleting"
          class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isDeleting ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </template>
  </Modal>
</template>
