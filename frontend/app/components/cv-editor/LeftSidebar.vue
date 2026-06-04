<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'

const {
  state,
  updateSummary,
  addWorkExperience, removeWorkExperience,
  addEducation, removeEducation,
  addSkill, removeSkill,
  addProject, removeProject,
  addCertificate, removeCertificate,
  addLanguage, removeLanguage,
  addCustomSection, removeCustomSection,
  reorderComponents,
} = useCVEditor()

interface SectionDef {
  type: string
  label: string
  icon: string
}

const sections: SectionDef[] = [
  { type: 'professional_summary', label: 'Professional Summary', icon: 'heroicons:document-text' },
  { type: 'work_experience', label: 'Experience', icon: 'heroicons:briefcase' },
  { type: 'education', label: 'Education', icon: 'heroicons:academic-cap' },
  { type: 'skills', label: 'Skills', icon: 'heroicons:sparkles' },
  { type: 'projects', label: 'Projects', icon: 'heroicons:folder' },
  { type: 'certificates', label: 'Certifications', icon: 'heroicons:trophy' },
  { type: 'languages', label: 'Languages', icon: 'heroicons:chat-bubble-left-right' },
  { type: 'custom_sections', label: 'Custom Sections', icon: 'heroicons:queue-list' },
]

const orderedSections = computed(() =>
  [...sections].sort((a, b) => {
    const aOrder = state.components.find(c => c.component_type === a.type)?.order_index ?? 0
    const bOrder = state.components.find(c => c.component_type === b.type)?.order_index ?? 0
    return aOrder - bOrder
  })
)

const getSectionData = (type: string): any[] => {
  switch (type) {
    case 'work_experience': return state.profileData.workExperiences
    case 'education': return state.profileData.education
    case 'skills': return state.profileData.skills
    case 'projects': return state.profileData.projects
    case 'certificates': return state.profileData.certificates
    case 'languages': return state.profileData.languages
    case 'custom_sections': return state.profileData.customSections
    default: return []
  }
}

const entryLabel = (type: string, entry: any): string => {
  switch (type) {
    case 'work_experience': return `${entry.job_title}${entry.company ? ` @ ${entry.company}` : ''}`
    case 'education': return `${entry.degree}${entry.institution ? `, ${entry.institution}` : ''}`
    case 'skills': return state.profileData.skillUseCategories && entry.category ? `${entry.category}: ${entry.name}` : entry.name
    case 'projects': return entry.name
    case 'certificates': return entry.name
    case 'languages': return `${entry.language} - ${entry.proficiency}`
    case 'custom_sections': return entry.title
    default: return ''
  }
}

const removeEntry = (type: string, uuid: string) => {
  switch (type) {
    case 'work_experience': removeWorkExperience(uuid); break
    case 'education': removeEducation(uuid); break
    case 'skills': removeSkill(uuid); break
    case 'projects': removeProject(uuid); break
    case 'certificates': removeCertificate(uuid); break
    case 'languages': removeLanguage(uuid); break
    case 'custom_sections': removeCustomSection(uuid); break
  }
}

const hasData = (type: string): boolean => {
  switch (type) {
    case 'professional_summary': return !!state.profileData.summary
    default: return getSectionData(type).length > 0
  }
}

const collapsedSections = ref(new Set<string>())

const toggleCollapse = (type: string) => {
  if (collapsedSections.value.has(type)) {
    collapsedSections.value.delete(type)
  } else {
    collapsedSections.value.add(type)
  }
}

const isCollapsed = (type: string): boolean => collapsedSections.value.has(type)

const draggedSection = ref<string | null>(null)
const addingToSection = ref<string | null>(null)

const formData = ref({
  job_title: '', company: '', start_date: '', end_date: '', description: '',
  institution: '', degree: '', field_of_study: '',
  name: '', category: '', proficiency: '',
  issuing_organization: '', issue_date: '',
  language: '',
  custom_title: '', custom_content: '',
})

const resetForm = () => {
  formData.value = {
    job_title: '', company: '', start_date: '', end_date: '', description: '',
    institution: '', degree: '', field_of_study: '',
    name: '', category: '', proficiency: '',
    issuing_organization: '', issue_date: '',
    language: '',
    custom_title: '', custom_content: '',
  }
}

