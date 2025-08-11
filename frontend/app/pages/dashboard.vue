<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center space-x-3">
            <Icon name="mdi:file-document-edit" class="text-2xl text-blue-600 dark:text-blue-400" />
            <span class="text-xl font-bold text-gray-900 dark:text-white">CAIV</span>
          </div>
          
          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <DarkModeToggle />
            <Button
              icon="mdi:account-circle"
              label="Profile"
              text
              class="text-gray-700 dark:text-gray-300"
            />
            <Button
              icon="mdi:logout"
              label="Logout"
              text
              class="text-gray-700 dark:text-gray-300"
              @click="handleLogout"
            />
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome to CAIV Dashboard
        </h1>
        <p class="text-gray-600 dark:text-gray-300">
          Start building your professional resume with AI assistance
        </p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- Create New Resume -->
        <Card class="hover:shadow-lg transition-shadow cursor-pointer bg-white dark:bg-gray-800">
          <template #content>
            <div class="p-6 text-center">
              <Icon name="mdi:plus-circle" class="text-4xl text-blue-600 dark:text-blue-400 mb-4" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Create New Resume
              </h3>
              <p class="text-gray-600 dark:text-gray-300 mb-4">
                Start with a template and let AI help you build a perfect resume
              </p>
              <Button
                label="Get Started"
                class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 border-0 text-white"
              />
            </div>
          </template>
        </Card>

        <!-- Import from LinkedIn -->
        <Card class="hover:shadow-lg transition-shadow cursor-pointer bg-white dark:bg-gray-800">
          <template #content>
            <div class="p-6 text-center">
              <Icon name="mdi:linkedin" class="text-4xl text-blue-700 mb-4" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Import from LinkedIn
              </h3>
              <p class="text-gray-600 dark:text-gray-300 mb-4">
                Automatically import your LinkedIn profile to get started quickly
              </p>
              <Button
                label="Import Now"
                outlined
                class="text-blue-600 dark:text-blue-400 border-blue-600 dark:border-blue-400"
              />
            </div>
          </template>
        </Card>

        <!-- Browse Templates -->
        <Card class="hover:shadow-lg transition-shadow cursor-pointer bg-white dark:bg-gray-800">
          <template #content>
            <div class="p-6 text-center">
              <Icon name="mdi:view-grid" class="text-4xl text-purple-600 dark:text-purple-400 mb-4" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Browse Templates
              </h3>
              <p class="text-gray-600 dark:text-gray-300 mb-4">
                Explore our collection of professional resume templates
              </p>
              <Button
                label="View All"
                outlined
                class="text-purple-600 dark:text-purple-400 border-purple-600 dark:border-purple-400"
              />
            </div>
          </template>
        </Card>
      </div>

      <!-- Recent Resumes -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Your Resumes
        </h2>
        <Card class="bg-white dark:bg-gray-800">
          <template #content>
            <div class="p-6">
              <div class="text-center py-12">
                <Icon name="mdi:file-document-outline" class="text-6xl text-gray-400 mb-4" />
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  No resumes yet
                </h3>
                <p class="text-gray-500 dark:text-gray-400 mb-4">
                  Create your first resume to get started
                </p>
                <Button
                  label="Create Resume"
                  class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 border-0 text-white"
                />
              </div>
            </div>
          </template>
        </Card>
      </div>

      <!-- Tips & Help -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Tips -->
        <Card class="bg-white dark:bg-gray-800">
          <template #header>
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Resume Tips
              </h3>
            </div>
          </template>
          <template #content>
            <div class="p-4 space-y-4">
              <div class="flex items-start space-x-3">
                <Icon name="mdi:lightbulb" class="text-yellow-500 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-white">
                    Tailor for each job
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-300">
                    Customize your resume for each application using AI suggestions
                  </p>
                </div>
              </div>
              <div class="flex items-start space-x-3">
                <Icon name="mdi:target" class="text-green-500 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-white">
                    Use action verbs
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-300">
                    Start bullet points with strong action verbs to show impact
                  </p>
                </div>
              </div>
              <div class="flex items-start space-x-3">
                <Icon name="mdi:chart-line" class="text-blue-500 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-white">
                    Quantify achievements
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-300">
                    Include numbers and metrics to demonstrate your impact
                  </p>
                </div>
              </div>
            </div>
          </template>
        </Card>

        <!-- Help & Support -->
        <Card class="bg-white dark:bg-gray-800">
          <template #header>
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Need Help?
              </h3>
            </div>
          </template>
          <template #content>
            <div class="p-4 space-y-4">
              <Button
                icon="mdi:book-open"
                label="User Guide"
                text
                class="w-full justify-start text-gray-700 dark:text-gray-300"
              />
              <Button
                icon="mdi:video"
                label="Video Tutorials"
                text
                class="w-full justify-start text-gray-700 dark:text-gray-300"
              />
              <Button
                icon="mdi:help-circle"
                label="FAQ"
                text
                class="w-full justify-start text-gray-700 dark:text-gray-300"
              />
              <Button
                icon="mdi:message"
                label="Contact Support"
                text
                class="w-full justify-start text-gray-700 dark:text-gray-300"
              />
            </div>
          </template>
        </Card>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// SEO Meta
useSeoMeta({
  title: 'Dashboard - CAIV',
  description: 'Your CAIV dashboard - create and manage your AI-powered resumes.',
})

// Handle Logout
const handleLogout = async () => {
  try {
    // TODO: Implement actual logout logic
    console.log('Logging out...')
    
    // Clear any stored tokens/data
    // localStorage.removeItem('auth-token')
    
    // Redirect to home page
    await navigateTo('/')
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>
