<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { 
  type Language, 
  type LanguageFormData, 
  type LanguageDisplay,
  PROFICIENCY_LEVELS, 
  COMMON_LANGUAGES 
} from './types'

// Reactive state
const languages = ref<Language[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)
const error = ref<string | null>(null)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingLanguage = ref<Language | null>(null)

// Form data
const formData = reactive<LanguageFormData>({
  language: '',
  proficiency: 'conversational'
})

// Computed properties
const hasLanguages = computed(() => languages.value.length > 0)

const displayLanguages = computed<LanguageDisplay[]>(() => {
  return languages.value.map(lang => {
    const profLevel = PROFICIENCY_LEVELS.find(p => p.value === lang.proficiency) || PROFICIENCY_LEVELS[2]
    const commonLang = COMMON_LANGUAGES.find(c => c.name.toLowerCase() === lang.language.toLowerCase())
    
    return {
      ...lang,
      nativeName: commonLang?.nativeName,
      proficiencyLevel: profLevel.level,
      canWorkIn: profLevel.level >= 3
    }
  })
})

const nativeLanguages = computed(() => displayLanguages.value.filter(l => l.proficiency === 'native'))
const workingLanguages = computed(() => displayLanguages.value.filter(l => l.canWorkIn && l.proficiency !== 'native'))
const learningLanguages = computed(() => displayLanguages.value.filter(l => !l.canWorkIn))

const isFormValid = computed(() => {
  return formData.language.trim().length > 0 && formData.proficiency.length > 0
})

// Methods
const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingLanguage.value = null
  resetForm()
  isModalOpen.value = true
}

const openEditModal = (language: Language) => {
  isEditing.value = true
  editingLanguage.value = language
  formData.language = language.language
  formData.proficiency = language.proficiency
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  resetForm()
  error.value = null
}

const resetForm = () => {
  formData.language = ''
  formData.proficiency = 'conversational'
}

const handleSave = async () => {
  if (!isFormValid.value) return
  
  isLoading.value = true
  error.value = null
  
  try {
    if (isEditing.value && editingLanguage.value) {
      await updateLanguage(editingLanguage.value.id!, formData)
    } else {
      await saveLanguage(formData)
    }
    closeModal()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to save language'
  } finally {
    isLoading.value = false
  }
}

const removeLanguage = async (id: number) => {
  if (!confirm('Are you sure you want to remove this language?')) return
  
  isLoading.value = true
  try {
    await deleteLanguage(id)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to remove language'
  } finally {
    isLoading.value = false
  }
}

// API methods (mock implementations)
const saveLanguage = async (languageData: LanguageFormData) => {
  // TODO: Replace with actual API call
  const newLanguage: Language = {
    id: Date.now(),
    language: languageData.language,
    proficiency: languageData.proficiency,
    createdAt: new Date().toISOString()
  }
  languages.value.push(newLanguage)
}

const updateLanguage = async (id: number, languageData: LanguageFormData) => {
  // TODO: Replace with actual API call
  const index = languages.value.findIndex(l => l.id === id)
  if (index !== -1) {
    languages.value[index] = {
      ...languages.value[index],
      language: languageData.language,
      proficiency: languageData.proficiency,
      updatedAt: new Date().toISOString()
    }
  }
}

const deleteLanguage = async (id: number) => {
  // TODO: Replace with actual API call
  languages.value = languages.value.filter(l => l.id !== id)
}

const getProficiencyColor = (proficiency: string) => {
  const level = PROFICIENCY_LEVELS.find(p => p.value === proficiency)
  if (!level) return 'bg-gray-100 text-gray-700 border-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600'
  
  switch (level.level) {
    case 5: return 'bg-purple-100 text-purple-700 border-purple-300 dark:bg-purple-900/30 dark:text-purple-300 dark:border-purple-600'
    case 4: return 'bg-green-100 text-green-700 border-green-300 dark:bg-green-900/30 dark:text-green-300 dark:border-green-600'
    case 3: return 'bg-blue-100 text-blue-700 border-blue-300 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-600'
    case 2: return 'bg-yellow-100 text-yellow-700 border-yellow-300 dark:bg-yellow-900/30 dark:text-yellow-300 dark:border-yellow-600'
    default: return 'bg-orange-100 text-orange-700 border-orange-300 dark:bg-orange-900/30 dark:text-orange-300 dark:border-orange-600'
  }
}

