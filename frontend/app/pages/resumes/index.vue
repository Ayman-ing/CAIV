<script setup lang="ts">
import ResumesList from '~/components/resumes/ResumesList.vue'

definePageMeta({
  middleware: 'auth',
  layout: 'auth',
})
</script>

<template>
  <ResumesList />
</template>
