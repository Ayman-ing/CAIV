<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'

const { state, includedComponents } = useCVEditor()

const containerRef = ref<HTMLElement | null>(null)
const scale = ref(1)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const lastMouseX = ref(0)
const lastMouseY = ref(0)

const minScale = 0.3
const maxScale = 3

const paperTransform = computed(() =>
  `translate(${panX.value}px, ${panY.value}px) scale(${scale.value})`
)

const zoomIndicator = computed(() => `${Math.round(scale.value * 100)}%`)

function handleWheel(e: WheelEvent) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  const newScale = Math.min(maxScale, Math.max(minScale, scale.value + delta))

  const rect = containerRef.value?.getBoundingClientRect()
  if (rect) {
    const cx = e.clientX - rect.left
    const cy = e.clientY - rect.top
    const paperX = (cx - panX.value) / scale.value
    const paperY = (cy - panY.value) / scale.value
    panX.value = cx - paperX * newScale
    panY.value = cy - paperY * newScale
  }

  scale.value = newScale
}

function handleMouseDown(e: MouseEvent) {
  if (e.button !== 0 && e.button !== 1) return
  e.preventDefault()
  isPanning.value = true
  lastMouseX.value = e.clientX
  lastMouseY.value = e.clientY
}

function handleMouseMove(e: MouseEvent) {
  if (!isPanning.value) return
  const dx = e.clientX - lastMouseX.value
  const dy = e.clientY - lastMouseY.value
  panX.value += dx
  panY.value += dy
  lastMouseX.value = e.clientX
  lastMouseY.value = e.clientY
}

function handleMouseUp() {
  isPanning.value = false
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
})

// Skill display
const skillDisplay = (skill: { name: string; category: string | null }) => {
  if (state.profileData.skillUseCategories && skill.category) {
    return `${skill.category}: ${skill.name}`
  }
  return skill.name
}

const contactInfo = computed(() => {
  const parts: string[] = []
  const { phone, email, location } = state.profileData.basicInfo
  if (email) parts.push(email)
  if (phone) parts.push(phone)
  if (location) parts.push(location)
  return parts
})

const activeLinks = computed(() =>
  state.profileData.links.filter(l => l.is_visible)
)

const formatDate = (dateStr: string | null | undefined): string => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
}

const dateRange = (start: string | null | undefined, end: string | null | undefined): string => {
  const s = formatDate(start)
  const e = formatDate(end)
  if (!s && !e) return ''
  return `${s} — ${e || 'Present'}`
}

const hasData = computed(() => !!state.profileData.basicInfo.name)
</script>

