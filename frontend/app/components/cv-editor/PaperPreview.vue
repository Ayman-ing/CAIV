<script setup lang="ts">
import { computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'

const { state, includedComponents } = useCVEditor()

const containerRef = ref<HTMLElement | null>(null)
const rulerRef = ref<HTMLElement | null>(null)
const scale = ref(1)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const lastMouseX = ref(0)
const lastMouseY = ref(0)
const sectionHeights = ref<number[]>([])
const pages = ref<{ start: number; end: number }[]>([])

const minScale = 0.3
const maxScale = 3

const A4_HEIGHT_MM = 297
const MM_PER_PX = 0.264583

const contentHeightPx = computed(() =>
  A4_HEIGHT_MM / MM_PER_PX - (state.layout.pageMargins.top + state.layout.pageMargins.bottom)
)

const pageInnerStyle = computed(() => ({
  padding: `${state.layout.pageMargins.top}px ${state.layout.pageMargins.right}px ${state.layout.pageMargins.bottom}px ${state.layout.pageMargins.left}px`,
}))

const sectionStyle = computed(() => ({
  fontSize: `${state.layout.fontSize}px`,
  lineHeight: state.layout.lineHeight,
  whiteSpace: 'pre-line',
}))

const rulerStyle = computed(() => ({
  fontSize: `${state.layout.fontSize}px`,
  lineHeight: state.layout.lineHeight,
  padding: `${state.layout.pageMargins.top}px ${state.layout.pageMargins.right}px ${state.layout.pageMargins.bottom}px ${state.layout.pageMargins.left}px`,
}))

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

function computePages() {
  const maxPx = contentHeightPx.value
  const heights = sectionHeights.value
  if (heights.length === 0) {
    pages.value = []
    return
  }
  const result: { start: number; end: number }[] = []
  let acc = 0
  let start = 0
  for (let i = 0; i < heights.length; i++) {
    const h = heights[i]
    if (acc + h > maxPx && acc > 0) {
      result.push({ start, end: i })
      start = i
      acc = h
    } else {
      acc += h
    }
  }
  if (start < heights.length) {
    result.push({ start, end: heights.length })
  }
  pages.value = result
}

let rulerObserver: ResizeObserver | null = null

function measureSections() {
  if (!rulerRef.value) return
  const children = rulerRef.value.children
  const heights: number[] = []
  for (let i = 0; i < children.length; i++) {
    heights.push(children[i].getBoundingClientRect().height)
  }
  sectionHeights.value = heights
  computePages()
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
  nextTick(measureSections)
  rulerObserver = new ResizeObserver(measureSections)
  if (rulerRef.value) rulerObserver.observe(rulerRef.value)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
  rulerObserver?.disconnect()
})

watch(
  () => [
    state.profileData,
    state.layout,
    state.components,
    includedComponents.value,
  ],
  () => nextTick(measureSections),
  { deep: true }
)

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

const visibleCustomSections = computed(() =>
  state.profileData.customSections.filter(cs =>
    !cs.title.toLowerCase().startsWith('unresolved')
  )
)

const paperTransform = computed(() =>
  `translate(${panX.value}px, ${panY.value}px) scale(${scale.value})`
)

const zoomIndicator = computed(() => `${Math.round(scale.value * 100)}%`)
</script>

