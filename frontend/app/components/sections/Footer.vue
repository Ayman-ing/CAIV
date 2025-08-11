<template>
  <footer class="bg-gray-900 dark:bg-gray-950 text-white transition-colors duration-300">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand -->
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <Icon name="mdi:file-document-edit" class="text-2xl text-blue-400 dark:text-blue-300" />
            <span class="text-xl font-bold">CAIV</span>
          </div>
          <p class="text-gray-300 dark:text-gray-400 max-w-md">
            Build professional resumes with AI assistance. 
            Stand out from the crowd and land your dream job.
          </p>
        </div>
        
        <!-- Links -->
        <div>
          <h3 class="font-semibold mb-4 text-white dark:text-gray-100">Product</h3>
          <ul class="space-y-2 text-gray-300 dark:text-gray-400">
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Features</a></li>
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Templates</a></li>
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Examples</a></li>
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Pricing</a></li>
          </ul>
        </div>
        
        <div>
          <h3 class="font-semibold mb-4 text-white dark:text-gray-100">Support</h3>
          <ul class="space-y-2 text-gray-300 dark:text-gray-400">
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Help Center</a></li>
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Contact</a></li>
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Privacy</a></li>
            <li><a href="#" class="hover:text-white dark:hover:text-gray-200 transition-colors">Terms</a></li>
          </ul>
        </div>
      </div>
      
      <div class="h-px bg-gray-700 dark:bg-gray-800 my-8"></div>
      
      <div class="flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-400 dark:text-gray-500">
          © {{ getCurrentYear() }} CAIV. All rights reserved.
        </p>
        <div class="flex space-x-6 mt-4 md:mt-0">
          <Icon name="mdi:twitter" class="text-gray-400 dark:text-gray-500 hover:text-white dark:hover:text-gray-300 cursor-pointer transition-colors" />
          <Icon name="mdi:linkedin" class="text-gray-400 dark:text-gray-500 hover:text-white dark:hover:text-gray-300 cursor-pointer transition-colors" />
          <Icon name="mdi:github" class="text-gray-400 dark:text-gray-500 hover:text-white dark:hover:text-gray-300 cursor-pointer transition-colors" />
        </div>
      </div>
    </div>
  </footer>
</template>
<script setup lang="ts">
const getCurrentYear = () => {
  return new Date().getFullYear()
}
</script>