const handleAdd = (type: string) => {
  const d = formData.value
  switch (type) {
    case 'work_experience':
      addWorkExperience({ job_title: d.job_title, company: d.company, start_date: d.start_date, end_date: d.end_date, description: d.description })
      break
    case 'education':
      addEducation({ institution: d.institution, degree: d.degree, field_of_study: d.field_of_study, start_date: d.start_date, end_date: d.end_date, description: d.description })
      break
    case 'skills':
      addSkill({ name: d.name, category: d.category, proficiency: d.proficiency })
      break
    case 'projects':
      addProject({ name: d.name, description: d.description, technologies: d.category, start_date: d.start_date, end_date: d.end_date })
      break
    case 'certificates':
      addCertificate({ name: d.name, issuing_organization: d.issuing_organization, issue_date: d.issue_date })
      break
    case 'languages':
      addLanguage({ language: d.language, proficiency: d.proficiency })
      break
    case 'custom_sections':
      addCustomSection({ title: d.custom_title, content: d.custom_content })
      break
  }
  resetForm()
  addingToSection.value = null
}

const handleAddClick = (type: string) => {
  if (isCollapsed(type)) {
    toggleCollapse(type)
  }
  addingToSection.value = type
}

const handleDragStart = (e: DragEvent, type: string) => {
  draggedSection.value = type
  if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move'
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  if (e.dataTransfer) e.dataTransfer.dropEffect = 'move'
}

