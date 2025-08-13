<template>
  <div class="transition-colors duration-300 min-h-screen bg-background text-primary">
    <NuxtPage />
  </div>
</template>

<script setup>
// Ensure theme is applied on initial load
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light')
  document.documentElement.setAttribute('data-theme', theme)
})
</script>

<style>
/* Ensure root element inherits theme colors */
html {
  background-color: rgb(var(--color-background));
  color: rgb(var(--color-text-primary));
}

/* Force dark mode text colors */
[data-theme="dark"] {
  color-scheme: dark;
}

[data-theme="dark"] body {
  background-color: rgb(17 17 17) !important;
  color: rgb(255 255 255) !important;
}

[data-theme="dark"] * {
  border-color: rgb(82 82 82);
}

/* Force light mode text to be very dark */
html:not([data-theme="dark"]) {
  color-scheme: light;
}

html:not([data-theme="dark"]) body {
  background-color: rgb(255 255 255) !important;
  color: rgb(15 15 15) !important;
}

/* Aggressive light mode text color enforcement */
html:not([data-theme="dark"]) .dashboard-content * {
  color: rgb(15 15 15) !important;
}

html:not([data-theme="dark"]) .dashboard-content .text-white {
  color: rgb(255 255 255) !important;
}

html:not([data-theme="dark"]) .dashboard-content [class*="text-primary"] {
  color: rgb(var(--color-primary-600)) !important;
}

html:not([data-theme="dark"]) .dashboard-content [class*="text-green"] {
  color: rgb(var(--color-success)) !important;
}

html:not([data-theme="dark"]) .dashboard-content [class*="text-blue"] {
  color: rgb(var(--color-info)) !important;
}

html:not([data-theme="dark"]) .dashboard-content [class*="text-accent"] {
  color: rgb(var(--color-accent-600)) !important;
}
</style>