<template>
  <div
    ref="containerRef"
    class="w-full h-full overflow-hidden p-8 flex justify-start bg-gray-100 dark:bg-gray-900 select-none"
    :class="{ 'cursor-grab': !isPanning, 'cursor-grabbing': isPanning }"
    @wheel.prevent="handleWheel"
    @mousedown="handleMouseDown"
  >
    <div
      class="paper-preview w-full max-w-[210mm] bg-white shadow-xl"
      :style="{ transform: paperTransform, transformOrigin: '0 0' }"
    >
      <template v-if="hasData">
        <div class="px-8 pt-8 pb-4 text-center">
          <h1 class="text-[22px] font-bold text-gray-900 leading-tight">
            {{ state.profileData.basicInfo.name }}
          </h1>
          <div
            v-if="contactInfo.length > 0 || activeLinks.length > 0"
            class="text-xs text-gray-600 mt-2 leading-relaxed"
          >
            <span v-for="(info, i) in contactInfo" :key="'ci-' + i">
              {{ info }}<span v-if="i < contactInfo.length - 1 || activeLinks.length > 0"> &middot; </span>
            </span>
            <a
              v-for="(link, i) in activeLinks"
              :key="link.uuid"
              :href="link.url"
              target="_blank"
              class="text-gray-600 hover:underline"
            >
              {{ link.label || link.platform }}<span v-if="i < activeLinks.length - 1"> &middot; </span>
            </a>
          </div>
        </div>

        <div class="px-8 pb-8">
          <template v-for="component in includedComponents" :key="component.uuid">
            <div
              v-if="component.component_type === 'professional_summary' && state.profileData.summary"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-3">
              <p class="text-sm leading-relaxed text-gray-800">
                {{ state.profileData.summary }}
              </p>
            </div>

            <div
              v-else-if="component.component_type === 'work_experience' && state.profileData.workExperiences.length > 0"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-2">
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Experience</h2>
              <div v-for="exp in state.profileData.workExperiences" :key="exp.uuid" class="mb-3">
                <div class="flex justify-between items-baseline">
                  <div>
                    <span class="text-sm font-semibold text-gray-900">{{ exp.job_title }}</span>
                    <span v-if="exp.company" class="text-sm text-gray-700">, {{ exp.company }}</span>
                  </div>
                  <span class="text-xs text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap">
                    {{ dateRange(exp.start_date, exp.end_date) }}
                  </span>
                </div>
                <p v-if="exp.description" class="text-sm text-gray-700 mt-0.5 leading-relaxed">{{ exp.description }}</p>
              </div>
            </div>

            <div
              v-else-if="component.component_type === 'education' && state.profileData.education.length > 0"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-2">
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Education</h2>
              <div v-for="edu in state.profileData.education" :key="edu.uuid" class="mb-2">
                <div class="flex justify-between items-baseline">
                  <div>
                    <span class="text-sm font-semibold text-gray-900">{{ edu.degree }}</span>
                    <span v-if="edu.institution" class="text-sm text-gray-700">, {{ edu.institution }}</span>
                  </div>
                  <span class="text-xs text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap">
                    {{ dateRange(edu.start_date, edu.end_date) }}
                  </span>
                </div>
                <span v-if="edu.field_of_study" class="text-sm text-gray-600">{{ edu.field_of_study }}</span>
                <p v-if="edu.description" class="text-sm text-gray-700 mt-0.5 leading-relaxed">{{ edu.description }}</p>
              </div>
            </div>

            <div
              v-else-if="component.component_type === 'skills' && state.profileData.skills.length > 0"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-2">
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Skills</h2>
              <div class="flex flex-wrap gap-x-3 gap-y-1">
                <span v-for="skill in state.profileData.skills" :key="skill.uuid" class="text-sm text-gray-800">
                  {{ skillDisplay(skill) }}
                </span>
              </div>
            </div>

            <div
              v-else-if="component.component_type === 'projects' && state.profileData.projects.length > 0"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-2">
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Projects</h2>
              <div v-for="proj in state.profileData.projects" :key="proj.uuid" class="mb-2">
                <div class="flex justify-between items-baseline">
                  <span class="text-sm font-semibold text-gray-900">{{ proj.name }}</span>
                  <span class="text-xs text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap">
                    {{ dateRange(proj.start_date, proj.end_date) }}
                  </span>
                </div>
                <p v-if="proj.description" class="text-sm text-gray-700 mt-0.5 leading-relaxed">{{ proj.description }}</p>
                <div v-if="proj.technologies" class="text-xs text-gray-500 mt-0.5">
                  <span class="font-medium">Technologies:</span> {{ proj.technologies }}
                </div>
              </div>
            </div>

            <div
              v-else-if="component.component_type === 'certificates' && state.profileData.certificates.length > 0"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-2">
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Certifications</h2>
              <div v-for="cert in state.profileData.certificates" :key="cert.uuid" class="mb-2">
                <div class="flex justify-between items-baseline">
                  <div>
                    <span class="text-sm font-semibold text-gray-900">{{ cert.name }}</span>
                    <span v-if="cert.issuing_organization" class="text-sm text-gray-700">, {{ cert.issuing_organization }}</span>
                  </div>
                  <span v-if="cert.issue_date" class="text-xs text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap">
                    {{ formatDate(cert.issue_date) }}
                  </span>
                </div>
              </div>
            </div>

            <div
              v-else-if="component.component_type === 'languages' && state.profileData.languages.length > 0"
              class="mb-4"
            >
              <hr class="border-t border-gray-800 mb-2">
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Languages</h2>
              <div class="flex flex-wrap gap-x-4 gap-y-1">
                <span v-for="lang in state.profileData.languages" :key="lang.uuid" class="text-sm text-gray-800">
                  {{ lang.language }} <span class="text-gray-500">{{ lang.proficiency }}</span>
                </span>
              </div>
            </div>

            <template v-else-if="component.component_type === 'custom_sections'">
              <div v-for="cs in state.profileData.customSections" :key="cs.uuid" class="mb-4">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">{{ cs.title }}</h2>
                <p class="text-sm leading-relaxed text-gray-800">{{ cs.content }}</p>
              </div>
            </template>
          </template>
        </div>
      </template>

      <div
        v-else
        class="flex flex-col items-center justify-center py-16 text-gray-400"
      >
        <Icon name="heroicons:document-text" class="w-12 h-12 mb-3" />
        <p class="text-sm italic">No profile data loaded</p>
        <p class="text-xs mt-1">
          Add your information from the sidebar to see it here
        </p>
      </div>
    </div>

    <div
      class="fixed bottom-4 left-1/2 -translate-x-1/2 pointer-events-none px-2.5 py-1 rounded-md bg-gray-800/70 text-white text-xs tabular-nums"
    >
      {{ zoomIndicator }}
    </div>
  </div>
</template>

<style scoped>
.paper-preview {
  min-height: 297mm;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.08);
  font-family: Georgia, 'Times New Roman', serif;
}

@media print {
  .paper-preview {
    box-shadow: none;
    max-width: none;
  }
}
</style>
