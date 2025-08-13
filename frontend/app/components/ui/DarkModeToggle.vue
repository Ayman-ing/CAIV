<template>
  <Button
    :icon="isDark ? 'lucide:sun' : 'lucide:moon'"
    variant="outline"
    size="sm"
    @click="toggleTheme"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    {{ isDark ? 'Light Mode' : 'Dark Mode' }}
  </Button>
</template>

<script setup lang="ts">
// Composable for theme management
const isDark = ref(false)

// Initialize theme from localStorage or system preference
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  isDark.value = savedTheme ? savedTheme === 'dark' : systemPrefersDark
  applyTheme()
})

// Watch for theme changes
watch(isDark, () => {
  applyTheme()
})

// Apply theme to document
const applyTheme = () => {
  const theme = isDark.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

// Toggle theme
const toggleTheme = () => {
  isDark.value = !isDark.value
}

// Export for parent components
defineExpose({
  isDark: readonly(isDark),
  toggleTheme
})
</script>
