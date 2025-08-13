<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 font-sans antialiased">
    <!-- Navigation -->
    <nav class="bg-white/95 dark:bg-gray-900/95 backdrop-blur-2xl shadow-sm border-b border-gray-200/50 dark:border-gray-700/50 fixed w-full z-50 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center space-x-3">
            <div class="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-500 dark:from-blue-500 dark:to-blue-400 rounded-xl shadow-md">
              <Icon name="lucide:brain-circuit" class="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 class="text-xl font-semibold text-gray-900 dark:text-white tracking-tight">AI Resume Builder</h1>
              <p class="text-xs text-gray-500 dark:text-gray-400">Professional Resumes, AI-Powered</p>
            </div>
          </div>

          <!-- Navigation Items (Desktop) -->
          <div class="hidden md:flex items-center space-x-8">
            <Button variant="ghost" size="sm" class="group relative flex items-center space-x-2 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all">
              <Icon name="lucide:file-text" class="w-4 h-4 group-hover:text-blue-600 dark:group-hover:text-blue-400" />
              <span>My Resumes</span>
              <span class="absolute -top-2 -right-2 bg-blue-600 text-white text-xs rounded-full px-1.5 py-0.5 hidden group-hover:block">3</span>
            </Button>
            <Button variant="ghost" size="sm" class="group relative flex items-center space-x-2 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all">
              <Icon name="lucide:template" class="w-4 h-4 group-hover:text-blue-600 dark:group-hover:text-blue-400" />
              <span>Templates</span>
            </Button>
            <Button variant="ghost" size="sm" class="group relative flex items-center space-x-2 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all">
              <Icon name="lucide:settings" class="w-4 h-4 group-hover:text-blue-600 dark:group-hover:text-blue-400" />
              <span>Settings</span>
            </Button>
          </div>

          <!-- Right Side -->
          <div class="flex items-center space-x-4">
            <!-- Dark Mode Toggle -->
            <DarkModeToggle class="p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors" />

            <!-- User Menu -->
            <div class="relative">
              <Button variant="ghost" size="sm" class="flex items-center space-x-2 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all">
                <div class="w-9 h-9 bg-gradient-to-br from-blue-600 to-blue-500 dark:from-blue-500 dark:to-blue-400 rounded-full flex items-center justify-center shadow-sm">
                  <span class="text-white text-sm font-medium">JD</span>
                </div>
                <span class="hidden md:block text-gray-900 dark:text-white font-medium">John Doe</span>
                <Icon name="lucide:chevron-down" class="w-4 h-4 text-gray-500 dark:text-gray-400 transition-transform" :class="{ 'rotate-180': userMenuOpen }" @click="toggleUserMenu" />
              </Button>
              <!-- Dropdown Menu -->
              <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
                <div v-if="userMenuOpen" class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg py-2 z-50">
                  <Button variant="ghost" size="sm" class="w-full text-left px-4 py-2 text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-800">Profile</Button>
                  <Button variant="ghost" size="sm" class="w-full text-left px-4 py-2 text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-800">Sign Out</Button>
                </div>
              </transition>
            </div>

            <!-- Mobile Menu Button -->
            <Button variant="ghost" size="sm" class="md:hidden p-2" @click="toggleMobileMenu">
              <Icon :name="mobileMenuOpen ? 'lucide:x' : 'lucide:menu'" class="w-6 h-6 text-gray-900 dark:text-white" />
            </Button>
          </div>
        </div>

        <!-- Mobile Menu -->
        <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-2">
          <div v-if="mobileMenuOpen" class="md:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 py-4">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-2">
              <Button variant="ghost" size="sm" class="w-full flex items-center space-x-2 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30">
                <Icon name="lucide:file-text" class="w-4 h-4" />
                <span>My Resumes</span>
              </Button>
              <Button variant="ghost" size="sm" class="w-full flex items-center space-x-2 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30">
                <Icon name="lucide:template" class="w-4 h-4" />
                <span>Templates</span>
              </Button>
              <Button variant="ghost" size="sm" class="w-full flex items-center space-x-2 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30">
                <Icon name="lucide:settings" class="w-4 h-4" />
                <span>Settings</span>
              </Button>
            </div>
          </div>
        </transition>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Welcome Header -->
      <div class="mb-12">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-6">
          <div>
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2 tracking-tight animate-fade-in">
              Welcome back, John! 👋
            </h2>
            <p class="text-lg text-gray-600 dark:text-gray-300 max-w-md">
              Craft your next standout resume with our AI-powered tools and professional templates.
            </p>
          </div>

        </div>
