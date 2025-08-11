export const useDarkMode = () => {
  // Use Nuxt's built-in state management
  const isDark = useState<boolean>('darkMode', () => false)
  
  // Toggle dark mode
  const toggle = () => {
    isDark.value = !isDark.value
    updateTheme()
    
    // Save preference to localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('darkMode', isDark.value.toString())
    }
  }
  
  // Set dark mode
  const setDark = (value: boolean) => {
    isDark.value = value
    updateTheme()
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('darkMode', value.toString())
    }
  }
  
  // Update HTML class for Tailwind CSS dark mode
  const updateTheme = () => {
    if (typeof window !== 'undefined') {
      const html = document.documentElement
      
      if (isDark.value) {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
    }
  }
  
  // Initialize dark mode from localStorage or system preference
  const initDarkMode = () => {
    if (typeof window !== 'undefined') {
      // Check localStorage first
      const stored = localStorage.getItem('darkMode')
      if (stored !== null) {
        isDark.value = stored === 'true'
      } else {
        // Fall back to system preference
        isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      
      updateTheme()
      
      // Listen for system theme changes
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (localStorage.getItem('darkMode') === null) {
          isDark.value = e.matches
          updateTheme()
        }
      })
    }
  }
  
  return {
    isDark: readonly(isDark),
    toggle,
    setDark,
    initDarkMode
  }
}
