<template>
  <section id="features" class="py-20 bg-white dark:bg-gray-900 transition-colors duration-300">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center max-w-3xl mx-auto mb-16">
        <div class="inline-block mb-4 px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium">
          Features
        </div>
        <h2 class="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-6">
          Everything you need to land your dream job
        </h2>
        <p class="text-xl text-gray-600 dark:text-gray-300">
          Our AI-powered platform provides all the tools you need to create professional, 
          compelling resumes that get noticed by employers.
        </p>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- AI-Powered Optimization -->
        <div class="card-hover border-0 shadow-lg dark:shadow-xl dark:shadow-blue-500/5 bg-white dark:bg-gray-800/80 backdrop-blur-sm rounded-xl transition-all duration-300 hover:shadow-2xl hover:scale-105">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Icon name="mdi:brain" class="text-3xl text-blue-600 dark:text-blue-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              AI-Powered Optimization
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Our AI analyzes job descriptions and optimizes your resume content for maximum 
              impact and ATS compatibility.
            </p>
          </div>
        </div>

        <!-- Professional Templates -->
        <div class="card-hover border-0 shadow-lg dark:shadow-xl dark:shadow-green-500/5 bg-white dark:bg-gray-800/80 backdrop-blur-sm rounded-xl transition-all duration-300 hover:shadow-2xl hover:scale-105">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Icon name="mdi:file-document-outline" class="text-3xl text-green-600 dark:text-green-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Professional Templates
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Choose from a variety of professionally designed templates that showcase 
              your skills and experience effectively.
            </p>
          </div>
        </div>

        <!-- Real-time Preview -->
        <div class="card-hover border-0 shadow-lg dark:shadow-xl dark:shadow-purple-500/5 bg-white dark:bg-gray-800/80 backdrop-blur-sm rounded-xl transition-all duration-300 hover:shadow-2xl hover:scale-105">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Icon name="mdi:eye" class="text-3xl text-purple-600 dark:text-purple-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Real-time Preview
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              See your changes instantly with our real-time preview feature. 
              What you see is what you get.
            </p>
          </div>
        </div>

        <!-- Smart Matching -->
        <div class="card-hover border-0 shadow-lg dark:shadow-xl dark:shadow-orange-500/5 bg-white dark:bg-gray-800/80 backdrop-blur-sm rounded-xl transition-all duration-300 hover:shadow-2xl hover:scale-105">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-orange-100 dark:bg-orange-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Icon name="mdi:target" class="text-3xl text-orange-600 dark:text-orange-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Smart Job Matching
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Get personalized suggestions and optimizations based on specific 
              job requirements and industry standards.
            </p>
          </div>
        </div>

        <!-- Export Options -->
        <div class="card-hover border-0 shadow-lg dark:shadow-xl dark:shadow-red-500/5 bg-white dark:bg-gray-800/80 backdrop-blur-sm rounded-xl transition-all duration-300 hover:shadow-2xl hover:scale-105">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Icon name="mdi:download" class="text-3xl text-red-600 dark:text-red-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Multiple Export Formats
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Download your resume in various formats including PDF, Word, 
              and plain text for different application requirements.
            </p>
          </div>
        </div>

        <!-- Analytics -->
        <div class="card-hover border-0 shadow-lg dark:shadow-xl dark:shadow-indigo-500/5 bg-white dark:bg-gray-800/80 backdrop-blur-sm rounded-xl transition-all duration-300 hover:shadow-2xl hover:scale-105">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Icon name="mdi:chart-line" class="text-3xl text-indigo-600 dark:text-indigo-400" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Performance Analytics
            </h3>
            <p class="text-gray-600 dark:text-gray-300">
              Track how your resume performs and get insights on how to 
              improve your job application success rate.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>