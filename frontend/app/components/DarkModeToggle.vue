<template>
  <Button 
   
    @click="toggle" 
    
    outlined
    class="dark-mode-toggle"
    
  >
    <Icon :name="isDark ? 'mdi:weather-sunny' : 'mdi:weather-night'" class="text-black dark:text-white"/>
  </Button>
</template>

<script setup>
const { isDark, toggle } = useDarkMode()
</script>
