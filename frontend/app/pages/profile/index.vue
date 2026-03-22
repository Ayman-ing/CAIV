<script setup lang="ts">
import Profile from '~/components/profile/index.vue'

definePageMeta({
  middleware: 'auth'
})
</script>
<template>
  <Profile /> 
</template>