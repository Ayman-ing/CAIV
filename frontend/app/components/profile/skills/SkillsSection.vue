<script setup lang="ts">
// filepath: frontend/app/components/profile/skills/SkillsSection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { Skill, SkillFormData, SkillGroup } from './types'
import { SKILL_CATEGORIES, PROFICIENCY_LEVELS } from './types'

// Skills Data
const skills = ref<Skill[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingSkill = ref<Skill | null>(null)

// Form state
const formData = ref<SkillFormData>({
  category: '',
  name: '',
  proficiency: ''
})

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
    category: skill.category,
    name: skill.name,
    proficiency: skill.proficiency
  }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingSkill.value) {
    // Update existing skill
    const index = skills.value.findIndex(skill => skill.id === editingSkill.value!.id)
    if (index !== -1 && skills.value[index]) {
      skills.value[index] = {
        ...skills.value[index],
        category: formData.value.category.trim(),
        name: formData.value.name.trim(),
        proficiency: formData.value.proficiency
      }
    }
  } else {
    // Add new skill
    const newSkill: Skill = {
      id: Date.now(),
      category: formData.value.category.trim(),
      name: formData.value.name.trim(),
      proficiency: formData.value.proficiency,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    skills.value.push(newSkill)
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingSkill.value = null
  formData.value = {
    category: '',
    name: '',
    proficiency: ''
  }
}

const removeSkill = (id: number) => {
  const index = skills.value.findIndex(skill => skill.id === id)
  if (index !== -1) {
    skills.value.splice(index, 1)
  }
}

const isFormValid = computed(() => {
  return formData.value.category.trim() !== '' && 
         formData.value.name.trim() !== '' && 
         formData.value.proficiency !== ''
})

const hasSkills = computed(() => {
  return skills.value.length > 0
})

// Group skills by category for better display
const groupedSkills = computed((): SkillGroup[] => {
  const groups = new Map<string, Skill[]>()
  
  skills.value.forEach(skill => {
    if (!groups.has(skill.category)) {
      groups.set(skill.category, [])
    }
    groups.get(skill.category)?.push(skill)
  })
  
  return Array.from(groups.entries()).map(([category, categorySkills]) => ({
    category,
    skills: categorySkills.sort((a, b) => a.name.localeCompare(b.name)),
    count: categorySkills.length
  })).sort((a, b) => a.category.localeCompare(b.category))
})

const getProficiencyColor = (proficiency: string) => {
  const colors = {
    'beginner': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800',
    'intermediate': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800',
    'advanced': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800',
    'expert': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800'
  }
  return colors[proficiency as keyof typeof colors] || colors.intermediate
}

const getProficiencyLabel = (proficiency: string) => {
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
    :is-empty="!hasSkills"
    empty-message="Add your skills"
    add-button-text="Add Skill"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="hasSkills" class="space-y-6">
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
            <div v-for="skill in group.skills" :key="skill.id" class="relative p-4 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg hover:shadow-sm transition-shadow group">
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
              <div class="flex items-center justify-end space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  @click="openEditModal(skill)"
                  class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  title="Edit skill"
                >
                  <Icon name="mdi:pencil" class="w-4 h-4" />
                </button>
                
                <button
                  @click="removeSkill(skill.id!)"
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
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Skill' : 'Add Skill' }}
      </h2>
    </template>
    
    <div class="space-y-6">
      <!-- Skill Name -->
      <div>
        <label for="skillName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Skill Name *
        </label>
        <input
          id="skillName"
          v-model="formData.name"
          type="text"
          placeholder="e.g. JavaScript, Project Management, Adobe Photoshop"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Enter the specific name of the skill or technology
        </p>
      </div>

      <!-- Category -->
      <div>
        <label for="category" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Category *
        </label>
        <select
          id="category"
          v-model="formData.category"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option value="">Select a category</option>
          <option v-for="category in SKILL_CATEGORIES" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Choose the most appropriate category for this skill
        </p>
      </div>

      <!-- Proficiency Level -->
      <div>
        <label for="proficiency" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Proficiency Level *
        </label>
        <select
          id="proficiency"
          v-model="formData.proficiency"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option value="">Select proficiency level</option>
          <option v-for="level in PROFICIENCY_LEVELS" :key="level.value" :value="level.value">
            {{ level.label }} - {{ level.description }}
          </option>
        </select>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Be honest about your skill level - this helps create accurate resumes
        </p>
      </div>

      <!-- Proficiency Preview -->
      <div v-if="formData.proficiency" class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
        <div class="flex items-center space-x-2">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Preview:</span>
          <span :class="getProficiencyColor(formData.proficiency)" class="px-2 py-1 text-xs font-medium border rounded-full">
            {{ getProficiencyLabel(formData.proficiency) }}
          </span>
        </div>
      </div>

      <!-- Guidelines -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Skill Tips</p>
            <ul class="text-xs space-y-1 list-disc list-inside">
              <li>Be specific (e.g., "React.js" instead of just "Frontend")</li>
              <li>Include relevant certifications as separate skills</li>
              <li>Consider both technical and soft skills</li>
              <li>Keep proficiency levels realistic and honest</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button
        @click="closeModal"
        class="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
      >
        Cancel
      </button>
      
      <button
        @click="handleSave"
        :disabled="!isFormValid"
        class="px-4 py-2 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Skill' : 'Save Skill' }}
      </button>
    </template>
  </Modal>
</template>
