<script setup>

useSeoMeta({
  title: 'CAIV - Build Your Perfect AI-Powered Resume',
  description: 'Create professional resumes tailored to any job description using advanced AI technology. Stand out from the crowd with personalized, ATS-friendly resumes.',
})
definePageMeta({
  middleware: 'guest'
})
</script>

<template>
  <div>
    <SectionsNavigation />
    <SectionsHero />
    <SectionsFeatures />
    <SectionsFooter />
  </div>
</template>

