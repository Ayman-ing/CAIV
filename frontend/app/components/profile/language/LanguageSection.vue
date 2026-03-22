<script setup lang="ts">
// filepath: frontend/app/components/profile/language/LanguageSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { Language, LanguageFormData, LanguageDisplay } from './types'
import { PROFICIENCY_LEVELS, COMMON_LANGUAGES } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'
import { useToast } from '~/composables/useToast'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()

// Languages Data
const languages = ref<Language[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Form validation errors
const languageValidationError = ref<string | null>(null)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingLanguage = ref<Language | null>(null)
const isDeleteModalOpen = ref(false)
const languageToDelete = ref<Language | null>(null)
const isDeleting = ref(false)

// Form data
const formData = ref<LanguageFormData>({
  language: '',
  proficiency: 'Conversational',
  can_read: true,
  can_write: true,
  can_speak: true
})

onMounted(async () => {
  await fetchLanguages()
})

const fetchLanguages = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllLanguages(activeProfile.value.uuid)
    languages.value = data
  } catch (error) {
    console.error('Failed to fetch languages:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingLanguage.value = null
  languageValidationError.value = null
  formData.value = {
    language: '',
    proficiency: 'Conversational',
    can_read: true,
    can_write: true,
    can_speak: true
  }
  isModalOpen.value = true
}

const openEditModal = (lang: Language) => {
  isEditing.value = true
  editingLanguage.value = lang
  languageValidationError.value = null
  formData.value = {
    language: lang.language,
    proficiency: lang.proficiency,
    can_read: lang.can_read ?? true,
    can_write: lang.can_write ?? true,
    can_speak: lang.can_speak ?? true
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  // Check for duplicate language when adding (not editing)
  if (!isEditing.value) {
    const isDuplicate = languages.value.some(
      l => l.language.toLowerCase() === formData.value.language.trim().toLowerCase()
    )
    if (isDuplicate) {
      languageValidationError.value = `Language '${formData.value.language}' already exists`
      return
    }
  }
  languageValidationError.value = null
  
  const payload: Omit<Language, 'uuid'> = {
    language: formData.value.language.trim(),
    proficiency: formData.value.proficiency,
    can_read: formData.value.can_read,
    can_write: formData.value.can_write,
    can_speak: formData.value.can_speak
  }

  try {
    if (isEditing.value && editingLanguage.value) {
      await profileSectionsService.updateLanguage(
        activeProfile.value.uuid,
        editingLanguage.value.uuid,
        payload
      )
      success('Language updated successfully!')
    } else {
      await profileSectionsService.createLanguage(activeProfile.value.uuid, payload)
      success('Language added successfully!')
    }
    await fetchLanguages()
    closeModal()
  } catch (err) {
    error(`Failed to save language: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingLanguage.value = null
  languageValidationError.value = null
}

const openDeleteModal = (lang: Language) => {
  languageToDelete.value = lang
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  languageToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !languageToDelete.value) return
  isDeleting.value = true
  try {
    await profileSectionsService.deleteLanguage(activeProfile.value.uuid, languageToDelete.value.uuid)
    await fetchLanguages()
    closeDeleteModal()
    success('Language deleted successfully!')
  } catch (err) {
    error(`Failed to delete language: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  return formData.value.language.trim().length > 0 && formData.value.proficiency.length > 0
})

const hasLanguages = computed(() => languages.value.length > 0)

const displayLanguagesSorted = computed<LanguageDisplay[]>(() => {
  return languages.value.map(lang => {
    const profLevel = PROFICIENCY_LEVELS.find(p => p.value === lang.proficiency) || PROFICIENCY_LEVELS[2]
    const commonLang = COMMON_LANGUAGES.find(c => c.name.toLowerCase() === lang.language.toLowerCase())
    
    return {
      ...lang,
      nativeName: commonLang?.nativeName,
      proficiencyLevel: profLevel.level,
      canWorkIn: profLevel.level >= 3
    }
  }).sort((a, b) => b.proficiencyLevel - a.proficiencyLevel)
})

const getProficiencyColor = (proficiency: string) => {
  const level = PROFICIENCY_LEVELS.find(p => p.value === proficiency)
  if (!level) return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
  
  switch (level.level) {
    case 5: return 'bg-purple-100 text-purple-700 border-purple-200 dark:bg-purple-900/30 dark:text-purple-300'
    case 4: return 'bg-green-100 text-green-700 border-green-200 dark:bg-green-900/30 dark:text-green-300'
    case 3: return 'bg-blue-100 text-blue-700 border-blue-200 dark:bg-blue-900/30 dark:text-blue-300'
    case 2: return 'bg-yellow-100 text-yellow-700 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-300'
    default: return 'bg-gray-100 text-gray-700 border-gray-200 dark:bg-gray-700 dark:text-gray-300'
  }
}
</script>

<template>
  <CollapsibleSection
    title="Languages"
    description="Languages you speak and your proficiency levels"
    icon="mdi:language"
    icon-color="text-indigo-600 dark:text-indigo-400"
    icon-bg-color="bg-indigo-100 dark:bg-indigo-900/30"
    button-color="bg-indigo-600 dark:bg-indigo-500 hover:bg-indigo-700 dark:hover:bg-indigo-600"
    :is-expanded="isExpanded"
    :is-empty="!isLoading && !hasLanguages"
    empty-message="Add languages you speak"
    add-button-text="Add Language"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-indigo-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasLanguages" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:language-typescript" class="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <div>
              <p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">Languages</p>
              <p class="text-xs text-indigo-600 dark:text-indigo-400">{{ displayLanguagesSorted.length }} language{{ displayLanguagesSorted.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Language
        </button>
      </div>

      <!-- Languages List -->
      <div class="space-y-6">
        <div v-for="lang in displayLanguagesSorted" :key="lang.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ lang.language }}
              <span v-if="lang.nativeName && lang.nativeName !== lang.language" class="text-sm font-normal text-gray-500 ml-2">({{ lang.nativeName }})</span>
            </h4>
            <div class="mt-2 flex flex-wrap gap-2">
              <span :class="getProficiencyColor(lang.proficiency)" class="px-2 py-1 text-xs font-medium border rounded-full">
                {{ PROFICIENCY_LEVELS.find(p => p.value === lang.proficiency)?.label }}
              </span>
              <span v-if="lang.can_read" class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">Read</span>
              <span v-if="lang.can_write" class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">Write</span>
              <span v-if="lang.can_speak" class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">Speak</span>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <button @click="openEditModal(lang)" class="p-2 text-gray-400 hover:text-indigo-600 transition-colors">
              <Icon name="mdi:pencil" class="w-5 h-5" />
            </button>
            <button @click="openDeleteModal(lang)" class="p-2 text-gray-400 hover:text-red-600 transition-colors">
              <Icon name="mdi:delete" class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
      </div>

      <!-- Add Another Button -->
      <div class="flex justify-center pt-3">
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Another Language
        </button>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Language"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Language?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ languageToDelete?.language }}</span>? This action cannot be undone.
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

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Language' : 'Add Language'"
    size="lg"
    @close="closeModal"
  >
    <div class="space-y-6">
      <div>
        <label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Language *
        </label>
        <input
          id="language"
          v-model="formData.language"
          type="text"
          list="languages-list"
          placeholder="e.g. English, French"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 transition-colors"
          :class="[
            languageValidationError
              ? 'border-red-500 dark:border-red-500'
              : 'border-gray-300 dark:border-gray-600'
          ]"
          required
        />
        <datalist id="languages-list">
          <option v-for="l in COMMON_LANGUAGES" :key="l.code" :value="l.name"></option>
        </datalist>
        <p v-if="languageValidationError" class="text-red-500 dark:text-red-400 text-sm mt-1">
          {{ languageValidationError }}
        </p>
      </div>

      <div>
        <label for="proficiency" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Proficiency *
        </label>
        <select
          id="proficiency"
          v-model="formData.proficiency"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option v-for="level in PROFICIENCY_LEVELS" :key="level.value" :value="level.value">
            {{ level.label }}
          </option>
        </select>
      </div>

      <div class="space-y-3">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Capabilities</label>
        <div class="flex space-x-6">
          <label class="flex items-center text-sm">
            <input v-model="formData.can_read" type="checkbox" class="rounded text-indigo-600 mr-2" />
            Read
          </label>
          <label class="flex items-center text-sm">
            <input v-model="formData.can_write" type="checkbox" class="rounded text-indigo-600 mr-2" />
            Write
          </label>
          <label class="flex items-center text-sm">
            <input v-model="formData.can_speak" type="checkbox" class="rounded text-indigo-600 mr-2" />
            Speak
          </label>
        </div>
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
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>
</template>
