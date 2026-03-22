
<script setup lang="ts">
import Profile from '~/components/profile/index.vue'

// Protect this route - require authentication and use auth layout
definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})
</script>

<template>
  <Profile />
</template>