<!-- Quick Stats -->
        <div class="">
          <Card class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow">
       
            
            <div class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
              <h4 class="font-medium text-gray-900 dark:text-white mb-3">Quick Tips</h4>
              <ul class="space-y-3 text-sm text-gray-600 dark:text-gray-300">
                <li class="flex items-start space-x-2">
                  <Icon name="lucide:check-circle" class="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Add a professional summary to stand out</span>
                </li>
                <li class="flex items-start space-x-2">
                  <Icon name="lucide:circle" class="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5 flex-shrink-0" />
                  <span>Include relevant skills for your role</span>
                </li>
                <li class="flex items-start space-x-2">
                  <Icon name="lucide:circle" class="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5 flex-shrink-0" />
                  <span>Add detailed work experience</span>
                </li>
              </ul>
            </div>
          </Card>
        </div>
        <!-- Quick Actions Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Create New Resume -->
          <Card class="group cursor-pointer bg-white dark:bg-gray-900 border rounded-lg border-gray-200 dark:border-gray-700 hover:shadow-xl hover:scale-[1.02] transition-all duration-300 hover:border-blue-400 dark:hover:border-blue-600 overflow-hidden">
            <div class="p-6 relative">
              <div class="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-transparent group-hover:from-blue-100/50 dark:from-blue-900/20 dark:group-hover:from-blue-800/30 transition-all duration-300 "></div>
              <div class="flex items-center justify-center w-16 h-16 bg-blue-50 dark:bg-blue-900/30 rounded-xl mb-4 group-hover:bg-blue-100 dark:group-hover:bg-blue-800/40 transition-colors relative z-10">
                <Icon name="lucide:plus-circle" class="w-8 h-8 text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2 relative z-10">Create New Resume</h3>
              <p class="text-gray-600 dark:text-gray-300 mb-4 relative z-10">Start fresh with our AI-powered resume builder and professional templates.</p>
              <Button variant="primary" size="sm" class="w-full h-8 border bg-blue-200 hover:bg-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 text-black dark:text-white rounded-lg transition-colors relative z-10">
                <Icon name="lucide:sparkles" class="w-4 h-4 mr-2" />
                Start Creating
              </Button>
            </div>
          </Card>

          <!-- Upload Existing Resume -->
          <Card class="group cursor-pointer bg-white rounded-lg dark:bg-gray-900 border border-gray-200 dark:border-gray-700 hover:shadow-xl hover:scale-[1.02] transition-all duration-300 hover:border-yellow-400 dark:hover:border-yellow-600 overflow-hidden">
            <div class="p-6 relative">
              <div class="absolute inset-0 bg-gradient-to-br from-yellow-50/50 to-transparent group-hover:from-yellow-100/50 dark:from-yellow-900/20 dark:group-hover:from-yellow-800/30 transition-all duration-300"></div>
              <div class="flex items-center justify-center w-16 h-16 bg-yellow-50 dark:bg-yellow-900/30 rounded-xl mb-4 group-hover:bg-yellow-100 dark:group-hover:bg-yellow-800/40 transition-colors relative z-10">
                <Icon name="lucide:upload" class="w-8 h-8 text-yellow-600 dark:text-yellow-400 group-hover:scale-110 transition-transform" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2 relative z-10">Upload & Enhance</h3>
              <p class="text-gray-600 dark:text-gray-300 mb-4 relative z-10">Upload your existing resume and let AI enhance it with improvements.</p>
              <Button variant="secondary" size="sm" class="w-full h-8 bg-yellow-50 hover:bg-yellow-100 dark:bg-yellow-900/30 dark:hover:bg-yellow-800/40 text-gray-900 dark:text-white border border-yellow-400 dark:border-yellow-400 rounded-lg transition-colors relative z-10">
                <Icon name="lucide:file-up" class="w-4 h-4 mr-2" />
                Upload Resume
              </Button>
            </div>
          </Card>

          <!-- Import from LinkedIn -->
          <Card class="group cursor-pointer rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 hover:shadow-xl hover:scale-[1.02] transition-all duration-300 hover:border-blue-400 dark:hover:border-blue-600 overflow-hidden">
            <div class="p-6 relative">
              <div class="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-transparent group-hover:from-blue-100/50 dark:from-blue-900/20 dark:group-hover:from-blue-800/30 transition-all duration-300"></div>
              <div class="flex items-center justify-center w-16 h-16 bg-blue-50 dark:bg-blue-900/30 rounded-xl mb-4 group-hover:bg-blue-100 dark:group-hover:bg-blue-800/40 transition-colors relative z-10">
                <Icon name="lucide:linkedin" class="w-8 h-8 text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2 relative z-10">Import LinkedIn</h3>
              <p class="text-gray-600 dark:text-gray-300 mb-4 relative z-10">Automatically import your LinkedIn profile and create a professional resume.</p>
              <Button variant="outline" size="sm" class="w-full h-8 border border-blue-400 dark:border-blue-400 text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors relative z-10">
                <Icon name="lucide:download" class="w-4 h-4 mr-2" />
                Import Profile
              </Button>
            </div>
          </Card>
        </div>
      </div>

      <!-- Recent Activity & Quick Stats -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Recent Activity -->
        <div class="lg:col-span-2">
          <Card title="Recent Activity" class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow">
            <div class="space-y-4 p-4">
              <div v-for="activity in recentActivities" :key="activity.id" 
                   class="flex items-center space-x-4 p-3 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-all duration-200 group">
                <div class="flex items-center justify-center w-10 h-10 rounded-full relative z-10"
                     :class="getActivityBgColor(activity.type)">
                  <Icon :name="getActivityIcon(activity.type)" 
                        class="w-5 h-5 group-hover:scale-110 transition-transform" 
                        :class="getActivityIconColor(activity.type)" />
                </div>
                <div class="flex-1">
                  <p class="font-medium text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{{ activity.title }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(activity.date) }}</p>
                </div>
                <Button variant="ghost" size="sm" class="text-gray-900 dark:text-white hover:bg-blue-50 dark:hover:bg-blue-900/30">View</Button>
              </div>
            </div>
          </Card>
        </div>

        
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// State for mobile menu and user dropdown
const mobileMenuOpen = ref(false);
const userMenuOpen = ref(false);

