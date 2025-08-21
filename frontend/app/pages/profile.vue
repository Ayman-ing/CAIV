

<script setup lang="ts">
// Protect this route - require authentication and use auth layout
definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})
</script>

<template>
  <Profile />
</template>