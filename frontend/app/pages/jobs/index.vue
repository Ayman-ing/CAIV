<script setup lang="ts">
import JobsPlaceholder from '~/components/jobs/JobsPlaceholder.vue'

definePageMeta({
  middleware: 'auth',
  layout: 'auth',
})
</script>

<template>
  <JobsPlaceholder />
</template>
