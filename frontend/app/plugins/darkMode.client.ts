export default defineNuxtPlugin(() => {
  const { initDarkMode } = useDarkMode()
  
  // Initialize dark mode on app start
  initDarkMode()
})