const getProficiencyIcon = (proficiency: string) => {
  const level = PROFICIENCY_LEVELS.find(p => p.value === proficiency)
  if (!level) return 'heroicons:question-mark-circle'
  
  switch (level.level) {
    case 5: return 'heroicons:star'
    case 4: return 'heroicons:hand-thumb-up'
    case 3: return 'heroicons:briefcase'
    case 2: return 'heroicons:chat-bubble-left'
    default: return 'heroicons:academic-cap'
  }
}

// Load initial data (mock)
const loadLanguages = async () => {
  // TODO: Replace with actual API call
  languages.value = []
}

// Load data on component mount
onMounted(() => {
  loadLanguages()
})
</script>

<template>
  <CollapsibleSection
    title="Languages"
    description="Languages you speak and your proficiency levels"
    icon="heroicons:language"
    icon-color="text-indigo-600 dark:text-indigo-400"
    icon-bg-color="bg-indigo-100 dark:bg-indigo-900/30"
    button-color="bg-indigo-600 dark:bg-indigo-500 hover:bg-indigo-700 dark:hover:bg-indigo-600"
    :is-expanded="isExpanded"
    :is-empty="!hasLanguages"
    empty-message="Add languages you speak"
    add-button-text="Add Language"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="hasLanguages" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="heroicons:language" class="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <div>
              <p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">Languages</p>
              <p class="text-xs text-indigo-600 dark:text-indigo-400">
                {{ languages.length }} language{{ languages.length !== 1 ? 's' : '' }}
                {{ workingLanguages.length > 0 ? `• ${workingLanguages.length} for work` : '' }}
              </p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="heroicons:plus" class="w-4 h-4 mr-2" />
          Add Language
        </button>
      </div>

      <!-- Native Languages -->
      <div v-if="nativeLanguages.length > 0" class="space-y-3">
        <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center">
          <Icon name="heroicons:star" class="w-4 h-4 mr-2 text-purple-600 dark:text-purple-400" />
          Native Languages
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-for="language in nativeLanguages" :key="language.id" class="relative p-4 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-purple-900 dark:text-purple-100">{{ language.language }}</h4>
                <p v-if="language.nativeName && language.nativeName !== language.language" class="text-sm text-purple-700 dark:text-purple-300">
                  {{ language.nativeName }}
                </p>
                <span class="inline-flex items-center px-2 py-1 text-xs font-medium bg-purple-100 text-purple-700 border border-purple-300 rounded-full mt-1 dark:bg-purple-900/30 dark:text-purple-300 dark:border-purple-600">
                  <Icon :name="getProficiencyIcon(language.proficiency)" class="w-3 h-3 mr-1" />
                  Native
                </span>
              </div>
              <div class="flex items-center space-x-1">
                <button
                  @click="openEditModal(language)"
                  class="p-1.5 text-purple-600 hover:bg-purple-200 dark:text-purple-400 dark:hover:bg-purple-800 rounded transition-colors"
                >
                  <Icon name="heroicons:pencil" class="w-4 h-4" />
                </button>
                <button
                  @click="removeLanguage(language.id!)"
                  class="p-1.5 text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900/30 rounded transition-colors"
                >
                  <Icon name="heroicons:trash" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Working Languages -->
      <div v-if="workingLanguages.length > 0" class="space-y-3">
        <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center">
          <Icon name="heroicons:briefcase" class="w-4 h-4 mr-2 text-blue-600 dark:text-blue-400" />
          Professional Working Languages
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-for="language in workingLanguages" :key="language.id" class="relative p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-gray-900 dark:text-gray-100">{{ language.language }}</h4>
                <p v-if="language.nativeName && language.nativeName !== language.language" class="text-sm text-gray-600 dark:text-gray-400">
                  {{ language.nativeName }}
                </p>
                <span :class="getProficiencyColor(language.proficiency)" class="inline-flex items-center px-2 py-1 text-xs font-medium border rounded-full mt-1">
                  <Icon :name="getProficiencyIcon(language.proficiency)" class="w-3 h-3 mr-1" />
                  {{ PROFICIENCY_LEVELS.find(p => p.value === language.proficiency)?.label }}
                </span>
              </div>
              <div class="flex items-center space-x-1">
                <button
                  @click="openEditModal(language)"
                  class="p-1.5 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700 rounded transition-colors"
                >
                  <Icon name="heroicons:pencil" class="w-4 h-4" />
                </button>
                <button
                  @click="removeLanguage(language.id!)"
                  class="p-1.5 text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900/30 rounded transition-colors"
                >
                  <Icon name="heroicons:trash" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Languages -->
      <div v-if="learningLanguages.length > 0" class="space-y-3">
        <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center">
          <Icon name="heroicons:academic-cap" class="w-4 h-4 mr-2 text-orange-600 dark:text-orange-400" />
          Languages I'm Learning
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div v-for="language in learningLanguages" :key="language.id" class="relative p-4 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-orange-900 dark:text-orange-100">{{ language.language }}</h4>
                <p v-if="language.nativeName && language.nativeName !== language.language" class="text-sm text-orange-700 dark:text-orange-300">
                  {{ language.nativeName }}
                </p>
                <span :class="getProficiencyColor(language.proficiency)" class="inline-flex items-center px-2 py-1 text-xs font-medium border rounded-full mt-1">
                  <Icon :name="getProficiencyIcon(language.proficiency)" class="w-3 h-3 mr-1" />
                  {{ PROFICIENCY_LEVELS.find(p => p.value === language.proficiency)?.label }}
                </span>
              </div>
              <div class="flex items-center space-x-1">
                <button
                  @click="openEditModal(language)"
                  class="p-1.5 text-orange-600 hover:bg-orange-200 dark:text-orange-400 dark:hover:bg-orange-800 rounded transition-colors"
                >
                  <Icon name="heroicons:pencil" class="w-4 h-4" />
                </button>
                <button
                  @click="removeLanguage(language.id!)"
                  class="p-1.5 text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900/30 rounded transition-colors"
                >
                  <Icon name="heroicons:trash" class="w-4 h-4" />
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
    :title="isEditing ? 'Edit Language' : 'Add Language'"
    size="lg"
    @close="closeModal"
  >
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Language' : 'Add Language' }}
      </h2>
    </template>
    
    <div class="space-y-6">
      <!-- Language Selection -->
      <div>
        <label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Language *
        </label>
        <div class="relative">
          <input
            id="language"
            v-model="formData.language"
            type="text"
            list="languages-list"
            placeholder="Type or select a language"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            required
          />
          <datalist id="languages-list">
            <option v-for="lang in COMMON_LANGUAGES" :key="lang.code" :value="lang.name">
              {{ lang.nativeName }}
            </option>
          </datalist>
        </div>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Select from common languages or type your own
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
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option v-for="level in PROFICIENCY_LEVELS" :key="level.value" :value="level.value">
            {{ level.label }} - {{ level.description }}
          </option>
        </select>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Be honest about your current level
        </p>
      </div>

      <!-- Proficiency Guidelines -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div class="flex items-start space-x-2">
          <Icon name="heroicons:information-circle" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Proficiency Guidelines</p>
            <ul class="text-xs space-y-1 list-disc list-inside">
              <li><strong>Native:</strong> First language or equal to native level</li>
              <li><strong>Fluent:</strong> Can work professionally without issues</li>
              <li><strong>Proficient:</strong> Advanced level suitable for most work contexts</li>
              <li><strong>Intermediate:</strong> Good for basic work tasks and communication</li>
              <li><strong>Basic/Beginner:</strong> Limited ability, still learning</li>
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
        :disabled="!isFormValid || isLoading"
        class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="heroicons:check" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Language' : 'Add Language' }}
      </button>
    </template>
  </Modal>
</template>