// Toggle mobile menu
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

// Toggle user menu
const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value;
};

// Define activity interface
interface Activity {
  id: string;
  type: 'create' | 'edit' | 'download' | 'share' | 'upload';
  title: string;
  action: string;
  date: Date;
}

// Reactive data
const recentActivities = ref<Activity[]>([
  { 
    id: '1', 
    type: 'create', 
    title: 'Created "Software Engineer Resume"', 
    action: 'Created a new document', 
    date: new Date('2024-08-10T12:00:00Z') 
  },
  { 
    id: '2', 
    type: 'edit', 
    title: 'Updated "Marketing Manager Resume"', 
    action: 'Updated profile information', 
    date: new Date('2024-08-09T14:30:00Z') 
  },
  { 
    id: '3', 
    type: 'download', 
    title: 'Downloaded "Data Analyst Resume"', 
    action: 'Downloaded as PDF', 
    date: new Date('2024-08-08T09:15:00Z') 
  },
  { 
    id: '4', 
    type: 'share', 
    title: 'Shared "Product Manager Resume"', 
    action: 'Shared via link', 
    date: new Date('2024-08-07T16:45:00Z') 
  }
]);

// Helper methods
const getActivityIcon = (type: Activity['type']) => {
  const icons = {
    create: 'lucide:plus-circle',
    edit: 'lucide:edit',
    download: 'lucide:download',
    share: 'lucide:share',
    upload: 'lucide:upload'
  };
  return icons[type];
};

const getActivityBgColor = (type: Activity['type']) => {
  const colors = {
    create: 'bg-green-50 dark:bg-green-900/30',
    edit: 'bg-blue-50 dark:bg-blue-900/30',
    download: 'bg-purple-50 dark:bg-purple-900/30',
    share: 'bg-orange-50 dark:bg-orange-900/30',
    upload: 'bg-cyan-50 dark:bg-cyan-900/30'
  };
  return colors[type];
};

const getActivityIconColor = (type: Activity['type']) => {
  const colors = {
    create: 'text-green-600 dark:text-green-400',
    edit: 'text-blue-600 dark:text-blue-400',
    download: 'text-purple-600 dark:text-purple-400',
    share: 'text-orange-600 dark:text-orange-400',
    upload: 'text-cyan-600 dark:text-cyan-400'
  };
  return colors[type];
};

const formatDate = (date: Date) => {
  const now = new Date();
  const diffTime = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) {
    return 'Today';
  } else if (diffDays === 1) {
    return 'Yesterday';
  } else if (diffDays < 7) {
    return `${diffDays} days ago`;
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }
};
</script>

<style scoped>
/* Custom animation for fade-in */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
</style>