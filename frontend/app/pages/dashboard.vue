<script setup lang="ts">
import DashboardHome from '~/components/dashboard/DashboardHome.vue'

// Protect this route - require authentication and use auth layout
definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})
</script>

<template>
  <DashboardHome />
</template>