<template>
  <div
    ref="containerRef"
    class="w-full h-full overflow-hidden p-8 flex flex-col items-start justify-start bg-gray-100 dark:bg-gray-900 select-none"
    :class="{ 'cursor-grab': !isPanning, 'cursor-grabbing': isPanning }"
    @wheel.prevent="handleWheel"
    @mousedown="handleMouseDown"
  >
    <div
      v-if="pages.length > 0"
      class="flex flex-col items-center space-y-6"
      :style="{ transform: paperTransform, transformOrigin: '0 0' }"
    >
      <div
        v-for="(page, pi) in pages"
        :key="pi"
        class="paper-page bg-white shadow-xl"
        :style="{ width: '210mm', height: A4_HEIGHT_MM + 'mm' }"
      >
        <div :style="pageInnerStyle" class="h-full overflow-hidden">
          <template v-if="hasData">
            <section-block v-if="pi === 0">
              <h1 class="font-bold text-gray-900 leading-tight text-center" :style="{ fontSize: state.layout.fontSize + 6 + 'px' }">
                {{ state.profileData.basicInfo.name }}
              </h1>
              <div
                v-if="contactInfo.length > 0 || activeLinks.length > 0"
                class="text-gray-600 text-center mt-2"
                :style="{ fontSize: state.layout.fontSize - 2 + 'px', lineHeight: state.layout.lineHeight }"
              >
                <span v-for="(info, i) in contactInfo" :key="'ci-' + i">
                  {{ info }}<span v-if="i < contactInfo.length - 1 || activeLinks.length > 0"> &middot; </span>
                </span>
                <a
                  v-for="(link, i) in activeLinks"
                  :key="'li-' + link.uuid"
                  :href="link.url"
                  target="_blank"
                  class="text-gray-600 hover:underline"
                >
                  {{ link.label || link.platform }}<span v-if="i < activeLinks.length - 1"> &middot; </span>
                </a>
              </div>
            </section-block>

            <template v-for="comp in includedComponents.slice(Math.max(0, page.start - 1), Math.max(0, page.end - 1))" :key="'pp-' + comp.uuid">
              <section-block v-if="comp.component_type === 'professional_summary' && state.profileData.summary" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <p :style="sectionStyle" class="text-gray-800">{{ state.profileData.summary }}</p>
              </section-block>

              <section-block v-else-if="comp.component_type === 'work_experience' && state.profileData.workExperiences.length > 0" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Experience</h2>
                <div v-for="exp in state.profileData.workExperiences" :key="'exp-' + exp.uuid" class="mb-3">
                  <div class="flex justify-between items-baseline">
                    <div>
                      <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ exp.job_title }}</span>
                      <span v-if="exp.company" class="text-gray-700" :style="{ fontSize: state.layout.fontSize + 'px' }">, {{ exp.company }}</span>
                    </div>
                    <span class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ dateRange(exp.start_date, exp.end_date) }}</span>
                  </div>
                  <p v-if="exp.description" class="text-gray-700 mt-0.5" :style="sectionStyle">{{ exp.description }}</p>
                </div>
              </section-block>

              <section-block v-else-if="comp.component_type === 'education' && state.profileData.education.length > 0" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Education</h2>
                <div v-for="edu in state.profileData.education" :key="'edu-' + edu.uuid" class="mb-2">
                  <div class="flex justify-between items-baseline">
                    <div>
                      <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ edu.degree }}</span>
                      <span v-if="edu.institution" class="text-gray-700" :style="{ fontSize: state.layout.fontSize + 'px' }">, {{ edu.institution }}</span>
                    </div>
                    <span class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ dateRange(edu.start_date, edu.end_date) }}</span>
                  </div>
                  <span v-if="edu.field_of_study" class="text-gray-600" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ edu.field_of_study }}</span>
                  <p v-if="edu.description" class="text-gray-700 mt-0.5" :style="sectionStyle">{{ edu.description }}</p>
                </div>
              </section-block>

              <section-block v-else-if="comp.component_type === 'skills' && state.profileData.skills.length > 0" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Skills</h2>
                <div class="flex flex-wrap gap-x-3 gap-y-1">
                  <span v-for="skill in state.profileData.skills" :key="'sk-' + skill.uuid" class="text-gray-800" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ skillDisplay(skill) }}</span>
                </div>
              </section-block>

              <section-block v-else-if="comp.component_type === 'projects' && state.profileData.projects.length > 0" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Projects</h2>
                <div v-for="proj in state.profileData.projects" :key="'pr-' + proj.uuid" class="mb-2">
                  <div class="flex justify-between items-baseline">
                    <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ proj.name }}</span>
                    <span class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ dateRange(proj.start_date, proj.end_date) }}</span>
                  </div>
                  <p v-if="proj.description" class="text-gray-700 mt-0.5" :style="sectionStyle">{{ proj.description }}</p>
                  <div v-if="proj.technologies" class="text-gray-500 mt-0.5" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">
                    <span class="font-medium">Technologies:</span> {{ proj.technologies }}
                  </div>
                </div>
              </section-block>

              <section-block v-else-if="comp.component_type === 'certificates' && state.profileData.certificates.length > 0" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Certifications</h2>
                <div v-for="cert in state.profileData.certificates" :key="'ce-' + cert.uuid" class="mb-2">
                  <div class="flex justify-between items-baseline">
                    <div>
                      <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ cert.name }}</span>
                      <span v-if="cert.issuing_organization" class="text-gray-700" :style="{ fontSize: state.layout.fontSize + 'px' }">, {{ cert.issuing_organization }}</span>
                    </div>
                    <span v-if="cert.issue_date" class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ formatDate(cert.issue_date) }}</span>
                  </div>
                </div>
              </section-block>

              <section-block v-else-if="comp.component_type === 'languages' && state.profileData.languages.length > 0" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                <hr class="border-t border-gray-800 mb-2">
                <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Languages</h2>
                <div class="flex flex-wrap gap-x-4 gap-y-1">
                  <span v-for="lang in state.profileData.languages" :key="'la-' + lang.uuid" class="text-gray-800" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ lang.language }} <span class="text-gray-500">{{ lang.proficiency }}</span></span>
                </div>
              </section-block>

              <template v-else-if="comp.component_type === 'custom_sections'">
                <section-block v-for="cs in visibleCustomSections" :key="'cs-' + cs.uuid" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
                  <hr class="border-t border-gray-800 mb-2">
                  <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ cs.title }}</h2>
                  <p :style="sectionStyle" class="text-gray-800">{{ cs.content }}</p>
                </section-block>
              </template>
            </template>
          </template>

          <div
            v-else
            class="flex flex-col items-center justify-center h-full text-gray-400"
          >
            <Icon name="heroicons:document-text" class="w-12 h-12 mb-3" />
            <p class="text-sm italic">No profile data loaded</p>
            <p class="text-xs mt-1">Add your information from the sidebar to see it here</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="hasData" class="flex items-center justify-center w-full h-full text-gray-400">
      <p class="text-sm italic">Measuring content...</p>
    </div>

    <!-- Hidden ruler for section height measurement -->
    <div ref="rulerRef" class="ruler" :style="rulerStyle" aria-hidden="true">
      <section-block>
        <h1 class="font-bold text-gray-900 leading-tight text-center" :style="{ fontSize: state.layout.fontSize + 6 + 'px' }">
          {{ state.profileData.basicInfo.name }}
        </h1>
        <div
          v-if="contactInfo.length > 0 || activeLinks.length > 0"
          class="text-gray-600 text-center mt-2"
          :style="{ fontSize: state.layout.fontSize - 2 + 'px', lineHeight: state.layout.lineHeight }"
        >
          <span v-for="(info, i) in contactInfo" :key="'r-ci-' + i">
            {{ info }}<span v-if="i < contactInfo.length - 1 || activeLinks.length > 0"> &middot; </span>
          </span>
          <a
            v-for="(link, i) in activeLinks"
            :key="'r-li-' + link.uuid"
            :href="link.url"
            target="_blank"
            class="text-gray-600 hover:underline"
          >
            {{ link.label || link.platform }}<span v-if="i < activeLinks.length - 1"> &middot; </span>
          </a>
        </div>
      </section-block>

      <template v-for="comp in includedComponents" :key="'r-' + comp.uuid">
        <section-block v-if="comp.component_type !== 'custom_sections'" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
          <template v-if="comp.component_type === 'professional_summary' && state.profileData.summary">
            <hr class="border-t border-gray-800 mb-2">
            <p :style="sectionStyle" class="text-gray-800">{{ state.profileData.summary }}</p>
          </template>

          <template v-else-if="comp.component_type === 'work_experience' && state.profileData.workExperiences.length > 0">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Experience</h2>
            <div v-for="exp in state.profileData.workExperiences" :key="'r-exp-' + exp.uuid" class="mb-3">
              <div class="flex justify-between items-baseline">
                <div>
                  <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ exp.job_title }}</span>
                  <span v-if="exp.company" class="text-gray-700" :style="{ fontSize: state.layout.fontSize + 'px' }">, {{ exp.company }}</span>
                </div>
                <span class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ dateRange(exp.start_date, exp.end_date) }}</span>
              </div>
              <p v-if="exp.description" class="text-gray-700 mt-0.5" :style="sectionStyle">{{ exp.description }}</p>
            </div>
          </template>

          <template v-else-if="comp.component_type === 'education' && state.profileData.education.length > 0">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Education</h2>
            <div v-for="edu in state.profileData.education" :key="'r-edu-' + edu.uuid" class="mb-2">
              <div class="flex justify-between items-baseline">
                <div>
                  <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ edu.degree }}</span>
                  <span v-if="edu.institution" class="text-gray-700" :style="{ fontSize: state.layout.fontSize + 'px' }">, {{ edu.institution }}</span>
                </div>
                <span class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ dateRange(edu.start_date, edu.end_date) }}</span>
              </div>
              <span v-if="edu.field_of_study" class="text-gray-600" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ edu.field_of_study }}</span>
              <p v-if="edu.description" class="text-gray-700 mt-0.5" :style="sectionStyle">{{ edu.description }}</p>
            </div>
          </template>

          <template v-else-if="comp.component_type === 'skills' && state.profileData.skills.length > 0">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Skills</h2>
            <div class="flex flex-wrap gap-x-3 gap-y-1">
              <span v-for="skill in state.profileData.skills" :key="'r-sk-' + skill.uuid" class="text-gray-800" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ skillDisplay(skill) }}</span>
            </div>
          </template>

          <template v-else-if="comp.component_type === 'projects' && state.profileData.projects.length > 0">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Projects</h2>
            <div v-for="proj in state.profileData.projects" :key="'r-pr-' + proj.uuid" class="mb-2">
              <div class="flex justify-between items-baseline">
                <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ proj.name }}</span>
                <span class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ dateRange(proj.start_date, proj.end_date) }}</span>
              </div>
              <p v-if="proj.description" class="text-gray-700 mt-0.5" :style="sectionStyle">{{ proj.description }}</p>
              <div v-if="proj.technologies" class="text-gray-500 mt-0.5" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">
                <span class="font-medium">Technologies:</span> {{ proj.technologies }}
              </div>
            </div>
          </template>

          <template v-else-if="comp.component_type === 'certificates' && state.profileData.certificates.length > 0">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Certifications</h2>
            <div v-for="cert in state.profileData.certificates" :key="'r-ce-' + cert.uuid" class="mb-2">
              <div class="flex justify-between items-baseline">
                <div>
                  <span class="font-semibold text-gray-900" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ cert.name }}</span>
                  <span v-if="cert.issuing_organization" class="text-gray-700" :style="{ fontSize: state.layout.fontSize + 'px' }">, {{ cert.issuing_organization }}</span>
                </div>
                <span v-if="cert.issue_date" class="text-gray-500 flex-shrink-0 ml-4 whitespace-nowrap" :style="{ fontSize: state.layout.fontSize - 2 + 'px' }">{{ formatDate(cert.issue_date) }}</span>
              </div>
            </div>
          </template>

          <template v-else-if="comp.component_type === 'languages' && state.profileData.languages.length > 0">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">Languages</h2>
            <div class="flex flex-wrap gap-x-4 gap-y-1">
              <span v-for="lang in state.profileData.languages" :key="'r-la-' + lang.uuid" class="text-gray-800" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ lang.language }} <span class="text-gray-500">{{ lang.proficiency }}</span></span>
            </div>
          </template>
        </section-block>

        <template v-else>
          <section-block v-for="cs in visibleCustomSections" :key="'r-cs-' + cs.uuid" :style="{ marginBottom: state.layout.sectionSpacing + 'px' }">
            <hr class="border-t border-gray-800 mb-2">
            <h2 class="font-bold text-gray-900 uppercase tracking-wider mb-2" :style="{ fontSize: state.layout.fontSize + 'px' }">{{ cs.title }}</h2>
            <p :style="sectionStyle" class="text-gray-800">{{ cs.content }}</p>
          </section-block>
        </template>
      </template>
    </div>

    <div
      class="fixed bottom-4 left-1/2 -translate-x-1/2 pointer-events-none px-2.5 py-1 rounded-md bg-gray-800/70 text-white text-xs tabular-nums"
    >
      {{ zoomIndicator }}
    </div>
  </div>
</template>

<style scoped>
section-block {
  display: block;
}

.paper-page {
  font-family: Georgia, 'Times New Roman', serif;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.08);
}

.ruler {
  position: fixed;
  left: -9999px;
  top: 0;
  width: 210mm;
  font-family: Georgia, 'Times New Roman', serif;
  visibility: hidden;
  pointer-events: none;
}

@media print {
  .paper-page {
    box-shadow: none;
  }
}
</style>
