<script setup>
const scrollToExamples = () => {
  // Smooth scroll to examples section
  const element = document.getElementById('examples')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <section class="hero-gradient min-h-screen flex items-center pt-16">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-4xl mx-auto">
        <!-- Hero Content -->
        <div class="space-y-8 animate-fade-in">
          <div class="space-y-4">
            <div class="inline-flex items-center px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full text-blue-800 dark:text-blue-200 text-sm font-medium mb-4">
              <Icon name="mdi:sparkles" class="mr-2" />
              AI-Powered Resume Generation
            </div>
            <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-gray-900 dark:text-white">
              Build Your Perfect
              <span class="text-gradient block mt-2">Professional Resume</span>
              <span class="text-gradient block mt-2">with AI</span>
            </h1>
          </div>
          
          <p class="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Create professional resumes tailored to any job description using advanced AI technology. 
            Stand out from the crowd with personalized, ATS-friendly resumes.
          </p>
          
          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mt-10">
            <button
              type="button" 
              class="px-8 py-4 text-lg font-semibold bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors transform hover:scale-105 shadow-lg hover:shadow-xl"
              @click="navigateTo('/register')"
            >
              Create Your Resume
            </button>
            <button
              type="button" 
              class="px-8 py-4 text-lg font-semibold text-blue-600 dark:text-blue-400 border-2 border-blue-600 dark:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors"
              @click="scrollToExamples"
            >
              View Examples
            </button>
          </div>
          
          <!-- Trust Indicators -->
          <div class="flex items-center justify-center space-x-8 mt-12 text-gray-500 dark:text-gray-400">
            <div class="flex items-center space-x-2">
              <Icon name="mdi:check-circle" class="text-green-500" />
              <span>ATS-Friendly</span>
            </div>
            <div class="flex items-center space-x-2">
              <Icon name="mdi:lightning-bolt" class="text-yellow-500" />
              <span>AI-Powered</span>
            </div>
            <div class="flex items-center space-x-2">
              <Icon name="mdi:shield-check" class="text-blue-500" />
              <span>Secure & Private</span>
            </div>
          </div>
        </div>
        
        <!-- Hero Image/Animation -->
        <div class="mt-16 relative">
          <div class="relative mx-auto max-w-2xl">
            <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-3xl blur-3xl opacity-20 animate-pulse"></div>
            <div class="relative bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-2xl border border-gray-200/50 dark:border-gray-700/50">
              <div class="p-8">
                <div class="flex items-center space-x-4 mb-6">
                  <div class="w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center">
                    <Icon name="mdi:account" class="text-xl" />
                  </div>
                  <div class="text-left">
                    <h3 class="font-semibold text-lg text-gray-900 dark:text-white">John Doe</h3>
                    <p class="text-gray-600 dark:text-gray-300">Software Engineer</p>
                  </div>
                </div>
                
                <div class="space-y-3 text-left">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span class="text-sm text-gray-600 dark:text-gray-300">AI-optimized for job matching</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-sm text-gray-600 dark:text-gray-300">Professional formatting</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
                    <span class="text-sm text-gray-600 dark:text-gray-300">Keyword optimization</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