const handleDrop = (e: DragEvent, targetType: string) => {
  e.preventDefault()
  const source = draggedSection.value
  if (!source || source === targetType) {
    draggedSection.value = null
    return
  }
  const ordered = [...orderedSections.value]
  const sourceIdx = ordered.findIndex(s => s.type === source)
  const targetIdx = ordered.findIndex(s => s.type === targetType)
  if (sourceIdx !== -1 && targetIdx !== -1) {
    const [moved] = ordered.splice(sourceIdx, 1)
    ordered.splice(targetIdx, 0, moved!)
    const newComponents = ordered.map((s, i) => {
      const c = state.components.find(c => c.component_type === s.type)
      return c ? { ...c, order_index: i } : null
    }).filter(Boolean)
    reorderComponents(newComponents as any[])
  }
  draggedSection.value = null
}
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
      <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
        <Icon name="heroicons:rectangle-stack" class="w-5 h-5" />
        <span>Sections</span>
      </h3>
    </div>

    <div class="flex-1 overflow-y-auto">
      <div
        v-for="section in orderedSections"
        :key="section.type"
        :draggable="section.type !== 'professional_summary'"
        class="border-b border-gray-200 dark:border-gray-700"
        @dragstart="handleDragStart($event, section.type)"
        @dragover="handleDragOver"
        @drop="handleDrop($event, section.type)"
      >
        <div
          class="flex items-center justify-between px-4 py-2.5 bg-blue-50 dark:bg-blue-900/20"
          @click="toggleCollapse(section.type)"
        >
          <div class="flex items-center space-x-2 min-w-0">
            <Icon v-if="section.type !== 'professional_summary'" name="heroicons:bars-3" class="w-4 h-4 text-gray-400 flex-shrink-0 cursor-grab" />
            <Icon :name="section.icon" class="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0" />
            <span class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
              {{ section.label }}
            </span>
          </div>
          <div class="flex items-center space-x-1 flex-shrink-0">
            <button
              class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              title="Collapse section"
            >
              <Icon
                :name="isCollapsed(section.type) ? 'heroicons:chevron-down' : 'heroicons:chevron-up'"
                class="w-4 h-4"
              />
            </button>
          </div>
        </div>

        <div v-if="!isCollapsed(section.type)" class="px-4 py-2">
          <textarea
            v-if="section.type === 'professional_summary'"
            :value="state.profileData.summary"
            placeholder="Write a brief professional summary..."
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            @input="updateSummary(($event.target as HTMLTextAreaElement).value)"
          />

          <template v-else>
            <div v-for="entry in getSectionData(section.type)" :key="entry.uuid" class="flex items-center justify-between py-1 group">
              <span class="text-sm text-gray-700 dark:text-gray-300 truncate">{{ entryLabel(section.type, entry) }}</span>
              <button
                class="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0"
                title="Remove"
                @click="removeEntry(section.type, entry.uuid)"
              >
                <Icon name="heroicons:x-mark" class="w-4 h-4" />
              </button>
            </div>

            <div v-if="addingToSection === section.type" class="mt-2 space-y-2 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg">
              <!-- Work Experience Form -->
              <template v-if="section.type === 'work_experience'">
                <input v-model="formData.job_title" placeholder="Job Title" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.company" placeholder="Company" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <div class="flex space-x-2">
                  <input v-model="formData.start_date" placeholder="Start Date" type="month" class="flex-1 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  <input v-model="formData.end_date" placeholder="End Date" type="month" class="flex-1 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <input v-model="formData.description" placeholder="Description" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </template>

              <!-- Education Form -->
              <template v-if="section.type === 'education'">
                <input v-model="formData.degree" placeholder="Degree" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.institution" placeholder="Institution" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.field_of_study" placeholder="Field of Study" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <div class="flex space-x-2">
                  <input v-model="formData.start_date" placeholder="Start Date" type="month" class="flex-1 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  <input v-model="formData.end_date" placeholder="End Date" type="month" class="flex-1 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
              </template>

              <!-- Skills Form -->
              <template v-if="section.type === 'skills'">
                <label class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">
                  <input
                    type="checkbox"
                    :checked="state.profileData.skillUseCategories"
                    class="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
                    @change="state.profileData.skillUseCategories = ($event.target as HTMLInputElement).checked"
                  />
                  <span>Use categories</span>
                </label>
                <input v-model="formData.name" placeholder="Skill Name" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input
                  v-if="state.profileData.skillUseCategories"
                  v-model="formData.category"
                  placeholder="Category"
                  class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </template>

              <!-- Projects Form -->
              <template v-if="section.type === 'projects'">
                <input v-model="formData.name" placeholder="Project Name" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.category" placeholder="Technologies" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.description" placeholder="Description" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <div class="flex space-x-2">
                  <input v-model="formData.start_date" placeholder="Start Date" type="month" class="flex-1 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  <input v-model="formData.end_date" placeholder="End Date" type="month" class="flex-1 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
              </template>

              <!-- Certificates Form -->
              <template v-if="section.type === 'certificates'">
                <input v-model="formData.name" placeholder="Certificate Name" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.issuing_organization" placeholder="Issuing Organization" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="formData.issue_date" placeholder="Issue Date" type="month" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </template>

              <!-- Languages Form -->
              <template v-if="section.type === 'languages'">
                <input v-model="formData.language" placeholder="Language" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <select
                  v-model="formData.proficiency"
                  class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="" disabled>Select proficiency</option>
                  <option value="Native">Native</option>
                  <option value="Fluent">Fluent</option>
                  <option value="Advanced">Advanced</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Basic">Basic</option>
                </select>
              </template>

              <!-- Custom Section Form -->
              <template v-if="section.type === 'custom_sections'">
                <input v-model="formData.custom_title" placeholder="Section Title" class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <textarea
                  v-model="formData.custom_content"
                  placeholder="Content..."
                  rows="3"
                  class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
              </template>

              <div class="flex space-x-2 pt-1">
                <button
                  class="px-3 py-1.5 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                  @click="handleAdd(section.type)"
                >
                  Add
                </button>
                <button
                  class="px-3 py-1.5 text-xs text-gray-600 dark:text-gray-400 hover:underline"
                  @click="addingToSection = null; resetForm()"
                >
                  Cancel
                </button>
              </div>
            </div>

            <button
              v-else
              class="text-xs text-blue-600 dark:text-blue-400 hover:underline mt-1"
              @click="addingToSection = section.type"
            >
              + Add {{ section.label }}
            </button>
          </template>
        </div>

        <div v-else class="px-4 pb-2 pt-1">
          <button
            v-if="section.type !== 'professional_summary'"
            class="text-xs text-blue-600 dark:text-blue-400 hover:underline"
            @click="handleAddClick(section.type)"
          >
            + Add {{ section.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
