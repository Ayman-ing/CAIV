<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import LeftSidebar from './LeftSidebar.vue'
import CenterCanvas from './CenterCanvas.vue'
import RightSidebar from './RightSidebar.vue'
import { useCVEditor } from '~/composables/useCVEditor'

const { state, updateSidebarWidth } = useCVEditor()

// Resizing state
const isResizingLeft = ref(false)
const isResizingRight = ref(false)
const startX = ref(0)
const startLeftWidth = ref(0)
const startRightWidth = ref(0)

// Computed styles for grid layout
const gridTemplateColumns = computed(() =>
  `${state.sidebarWidths.left}px 4px 1fr 4px ${state.sidebarWidths.right}px`
)

// Handle left divider drag start
const startResizeLeft = (e: MouseEvent) => {
  isResizingLeft.value = true
  startX.value = e.clientX
  startLeftWidth.value = state.sidebarWidths.left
}

// Handle right divider drag start
const startResizeRight = (e: MouseEvent) => {
  isResizingRight.value = true
  startX.value = e.clientX
  startRightWidth.value = state.sidebarWidths.right
}

// Handle mouse move
const handleMouseMove = (e: MouseEvent) => {
  if (isResizingLeft.value) {
    const delta = e.clientX - startX.value
    updateSidebarWidth('left', startLeftWidth.value + delta)
  } else if (isResizingRight.value) {
    const delta = startX.value - e.clientX
    updateSidebarWidth('right', startRightWidth.value + delta)
  }
}

// Handle mouse up
const handleMouseUp = () => {
  isResizingLeft.value = false
  isResizingRight.value = false
}

// Attach event listeners
onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
})
</script>

<template>
  <div class="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Editor Container with 3-column layout -->
    <div
      class="flex-1 overflow-hidden flex"
      :class="{ 'cursor-col-resize': isResizingLeft || isResizingRight }"
    >
      <!-- Grid container for layout -->
      <div
        class="grid w-full h-full"
        :style="{ gridTemplateColumns }"
      >
        <!-- Left Sidebar -->
        <div class="border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden flex flex-col">
          <LeftSidebar />
        </div>

        <!-- Left Divider -->
        <div
          class="w-1 bg-gray-300 dark:bg-gray-600 hover:bg-blue-500 dark:hover:bg-blue-400 cursor-col-resize transition-colors"
          :class="{ 'bg-blue-500 dark:bg-blue-400': isResizingLeft }"
          @mousedown="startResizeLeft"
        />

        <!-- Center Canvas -->
        <div class="overflow-hidden bg-gray-100 dark:bg-gray-900 flex flex-col">
          <CenterCanvas />
        </div>

        <!-- Right Divider -->
        <div
          class="w-1 bg-gray-300 dark:bg-gray-600 hover:bg-blue-500 dark:hover:bg-blue-400 cursor-col-resize transition-colors"
          :class="{ 'bg-blue-500 dark:bg-blue-400': isResizingRight }"
          @mousedown="startResizeRight"
        />

        <!-- Right Sidebar -->
        <div class="border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden flex flex-col">
          <RightSidebar />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Prevent text selection while resizing */
:global(.cursor-col-resize) {
  user-select: none;
}
</style>
